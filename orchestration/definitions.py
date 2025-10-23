from pathlib import Path
import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster import define_asset_job, ScheduleDefinition, AssetSelection
from data_extract_load.snapshot_load_ads import snapshot_ads_source
from data_extract_load.stream_load_ads import stream_ads_source
import sys


project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root))

db_path = str(Path(__file__).parents[1] / "data_warehouse/job_ads.duckdb")

dlt_resource = DagsterDltResource()


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


dbt_project_dir = str(Path(__file__).parents[1] / "data_transformation")
dbt_profiles_dir = Path("/pipeline")

dbt_project = DbtProject(project_dir=dbt_project_dir, profiles_dir=dbt_profiles_dir)
dbt_resource = DbtCliResource(project_dir=dbt_project_dir)

dbt_project.prepare_if_dev()


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


stream_job = define_asset_job(
    "stream_job", selection=AssetSelection.keys("dlt_stream_asset").downstream()
)
daily_schedule = ScheduleDefinition(job=stream_job, cron_schedule="@daily")

defs = dg.Definitions(
    assets=[dlt_snapshot_asset, dlt_stream_asset, dbt_models],
    resources={"dlt": dlt_resource, "dbt": dbt_resource},
    schedules=[daily_schedule],
)
