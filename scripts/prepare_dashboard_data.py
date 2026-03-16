import pandas as pd

print("Preparing dashboard data...")

trans = pd.read_csv("data/aml_scored.csv")
accounts = pd.read_csv("data/HI-Small_accounts.csv")

accounts.columns = ["bank_name", "bank_id", "account_number", "entity_id", "entity_name"]

trans = trans.merge(
    accounts[["account_number", "entity_name"]],
    left_on="from_account",
    right_on="account_number",
    how="left"
)
trans.rename(columns={"entity_name": "sender_name"}, inplace=True)

trans = trans.merge(
    accounts[["account_number", "entity_name"]],
    left_on="to_account",
    right_on="account_number",
    how="left"
)
trans.rename(columns={"entity_name": "receiver_name"}, inplace=True)

dashboard = trans[[
    "timestamp", "from_bank", "from_account", "to_bank", "to_account",
    "sender_name", "receiver_name", "amount_paid", "payment_currency",
    "payment_format", "is_laundering", "risk_score", "risk_level",
    "fraud_pattern", "flag_round_amount", "flag_high_value",
    "flag_currency_mismatch", "flag_velocity", "flag_reinvestment"
]].copy()

dashboard.columns = [
    "date", "from_bank", "transaction_id", "to_bank", "to_account",
    "sender", "receiver", "amount", "currency",
    "transaction_type", "is_laundering", "risk_score", "risk_level",
    "fraud_pattern", "flag_round_amount", "flag_high_value",
    "flag_currency_mismatch", "flag_velocity", "flag_reinvestment"
]

dashboard["sender"] = dashboard["sender"].fillna(dashboard["transaction_id"])
dashboard["receiver"] = dashboard["receiver"].fillna(dashboard["to_account"])

high = dashboard[dashboard["risk_level"] == "High"].head(3000)
medium = dashboard[dashboard["risk_level"] == "Medium"].head(3000)
low = dashboard[dashboard["risk_level"] == "Low"].head(2000)
clean = dashboard[dashboard["risk_level"] == "Clean"].head(2000)

top = pd.concat([high, medium, low, clean]).sample(frac=1).reset_index(drop=True)
top.to_csv("data/aml_dashboard.csv", index=False)

print(f"Dashboard data saved: {len(top)} transactions")
print(top["risk_level"].value_counts())
print(top["fraud_pattern"].value_counts())
