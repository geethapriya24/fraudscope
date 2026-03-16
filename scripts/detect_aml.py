import pandas as pd

print("Loading data...")
trans = pd.read_csv("data/HI-Small_Trans.csv")
accounts = pd.read_csv("data/HI-Small_accounts.csv")

trans.columns = ["timestamp", "from_bank", "from_account", "to_bank",
                 "to_account", "amount_received", "receiving_currency",
                 "amount_paid", "payment_currency", "payment_format", "is_laundering"]

trans["flag_round_amount"] = trans["amount_paid"].apply(
    lambda x: x % 1000 == 0 and x > 0
)
trans["flag_high_value"] = trans["amount_paid"] > 50000
trans["flag_currency_mismatch"] = (
    trans["payment_currency"] != trans["receiving_currency"]
)
velocity = trans.groupby("from_account")["timestamp"].count()
high_velocity = velocity[velocity > 10].index
trans["flag_velocity"] = trans["from_account"].isin(high_velocity)
trans["flag_reinvestment"] = trans["payment_format"] == "Reinvestment"

trans["fraud_pattern"] = "unknown"
trans.loc[trans["flag_round_amount"] & trans["flag_velocity"], "fraud_pattern"] = "structuring"
trans.loc[trans["flag_reinvestment"], "fraud_pattern"] = "layering"
trans.loc[trans["flag_currency_mismatch"], "fraud_pattern"] = "currency_switch"
trans.loc[trans["flag_high_value"] & trans["flag_velocity"], "fraud_pattern"] = "round_trip"
trans.loc[trans["is_laundering"] == 1, "fraud_pattern"] = "confirmed_aml"

trans["risk_score"] = (
    trans["flag_round_amount"].astype(int) * 20 +
    trans["flag_high_value"].astype(int) * 25 +
    trans["flag_currency_mismatch"].astype(int) * 20 +
    trans["flag_velocity"].astype(int) * 20 +
    trans["flag_reinvestment"].astype(int) * 15
)

trans["risk_level"] = pd.cut(
    trans["risk_score"],
    bins=[-1, 0, 30, 60, 100],
    labels=["Clean", "Low", "Medium", "High"]
)

print("Saving results...")
flagged = trans[trans["risk_score"] > 0]
flagged.to_csv("data/aml_flagged.csv", index=False)
trans.to_csv("data/aml_scored.csv", index=False)

print(f"\nTotal transactions  : {len(trans)}")
print(f"Flagged transactions: {len(flagged)}")
print(f"Known laundering    : {trans['is_laundering'].sum()}")
print(f"\nRisk level breakdown:")
print(trans["risk_level"].value_counts())
print(f"\nFraud patterns:")
print(trans["fraud_pattern"].value_counts())
