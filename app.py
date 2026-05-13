import streamlit as st
import pandas as pd
import random
import requests
from sklearn.ensemble import IsolationForest
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SentinelX AI Cyber Defense System",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #050816;
}

h1, h2, h3 {
    color: #00F5FF;
}

html, body, [class*="css"] {
    color: white;
}

.stButton>button {
    background-color: #00F5FF;
    color: black;
    border-radius: 10px;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
}

.stButton>button:hover {
    background-color: #00c8d7;
    color: white;
}

.stTextInput>div>div>input {
    background-color: #0B1120;
    color: white;
    border-radius: 8px;
    border: 1px solid #00F5FF;
}

[data-testid="metric-container"] {
    background-color: #111827;
    border: 1px solid #00F5FF;
    padding: 15px;
    border-radius: 12px;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🛡️ SentinelX AI Cyber Defense System")

st.markdown(
    "AI-powered cybersecurity monitoring, IP intelligence, and threat analysis platform"
)

# ---------------- SIDEBAR ----------------

st.sidebar.header("🌐 Threat Scanner")

ip_address = st.sidebar.text_input(
    "Enter Public IP Address",
    "8.8.8.8"
)

# ---------------- FETCH IP INFO ----------------

def get_ip_info(ip):

    try:

        response = requests.get(
            f"https://ipinfo.io/{ip}/json"
        )

        data = response.json()

        return data

    except:

        return {}

# ---------------- GENERATE NETWORK DATA ----------------

def generate_activity():

    requests_count = random.randint(100, 10000)

    failed_logins = random.randint(0, 120)

    data_transfer = random.randint(100, 25000)

    return requests_count, failed_logins, data_transfer

# ---------------- THREAT DETECTION ----------------

def detect_threat(df):

    features = df[
        ['requests', 'failed_logins', 'data_transfer']
    ]

    model = IsolationForest(
        contamination=0.3,
        random_state=42
    )

    model.fit(features)

    prediction = model.predict(features)

    df['Threat'] = [
        "🚨 Suspicious"
        if p == -1
        else "✅ Normal"
        for p in prediction
    ]

    return df

# ---------------- ANALYZE BUTTON ----------------

if st.sidebar.button("Analyze IP"):

    with st.spinner("🔍 Scanning IP and analyzing threats..."):

        # Fetch IP Info
        ip_info = get_ip_info(ip_address)

        # Generate activity
        requests_count, failed_logins, data_transfer = generate_activity()

        # Create dataframe
        df = pd.DataFrame({
            'ip': [ip_address],
            'requests': [requests_count],
            'failed_logins': [failed_logins],
            'data_transfer': [data_transfer]
        })

        # Threat detection
        result = detect_threat(df)

        threat = result['Threat'].iloc[0]

        # ---------------- TOP METRICS ----------------

        st.subheader("📊 Security Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🌐 IPs Analyzed",
            "1"
        )

        col2.metric(
            "🚨 Threat Level",
            threat
        )

        col3.metric(
            "📡 Requests",
            requests_count
        )

        col4.metric(
            "🛡️ System Status",
            "ACTIVE"
        )

        # ---------------- IP INFO ----------------

        st.subheader("🌍 IP Intelligence")

        col1, col2 = st.columns(2)

        with col1:

            st.write(f"🌐 IP Address: {ip_address}")

            st.write(f"🏙️ City: {ip_info.get('city', 'Unknown')}")

            st.write(f"🌎 Country: {ip_info.get('country', 'Unknown')}")

        with col2:

            st.write(f"🏢 Organization: {ip_info.get('org', 'Unknown')}")

            st.write(f"📍 Location: {ip_info.get('loc', 'Unknown')}")

            st.write(f"⏰ Timezone: {ip_info.get('timezone', 'Unknown')}")

        # ---------------- MAP ----------------

        location = ip_info.get('loc')

        if location:

            try:

                latitude, longitude = map(
                    float,
                    location.split(',')
                )

                st.subheader("🗺️ Approximate IP Location")

                map_data = pd.DataFrame({
                    'lat': [latitude],
                    'lon': [longitude]
                })

                st.map(map_data)

            except:

                st.warning(
                    "Unable to load map location."
                )

        # ---------------- NETWORK TABLE ----------------

        st.subheader("📑 Simulated Network Activity")

        st.dataframe(
            result,
            width='stretch'
        )

        # ---------------- THREAT STATUS ----------------

        st.subheader("🚨 Threat Status")

        if "Suspicious" in threat:

            st.error(
                "🚨 Suspicious activity detected!"
            )

        else:

            st.success(
                "✅ Normal activity detected"
            )

        # ---------------- ACTIVITY METRICS ----------------

        st.subheader("📈 Activity Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "📨 Requests",
            requests_count
        )

        col2.metric(
            "🔑 Failed Logins",
            failed_logins
        )

        col3.metric(
            "📡 Data Transfer",
            data_transfer
        )

        # ---------------- CHART ----------------

        st.subheader("📊 Cybersecurity Analytics")

        chart_df = pd.DataFrame({
            'Metric': [
                'Requests',
                'Failed Logins',
                'Data Transfer'
            ],
            'Value': [
                requests_count,
                failed_logins,
                data_transfer
            ]
        })

        fig = px.bar(
            chart_df,
            x='Metric',
            y='Value',
            color='Metric',
            text='Value',
            title='Network Activity Analysis'
        )

        fig.update_layout(
            plot_bgcolor="#050816",
            paper_bgcolor="#050816",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
🛡️ Powered by SentinelX Threat Intelligence Engine  
Developed using Python • Streamlit • Machine Learning • Plotly • IP Intelligence APIs • Isolation Forest
""")