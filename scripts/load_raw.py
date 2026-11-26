"""Load every Synthea CSV into one DuckDB database as raw_<table>."""
import duckdb, pathlib

RAW = pathlib.Path("data/raw/synthea/csv")
DB = "data/warehouse/kpi.duckdb"

con = duckdb.connect(DB)
for csv in sorted(RAW.glob("*.csv")):
    table = "raw_" + csv.stem
    con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('{csv}', header=true)")
    rows = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table:<28} {rows:>10,} rows")
con.close()
print(f"\nDone -> {DB}")
