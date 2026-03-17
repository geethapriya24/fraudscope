import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FraudScope",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stMetric"] {
    background: #1e293b;
    border-radius: 10px;
    padding: 16px;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔍 FraudScope")
st.markdown("**Transaction Risk Intelligence Platform** — Built on IBM AML Dataset")
st.divider()

@st.cache_data
def load_data():
    df = pd.read_csv("data/aml_dashboard.csv")
    df = df.fillna("")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df

with st.spinner("Loading AML data..."):
    df = load_data()

st.sidebar.header("🔎 Filters")

risk_filter = st.sidebar.selectbox(
    "Risk Level",
    options=["All", "High", "Medium", "Low", "Clean"]
)

type_filter = st.sidebar.selectbox(
    "Transaction Type",
    options=["All"] + sorted(df["transaction_type"].unique().tolist())
)

pattern_filter = st.sidebar.selectbox(
    "Fraud Pattern",
    options=["All"] + sorted(df["fraud_pattern"].unique().tolist())
)

amount_filter = st.sidebar.number_input(
    "Min Amount ($)",
    min_value=0,
    value=0
)

search = st.sidebar.text_input("🔍 Search Sender / Receiver")

filtered = df.copy()
if risk_filter != "All":
    filtered = filtered[filtered["risk_level"] == risk_filter]
if type_filter != "All":
    filtered = filtered[filtered["transaction_type"] == type_filter]
if pattern_filter != "All":
    filtered = filtered[filtered["fraud_pattern"] == pattern_filter]
filtered = filtered[filtered["amount"] >= amount_filter]
if search:
    filtered = filtered[
        filtered["sender"].str.contains(search, case=False, na=False) |
        filtered["receiver"].str.contains(search, case=False, na=False)
    ]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{len(filtered):,}")
col2.metric("Flagged Cases", f"{len(filtered[filtered['risk_level'] != 'Clean']):,}")
col3.metric("High Risk", f"{len(filtered[filtered['risk_level'] == 'High']):,}")
col4.metric("Confirmed AML", f"{len(filtered[filtered['is_laundering'] == 1]):,}")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Risk Level Breakdown")
    risk_counts = filtered["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]
    fig = px.pie(
        risk_counts, values="count", names="risk_level",
        color_discrete_map={
            "High": "#f87171",
            "Medium": "#fbbf24",
            "Low": "#38bdf8",
            "Clean": "#34d399"
        },
        hole=0.4
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Fraud Patterns")
    pattern_counts = filtered[filtered["fraud_pattern"] != "unknown"]["fraud_pattern"].value_counts().reset_index()
    pattern_counts.columns = ["pattern", "count"]
    fig2 = px.bar(
        pattern_counts, x="pattern", y="count",
        color_discrete_sequence=["#38bdf8"]
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        xaxis=dict(gridcolor="#334155"),
        yaxis=dict(gridcolor="#334155")
    )
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.subheader("Transaction Types")
    type_counts = filtered["transaction_type"].value_counts().reset_index()
    type_counts.columns = ["type", "count"]
    fig3 = px.pie(
        type_counts, values="count", names="type",
        hole=0.4
    )
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.subheader("📋 Transaction Investigation Table")
st.dataframe(
    filtered[[
        "transaction_id", "date", "sender", "receiver",
        "amount", "currency", "transaction_type",
        "risk_score", "risk_level", "fraud_pattern", "is_laundering"
    ]].head(500),
    use_container_width=True,
    hide_index=True,
    column_config={
        "risk_score": st.column_config.ProgressColumn(
            "Risk Score",
            min_value=0,
            max_value=100
        ),
        "amount": st.column_config.NumberColumn(
            "Amount",
            format="$%.2f"
        ),
        "is_laundering": st.column_config.CheckboxColumn(
            "Confirmed AML"
        )
    }
)

st.divider()

st.subheader("📄 Generate SAR Report")

high_risk = filtered[filtered["risk_level"] == "High"]["transaction_id"].head(50).tolist()

if high_risk:
    selected_id = st.selectbox("Select High Risk Transaction", options=high_risk)
    if selected_id:
        row = filtered[filtered["transaction_id"] == selected_id].iloc[0]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Entity Details**")
            st.write(f"Sender: {row['sender']}")
            st.write(f"Receiver: {row['receiver']}")
            st.write(f"Amount: {row['currency']} {row['amount']:,.2f}")
            st.write(f"Type: {row['transaction_type']}")
        with col2:
            st.markdown("**Risk Assessment**")
            st.write(f"Risk Score: {row['risk_score']} / 100")
            st.write(f"Risk Level: {row['risk_level']}")
            st.write(f"Fraud Pattern: {row['fraud_pattern']}")
            st.write(f"Confirmed AML: {'Yes 🚨' if str(row['is_laundering']) == '1' else 'No'}")

        if st.button("Generate SAR Report"):
            sar = f"""
SUSPICIOUS ACTIVITY REPORT (SAR)
==================================
Transaction ID  : {row['transaction_id']}
Date            : {row['date']}
Sender          : {row['sender']}
Receiver        : {row['receiver']}
Amount          : {row['currency']} {row['amount']:,.2f}
Type            : {row['transaction_type']}
Risk Score      : {row['risk_score']} / 100
Risk Level      : {row['risk_level']}
Fraud Pattern   : {row['fraud_pattern']}
Confirmed AML   : {'Yes' if str(row['is_laundering']) == '1' else 'No'}

RECOMMENDED ACTION:
1. Escalate to Senior Compliance Officer
2. Place on Enhanced Due Diligence watchlist
3. File with Financial Intelligence Unit
4. Cross-reference against OFAC sanctions list
==================================
"""
            st.code(sar)
            st.download_button(
                "⬇️ Download SAR Report",
                sar,
                file_name=f"SAR_{selected_id}.txt"
            )
else:
    st.info("No high risk transactions found with current filters.")

st.markdown("---")
st.markdown("*FraudScope — Transaction Risk Intelligence Platform | Built on IBM AML Dataset*")