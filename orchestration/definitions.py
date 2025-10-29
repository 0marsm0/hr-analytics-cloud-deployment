from pathlib import Path
import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster import define_asset_job, ScheduleDefinition, AssetSelection
from dlt_code.snapshot_load_ads import snapshot_ads_source
from dlt_code.stream_load_ads import stream_ads_source

import sys
import os

# project_root = Path(__file__).parents[1]
# sys.path.insert(0, str(project_root))
# db_path = str(project_root / "data_warehouse/job_ads.duckdb")


# db_path = "/data_warehouse/job_ads.duckdb"

dlt_resource = DagsterDltResource()

# dbt_project_dir = "/pipeline/"
# default_dbt_path = Path.home() / ".dbt"
# dbt_profiles_dir = os.getenv("DBT_PROFILES_DIR", default=default_dbt_path)



if os.path.exists("/pipeline"):  
    project_root = Path("/pipeline")
else:  
    project_root = Path(__file__).parents[1]

sys.path.insert(0, str(project_root))
#db_path = str(project_root / "data_warehouse/job_ads.duckdb")
db_path = os.getenv("DUCKDB_PATH", str(project_root / "data_warehouse/job_ads.duckdb"))

#dbt_project_dir = str(project_root / "dbt_code")
#dbt_profiles_dir = "/root/.dbt" if os.path.exists("/app") else str(Path.home() / ".dbt")
dbt_project_dir = str(project_root / "dbt_code")
dbt_profiles_dir = os.getenv("DBT_PROFILES_DIR", str(Path.home() / ".dbt"))



dbt_project = DbtProject(project_dir=dbt_project_dir, profiles_dir=dbt_profiles_dir)
dbt_resource = DbtCliResource(
    project_dir=dbt_project_dir, profiles_dir=dbt_profiles_dir
)



@dlt_assets(
    dlt_source=snapshot_ads_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="snapshot_ads",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(credentials=db_path),
    ),
)
def dlt_snapshot_asset(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


@dlt_assets(
    dlt_source=stream_ads_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="stream_ads",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(credentials=db_path),
    ),
)
def dlt_stream_asset(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


dbt_project.prepare_if_dev()


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


snapshot_job = define_asset_job(
    "snapshot_job",
    selection=AssetSelection.assets(dlt_snapshot_asset).downstream(),
)

# stream_job = define_asset_job(
#     "stream_job",
#     selection=AssetSelection.assets(dlt_stream_asset).downstream(),
# )

daily_schedule = ScheduleDefinition(job=snapshot_job, cron_schedule="@daily")

defs = dg.Definitions(
    assets=[dlt_snapshot_asset, dbt_models],
    resources={"dlt": dlt_resource, "dbt": dbt_resource},
    schedules=[daily_schedule],
)
