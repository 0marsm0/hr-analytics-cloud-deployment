import requests
import dlt
from datetime import timedelta, datetime, date
from dlt.sources import incremental


URL = "https://jobsearch.api.jobtechdev.se/search"
occupation_fields = {
    "Data/IT": "apaJ_2ja_LuF",
    "Transport, distribution, lager": "ASGV_zcE_bWf",
    "Hälso- och sjukvård": "NYW6_mP6_vwf",
}
HEADERS = {"accept": "application/json"}


def _get_ads(params):
    response = requests.get(URL, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


@dlt.resource(write_disposition="merge", primary_key="id")
def job_ads_resource(
    publication_date_bookmark=dlt.sources.incremental(cursor_column="publication_date"),
):
    delta_day = timedelta(days=1)
    delta_week = timedelta(days=7)
    # delta_month = timedelta(days=30)
    delta_year = timedelta(days=365)
    end = datetime.now().date() - delta_year

    for key, job in occupation_fields.items():
        limit = 100
        current_date = datetime.now().date()

        while current_date > end:
            offset = 0

            while True:

                params = {
                    "occupation-field": job,
                    "limit": 100,
                    "offset": offset,
                    "published-after": current_date - delta_week,
                    "published-before": current_date,
                }

                job_ads = _get_ads(params=params).get("hits", [])

                if not job_ads:
                    break

                for ad in job_ads:
                    ad["occupation_field"] = key
                    yield ad

                offset += limit

            current_date = current_date - delta_week


# today = datetime.now().date()
# week = today - timedelta(weeks=1)
# print(
#     _get_ads(params={"occupation-field": "apaJ_2ja_LuF", "published-after": week})[
#         "total"
#     ]
# )
# print(today)
