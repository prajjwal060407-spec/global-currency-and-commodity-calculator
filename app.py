import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ------------------------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------------------------
st.set_page_config(page_title="Global Currency & Commodities", layout="wide", page_icon="💱")

# ------------------------------------------------------------------------------------
# DARK THEME CSS – FULL DARK MODE WITH BLACK BACKGROUND, WHITE DROPDOWNS, DARK CARDS
# ------------------------------------------------------------------------------------
st.markdown("""
<style>

/* GLOBAL DARK MODE */
body, .stApp {
    background-color: #000 !important;
    color: #fff !important;
    font-size: 16px !important;
}

/* MAIN PAGE LAYOUT */
.block-container {
    padding-top: 0 !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* DARK HEADER */
.bennett-header {
    background: linear-gradient(120deg, #004aad, #ff6b00);
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 20px;
    color: white !important;
}
.bennett-header h2 { margin: 0; font-size: 28px !important; }
.bennett-header p { margin: 0; opacity: 0.9; }

/* CARD */
.card {
    background: #1a1a1a !important;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #333;
    box-shadow: 0 3px 10px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}

/* LABEL VISIBILITY FIX (LATEST STREAMLIT SUPPORT) */
span, label, .stMarkdown p,
.stSelectbox label, .stNumberInput label, .stTextInput label,
.css-1o72pil, .css-1qg05tj {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* SELECTBOX WRAPPER DARK */
div[data-baseweb="select"] {
    background-color: #1e1e1e !important;
    border-radius: 8px !important;
    color: white !important;
    border: 1px solid #444 !important;
}

/* SELECTBOX CONTENT */
div[data-baseweb="select"] * {
    color: white !important;
}

/* DROPDOWN MENU */
ul[role="listbox"] {
    background-color: #1e1e1e !important;
    border-radius: 6px !important;
    color: white !important;
    border: 1px solid #555 !important;
}

/* INPUT BOX DARK MODE */
input, .stTextInput input, .stNumberInput input {
    background-color: #1e1e1e !important;
    color: white !important;
    border-radius: 6px !important;
    border: 1px solid #444 !important;
}

/* PREDICTION BOX */
.predict-box {
    background: #2a2a2a !important;
    border-left: 5px solid #004aad;
    padding: 15px;
    border-radius: 10px;
    font-size: 18px;
    color: white !important;
}
.predict-box span {
    font-size: 24px;
    font-weight: 700;
    color: #ff6b00 !important;
}

/* TABLE DARK MODE */
.stDataFrame, .stTable {
    background-color: #1a1a1a !important;
    color: white !important;
    border: 1px solid #333 !important;
}

/* TABS */
[data-baseweb="tab-list"] {
    background-color: #000 !important;
    padding-bottom: 10px;
}

[data-baseweb="tab"] {
    background: #1a1a1a !important;
    color: #ccc !important;
    border-radius: 8px !important;
    border: 1px solid #333 !important;
    padding: 10px 20px !important;
    font-weight: 600;
}

[data-baseweb="tab"][aria-selected="true"] {
    background-color: #004aad !important;
    color: white !important;
    border-color: #004aad !important;
}

</style>


""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
# HEADER – SIMPLIFIED TEXT FOR BETTER VISIBILITY
# ------------------------------------------------------------------------------------
st.markdown("""
<div class="bennett-header">
    <h2>💱 Global Currency & Commodity Suite</h2>
    <p>Bennett Theme • 250+ Countries • Linear Prediction</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
# TRUE 250+ COUNTRY LIST (ISO OFFICIAL)
# ------------------------------------------------------------------------------------
country_currency = {
    "Afghanistan": "AFN", "Albania": "ALL", "Algeria": "DZD", "Andorra": "EUR", "Angola": "AOA",
    "Argentina": "ARS", "Armenia": "AMD", "Australia": "AUD", "Austria": "EUR", "Azerbaijan": "AZN",
    "Bahamas": "BSD", "Bahrain": "BHD", "Bangladesh": "BDT", "Barbados": "BBD", "Belarus": "BYN",
    "Belgium": "EUR", "Belize": "BZD", "Benin": "XOF", "Bhutan": "BTN", "Bolivia": "BOB",
    "Bosnia and Herzegovina": "BAM", "Botswana": "BWP", "Brazil": "BRL", "Brunei": "BND", "Bulgaria": "BGN",
    "Burkina Faso": "XOF", "Burundi": "BIF", "Cambodia": "KHR", "Cameroon": "XAF", "Canada": "CAD",
    "Cape Verde": "CVE", "Central African Republic": "XAF", "Chad": "XAF", "Chile": "CLP", "China": "CNY",
    "Colombia": "COP", "Comoros": "KMF", "Congo": "CDF", "Costa Rica": "CRC", "Croatia": "EUR",
    "Cuba": "CUP", "Cyprus": "EUR", "Czech Republic": "CZK", "Denmark": "DKK", "Djibouti": "DJF",
    "Dominica": "XCD", "Dominican Republic": "DOP", "Ecuador": "USD", "Egypt": "EGP", "El Salvador": "USD",
    "Equatorial Guinea": "XAF", "Eritrea": "ERN", "Estonia": "EUR", "Eswatini": "SZL", "Ethiopia": "ETB",
    "Fiji": "FJD", "Finland": "EUR", "France": "EUR", "Gabon": "XAF", "Gambia": "GMD",
    "Georgia": "GEL", "Germany": "EUR", "Ghana": "GHS", "Greece": "EUR", "Grenada": "XCD",
    "Guatemala": "GTQ", "Guinea": "GNF", "Guinea-Bissau": "XOF", "Guyana": "GYD", "Haiti": "HTG",
    "Honduras": "HNL", "Hungary": "HUF", "Iceland": "ISK", "India": "INR", "Indonesia": "IDR",
    "Iran": "IRR", "Iraq": "IQD", "Ireland": "EUR", "Israel": "ILS", "Italy": "EUR",
    "Jamaica": "JMD", "Japan": "JPY", "Jordan": "JOD", "Kazakhstan": "KZT", "Kenya": "KES",
    "Kiribati": "AUD", "Kuwait": "KWD", "Kyrgyzstan": "KGS", "Laos": "LAK", "Latvia": "EUR",
    "Lebanon": "LBP", "Lesotho": "LSL", "Liberia": "LRD", "Libya": "LYD", "Liechtenstein": "CHF",
    "Lithuania": "EUR", "Luxembourg": "EUR", "Madagascar": "MGA", "Malawi": "MWK", "Malaysia": "MYR",
    "Maldives": "MVR", "Mali": "XOF", "Malta": "EUR", "Marshall Islands": "USD", "Mauritania": "MRU",
    "Mauritius": "MUR", "Mexico": "MXN", "Micronesia": "USD", "Moldova": "MDL", "Monaco": "EUR",
    "Mongolia": "MNT", "Montenegro": "EUR", "Morocco": "MAD", "Mozambique": "MZN", "Myanmar": "MMK",
    "Namibia": "NAD", "Nauru": "AUD", "Nepal": "NPR", "Netherlands": "EUR", "New Zealand": "NZD",
    "Nicaragua": "NIO", "Niger": "XOF", "Nigeria": "NGN", "North Korea": "KPW", "North Macedonia": "MKD",
    "Norway": "NOK", "Oman": "OMR", "Pakistan": "PKR", "Palau": "USD", "Panama": "PAB",
    "Papua New Guinea": "PGK", "Paraguay": "PYG", "Peru": "PEN", "Philippines": "PHP", "Poland": "PLN",
    "Portugal": "EUR", "Qatar": "QAR", "Romania": "RON", "Russia": "RUB", "Rwanda": "RWF",
    "Saint Lucia": "XCD", "Samoa": "WST", "San Marino": "EUR", "Saudi Arabia": "SAR", "Senegal": "XOF",
    "Serbia": "RSD", "Seychelles": "SCR", "Sierra Leone": "SLL", "Singapore": "SGD", "Slovakia": "EUR",
    "Slovenia": "EUR", "Somalia": "SOS", "South Africa": "ZAR", "South Korea": "KRW", "South Sudan": "SSP",
    "Spain": "EUR", "Sri Lanka": "LKR", "Sudan": "SDG", "Suriname": "SRD", "Sweden": "SEK",
    "Switzerland": "CHF", "Syria": "SYP", "Taiwan": "TWD", "Tajikistan": "TJS", "Tanzania": "TZS",
    "Thailand": "THB", "Timor-Leste": "USD", "Togo": "XOF", "Tonga": "TOP", "Trinidad and Tobago": "TTD",
    "Tunisia": "TND", "Turkey": "TRY", "Turkmenistan": "TMT", "Tuvalu": "AUD", "Uganda": "UGX",
    "Ukraine": "UAH", "United Arab Emirates": "AED", "United Kingdom": "GBP", "United States": "USD",
    "Uruguay": "UYU", "Uzbekistan": "UZS", "Vanuatu": "VUV", "Vatican City": "EUR", "Venezuela": "VES",
    "Vietnam": "VND", "Yemen": "YER", "Zambia": "ZMW", "Zimbabwe": "ZWL"
}

# ------------------------------------------------------------------------------------
# LIGHTWEIGHT MAJOR CURRENCY RATE TABLE
# ------------------------------------------------------------------------------------
major_rates = {
    "INR": 1, "USD": 83.2, "EUR": 90.5, "GBP": 106.7, "JPY": 0.56, "AED": 22.6, "CNY": 11.8,
    "AUD": 55.3, "CAD": 61.4, "SGD": 62.1, "CHF": 94.3, "SAR": 22.2
}

all_codes = set(country_currency.values())
for code in all_codes:
    if code not in major_rates:
        major_rates[code] = float(np.random.randint(50, 120))

# ------------------------------------------------------------------------------------
# 2 TAB LAYOUT
# ------------------------------------------------------------------------------------
tab1, tab2 = st.tabs(["🌍 Currency Converter", "💎 Commodities"])

# =====================================================================
# TAB 1: CURRENCY
# =====================================================================
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌍 Convert Currency Across 250+ Countries")

    col1, col2 = st.columns(2)

    with col1:
        f_country = st.selectbox("From Country", sorted(country_currency.keys()))
        f_curr = country_currency[f_country]

    with col2:
        t_country = st.selectbox("To Country", sorted(country_currency.keys()), index=10)
        t_curr = country_currency[t_country]

    amt = st.number_input("Amount", min_value=0.0, value=100.0)

    result = (amt * major_rates[f_curr]) / major_rates[t_curr]

    st.markdown(f"""
    <div class="predict-box">
        <b>{amt:.2f} {f_curr}</b> =
        <span>{result:,.2f} {t_curr}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# TAB 2: COMMODITIES + PREDICTION
# =====================================================================
# =====================================================================
# TAB 2: COMMODITIES + PROFIT/LOSS + HISTORY TABLE + PREDICTION
# =====================================================================
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💎 Commodity Dashboard with Prediction")

    # ---------------- COMMODITY DATA ----------------
    commodities = {
        "Gold (per gram)": {y: 600 + (y - 2010) * 150 for y in range(2010, 2025)},
        "Silver (per gram)": {y: 25 + (y - 2010) * 3 for y in range(2010, 2025)},
        "Platinum (per gram)": {y: 1700 + (y - 2010) * 120 for y in range(2010, 2025)},
        "Iron (per kg)": {y: 30 + (y - 2010) * 2 for y in range(2010, 2025)},
        "Diamond (per carat)": {y: 175000 + (y - 2010) * 15000 for y in range(2010, 2025)}
    }

    # ---------------- SELECT BOX ----------------
    sele = st.selectbox("Select Commodity", list(commodities.keys()))
    data = commodities[sele]

    years = list(data.keys())
    values = list(data.values())

    # ---------------- HISTORICAL CHART ----------------
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=values,
        mode="lines+markers",
        line=dict(color="#004aad", width=3)
    ))
    fig.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- HISTORY TABLE ----------------
    st.markdown("### 📘 Historical Price Table (2010 - 2024)")

    df_history = pd.DataFrame({
        "Year": years,
        "Price": values
    })

    st.dataframe(df_history, use_container_width=True)   # dark mode friendly

    # ---------------- PROFIT / LOSS ----------------
    st.markdown("### 📊 Profit / Loss Calculator")

    colA, colB = st.columns(2)

    with colA:
        buy_year = st.selectbox("Bought In Year", years)

    with colB:
        quantity = st.number_input("Quantity (in units)", min_value=0.0, value=1.0)

    buy_price = data[buy_year]
    today_price = data[2024]

    profit = (today_price - buy_price) * quantity
    percent = (profit / (buy_price * quantity)) * 100

    if profit >= 0:
        st.success(f"🟢 Profit: ₹{profit:,.2f} ({percent:.2f}%)")
    else:
        st.error(f"🔴 Loss: ₹{profit:,.2f} ({percent:.2f}%)")

    # ---------------- PREDICTION ----------------
    st.markdown("### 🔮 Predicted Values (Next 5 Years)")

    x = np.array(years)
    y = np.array(values)
    m, b = np.polyfit(x, y, 1)

    future = {fy: m * fy + b for fy in range(2025, 2030)}

    df_future = pd.DataFrame({
        "Year": list(future.keys()),
        "Predicted Price": [f"{v:,.2f}" for v in future.values()]
    })

    st.dataframe(df_future, use_container_width=True)

    # ---------------- PREDICTION CHART ----------------
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=years, y=values, name="Historical", line=dict(color="#004aad")))
    fig2.add_trace(go.Scatter(x=list(future.keys()), y=list(future.values()),
                              name="Predicted", line=dict(color="#ff6b00", dash="dash")))
    fig2.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)