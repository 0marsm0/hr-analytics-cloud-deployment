# test.py
from snapshot_load_ads import snapshot_ads_source
import dlt
from pathlib import Path

print("=== Step 1: Testing source ===")
try:
    source = snapshot_ads_source()
    print(f"Source created: {source}")
except Exception as e:
    print(f"ERROR creating source: {e}")
    import traceback

    traceback.print_exc()
    exit(1)

print("\n=== Step 2: Getting resources ===")
for resource_name in source.resources.keys():
    print(f"Resource: {resource_name}")

print("\n=== Step 3: Testing pipeline ===")
db_path = str(Path(__file__).parents[1] / "data_warehouse" / "test_job_ads.duckdb")
print(f"=== DB PATH: {db_path} ===")

# Создай папку если нужно
Path(db_path).parent.mkdir(parents=True, exist_ok=True)

try:
    pipeline = dlt.pipeline(
        pipeline_name="test_snapshot",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(credentials=db_path),
    )
    print("Pipeline created successfully")
except Exception as e:
    print(f"ERROR creating pipeline: {e}")
    import traceback

    traceback.print_exc()
    exit(1)

print("\n=== Step 4: Running load ===")
try:
    load_info = pipeline.run(source)
    print(f"\nLoad info: {load_info}")
    print(f"Has failed jobs: {load_info.has_failed_jobs}")
except Exception as e:
    print(f"ERROR running pipeline: {e}")
    import traceback

    traceback.print_exc()
    exit(1)

print("\n=== Step 5: Checking tables ===")
import duckdb

conn = duckdb.connect(db_path)
tables = conn.execute(
    "SELECT table_schema, table_name FROM information_schema.tables"
).fetchall()
print(f"Tables created: {tables}")

for schema, table in tables:
    count = conn.execute(f'SELECT COUNT(*) FROM "{schema}"."{table}"').fetchone()[0]
    print(f"  {schema}.{table}: {count} rows")

conn.close()
print("\n=== SUCCESS ===")
