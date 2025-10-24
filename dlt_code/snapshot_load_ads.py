import requests
import dlt
import json
import ijson
from ijson.common import IncompleteJSONError


URL = "https://jobstream.api.jobtechdev.se/snapshot"
HEADERS = {"accept": "application/json"}


def _get_ads():
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    response.raise_for_status()
    return response.raw


@dlt.resource(table_name="job_ads", write_disposition="merge", primary_key="id")
def snapshot_ads_resource():
    ads_stream = ijson.items(_get_ads(), "item")
    try:
        for ad in ads_stream:
            yield ad
    except IncompleteJSONError:
        print("Error: Stream JSON has been interrupted. Not all data loaded.")


@dlt.source()
def snapshot_ads_source():
    return snapshot_ads_resource()
