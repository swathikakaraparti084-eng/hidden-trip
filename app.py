"""Hidden Trails: an AI trip planner that mixes one famous spot a day
with nearby hidden places so locals earn and famous spots get less crowded.

Run:  pip install -r requirements.txt
      export ANTHROPIC_API_KEY=your_key   (only needed for "My own place")
      streamlit run app.py
"""
import json
import os

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hidden Trails", page_icon="🛕", layout="centered")

REGIONS = {"hampi": "Hampi (Karnataka)", "jaipur": "Jaipur (Rajasthan)",
           "mysuru": "Mysuru (Karnataka)", "varanasi": "Varanasi (Uttar Pradesh)"}
TYPES = ["famous", "temple", "nature", "artisan", "food", "village", "homestay", "guide"]
INTERESTS = {"Temples": "temple", "Nature": "nature", "Crafts": "artisan",
             "Food": "food", "Village life": "village"}
COLS = ["id", "name", "type", "km", "price", "time", "popularity", "uniqueness", "description"]


# ---------- data ----------
@st.cache_data
def load_csv() -> pd.DataFrame:
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "places.csv"))


def region_places(key: str) -> pd.DataFrame:
    df = load_csv()
    return df[df.region == key].drop(columns="region").reset_index(drop=True)


def generate_places(place: str) -> pd.DataFrame:
    """Ask Claude for places around any destination. Verify results before real use."""
    import anthropic  # imported here so the app works without the key for built-in regions

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    prompt = (
        f"You help tourists find hidden places. Destination: {place} (India). "
        "Return ONLY a JSON array, no other text. Each item is an array: "
        "[id, name, type, km_from_city_centre, price_inr_per_person, best_time, "
        "popularity_1to10, uniqueness_1to10, one_line_description]. "
        "Include exactly 3 well-known famous spots (type 'famous', popularity 8-10) and "
        "8-10 lesser-known REAL places within 40 km that you are confident exist "
        "(popularity 1-5, uniqueness 6-9). Allowed types: " + ", ".join(TYPES) + ". "
        "Cover temple, nature, artisan, food and village, plus one homestay and one guide. "
        "Prices are rough INR estimates."
    )
    msg = client.messages.create(model="claude-sonnet-5-5", max_tokens=3000,
                                 messages=[{"role": "user", "content": prompt}])
    text = msg.content[0].text.replace("```json", "").replace("```", "").strip()
    rows = [r for r in json.loads(text) if len(r) >= 9 and r[2] in TYPES]
    df = pd.DataFrame([r[:9] for r in rows], columns=COLS)
    for c in ["km", "price", "popularity", "uniqueness"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(5)
    df["popularity"] = df["popularity"].clip(lower=1)
    if not (df.type == "famous").any():
        raise ValueError("No famous anchor spot found")
    if not (df.type == "homestay").any():
        df.loc[len(df)] = ["H98", "Local family homestay (ask locals)", "homestay", 5, 1500,
                           "Evening stay", 2, 7, "Confirm details before booking."]
    if not (df.type == "guide").any():
        df.loc[len(df)] = ["H99", "Local guide (ask locals)", "guide", 0, 800,
                           "Full day", 2, 7, "Guide for quiet spots and timings."]
    return df


# ---------- planner ----------
def plan_trip(df: pd.DataFrame, days: int, budget: int, wanted: list[str]):
    df = df.copy()
    df["gem"] = df.uniqueness / df.popularity  # hidden-gem score
    famous = df[df.type == "famous"].sort_values("popularity")  # least crowded first
    stay = df[df.type == "homestay"].iloc[0]
    guide = df[df.type == "guide"].iloc[0]
    pool = df[~df.type.isin(["famous", "homestay", "guide"])].copy()
    pool["rank"] = pool.gem + pool.type.isin(wanted) * 3
    pool = pool.sort_values("rank", ascending=False)

    spent = local = 0
    itinerary = []
    for d in range(days):
        items, fam = [], famous.iloc[d % len(famous)]
        if spent + fam.price <= budget:
            items.append(fam)
            spent += fam.price
        if d == 0 and budget >= 2500 and spent + guide.price <= budget:
            items.append(guide)
            spent += guide.price
            local += guide.price
        picked = []
        for _, p in pool.iterrows():
            if len(picked) == 3:
                break
            if spent + p.price <= budget:
                picked.append(p)
                spent += p.price
                local += p.price
        pool = pool[~pool.id.isin([p.id for p in picked])]
        items += sorted(picked, key=lambda x: x.km)
        night = None
        if d < days - 1 and spent + stay.price <= budget:
            night = stay
            spent += stay.price
            local += stay.price
        itinerary.append((fam, items, night))
    return itinerary, spent, local


# ---------- UI ----------
st.title("🛕 Hidden Trails")
st.caption("One famous spot a day, plus hidden places nearby, so locals earn and famous spots breathe.")

choice = st.selectbox("Choose your destination", list(REGIONS) + ["custom"],
                      format_func=lambda k: REGIONS.get(k, "✏️ My own place…"))
own = st.text_input("Type any place", placeholder="e.g. Udaipur, Orchha") if choice == "custom" else ""
days = st.selectbox("Days", [1, 2, 3, 4], index=1)
budget = st.number_input("Total budget per person (₹)", 500, 100000, 4000, step=100)
busy = st.radio("Travelling on", ["Weekday", "Weekend / festival (busier)"], horizontal=True).startswith("Weekend")
picked = st.multiselect("Interests", list(INTERESTS), default=["Temples", "Nature"])

if st.button("Plan my trip", type="primary", use_container_width=True):
    try:
        if choice == "custom":
            if not own.strip():
                st.warning("Type a place name first.")
                st.stop()
            with st.spinner(f"Finding hidden gems near {own}…"):
                data = generate_places(own.strip())
            st.info("AI-suggested places. Verify each one on Google Maps before travelling.")
        else:
            data = region_places(choice)
        itinerary, spent, local = plan_trip(data, days, int(budget), [INTERESTS[i] for i in picked])
    except Exception as e:  # missing key, bad JSON, etc.
        st.error(f"Could not build the plan: {e}")
        st.stop()

    c1, c2 = st.columns(2)
    c1.metric("Total spend", f"₹{spent:,.0f}")
    c2.metric("Goes directly to locals", f"₹{local:,.0f}", f"{local / spent * 100 if spent else 0:.0f}%")

    for i, (fam, items, night) in enumerate(itinerary, 1):
        with st.container(border=True):
            st.subheader(f"Day {i}")
            for p in items:
                tag = "🏛️ famous" if p.type == "famous" else f"💎 hidden gem {p.uniqueness / p.popularity:.1f}"
                st.markdown(f"**{p['name']}** · {tag} · {'Free' if p.price == 0 else f'₹{p.price:,.0f}'}  \n"
                            f"{p.description}  \n_{p.time} · {p.km:g} km from city centre_")
            if night is not None:
                st.markdown(f"🏠 **Night: {night['name']}** · local-owned · ₹{night.price:,.0f}")
            st.info(f"Visit {fam['name']} at opening time and spend the afternoon at the hidden places."
                    if busy else f"Visit {fam['name']} at {fam.time.lower()} to beat the crowds.")
    st.caption("Prices are estimates. Contacts are not included in this demo dataset.")
