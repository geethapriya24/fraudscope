import pandas as pd
from datetime import date

df = pd.read_csv("data/flagged_cases.csv")

top = df.sort_values("risk_score", ascending=False).head(1).iloc[0]

report = f"""
================================================================================
            SUSPICIOUS ACTIVITY REPORT (SAR) — CONFIDENTIAL
                      FraudScope | Transaction Risk Intelligence Platform
================================================================================

REPORT DATE       : {date.today()}
REPORT REFERENCE  : SAR-{top['transaction_id']}
PREPARED BY       : FraudScope Detection Engine

--------------------------------------------------------------------------------
SECTION 1 — SUBJECT DETAILS
--------------------------------------------------------------------------------
Entity Name       : {top['sender']}
Counterparty      : {top['receiver']}
Country           : {top['country']}
Transaction Type  : {top['transaction_type'].upper()}

--------------------------------------------------------------------------------
SECTION 2 — SUSPICIOUS TRANSACTION DETAILS
--------------------------------------------------------------------------------
Transaction ID    : {top['transaction_id']}
Date              : {top['date']}
Amount            : {top['currency']} {float(top['amount']):,.2f}
Risk Score        : {top['risk_score']} / 100
Risk Level        : {top['risk_level']}

--------------------------------------------------------------------------------
SECTION 3 — RED FLAGS IDENTIFIED
--------------------------------------------------------------------------------
Structuring Flag  : {'YES' if str(top['flag_structuring']) == 'True' else 'NO'}
Round Trip Flag   : {'YES' if str(top['flag_round_trip']) == 'True' else 'NO'}
High Risk Country : {'YES' if str(top['flag_high_risk_country']) == 'True' else 'NO'}
Velocity Flag     : {'YES' if str(top['flag_velocity']) == 'True' else 'NO'}
Large Cash Flag   : {'YES' if str(top['flag_cash_large']) == 'True' else 'NO'}
Fraud Pattern     : {top['fraud_pattern'].upper() if top['fraud_pattern'] else 'N/A'}

--------------------------------------------------------------------------------
SECTION 4 — NARRATIVE
--------------------------------------------------------------------------------
The transaction identified above has been flagged by the FraudScope
detection engine based on multiple red flag indicators. The entity
"{top['sender']}" conducted a {top['transaction_type']} transaction of
{top['currency']} {float(top['amount']):,.2f} with "{top['receiver']}"
on {top['date']}.

This activity is consistent with the "{top['fraud_pattern']}" typology,
which is commonly associated with financial crime and money laundering.
The transaction has been assigned a risk score of {top['risk_score']}/100
and classified as {top['risk_level']} risk.

--------------------------------------------------------------------------------
SECTION 5 — RECOMMENDED ACTION
--------------------------------------------------------------------------------
1. Escalate to Senior Compliance Officer for review
2. Place entity on enhanced due diligence (EDD) watchlist
3. File report with Financial Intelligence Unit (FIU)
4. Freeze account pending investigation if risk score exceeds 50
5. Cross-reference entity against OFAC / UN sanctions list

================================================================================
                         END OF SUSPICIOUS ACTIVITY REPORT
================================================================================
"""

with open("reports/SAR_output.txt", "w") as f:
    f.write(report)

print(report)
print("SAR saved to reports/SAR_output.txt")