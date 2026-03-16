import pandas as pd
from faker import Faker
import random

fake = Faker()
random.seed(42)

FRAUD_PATTERNS = ["structuring", "round_trip", "shell_company", "velocity_spike"]

def generate_transaction(i, is_fraud=False):
    pattern = random.choice(FRAUD_PATTERNS) if is_fraud else None

    if pattern == "structuring":
        amount = round(random.uniform(8000, 9999), 2)
    elif pattern == "round_trip":
        amount = round(random.choice([50000, 100000, 250000]), 2)
    else:
        amount = round(random.uniform(100, 50000), 2)

    return {
        "transaction_id": f"TXN{i:06d}",
        "date": str(fake.date_between(start_date="-1y", end_date="today")),
        "sender": fake.company(),
        "receiver": fake.company(),
        "amount": amount,
        "currency": random.choice(["USD", "EUR", "GBP", "AED"]),
        "country": fake.country(),
        "transaction_type": random.choice(["wire", "cash", "online", "cheque"]),
        "is_fraud": is_fraud,
        "fraud_pattern": pattern
    }

transactions = []

for i in range(9000):
    transactions.append(generate_transaction(i, is_fraud=False))
for i in range(9000, 10000):
    transactions.append(generate_transaction(i, is_fraud=True))

df = pd.DataFrame(transactions)
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("data/raw_transactions.csv", index=False)

print(f"Generated {len(df)} transactions")
print(df["is_fraud"].value_counts())