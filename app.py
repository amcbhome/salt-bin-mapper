import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# -------------------------
# App configuration
# -------------------------
st.set_page_config(
    page_title="Council Salt Bin Mapper",
    layout="wide"
)

st.title("🧂 Council Salt Bin Mapping Tool")
st.caption("Interactive map of salt bins by UNIT_AREA")

# -------------------------
# Load data
# -------------------------
@st.cache_data
def load_data():
    return pd.read_excel("data/Saltbins_with_UNIT_AREA.xlsx")

df = load_data()

# -------------------------
# Sidebar controls
# -------------------------
st.sidebar.header("Filter")
unit_areas = sorted(df["UNIT_AREA"].dropna().unique())
selected_area = st.sidebar.selectbox(
    "Select UNIT_AREA",
    unit_areas
)

# -------------------------
# Filter data
# -------------------------
area_df = df[df["UNIT_AREA"] == selected_area]

# -------------------------
# KPIs
# -------------------------
st.subheader(f"UNIT_AREA: {selected_area}")

col1, col2 = st.columns(2)
col1.metric("Salt Bin Count", len(area_df))
col2.metric("Unique UNITNOs", area_df["UNITNO"].nunique())

# -------------------------
# Map
# -------------------------
if not area_df.empty:
    center_lat = area_df["LAT"].mean()
    center_lon = area_df["LONG"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles="CartoDB positron"
    )

    for _, row in area_df.iterrows():
        folium.CircleMarker(
            location=[row["LAT"], row["LONG"]],
            radius=5,
            popup=f"UNITNO: {row['UNITNO']}",
            color="blue",
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    st.subheader("📍 Salt Bin Locations")
    st_folium(m, width=1000, height=600)
else:
    st.warning("No salt bins found for this UNIT_AREA.")

# -------------------------
# Table output
# -------------------------
st.subheader("📋 Salt Bin List")
st.dataframe(
    area_df[["UNITNO", "LAT", "LONG"]],
    use_container_width=True
)
