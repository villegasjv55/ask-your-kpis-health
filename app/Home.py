"""Ask Your KPIs — Health Plan Edition · Home (Phase 0 starter)."""
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Ask Your KPIs · Health Plan", page_icon="✦", layout="wide")

st.title("✦ Ask Your KPIs — Health Plan Edition")
st.caption(
    "Bluewave Health Plan (fictional) · Florida · 100% synthetic data generated with "
    "[Synthea](https://synthea.mitre.org) · work in progress"
)

# Find app_data/ next to this project, no matter which folder the app is started from
DATA = Path(__file__).resolve().parent.parent / "app_data"

con = duckdb.connect()
members = con.execute(f"SELECT * FROM '{DATA / 'members.parquet'}'").fetchdf()
payers = con.execute(f"SELECT * FROM '{DATA / 'payers.parquet'}'").fetchdf()
claims = con.execute(f"SELECT * FROM '{DATA / 'claims_by_year.parquet'}'").fetchdf()

living = members[members["death_date"].isna()].copy()
living["age"] = (pd.Timestamp.today() - pd.to_datetime(living["birth_date"])).dt.days // 365

c1, c2, c3, c4 = st.columns(4)
c1.metric("Members (living)", f"{len(living):,}")
c2.metric("Average age", f"{living['age'].mean():.0f}")
c3.metric("Counties", f"{living['county'].nunique():,}")
c4.metric("Claims since 2016", f"{int(claims['claims'].sum()):,}")

left, right = st.columns(2)
with left:
    st.subheader("Claims per year")
    by_year = claims.groupby("year", as_index=False)["claims"].sum()
    fig = px.line(by_year, x="year", y="claims", markers=True)
    fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0), yaxis_title=None, xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Members by county (top 12)")
    by_county = living["county"].value_counts().head(12).sort_values().reset_index()
    by_county.columns = ["county", "members"]
    fig = px.bar(by_county, x="members", y="county", orientation="h")
    fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0), yaxis_title=None, xaxis_title=None)
    fig.update_traces(marker_color="#14B8A6")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Claims by payer (since 2016)")
by_payer = claims.groupby("payer_name", as_index=False)["claims"].sum().sort_values("claims", ascending=False)
st.dataframe(by_payer, hide_index=True, use_container_width=True)

st.info("🚧 Coming next: governed KPIs (cost per member, denial rate, ER visits per 1,000), "
        "Question Library, Ask-a-question, Quality & Star Ratings.")
