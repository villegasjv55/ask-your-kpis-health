# Data findings: Synthea Florida, 1,000 patients, seed 42

Generated Nov 26, 2026. Full column list: `docs/data_profile.txt`.

## Row counts
| Table | Rows |
|---|---|
| patients | 1,145 (1,000 living + 145 who died in the simulation) |
| encounters | 80,909 |
| claims | 156,508 |
| claims_transactions | 1,649,643 |
| observations (labs, vitals) | 1,044,730 |
| procedures | 206,270 |
| conditions | 45,444 |
| payer_transitions | 50,705 |
| payers | 10 |

## What we learned (and what it changes)
1. **Payers use real company names** (Cigna, Aetna, Anthem, Humana, UnitedHealthcare, Blue Cross Blue Shield)
   plus Medicare, Medicaid, Dual Eligible and No Insurance. → Rename to fictional plan products so fake data
   is never attached to real insurers' names.
2. **No claim denials.** Every claim is CLOSED (156,366) or BILLED (142). → Denial status and reasons must be a
   labeled synthetic enrichment (planned).
3. **History is long.** Service dates go back to 1918 (lifetime records); claims are dense from ~2017 to Nov 2026.
   → Analyze 2017 → 2026 and treat 2026 as a partial year.
4. **Quality measures we can support:** A1c tests (11,321, LOINC 4548-4), blood pressure (17,992),
   diabetic retinal eye exams (690), colonoscopies (570), flu vaccines (9,221), mammography (127).
5. **Counties match real FIPS codes** (patients.FIPS), so CDC PLACES joins cleanly.
6. **Small denominators at 1,000 patients** (e.g. diabetes). → Consider 5,000 patients later.
7. **Identifying-looking fields exist** (names, SSN, passport, address, lat/lon; all synthetic). → Dropped
   before export; never shown in the app.
