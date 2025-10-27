import os
from dotenv import load_dotenv
import pandas as pd
import duckdb
from pathlib import Path


def get_job_list(query="SELECT * FROM jontech_analysis.marts.mart_main"):
    db_path=str(Path(__file__).parents[1]/"data_warehouse/job_ads.duckdb")

    with duckdb.connect(db_path, read_only=True) as conn:
       return conn.query(f"{query}").df()
   

