"""Print every table's columns + 3 sample rows (saved to docs/data_profile.txt)."""
import duckdb
con = duckdb.connect("data/warehouse/kpi.duckdb", read_only=True)
tables = [r[0] for r in con.execute("SELECT table_name FROM information_schema.tables ORDER BY 1").fetchall()]
for t in tables:
    n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    cols = con.execute(f"DESCRIBE {t}").fetchdf()[["column_name", "column_type"]]
    print(f"\n=== {t} ({n:,} rows, {len(cols)} columns) ===")
    print(", ".join(f"{c} [{ty}]" for c, ty in cols.values))
    print(con.execute(f"SELECT * FROM {t} LIMIT 3").fetchdf().to_string(max_colwidth=25))
