"""Write small, privacy-safe Parquet files for the live app (these DO go to GitHub).

Even though all data is synthetic, we drop identifying fields (names, SSN,
driver's license, passport, street address, exact coordinates) on purpose:
the public app should never show anything that looks like personal information.
"""
import duckdb, pathlib

pathlib.Path("app_data").mkdir(exist_ok=True)
con = duckdb.connect("data/warehouse/kpi.duckdb", read_only=True)

# Members: safe columns only
con.execute("""
COPY (
  SELECT Id AS member_id, BIRTHDATE AS birth_date, DEATHDATE AS death_date,
         GENDER AS gender, RACE AS race, ETHNICITY AS ethnicity,
         replace(COUNTY, ' County', '') AS county, FIPS AS county_fips, INCOME AS income
  FROM raw_patients
) TO 'app_data/members.parquet' (FORMAT parquet)
""")

# Payers: name + type
con.execute("""
COPY (SELECT Id AS payer_id, NAME AS payer_name, OWNERSHIP AS ownership FROM raw_payers)
TO 'app_data/payers.parquet' (FORMAT parquet)
""")

# Claims per year per payer (small summary for the first Home screen)
con.execute("""
COPY (
  SELECT year(c.SERVICEDATE) AS year, p.NAME AS payer_name, count(*) AS claims
  FROM raw_claims c
  LEFT JOIN raw_patients pt ON pt.Id = c.PATIENTID
  LEFT JOIN raw_encounters e ON e.Id = c.APPOINTMENTID
  LEFT JOIN raw_payers p ON p.Id = e.PAYER
  WHERE year(c.SERVICEDATE) BETWEEN 2016 AND 2026
  GROUP BY ALL
) TO 'app_data/claims_by_year.parquet' (FORMAT parquet)
""")

for f in sorted(pathlib.Path("app_data").glob("*.parquet")):
    print(f"✅ {f}  ({f.stat().st_size/1024:,.0f} KB)")
