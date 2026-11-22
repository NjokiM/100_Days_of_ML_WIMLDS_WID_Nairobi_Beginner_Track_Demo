"""Generates data/customers_raw.csv: a deliberately messy customer dataset (fixed seed, so everyone gets the same file).

Run once:   python make_dataset.py
Messiness (Day 6 cleans it): duplicate rows, missing values, impossible ages, text with stray spaces and
mixed capitalisation, income stored as text like "$54,000", signup dates in two different formats.
The columns `customer_id`, `plan` and `monthly_spend` are clean on purpose, so Day 5 can use them directly.
"""
import os

import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
N = 200
first = ["Amina", "Brian", "Cynthia", "David", "Esther", "Felix", "Grace", "Hassan", "Irene", "James",
         "Kevin", "Lucy", "Mercy", "Nathan", "Olive", "Peter", "Queen", "Ruth", "Samuel", "Tabitha"]
last = ["Otieno", "Wanjiru", "Kamau", "Mwangi", "Achieng", "Njoroge", "Hussein", "Chebet", "Mutua", "Odhiambo"]
cities = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika"]
plans = ["basic", "standard", "premium"]

df = pd.DataFrame({
    "customer_id": np.arange(1001, 1001 + N),
    "name": [f"{rng.choice(first)} {rng.choice(last)}" for _ in range(N)],
    "age": rng.integers(18, 70, N).astype(float),
    "city": rng.choice(cities, N),
    "signup_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 700, N), unit="D"),
    "plan": rng.choice(plans, N, p=[0.5, 0.3, 0.2]),
})
base = df["plan"].map({"basic": 20.0, "standard": 45.0, "premium": 90.0})
df["monthly_spend"] = (base * rng.uniform(0.7, 1.4, N)).round(2)
df["income"] = (rng.normal(60000, 18000, N).clip(15000, 150000) // 100 * 100)

# ---- make it messy ----
def pick(k):
    return rng.choice(N, k, replace=False)

df.loc[pick(12), "age"] = np.nan
df.loc[pick(15), "income"] = np.nan
df["city"] = df["city"].astype(object)
df.loc[pick(10), "city"] = np.nan
bad = pick(3)
df.loc[bad, "age"] = [-3.0, 250.0, 999.0]

# text noise: stray spaces and inconsistent capitalisation
for i in pick(25):
    df.loc[i, "city"] = df.loc[i, "city"] if pd.isna(df.loc[i, "city"]) else rng.choice(
        [f"  {df.loc[i, 'city']}", df.loc[i, "city"].upper(), df.loc[i, "city"].lower(), f"{df.loc[i, 'city']} "])
for i in pick(25):
    df.loc[i, "name"] = rng.choice([f" {df.loc[i, 'name']}", df.loc[i, "name"].lower(), df.loc[i, "name"].upper()])

# type noise: income as text, two date formats
df["income"] = df["income"].map(lambda v: np.nan if pd.isna(v) else f"${v:,.0f}")
fmt_alt = set(pick(80).tolist())
df["signup_date"] = [d.strftime("%b %d, %Y") if i in fmt_alt else d.strftime("%Y-%m-%d")
                     for i, d in enumerate(df["signup_date"])]

# 15 exact duplicate rows appended, then shuffled
dups = df.iloc[pick(15)]
df = pd.concat([df, dups], ignore_index=True).sample(frac=1, random_state=7).reset_index(drop=True)

os.makedirs("data", exist_ok=True)
df.to_csv("data/customers_raw.csv", index=False)
print(f"wrote data/customers_raw.csv  ({len(df)} rows)")
