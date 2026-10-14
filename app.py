# Hidden Trip - discover offbeat places in South India
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hidden Trip", page_icon="🧭", layout="wide")


@st.cache_data
def load_places():
    return pd.read_csv("places.csv")


df = load_places()

st.title("🧭 Hidden Trip")
st.caption("Discover offbeat places across South India")

# Sidebar filters
st.sidebar.header("Filters")
states = st.sidebar.multiselect("State", sorted(df["state"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["category"].unique()))
seasons = st.sidebar.multiselect("Best season", sorted(df["best_season"].unique()))
query = st.sidebar.text_input("Search by name or keyword")

filtered = df.copy()
if states:
    filtered = filtered[filtered["state"].isin(states)]
if categories:
    filtered = filtered[filtered["category"].isin(categories)]
if seasons:
    filtered = filtered[filtered["best_season"].isin(seasons)]
if query:
    q = query.lower()
    mask = filtered["name"].str.lower().str.contains(q) | filtered[
        "description"
    ].str.lower().str.contains(q)
    filtered = filtered[mask]

st.subheader(f"{len(filtered)} place(s) found")

if filtered.empty:
    st.info("No places match your filters. Try removing a few.")
else:
    st.map(filtered.rename(columns={"lat": "latitude", "lon": "longitude"}))

    cols = st.columns(2)
    for i, (_, row) in enumerate(filtered.iterrows()):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"### {row['name']}")
                st.write(f"📍 {row['state']}  |  🏷️ {row['category']}  |  🗓️ {row['best_season']}")
                st.write(row["description"])
                maps_url = f"https://www.google.com/maps?q={row['lat']},{row['lon']}"
                st.markdown(f"[Open in Google Maps]({maps_url})")
