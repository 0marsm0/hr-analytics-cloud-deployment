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


@dlt.resource(table_name="job_ads", write_disposition="merge", primary_key="id")
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

    if not isinstance(start_date, str):
        start_date = start_date.isoformat()

    print(f"Starting stream load from date: {start_date}")

    for line in _get_ads(params={"date": start_date}):
        if line:
            yield json.loads(line)


@dlt.source()
def stream_ads_source():
    return stream_ads_resource()
