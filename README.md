# Hidden Trip 🌴

A Streamlit app to discover offbeat, lesser-known places across South India.

**Live demo:** https://hidden-trip-7nhkw9zt8ugkfjnveqfnqq.streamlit.app/

## Problem Statement

Popular travel lists keep recommending the same crowded tourist spots, so travellers rarely find the quiet, authentic places South India has to offer. Information about offbeat destinations is scattered and hard to filter by what actually matters: location, type of experience and the best season to visit.

## Solution

Hidden Trip puts offbeat places in one searchable, filterable place:

- **Filter** by state, category and season
- **Search** by keyword
- **View results on a map** to plan routes and nearby stops

This directly addresses the problem by making hidden destinations easy to find and compare in seconds.

## Tech Stack

- Python
- Streamlit (UI)
- Pandas (data handling)
- CSV dataset (`places.csv`)

## Project Structure

```
app.py             # Streamlit app
places.csv         # Dataset of offbeat places
requirements.txt   # Dependencies
test_app.py        # Pytest tests
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Testing

```bash
pip install pytest
pytest
```

Tests check that the dataset loads, required columns exist, and filtering and keyword search behave correctly.

## Accessibility

- Clear text labels on every filter and input
- Results shown as text as well as on the map, so information is not map-only
- Default Streamlit theme with readable contrast

## Security

- No user data is collected or stored
- No API keys or secrets are committed to the repository
- The app only reads from a local, static CSV file

## Future Improvements

- More places and states
- User ratings and photos
- Route suggestions between places
