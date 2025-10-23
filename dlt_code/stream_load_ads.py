import requests
import dlt
import json
from datetime import datetime, timedelta


URL = "https://jobstream.api.jobtechdev.se/stream"
HEADERS = {"accept": "application/json"}


def _get_ads(params):
    response = requests.get(url=URL, headers=HEADERS, stream=True, params=params)
    response.raise_for_status()
    return response.iter_lines()


@dlt.resource(table_name="all_jobs", write_disposition="merge", primary_key="id")
def stream_ads_resource(
    publication_date_bookmark=dlt.sources.incremental(
        cursor_path="publication_date",
        initial_value=(
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            - timedelta(days=7)
        ).isoformat(),
    )
):
    start_date = publication_date_bookmark.last_value

    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date)

    for ad in _get_ads(params={"date": str(start_date)}):
        yield json.loads(ad)


@dlt.source()
def stream_ads_source():
    return stream_ads_resource()
