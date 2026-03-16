import pandas as pd

df = pd.read_csv("data/raw_transactions.csv")

df["flag_structuring"] = (
    (df["amount"] >= 8000) & (df["amount"] < 10000)
)

df["flag_round_trip"] = (
    df["amount"].isin([50000, 100000, 250000])
)

df["flag_high_risk_country"] = (
    df["country"].isin([
        "Iran", "North Korea", "Myanmar", "Syria",
        "Yemen", "Libya", "Somalia", "Sudan"
    ])
)

sender_counts = df.groupby("sender")["transaction_id"].count()
high_velocity_senders = sender_counts[sender_counts > 5].index
df["flag_velocity"] = df["sender"].isin(high_velocity_senders)

df["flag_cash_large"] = (
    (df["transaction_type"] == "cash") & (df["amount"] > 20000)
)

df["risk_score"] = (
    df["flag_structuring"].astype(int) * 30 +
    df["flag_round_trip"].astype(int) * 25 +
    df["flag_high_risk_country"].astype(int) * 20 +
    df["flag_velocity"].astype(int) * 15 +
    df["flag_cash_large"].astype(int) * 10
)

df["risk_level"] = pd.cut(
    df["risk_score"],
    bins=[-1, 0, 30, 60, 100],
    labels=["Clean", "Low", "Medium", "High"]
)

flagged = df[df["risk_score"] > 0]
flagged.to_csv("data/flagged_cases.csv", index=False)
df.to_csv("data/all_transactions_scored.csv", index=False)

print(f"Total transactions  : {len(df)}")
print(f"Flagged transactions: {len(flagged)}")
print(f"\nRisk level breakdown:")
print(df["risk_level"].value_counts())