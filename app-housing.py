from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(page_title="California Housing Data", page_icon="🏠", layout="wide")

DATA_PATH = Path(__file__).with_name("housing.csv")


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Load the California housing districts once per data-file change."""
    return pd.read_csv(path)


housing = load_data(DATA_PATH)
location_types = sorted(housing["ocean_proximity"].dropna().unique())

st.title("California Housing Data (1990) by Gao Yi")
minimum_value = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500_001,
    value=200_000,
)
st.subheader("See more filters in the sidebar:")

with st.sidebar:
    st.header("Filters")
    selected_locations = st.multiselect(
        "Choose the location type",
        options=location_types,
        default=location_types,
    )
    income_level = st.radio(
        "Choose income level",
        options=["Low", "Medium", "High"],
        index=1,
    )

filtered = housing[
    (housing["median_house_value"] >= minimum_value)
    & (housing["ocean_proximity"].isin(selected_locations))
].copy()

# The income-level filter uses the three requested bands.
if income_level == "Low":
    filtered = filtered[filtered["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered = filtered[
        (filtered["median_income"] > 2.5) & (filtered["median_income"] < 4.5)
    ]
else:
    filtered = filtered[filtered["median_income"] >= 4.5]

st.caption(f"{len(filtered):,} California districts match the current filters.")

if filtered.empty:
    st.warning("No districts match these filters. Adjust the slider or sidebar filters.")
else:
    st.map(filtered[["latitude", "longitude"]])

    figure, axis = plt.subplots(figsize=(9, 4))
    axis.hist(filtered["median_house_value"], bins=30, color="#4C78A8", edgecolor="white")
    axis.set_title("Median House Value for Filtered Districts")
    axis.set_xlabel("Median house value (USD)")
    axis.set_ylabel("Number of districts")
    figure.tight_layout()
    st.pyplot(figure)
