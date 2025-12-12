import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide", page_title="India Census Map Explorer")

# -------- CONFIG --------
DEFAULT_CSV_PATH = r"C:\Users\H P\Desktop\DSMP\Plotly\mini_proj\datasets\final_india.csv"  # point to your cleaned CSV

# -------- Load data (no checks) --------
df = pd.read_csv(DEFAULT_CSV_PATH)

# -------- Compute small derived fields if missing (Internet_Penetration) --------
# Compute Internet_Penetration if not present but base columns exist
if "Internet_Penetration" not in df.columns:
    if {"Households_Internet", "Households_Total"}.issubset(df.columns):
        # protect against zero division
        df["Internet_Penetration"] = (pd.to_numeric(df["Households_Internet"], errors="coerce")
                                      / pd.to_numeric(df["Households_Total"], errors="coerce")) * 100
    else:
        # will show N/A later if not computable
        pass

# -------- Canonical column names (YOU SAID THESE EXIST) --------
STATE = "State"
DIST  = "District"
LAT   = "Latitude"
LON   = "Longitude"
POP   = "Population"

# -------- Sidebar controls --------
st.sidebar.title("Filters & Options")

state_list = ["Whole India"] + sorted(df[STATE].fillna("Unknown").unique().tolist())
selected_state = st.sidebar.selectbox("State", state_list)

# choose numeric columns for primary & secondary
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# defaults
default_primary = "Population" if "Population" in numeric_cols else numeric_cols[0]
default_secondary = "Literacy_Rate" if "Literacy_Rate" in numeric_cols else ("Sex_Ratio" if "Sex_Ratio" in numeric_cols else (numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]))

primary = st.sidebar.selectbox("Primary (point size)", numeric_cols, index=numeric_cols.index(default_primary))
# prevent exact same selection for color
secondary_options = [c for c in numeric_cols if c != primary]
secondary = st.sidebar.selectbox("Secondary (color)", secondary_options, index=secondary_options.index(default_secondary) if default_secondary in secondary_options else 0)

use_log_color = st.sidebar.checkbox("Log scale for color (best effort)", value=False)
search_district = st.sidebar.text_input("Search district substring (optional)")

# -------- Data filtering & prep (straightforward) --------
df_work = df.copy()

if selected_state != "Whole India":
    df_work = df_work[df_work[STATE] == selected_state]

if search_district.strip():
    df_work = df_work[df_work[DIST].astype(str).str.contains(search_district.strip(), case=False, na=False)]

# prepare numeric columns used
df_work["_primary_raw"] = pd.to_numeric(df_work[primary], errors="coerce")
df_work["_secondary_raw"] = pd.to_numeric(df_work[secondary], errors="coerce")
df_work["_pop"] = pd.to_numeric(df_work[POP], errors="coerce")

# here we do NOT normalize (per your request)
df_work["_primary"] = df_work["_primary_raw"]
df_work["_secondary"] = df_work["_secondary_raw"]

# -------- KPIs (compact) --------
st.title("India Census — Minimal Map Explorer")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Districts Shown", f"{len(df_work):,}")

with k2:
    st.metric("Avg Literacy Rate (%)", f"{df_work['Literacy_Rate'].mean():.2f}" if "Literacy_Rate" in df_work.columns else "N/A")

with k3:
    st.metric("Avg Sex Ratio (F per 1000 M)", f"{df_work['Sex_Ratio'].mean():.1f}" if "Sex_Ratio" in df_work.columns else "N/A")

with k4:
    # Internet_Penetration will be shown if present and has numeric values; otherwise N/A
    if "Internet_Penetration" in df_work.columns and df_work["Internet_Penetration"].notna().any():
        st.metric("Avg Internet Penetration (%)", f"{df_work['Internet_Penetration'].mean():.2f}")
    else:
        st.metric("Avg Internet Penetration (%)", "N/A")

st.markdown("---")

# -------- Map (Plotly) --------
st.subheader("Map")
hover_cols = [DIST, STATE, POP, primary, secondary]
# ensure hover columns exist in df_work
hover_cols = [c for c in hover_cols if c in df_work.columns]

fig = px.scatter_mapbox(
    df_work,
    lat=LAT,
    lon=LON,
    size="_primary",
    color="_secondary",
    color_continuous_scale="Viridis",
    hover_name=DIST,
    hover_data=hover_cols,
    size_max=30,
    zoom=4 if selected_state == "Whole India" else 6,
    mapbox_style="open-street-map",
)


if use_log_color:
    try:
        numeric_secondary = pd.to_numeric(df_work["_secondary"], errors="coerce").fillna(0)
        fig.update_traces(marker=dict(color=np.log1p(numeric_secondary),
                                      colorscale="Plasma")) 
    except Exception:
        st.warning("Log transform failed; showing linear color.")

st.plotly_chart(fig, width='stretch', height=900)

# -------- Simple bar chart --------
st.subheader(f"Top {min(10, len(df_work))} districts by {secondary} (Descending Order)")
top_bar = df_work.sort_values("_secondary", ascending=False).head(10)
if len(top_bar) > 0:
    fig2 = px.bar(top_bar, x=DIST, y="_secondary", hover_data=[POP, primary], labels={"_secondary": secondary, DIST: "District"},text_auto=True)
    fig2.update_traces(marker_color='#DC3131')   
    fig2.update_layout(xaxis_tickangle=-45, height=400)
    st.plotly_chart(fig2, width='stretch')
else:
    st.info("No rows to show in bar chart.")

# -------- Data preview (minimal) --------
st.markdown("---")
st.subheader("Filtered Data Preview")

# Candidate columns we want to show (in order)
cols_to_show = [DIST, STATE, POP, primary, secondary, "Sex_Ratio", "Literacy_Rate"]
# Build unique ordered list
seen = set()
safe_cols = []
for c in cols_to_show:
    if not c:
        continue
    if c not in df_work.columns:
        continue
    if c in seen:
        continue
    seen.add(c)
    safe_cols.append(c)

# Fallback if nothing to show
if len(safe_cols) == 0:
    fallback = []
    for candidate in [DIST, STATE]:
        if candidate in df_work.columns:
            fallback.append(candidate)
    numeric_candidates = df_work.select_dtypes(include=[np.number]).columns.tolist()
    for n in numeric_candidates[:6]:
        if n not in fallback:
            fallback.append(n)
    safe_cols = fallback

st.dataframe(df_work[safe_cols].head(200))
st.caption(f"Data source: India Census 2011 - Demographic Census Data")
