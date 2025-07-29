"""Various standard procedures."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import warnings
import pandas as pd
import polars as pl

from nwm_explorer.urls import generate_reference_dates, generate_usgs_urls
from nwm_explorer.manifests import generate_default_manifest, generate_usgs_manifest
from nwm_explorer.downloads import download_files, download_routelinks
from nwm_explorer.data import scan_routelinks, generate_filepath, generate_directory
from nwm_explorer.data import (process_netcdf_parallel, process_nwis_tsv_parallel,
    delete_directory)
from nwm_explorer.mappings import FileType, Variable, Units, Domain, Configuration
from nwm_explorer.mappings import LEAD_TIME_FREQUENCY, NWM_URL_BUILDERS
from nwm_explorer.metrics import compute_metrics_pandas
from nwm_explorer.data import netcdf_validator, csv_gz_validator
from nwm_explorer.logger import get_logger
from nwm_explorer.readers import read_pairs, read_NWM_output, read_USGS_observations, scan_date_range

def load_NWM_output(
        root: Path,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
        routelinks: dict[Domain, pl.LazyFrame] | None = None,
        low_memory: bool = False
) -> dict[tuple[Domain, Configuration], pl.LazyFrame]:
    """
    Download and process NWM output.

    Parameters
    ----------
    root: Path, required
        Root directory to save downloaded and processed files.
    start_date: pd.Timestamp
        First date to start retrieving data.
    end_date: pd.Timestamp
        Last date to retrieve data.
    routelinks: dict[Domain, LazyFrame]
        Mapping from Domain to crosswalk data.
    low_memory: bool, default False
        Reduce memory pressure at the expense of performance.
    
    Returns
    -------
    dict[tuple[Domain, Configuration], pl.LazyFrame]
    """
    if routelinks is None:
        routelinks = scan_routelinks(*download_routelinks(root / "routelinks"))

    logger = get_logger("nwm_explorer.pipelines.load_NWM_output")
    reference_dates = generate_reference_dates(start_date, end_date)

    # Download and process model output
    model_output = {}
    for (domain, configuration), url_builder in NWM_URL_BUILDERS.items():
        day_files = []
        for rd in reference_dates:
            # Check for file existence
            parquet_file = generate_filepath(
                root, FileType.parquet, configuration, Variable.streamflow,
                Units.cubic_feet_per_second, rd
            )
            logger.info(f"Building {parquet_file}")
            if parquet_file.exists():
                logger.info(f"Found existing {parquet_file}")
                day_files.append(parquet_file)
                continue

            # Download
            urls = url_builder([rd])
            download_directory = generate_directory(
                root, FileType.netcdf, rd, configuration=configuration
            )
            logger.info(f"Downloading to {download_directory}")
            manifest = generate_default_manifest(len(urls),
                directory=download_directory)
            download_files(*zip(urls, manifest), limit=20, timeout=3600,
                file_validator=netcdf_validator)
            
            # Validate manifest
            logger.info(f"Validating manifest {domain} {configuration} {rd}")
            file_list = []
            for fp in manifest:
                if fp.exists():
                    file_list.append(fp)
                    continue
                warnings.warn(f"{fp} does not exist.", RuntimeWarning)
            
            # Check for at least one file
            if not file_list:
                logger.info(f"Found no files for {domain} {configuration} {rd}")
                continue

            # Process
            logger.info(f"Processing raw data {domain} {configuration} {rd}")
            features = routelinks[domain].select(
                "nwm_feature_id").collect()["nwm_feature_id"].to_list()
            data = process_netcdf_parallel(
                filepaths=file_list,
                variables=["streamflow"],
                features=features,
                max_processes=6,
                files_per_job=15
            ).rename(columns={
                    "time": "value_time",
                    "feature_id": "nwm_feature_id",
                    "streamflow": "value"
            })

            # Convert from cms to cfs
            data["value"] = data["value"].div(0.3048 ** 3.0)

            # Save to parquet
            logger.info(f"Saving {parquet_file}")
            pl.DataFrame(data).with_columns(
                pl.col("value").cast(pl.Float32)
            ).write_parquet(parquet_file)

            # Clean-up
            logger.info(f"Cleaning up {download_directory}")
            delete_directory(download_directory, parquet_file)
            day_files.append(parquet_file)
            
        # Check for at least one file
        if not day_files:
            logger.info(f"Found no data for {domain} {configuration}")
            continue
        
        # Merge files
        logger.info(f"Merging parquet files")
        model_output[(domain, configuration)] = pl.scan_parquet(day_files,
            low_memory=low_memory)
    return model_output

def load_USGS_observations(
        root: Path,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
        routelinks: dict[Domain, pl.LazyFrame]
) -> dict[Domain, pl.LazyFrame]:
    """
    Download and process USGS observations.

    Parameters
    ----------
    root: Path, required
        Root directory to save downloaded and processed files.
    start_date: pd.Timestamp
        First date to start retrieving data.
    end_date: pd.Timestamp
        Last date to retrieve data.
    routelinks: dict[Domain, LazyFrame]
        Mapping from Domain to crosswalk data.
    
    Returns
    -------
    dict[Domain, pl.LazyFrame]
    """
    logger = get_logger("nwm_explorer.pipelines.load_USGS_observations")
    # Download and process model output
    observations = {}
    s = start_date.strftime("%Y%m%dT%H")
    e = end_date.strftime("%Y%m%dT%H")
    for domain, rl in routelinks.items():
        # Check for file existence
        parquet_directory = root / FileType.parquet / Configuration.usgs
        parquet_file = parquet_directory / f"{domain}_{s}_{e}.parquet"
        logger.info(f"Building {parquet_file}")
        if parquet_file.exists():
            logger.info(f"Found existing {parquet_file}")
            observations[domain] = pl.scan_parquet(parquet_file)
            continue
        parquet_directory.mkdir(exist_ok=True, parents=True)

        # Download
        sites = rl.select(
            "usgs_site_code").collect().to_pandas()["usgs_site_code"]
        sites = sites[sites.str.isdigit()].to_list()
        urls = generate_usgs_urls(
            sites, start_date, end_date
        )
        download_directory = root / FileType.tsv / domain
        download_directory.mkdir(exist_ok=True, parents=True)
        logger.info(f"Downloading to {download_directory}")
        manifest = generate_usgs_manifest(
            sites,
            directory=download_directory)
        download_files(*zip(urls, manifest), limit=10, timeout=3600, 
            headers={"Accept-Encoding": "gzip"}, auto_decompress=False,
            file_validator=csv_gz_validator)
        
        # Validate manifest
        logger.info(f"Validating manifest {domain}")
        file_list = []
        for fp in manifest:
            if fp.exists():
                file_list.append(fp)
                continue
            warnings.warn(f"{fp} does not exist.", RuntimeWarning)

        # Process
        logger.info(f"Processing raw data {domain}")
        data = process_nwis_tsv_parallel(
            filepaths=file_list,
            max_processes=12
        ).rename(columns={
                "time": "value_time",
                "feature_id": "nwm_feature_id",
                "streamflow": "value"
        })

        # Save to parquet
        logger.info(f"Saving {parquet_file}")
        pl.DataFrame(data).write_parquet(parquet_file)
        observations[domain] = pl.scan_parquet(parquet_file)

        # Clean-up
        logger.info(f"Cleaning up {download_directory}")
        delete_directory(download_directory, parquet_file)
    return observations

def load_pairs(
        root: Path,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp
) -> dict[tuple[Domain, Configuration], pl.LazyFrame]:
    """
    Download and process NWM and USGS output.

    Parameters
    ----------
    root: Path, required
        Root directory to save downloaded and processed files.
    start_date: pd.Timestamp
        First date to start retrieving data.
    end_date: pd.Timestamp
        Last date to retrieve data.
    
    Returns
    -------
    dict[tuple[Domain, Configuration], pl.LazyFrame]
    """
    logger = get_logger("nwm_explorer.pipelines.load_pairs")
    routelinks = scan_routelinks(*download_routelinks(root / "routelinks"))

    logger.info("Scanning predictions for valid time range")
    predictions = read_NWM_output(
        root=root,
        start_date=start_date,
        end_date=end_date,
        low_memory=True
    )
    first, last = scan_date_range(predictions)
    logger.info("Loading observations")
    observations = read_USGS_observations(
        root=root,
        start_date=first,
        end_date=last
    )

    # Resample obs
    logger.info("Resampling observations")
    resampled_obs = {}
    for (domain, configuration), _ in predictions.items():
        if configuration in LEAD_TIME_FREQUENCY:
            resampling_frequency = LEAD_TIME_FREQUENCY[configuration][1]
            if (domain, resampling_frequency) in resampled_obs:
                continue
            resampled_obs[(
                domain,
                resampling_frequency
                )] = observations[domain].sort(
                    ("usgs_site_code", "value_time")
                ).group_by_dynamic(
                    "value_time",
                    every=resampling_frequency,
                    group_by="usgs_site_code"
                ).agg(
                    pl.col("value").max().alias("observed")
                ).with_columns(
                    pl.col("usgs_site_code").cast(pl.String)
                ).collect()
            continue
    
    for domain in observations:
        if (domain, "1d") in resampled_obs:
            continue
        resampled_obs[(
            domain,
            "1d"
            )] = observations[domain].sort(
                ("usgs_site_code", "value_time")
            ).group_by_dynamic(
                "value_time",
                every="1d",
                group_by="usgs_site_code"
            ).agg(
                pl.col("value").max().alias("observed")
            ).with_columns(
                pl.col("usgs_site_code").cast(pl.String)
            ).collect()
        
    # Load crosswalks
    logger.info("Loading crosswalks")
    crosswalks = {}
    for domain in routelinks:
        crosswalks[domain] = routelinks[domain].select(["nwm_feature_id",
                "usgs_site_code"]).collect()

    # Process model output
    logger.info("Resampling predictions and pairing")
    reference_dates = generate_reference_dates(start_date, end_date)
    pairs = {}
    for (domain, configuration), _ in predictions.items():
        day_files = []
        xwalk = crosswalks[domain]
        for rd in reference_dates:
            # Check for file existence
            parquet_file = generate_filepath(
                root, FileType.parquet, configuration, Variable.streamflow_pairs,
                Units.cubic_feet_per_second, rd
            )
            if parquet_file.exists():
                logger.info(f"Found existing file: {parquet_file}")
                day_files.append(parquet_file)
                # parquet_file.unlink()
                continue

            # Load input data
            ifile = generate_filepath(
                root, FileType.parquet, configuration, Variable.streamflow,
                Units.cubic_feet_per_second, rd
            )
            if not ifile.exists():
                logger.info(f"File does not exist, skipping: {ifile}")
                continue
            data = pl.scan_parquet(ifile).collect()
            logger.info(f"Building {parquet_file}")
            if configuration in LEAD_TIME_FREQUENCY:
                sampling_duration = LEAD_TIME_FREQUENCY[configuration][0]
                resampling_frequency = LEAD_TIME_FREQUENCY[configuration][1]
                hours = sampling_duration / pl.duration(hours=1)
                obs = resampled_obs[(domain, resampling_frequency)]
                paired_data = data.sort(
                    ("nwm_feature_id", "reference_time", "value_time")
                ).with_columns(
                    ((pl.col("value_time").sub(
                        pl.col("reference_time")
                        ) / sampling_duration).floor() *
                            hours).alias("lead_time_hours_min")
                ).group_by_dynamic(
                    "value_time",
                    every=resampling_frequency,
                    group_by=("nwm_feature_id", "reference_time")
                ).agg(
                    pl.col("value").max().alias("predicted"),
                    pl.col("lead_time_hours_min").min()
                ).with_columns(
                    usgs_site_code=pl.col("nwm_feature_id").replace_strict(
                    xwalk["nwm_feature_id"], xwalk["usgs_site_code"])
                ).join(obs, on=["usgs_site_code", "value_time"], how="left"
                    ).drop_nulls()
            else:
                # NOTE This will result in two simulation values per
                #  reference day. Handle this before computing metrics (max).
                obs = resampled_obs[(domain, "1d")]
                paired_data = data.sort(
                    ("nwm_feature_id", "value_time")
                ).group_by_dynamic(
                    "value_time",
                    every="1d",
                    group_by="nwm_feature_id"
                ).agg(
                    pl.col("value").max().alias("predicted")
                ).with_columns(
                usgs_site_code=pl.col("nwm_feature_id").replace_strict(
                    xwalk["nwm_feature_id"], xwalk["usgs_site_code"])
                ).join(obs, on=["usgs_site_code", "value_time"], how="left"
                    ).drop_nulls()

            # Save to parquet
            logger.info(f"Saving {parquet_file}")
            paired_data.write_parquet(parquet_file)

            # Add file to list
            day_files.append(parquet_file)
            
        # Check for at least one file
        if not day_files:
            logger.info(f"Found no data for {domain} {configuration}")
            continue
        
        # Merge files
        logger.info(f"Merging parquet files")
        pairs[(domain, configuration)] = pl.scan_parquet(day_files)
    return pairs

def load_metrics(
        root: Path,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp
) -> dict[tuple[Domain, Configuration], pl.LazyFrame]:
    """
    Download and process NWM and USGS output.

    Parameters
    ----------
    root: Path, required
        Root directory to save downloaded and processed files.
    start_date: pd.Timestamp
        First date to start retrieving data.
    end_date: pd.Timestamp
        Last date to retrieve data.
    
    Returns
    -------
    dict[tuple[Domain, Configuration], pl.LazyFrame]
    """
    logger = get_logger("nwm_explorer.pipelines.load_metrics")
    logger.info("Reading pairs")
    pairs = read_pairs(
        root=root,
        start_date=start_date,
        end_date=end_date
        )

    results = {}
    s = start_date.strftime("%Y%m%dT%H")
    e = end_date.strftime("%Y%m%dT%H")
    pool = ProcessPoolExecutor(max_workers=18)
    for (domain, configuration), paired in pairs.items():
        # Check for file existence
        parquet_directory = root / FileType.parquet / "metrics"
        parquet_file = parquet_directory / f"{domain}_{configuration}_{s}_{e}.parquet"
        logger.info(f"Building {parquet_file}")
        if parquet_file.exists():
            logger.info(f"Found existing {parquet_file}")
            results[(domain, configuration)] = pl.scan_parquet(parquet_file)
            continue
        parquet_directory.mkdir(exist_ok=True, parents=True)

        logger.info(f"Reading pairs {domain} {configuration}")
        if configuration in LEAD_TIME_FREQUENCY:
            groups = ["usgs_site_code", "lead_time_hours_min"]
            data = paired.sort(
                    ("nwm_feature_id", "reference_time", "value_time")
                ).group_by_dynamic(
                    "value_time",
                    every="1d",
                    group_by=["nwm_feature_id", "reference_time"]
                ).agg(
                    pl.col("observed").max(),
                    pl.col("predicted").max(),
                    pl.col("usgs_site_code").first(),
                    pl.col("lead_time_hours_min").min()
                ).with_columns(
                    pl.col("observed").cast(pl.Float32),
                    pl.col("usgs_site_code").cast(pl.Categorical),
                    pl.col("lead_time_hours_min").cast(pl.Int32)
                ).collect()
        else:
            groups = ["usgs_site_code"]
            data = paired.sort(
                    ("nwm_feature_id", "value_time")
                ).group_by_dynamic(
                    "value_time",
                    every="1d",
                    group_by="nwm_feature_id"
                ).agg(
                    pl.col("observed").max(),
                    pl.col("predicted").max(),
                    pl.col("usgs_site_code").first()
                ).with_columns(
                    pl.col("observed").cast(pl.Float32),
                    pl.col("usgs_site_code").cast(pl.Categorical)
                ).collect()

        logger.info(f"Computing metrics {domain} {configuration}")
        df = data.to_pandas()
        chunks = []
        for grp, chunk in df.groupby(groups, observed=True):
            chunks.append(chunk)
        chunk_size = max(1, int(len(chunks) / 18))
        jobs = list(pool.map(compute_metrics_pandas, chunks, chunksize=chunk_size))
        metric_results = pd.DataFrame(jobs)

        # Write results
        logger.info(f"Saving {parquet_file}")
        pl.DataFrame(metric_results).write_parquet(parquet_file)
        results[(domain, configuration)] = pl.scan_parquet(parquet_file)
    pool.shutdown()
    return results
