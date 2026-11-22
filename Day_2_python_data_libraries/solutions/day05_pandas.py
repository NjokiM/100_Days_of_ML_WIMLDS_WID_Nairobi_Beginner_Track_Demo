"""Day 5: Intro to Pandas DataFrames. Series, DataFrames, indexing, filtering.

Task: load the customer CSV and extract subset statistics.
Fill in each function (replace the `raise NotImplementedError` line), then run:   python day05_pandas.py
(First run `python make_dataset.py` once to create data/customers_raw.csv.)

Note: this file still has duplicate rows and missing values. Today you only use the clean columns
(customer_id, plan, monthly_spend). Cleaning the rest is Day 6.
"""
import pandas as pd

CSV = "data/customers_raw.csv"


def load(path=CSV):
    """Read the CSV into a DataFrame."""
    return pd.read_csv(path)


def overview(df):
    """Return {"rows": number of rows, "columns": list of column names}."""
    return {"rows": len(df), "columns": list(df.columns)}


def corner(df):
    """Return the first 5 rows and first 3 columns using position-based indexing (iloc)."""
    return df.iloc[:5, :3]


def premium_customers(df):
    """Return only the rows whose plan is "premium" (boolean filtering)."""
    return df[df["plan"] == "premium"]


def top_spenders(df, n=5):
    """Return the n rows with the highest monthly_spend, biggest first. Hint: nlargest, or sort_values."""
    return df.nlargest(n, "monthly_spend")


def spend_by_plan(df):
    """Return a Series: average monthly_spend per plan, sorted from highest to lowest. Hint: groupby."""
    return df.groupby("plan")["monthly_spend"].mean().sort_values(ascending=False)


def subset_stats(df, plan, min_spend):
    """For customers on `plan` with monthly_spend >= min_spend, return
    {"count": ..., "mean": ..., "median": ..., "std": ...} of monthly_spend.
    Hint: combine two conditions with & and put each in parentheses."""
    sub = df[(df["plan"] == plan) & (df["monthly_spend"] >= min_spend)]["monthly_spend"]
    return {"count": len(sub), "mean": sub.mean(), "median": sub.median(), "std": sub.std()}


# ------------------------------------------------------------------ checks (do not edit)
import csv  # noqa: E402


def _rows():
    with open(CSV, newline="") as f:
        return list(csv.DictReader(f))


def _check_load():
    df = load()
    assert isinstance(df, pd.DataFrame) and df.shape == (len(_rows()), 8)


def _check_overview():
    o = overview(load())
    assert o["rows"] == len(_rows()) and o["columns"][0] == "customer_id" and len(o["columns"]) == 8


def _check_corner():
    c = corner(load())
    assert c.shape == (5, 3) and list(c.columns) == ["customer_id", "name", "age"]


def _check_premium():
    p = premium_customers(load())
    assert len(p) == sum(r["plan"] == "premium" for r in _rows()) and set(p["plan"]) == {"premium"}


def _check_top():
    t = top_spenders(load(), 3)
    spends = sorted((float(r["monthly_spend"]) for r in _rows()), reverse=True)[:3]
    assert len(t) == 3 and [round(v, 2) for v in t["monthly_spend"]] == [round(v, 2) for v in spends]


def _check_by_plan():
    s = spend_by_plan(load())
    exp = {}
    for r in _rows():
        exp.setdefault(r["plan"], []).append(float(r["monthly_spend"]))
    for plan, vals in exp.items():
        assert abs(s[plan] - sum(vals) / len(vals)) < 1e-9
    assert list(s.index) == sorted(exp, key=lambda p: -sum(exp[p]) / len(exp[p]))


def _check_subset():
    out = subset_stats(load(), "standard", 45.0)
    vals = [float(r["monthly_spend"]) for r in _rows() if r["plan"] == "standard" and float(r["monthly_spend"]) >= 45.0]
    n = len(vals); mean = sum(vals) / n
    sd = (sum((v - mean) ** 2 for v in vals) / (n - 1)) ** 0.5     # sample std, like pandas
    assert out["count"] == n and abs(out["mean"] - mean) < 1e-9 and abs(out["std"] - sd) < 1e-9

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
    _run([("load", _check_load), ("overview", _check_overview), ("corner", _check_corner),
          ("premium_customers", _check_premium), ("top_spenders", _check_top),
          ("spend_by_plan", _check_by_plan), ("subset_stats", _check_subset)])
