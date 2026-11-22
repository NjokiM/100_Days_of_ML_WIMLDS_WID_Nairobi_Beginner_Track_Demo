"""Day 6: Data cleaning with Pandas. Missing values, duplicates, type conversions.

Task: clean the raw messy customer dataset.
Fill in each function (replace the `raise NotImplementedError` line), then run:   python day06_cleaning.py
Each function takes a DataFrame and RETURNS a new one; never modify the input in place.
"""
import pandas as pd

CSV = "data/customers_raw.csv"


def missing_report(df):
    """Return a Series: number of missing values per column, largest first. Hint: isna().sum()."""
    # TODO: write your code here (the docstring above has a hint)
    raise NotImplementedError("your turn")


def remove_duplicates(df):
    """Drop exact duplicate rows (keep the first). Hint: drop_duplicates."""
    # TODO: write your code here (the docstring above has a hint)
    raise NotImplementedError("your turn")


def clean_text(df):
    """name and city: strip stray spaces and use Title Case ("  nairobi " -> "Nairobi").
    Missing cities become the text "Unknown". Hint: .str.strip().str.title(), then fillna."""
    df = df.copy()
    # TODO: write your code here (the docstring above has a hint)
    raise NotImplementedError("your turn")
    return df


def fix_types(df):
    """income: text like "$54,000" -> float 54000.0.  signup_date: text in two formats -> datetime.
    Hint: str.replace with regex=True to remove "$" and ","; astype(float); pd.to_datetime(..., format="mixed")."""
    df = df.copy()
    # TODO: write your code here (the docstring above has a hint)
    raise NotImplementedError("your turn")
    return df


def fix_impossible_ages(df):
    """Ages below 16 or above 100 are data-entry errors: turn them into missing values (NaN).
    Hint: Series.where(condition) keeps values where the condition is True and sets NaN elsewhere."""
    df = df.copy()
    # TODO: write your code here (the docstring above has a hint)
    raise NotImplementedError("your turn")
    return df


def fill_missing(df):
    """Fill missing age with the median age and missing income with the median income."""
    df = df.copy()
    # TODO: write your code here (the docstring above has a hint)
    raise NotImplementedError("your turn")
    return df


def clean_pipeline(df):
    """Apply every step in a sensible order and return the clean DataFrame with a fresh 0..n-1 index.
    Think about the order: ages must be fixed BEFORE filling missing values; types before medians."""
    # TODO: write your code here (the docstring above has a hint)
    raise NotImplementedError("your turn")


# ------------------------------------------------------------------ checks (do not edit)
def _raw():
    return pd.read_csv(CSV)


def _check_missing_report():
    r = missing_report(_raw())
    assert r.iloc[0] >= r.iloc[-1] and r["income"] == _raw()["income"].isna().sum() and r["customer_id"] == 0


def _check_dups():
    raw = _raw(); out = remove_duplicates(raw)
    assert out.duplicated().sum() == 0 and len(out) == 200 and len(raw) == 215


def _check_text():
    out = clean_text(_raw())
    assert out["city"].isna().sum() == 0 and "Unknown" in set(out["city"])
    assert set(out["city"]) <= {"Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Unknown"}, set(out["city"])
    assert all(n == n.strip() and n == n.title() for n in out["name"])


def _check_types():
    out = fix_types(_raw())
    assert pd.api.types.is_float_dtype(out["income"]) and pd.api.types.is_datetime64_any_dtype(out["signup_date"])
    assert out["signup_date"].isna().sum() == 0 and out["income"].dropna().between(10000, 200000).all()


def _check_ages():
    raw = _raw(); out = fix_impossible_ages(raw)
    assert out["age"].dropna().between(16, 100).all() and out["age"].isna().sum() > raw["age"].isna().sum()
    assert raw["age"].max() > 100, "the input DataFrame must not be modified"


def _check_fill():
    out = fill_missing(fix_types(fix_impossible_ages(_raw())))
    assert out["age"].isna().sum() == 0 and out["income"].isna().sum() == 0


def _check_pipeline():
    raw = _raw(); out = clean_pipeline(raw)
    assert len(out) == 200 and out["customer_id"].is_unique and list(out.index) == list(range(200))
    assert out.isna().sum().sum() == 0
    assert out["age"].between(16, 100).all()
    assert pd.api.types.is_float_dtype(out["income"]) and pd.api.types.is_datetime64_any_dtype(out["signup_date"])
    assert len(raw) == 215 and raw["income"].isna().sum() > 0, "the input DataFrame must not be modified"

def _run(checks):
    passed = 0
    for name, fn in checks:
        try:
            fn(); print(f"PASS  {name}"); passed += 1
        except NotImplementedError as e:
            print(f"TODO  {name}  ({e})")
        except AssertionError as e:
            print(f"FAIL  {name}  {str(e)[:160]}")
        except Exception as e:
            print(f"ERROR {name}  {type(e).__name__}: {str(e)[:160]}")
    print(f"\n{passed}/{len(checks)} checks passed")


if __name__ == "__main__":
    _run([("missing_report", _check_missing_report), ("remove_duplicates", _check_dups),
          ("clean_text", _check_text), ("fix_types", _check_types),
          ("fix_impossible_ages", _check_ages), ("fill_missing", _check_fill), ("clean_pipeline", _check_pipeline)])
