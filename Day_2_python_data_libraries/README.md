# Beginner Track, Days 4–6: NumPy, Pandas, Data Cleaning

One catch-up session that covers three days, plus a template so a participant can run the sessions from tomorrow.

| Day | Topic | Concepts | Task |
|---|---|---|---|
| 4 | NumPy fundamentals | Arrays, indexing, slicing, basic operations | Statistical analysis of a numerical array |
| 5 | Intro to Pandas DataFrames | Series, DataFrames, indexing, filtering | Load a CSV and extract subset statistics |
| 6 | Data cleaning with Pandas | Missing values, duplicates, type conversions | Clean a raw, messy customer dataset |

## Files

```
make_dataset.py        run once: creates data/customers_raw.csv (same file for everyone)
data/customers_raw.csv 215 messy customer rows (a copy is already included)
day04_numpy.py         starter: 8 functions on a 30-day x 3-store sales array
day05_pandas.py        starter: 7 functions on the customer CSV
day06_cleaning.py      starter: 7 cleaning functions + a pipeline
solutions/             completed versions (lead only; share after the session)
```

**What goes in each `.py` file.** Each starter has a docstring that says what the function must return, a hint, and a `raise NotImplementedError` line to replace with code. Checks at the bottom compare each function against an independently computed answer. Run `python day04_numpy.py` and every function shows `PASS`, `TODO` (not written yet) or `FAIL` (with the reason). A day is done when it prints `N/N checks passed`.

**Running.** Locally: `pip install numpy pandas`, then `python make_dataset.py` once, then run each day's file from this folder. In Colab: upload the folder (or the three `.py` files plus `data/`), then `!python day04_numpy.py`. Run the solutions from this folder too: `python solutions/day06_cleaning.py`.

## Today's catch-up session (90 minutes)

| Time | Block | Who leads |
|---|---|---|
| 0–5 | Goal: "by the end you'll have cleaned a real messy dataset" | Facilitator |
| 5–30 | **Day 4 NumPy.** Live-code the demo below, then everyone does `day04_numpy.py` | Facilitator |
| 30–60 | **Day 5 Pandas.** Live-code, then `day05_pandas.py` | Facilitator |
| 60–85 | **Day 6 Cleaning.** Live-code, then `day06_cleaning.py` | **Future lead** (facilitator watches) |
| 85–90 | Wrap-up: share one thing that surprised you; the lead announces tomorrow's topic | Lead |

Anyone who does not finish a day finishes it as homework; the checks tell them where they are.

## Live-code demos (about 10 minutes per day)

**Day 4: NumPy**
```python
import numpy as np
a = np.array([[1, 2, 3], [4, 5, 6]])
a.shape, a.dtype, a[0, 1], a[:, 1], a[-1]          # indexing and slicing
a * 2, a + a, a.sum(axis=0), a.sum(axis=1)         # operations, axis
a.mean(), a.std(), np.median(a), a.max()           # statistics
a[a > 2]                                           # boolean mask
```
Key idea: arrays are fast because the loop happens in C. `axis=0` goes down the rows, `axis=1` goes across.

**Day 5: Pandas**
```python
import pandas as pd
df = pd.read_csv("data/customers_raw.csv")
df.head(); df.shape; df.info(); df.describe()
df["plan"]; df[["name", "plan"]]                    # Series vs DataFrame
df.loc[0, "name"]; df.iloc[0:3, 0:2]                # label vs position
df[df["plan"] == "premium"]                         # filtering
df[(df.plan == "basic") & (df.monthly_spend > 25)]  # & and parentheses
df.groupby("plan")["monthly_spend"].mean()
```
Key idea: a DataFrame is a table of Series. Selecting a column gives a Series; filtering uses a True/False mask.

**Day 6: Cleaning** (demo the problem first, then the fix)
```python
df.isna().sum()                          # what is missing?
df.duplicated().sum(); df.drop_duplicates()
df["city"].value_counts()                # see the messy spellings
df["city"].str.strip().str.title()       # fix text
df["income"].str.replace(r"[$,]", "", regex=True).astype(float)
pd.to_datetime(df["signup_date"], format="mixed")
df["age"].fillna(df["age"].median())
```
Key idea: look first (`isna`, `value_counts`, `describe`), then fix one issue at a time, and keep the original untouched (`df = df.copy()`). Order matters: remove impossible ages before filling missing values.

## Handover: running sessions from tomorrow

**Choosing the lead.** Pick today, ideally someone who finishes first and explains well. Rotating two leads is fine. The facilitator should not lead tomorrow's session.

**Recurring session (75 minutes):**
1. 10 min: recap and questions from yesterday's task.
2. 20 min: lead live-codes the day's concept using the day's demo snippets.
3. 30 min: everyone does the task in pairs; the lead circulates.
4. 15 min: share results (post the final `N/N checks passed` line in the channel), then announce the next topic and task.

**Lead's checklist for each day:**
- [ ] Read the day's topic and task line in the curriculum sheet the evening before.
- [ ] Do the task yourself first (30 minutes). If a function stumps you, ask in the channel.
- [ ] Prepare a 5-line demo for the concept (copy the snippets above as a model).
- [ ] After the session, post: who finished, who is stuck, and the next topic.

**House rules:** nobody stays stuck more than 10 minutes without asking; explaining a solution to a neighbour counts as learning; solutions are shared after the session, not during it.

**Facilitator after handover:** one 20-minute office hour per week, a channel for blockers, and a weekly look at who is falling behind. The facilitator no longer attends daily sessions.

**Note for the lead on what the data contains.** `customers_raw.csv` has 215 rows: 200 customers plus 15 duplicate rows; missing values in age, city and income; impossible ages (negative, 250, 999); inconsistent text (stray spaces, mixed capitalisation); income stored as text like "$54,000"; and signup dates in two formats. `customer_id`, `plan` and `monthly_spend` are clean on purpose so Day 5 works without cleaning.
