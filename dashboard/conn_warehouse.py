import os
import pandas as pd
import duckdb

from pathlib import Path

DB_PATH = Path("/mnt/data/job_ads.duckdb")

def get_job_list(query="SELECT * FROM jontech_analysis.marts.mart_main"):
   # db_path = "/data_warehouse/job_ads.duckdb"
   # db_path = os.getenv("DUCKDB_PATH", "/pipeline/data_warehouse/job_ads.duckdb")
    # db_path=str(Path(__file__).parents[1]/"data_warehouse/job_ads.duckdb")

    with duckdb.connect(DB_PATH, read_only=True) as conn:
        return conn.query(f"{query}").df()
