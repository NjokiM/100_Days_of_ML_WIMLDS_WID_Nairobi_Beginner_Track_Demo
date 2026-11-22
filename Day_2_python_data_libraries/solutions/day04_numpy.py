"""Day 4: NumPy fundamentals. Arrays, indexing, slicing, basic operations, statistics.

Task: perform a statistical analysis of daily sales (30 days x 3 stores).
Fill in each function (replace the `raise NotImplementedError` line), then run:   python day04_numpy.py
"""
import numpy as np


def make_sales(seed=42):
    """Given: daily sales for 30 days (rows) across 3 stores (columns)."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=[200, 150, 300], scale=[30, 20, 50], size=(30, 3)).round(1)


def store_stats(sales):
    """Return {"mean": ..., "median": ..., "std": ...}, each a length-3 array (one value per store).
    Hint: the stats functions take axis=0 to work down the rows (days)."""
    return {"mean": sales.mean(axis=0), "median": np.median(sales, axis=0), "std": sales.std(axis=0)}


def best_day(sales):
    """Return the index of the day with the highest TOTAL sales across the 3 stores (an int).
    Hint: sum along axis=1, then argmax."""
    return int(np.argmax(sales.sum(axis=1)))


def last_week(sales):
    """Return the last 7 days (all stores) by slicing. Shape (7, 3). Hint: negative index in the slice."""
    return sales[-7:, :]


def weekly_totals(sales):
    """Using only the first 28 days, return total sales per week per store, shape (4, 3).
    Hint: slice 28 days, reshape to (4, 7, 3), sum over axis=1."""
    return sales[:28].reshape(4, 7, 3).sum(axis=1)


def busy_days(sales, store):
    """Return the day indices where `store`'s sales were MORE than its mean + 1 standard deviation.
    Hint: build a boolean mask, then np.where(mask)[0]."""
    col = sales[:, store]
    return np.where(col > col.mean() + col.std())[0]


def zscore(x):
    """Standardise: (x - mean) / std (use the default population std). Works on a 1-D array."""
    return (x - x.mean()) / x.std()


def five_number_summary(x):
    """Return {"min", "q1", "median", "q3", "max"} for a 1-D array. Hint: np.percentile(x, [25, 50, 75])."""
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    return {"min": x.min(), "q1": q1, "median": med, "q3": q3, "max": x.max()}


def store_correlation(sales, a, b):
    """Return the correlation coefficient (a float) between store a and store b. Hint: np.corrcoef."""
    return float(np.corrcoef(sales[:, a], sales[:, b])[0, 1])


# ------------------------------------------------------------------ checks (do not edit)
def _check_stats():
    s = make_sales(); out = store_stats(s)
    for j in range(3):
        col = sorted(s[:, j].tolist()); n = len(col)
        mean = sum(col) / n
        median = (col[n // 2 - 1] + col[n // 2]) / 2
        std = (sum((v - mean) ** 2 for v in col) / n) ** 0.5
        assert abs(out["mean"][j] - mean) < 1e-9 and abs(out["median"][j] - median) < 1e-9 and abs(out["std"][j] - std) < 1e-9


def _check_best_day():
    s = make_sales()
    totals = [sum(row) for row in s.tolist()]
    assert best_day(s) == totals.index(max(totals))


def _check_last_week():
    s = make_sales(); lw = last_week(s)
    assert lw.shape == (7, 3) and np.array_equal(lw, s[23:30])


def _check_weekly():
    s = make_sales(); w = weekly_totals(s)
    assert w.shape == (4, 3)
    for k in range(4):
        for j in range(3):
            assert abs(w[k, j] - s[7 * k:7 * k + 7, j].sum()) < 1e-9


def _check_busy():
    s = make_sales()
    for j in range(3):
        col = s[:, j].tolist(); m = sum(col) / len(col)
        sd = (sum((v - m) ** 2 for v in col) / len(col)) ** 0.5
        assert list(busy_days(s, j)) == [i for i, v in enumerate(col) if v > m + sd]


def _check_zscore():
    z = zscore(make_sales()[:, 0])
    assert abs(z.mean()) < 1e-9 and abs(z.std() - 1) < 1e-9


def _check_five():
    x = make_sales()[:, 2]; f = five_number_summary(x)
    assert f["min"] == x.min() and f["max"] == x.max()
    assert abs(f["q1"] - np.quantile(x, 0.25)) < 1e-9 and abs(f["median"] - np.median(x)) < 1e-9 and abs(f["q3"] - np.quantile(x, 0.75)) < 1e-9


def _check_corr():
    s = make_sales(); c = store_correlation(s, 0, 2)
    assert isinstance(c, float) and -1 <= c <= 1 and abs(c - np.corrcoef(s.T)[0, 2]) < 1e-9

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
    _run([("store_stats", _check_stats), ("best_day", _check_best_day), ("last_week", _check_last_week),
          ("weekly_totals", _check_weekly), ("busy_days", _check_busy), ("zscore", _check_zscore),
          ("five_number_summary", _check_five), ("store_correlation", _check_corr)])
