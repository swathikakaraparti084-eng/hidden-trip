# Hidden Trip: AI Travel Planner for Offbeat India

Travel apps rank places by popularity, so famous spots get crowded while nearby villages, artisans and homestays earn almost nothing. **Hidden Trip** sends some visitors to those hidden places, so locals earn, tourists get unique trips, and famous spots breathe.

**Theme:** Agriculture, Tourism, and Local Development

## How it works
1. The traveller picks a destination, days, budget, travel day and interests.
2. The planner pairs one famous spot per day (least crowded first) with 2-3 nearby hidden places.
3. Hidden places are ranked by **hidden-gem score = uniqueness / popularity**, plus interest match.
4. A local homestay and guide are added when the budget allows.
5. The app shows total spend and how much goes **directly to locals**.
6. "My own place" uses the Claude API to suggest places for any destination.

## Features
- Hidden-gem scoring instead of popularity ranking
- Crowd-spreading visit-time tips (weekday vs weekend)
- Local earnings tracker (rupees and %)
- Built-in data: Hampi, Jaipur, Mysuru, Varanasi
- AI-generated data for any custom place

## Run it
```
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key   # only for "My own place"
streamlit run app.py
```

## Files
- `app.py`: Streamlit app and planner logic
- `places.csv`: dataset (region, type, distance, price, popularity, uniqueness)
- `requirements.txt`: dependencies

## Tech
Python, Streamlit, pandas, Claude API (Anthropic).

## Note
Data is sample or AI-suggested. Prices and places need local verification before real-world use.

## Future scope
Verified local partners and direct booking, live crowd data, regional languages, community-verified fair prices.

## Live demo
https://claude.ai/artifact/8AsHfiqBb4QyhjtmFuDqU7
