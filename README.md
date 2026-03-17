\#  FraudScope — Transaction Risk Intelligence Platform



!\[FraudScope Dashboard](preview.png)



\##  Live Demo

&#x20;\[Open FraudScope](https://fraudscope-gznwnyzjcgu6ame7wjruvz.streamlit.app/)



\---



\## About

FraudScope is an end-to-end financial crime detection and investigation platform built on the IBM Anti-Money Laundering (AML) dataset containing 5 million real transactions.



This project simulates the workflow of a real forensic risk consultant — detecting suspicious activity, scoring transactions by risk, investigating flagged cases, and generating Suspicious Activity Reports (SARs).



\---



\## Key Features

\- \*\*AML Detection Engine\*\* — 5 red flag rules based on real-world typologies

\- \*\*Risk Scoring\*\* — Every transaction scored 0–100

\- \*\*Interactive Dashboard\*\* — Filter by risk level, transaction type, fraud pattern

\- \*\*Investigation Table\*\* — Drill into any flagged transaction

\- \*\*SAR Report Generator\*\* — Auto-generate Suspicious Activity Reports

\- \*\*Built on Real Data\*\* — IBM AML dataset (5M transactions, 518K accounts)



\---



\## Fraud Patterns Detected

| Pattern | Description |

|---|---|

| Round Trip | Money sent and returned to same entity |

| Layering | Multiple reinvestment transactions to obscure origin |

| Currency Switch | Payment and receiving currency mismatch |

| Velocity Spike | Same account sending unusually high volume |

| Confirmed AML | Transactions flagged as laundering in IBM dataset |



\---



\## Tech Stack

| Tool | Purpose |

|---|---|

| Python | Data processing \& detection engine |

| Pandas | Data manipulation \& ETL |

| Streamlit | Interactive web dashboard |

| Plotly | Charts \& visualizations |

| IBM AML Dataset | Real-world transaction data |



\---



\## Project Structure

```

fraudscope/

├── app.py                      # Streamlit web app

├── requirements.txt            # Dependencies

├── data/

│   └── aml\_dashboard.csv       # Processed AML data

├── scripts/

│   ├── generate\_data.py        # Synthetic data generator

│   ├── detect\_fraud.py         # Detection engine

│   ├── detect\_aml.py           # IBM AML processor

│   ├── prepare\_dashboard\_data.py

│   └── embed\_data.py

├── dashboard/

│   └── index.html              # HTML dashboard

└── reports/

&#x20;   └── generate\_sar.py         # SAR report generator

```



\---



\## Run Locally

```bash

git clone https://github.com/geethapriya24/fraudscope.git

cd fraudscope

pip install -r requirements.txt

streamlit run app.py

```



\---



\## Dataset

\- \*\*Source\*\*: IBM Transactions for Anti-Money Laundering (AML)

\- \*\*Size\*\*: 5,078,345 transactions | 518,581 accounts

\- \*\*Confirmed Laundering Cases\*\*: 5,177

\- \*\*Link\*\*: \[Kaggle — IBM AML Dataset](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml)





