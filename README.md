# Hidden Trip

A small Streamlit app to discover offbeat places across South India.
Filter by state, category and season, search by keyword, and view results on a map.

## Files
- `app.py` - the Streamlit app
- `places.csv` - the places data (must stay in the same folder as `app.py`)
- `requirements.txt` - Python dependencies

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```

## Deploy free on Streamlit Community Cloud
1. Push these files to a GitHub repo.
2. Go to share.streamlit.io and sign in with GitHub.
3. Choose the repo, set the main file to `app.py`, and deploy.

## Add more places
Add a new row to `places.csv` with: name, state, category, lat, lon, best_season, description.
