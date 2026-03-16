import pandas as pd

print("Loading IBM AML dataset...")
trans = pd.read_csv("data/HI-Small_Trans.csv")
accounts = pd.read_csv("data/HI-Small_accounts.csv")

print(f"Transactions loaded: {len(trans)}")
print(f"Accounts loaded: {len(accounts)}")
print("\nTransaction columns:", list(trans.columns))
print("Account columns:", list(accounts.columns))
print("\nSample transactions:")
print(trans.head())
