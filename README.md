# ✦ Ask Your KPIs — Health Plan Edition

An AI analyst for a **fictional** health insurance company, *Bluewave Health Plan* (Florida).
Ask questions in plain English and get an answer, a chart, and the exact SQL behind it.

🔗 **Live demo:** _coming soon_
🧪 **Data:** 100% synthetic, generated with [Synthea](https://synthea.mitre.org). No real patient data.

> 🚧 Work in progress: Phase 0 (setup + first live app). See the project plan for what's coming.

---

## ▶️ Run it on your computer (3 steps)

**You need:** [Python 3.12](https://www.python.org/downloads/) (Mac, Windows or Linux).

1. **Download the project**
   ```bash
   git clone https://github.com/YOUR-USERNAME/ask-your-kpis-health.git
   cd ask-your-kpis-health
   ```
2. **Run one command**
   ```bash
   ./run.sh
   ```
   The first run takes 1–3 minutes to install everything. After that it starts in seconds.
3. **Your browser opens the app** at http://localhost:8501. Press `Ctrl+C` in the terminal to stop.

That's it. The small, ready-to-use data files are already included in `app_data/`.

<details>
<summary><b>Optional: rebuild all the data from scratch</b></summary>

Needs [Java 17+](https://adoptium.net) as well. This downloads Synthea, generates 1,000 Florida patients
(seed 42, so the result is identical every time), loads them into DuckDB and re-exports the app data:

```bash
./run.sh --rebuild
```
</details>

<details>
<summary><b>Windows users</b></summary>

Use Git Bash or WSL to run `./run.sh`, or run these in PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\streamlit run app/Home.py
```
</details>

---

## What's inside

| Folder | What it is |
|---|---|
| `app/` | The Streamlit web app |
| `app_data/` | Small, privacy-safe data files the app reads (in GitHub) |
| `scripts/` | Generate data → load into DuckDB → profile → export app data |
| `docs/` | Data profile, findings, screenshots |
| `data/` | Raw Synthea files + DuckDB database (created locally, **not** in GitHub) |

## Data

| Source | What it is |
|---|---|
| **Synthea** (MITRE) | Synthetic patients, visits, diagnoses, labs, medications, insurance plans and claims |
| **CMS Star Ratings** *(coming)* | Real Medicare plan quality cut points, used as a benchmark |
| **CDC PLACES** *(coming)* | Real county-level chronic disease rates |

Identifying fields (names, SSN, addresses, coordinates) are removed before any data reaches the app, even though they are synthetic.

## Built with
Python · SQL · DuckDB · Streamlit · Plotly *(more coming: dbt + MetricFlow, Tableau, FHIR, MCP, GitHub Actions)*

---
Built by **Juan Villegas** · Miami, FL
