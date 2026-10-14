"""Basic tests for the Hidden Trip app.

Run with:  pytest
NOTE: If your CSV uses different column names, edit the constants below.
"""
import pandas as pd
import pytest

CSV_PATH = "places.csv"
STATE_COL = "state"
CATEGORY_COL = "category"
SEASON_COL = "best_season"
NAME_COL = "name"


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(CSV_PATH)


def filter_places(data, state=None, category=None, season=None, keyword=None):
    """Same filtering idea the app uses: all filters are optional."""
    result = data
    if state:
        result = result[result[STATE_COL] == state]
    if category:
        result = result[result[CATEGORY_COL] == category]
    if season:
        result = result[result[SEASON_COL] == season]
    if keyword:
        mask = result.astype(str).apply(
            lambda col: col.str.contains(keyword, case=False, na=False)
        ).any(axis=1)
        result = result[mask]
    return result


def test_csv_loads_and_not_empty(df):
    assert not df.empty


def test_required_columns_exist(df):
    for col in [NAME_COL, STATE_COL, CATEGORY_COL, SEASON_COL]:
        assert col in df.columns, f"Missing column: {col}"


def test_no_missing_names(df):
    assert df[NAME_COL].notna().all()


def test_filter_by_state(df):
    state = df[STATE_COL].iloc[0]
    result = filter_places(df, state=state)
    assert len(result) > 0
    assert (result[STATE_COL] == state).all()


def test_keyword_search_is_case_insensitive(df):
    name = str(df[NAME_COL].iloc[0])
    result = filter_places(df, keyword=name.upper())
    assert len(result) >= 1


def test_unknown_keyword_returns_empty(df):
    assert filter_places(df, keyword="zzzz_no_match_zzzz").empty
