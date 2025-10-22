import requests
import dlt
import json


URL = "https://jobstream.api.jobtechdev.se/snapshot"
occupation_fields = {
    "Data/IT": "apaJ_2ja_LuF",
    "Transport, distribution, lager": "ASGV_zcE_bWf",
    "Hälso- och sjukvård": "NYW6_mP6_vwf",
}
HEADERS = {"accept": "application/json"}


def _get_ads():
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    response.raise_for_status()
    return response.iter_lines()


@dlt.resource(table_name="all_jobs", write_disposition="merge", primary_key="id")
def snapshot_ads_resource():
    for ad in _get_ads():
        yield json.loads(ad)


@dlt.source()
def snapshot_ads_source():
    return snapshot_ads_resource()
