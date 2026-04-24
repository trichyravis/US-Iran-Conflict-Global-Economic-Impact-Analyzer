
"""
US–Iran Conflict: Global Economic Impact Analyzer
Prof. V. Ravichandran | The Mountain Path — World of Finance
Visiting Faculty @ NMIMS Bangalore, BITS Pilani, RV University Bangalore, Goa Institute of Management

Multi-layer transmission model: Energy Shock → Inflation → Growth → External Sector → Supply Chains
Country archetypes: Energy Importers (Advanced), Emerging Importers, Semi-Insulated, Energy Flexible, Exporters
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="US–Iran War: Global Economic Impact Analyzer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# MOUNTAIN PATH DESIGN SYSTEM
# ──────────────────────────────────────────────────────────────────────────────
NAVY   = "#003366"
GOLD   = "#FFD700"
LBLUE  = "#ADD8E6"
CARD   = "#112240"
TXT    = "#e6f1ff"
MUTED  = "#8892b0"
GRN    = "#28a745"
RED    = "#dc3545"
MID    = "#004d80"
ORANGE = "#ff8c00"
PURPLE = "#9b59b6"

def apply_css():
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(135deg, #1a2332, #243447, #2a3f5f);
        }}
        [data-testid="stSidebar"] {{
            background: {CARD} !important;
        }}
        [data-testid="stSidebar"] * {{
            color: {TXT} !important;
            -webkit-text-fill-color: {TXT} !important;
        }}
        .stSelectbox label, .stMultiSelect label, .stSlider label, .stRadio label {{
            color: {TXT} !important;
            -webkit-text-fill-color: {TXT} !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {GOLD} !important;
            -webkit-text-fill-color: {GOLD} !important;
        }}
        .stMarkdown p, .stMarkdown li {{
            color: {TXT} !important;
            -webkit-text-fill-color: {TXT} !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {GOLD} !important;
            -webkit-text-fill-color: {GOLD} !important;
        }}
        [data-testid="stMetricDelta"] {{
            font-size: 0.9rem !important;
        }}
        div.stTabs [data-baseweb="tab-list"] button {{
            color: {MUTED} !important;
            -webkit-text-fill-color: {MUTED} !important;
        }}
        div.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
            color: {GOLD} !important;
            -webkit-text-fill-color: {GOLD} !important;
            border-bottom: 2px solid {GOLD} !important;
        }}
        .stDataFrame {{
            border: 1px solid {MID} !important;
        }}
        div[data-testid="stExpander"] details {{
            background: {CARD} !important;
            border: 1px solid {MID} !important;
        }}
        div[data-testid="stExpander"] summary p {{
            color: {GOLD} !important;
            -webkit-text-fill-color: {GOLD} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_css()

# ──────────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────────
st.html(f"""
<div style="text-align:center; padding:20px 10px 5px; user-select:none;">
    <h1 style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:2.2rem; margin-bottom:5px;
               font-family:'Playfair Display',Georgia,serif; letter-spacing:1px;">
        🌍 US–Iran Conflict: Global Economic Impact Analyzer
    </h1>
    <p style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE}; font-size:1.05rem; margin-bottom:2px;">
        Multi-Layer Transmission Model &nbsp;|&nbsp; Country & Regional Impact Assessment
    </p>
    <p style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.85rem;">
        Prof. V. Ravichandran &nbsp;|&nbsp; The Mountain Path — World of Finance
    </p>
</div>
""")

# ──────────────────────────────────────────────────────────────────────────────
# COMPREHENSIVE DATA LAYER
# Sources: IMF WEO (Apr 2025), World Bank WDI, EIA, BP Statistical Review
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data
def get_country_data():
    """
    Comprehensive country-level economic data.
    Sources: IMF WEO Apr 2025 estimates, World Bank WDI, EIA, BP Statistical Review 2024.
    Energy import dependence = net energy imports / total energy consumption (%).
    """
    data = {
        # Country, Region, Archetype, GDP_Bn_USD, GDP_Growth_%, CPI_Inflation_%,
        # Oil_Import_Dependence_%, Current_Account_%GDP, FX_Reserves_Bn, Debt_%GDP,
        # Energy_Intensity (MJ/$GDP), Trade_Openness_%GDP, Oil_Consumption_mbpd,
        # Oil_Production_mbpd, Subsidy_%GDP, Pop_Mn
        "Country": [
            "United States","Germany","France","United Kingdom","Italy","Spain","Netherlands",
            "Japan","South Korea","Australia","Canada",
            "India","China","Turkey","Indonesia","Thailand","Vietnam","Philippines","Pakistan","Bangladesh","Egypt",
            "Saudi Arabia","UAE","Qatar","Kuwait","Iraq","Iran",
            "Brazil","Mexico","Argentina","Colombia","Chile",
            "Nigeria","South Africa","Kenya","Ghana",
            "Russia","Poland","Czech Republic","Romania"
        ],
        "Region": [
            "North America","Euro Area","Euro Area","Europe","Euro Area","Euro Area","Euro Area",
            "East Asia","East Asia","Oceania","North America",
            "South Asia","East Asia","MENA/Europe","SE Asia","SE Asia","SE Asia","SE Asia","South Asia","South Asia","MENA",
            "MENA","MENA","MENA","MENA","MENA","MENA",
            "Latin America","Latin America","Latin America","Latin America","Latin America",
            "Sub-Saharan Africa","Sub-Saharan Africa","Sub-Saharan Africa","Sub-Saharan Africa",
            "Eastern Europe","Eastern Europe","Eastern Europe","Eastern Europe"
        ],
        "Archetype": [
            "Energy Flexible","Energy Importer (Advanced)","Energy Importer (Advanced)",
            "Energy Importer (Advanced)","Energy Importer (Advanced)","Energy Importer (Advanced)",
            "Energy Importer (Advanced)",
            "Energy Importer (Advanced)","Energy Importer (Advanced)","Energy Exporter","Energy Exporter",
            "Emerging Importer (Fragile FX)","Large Semi-Insulated","Emerging Importer (Fragile FX)",
            "Emerging Importer (Fragile FX)","Emerging Importer (Fragile FX)",
            "Emerging Importer (Fragile FX)","Emerging Importer (Fragile FX)",
            "Emerging Importer (Fragile FX)","Emerging Importer (Fragile FX)",
            "Emerging Importer (Fragile FX)",
            "Energy Exporter","Energy Exporter","Energy Exporter","Energy Exporter","Energy Exporter","Energy Exporter",
            "Emerging Importer (Fragile FX)","Emerging Importer (Fragile FX)",
            "Emerging Importer (Fragile FX)","Emerging Importer (Fragile FX)",
            "Emerging Importer (Fragile FX)",
            "Emerging Importer (Fragile FX)","Emerging Importer (Fragile FX)",
            "Emerging Importer (Fragile FX)","Emerging Importer (Fragile FX)",
            "Energy Exporter","Energy Importer (Advanced)","Energy Importer (Advanced)","Emerging Importer (Fragile FX)"
        ],
        "GDP_Bn": [
            28800, 4520, 3130, 3500, 2260, 1580, 1090,
            4230, 1710, 1800, 2240,
            3940, 18500, 1080, 1420, 515, 450, 410, 340, 460, 400,
            1100, 510, 220, 165, 265, 390,
            2170, 1790, 640, 340, 350,
            390, 400, 115, 80,
            2000, 840, 340, 370
        ],
        "GDP_Growth": [
            2.3, 0.8, 1.1, 1.3, 0.7, 2.1, 1.0,
            1.0, 2.2, 2.0, 1.8,
            6.5, 4.5, 3.0, 5.1, 2.8, 6.0, 5.8, 2.5, 5.5, 3.8,
            3.5, 4.0, 2.5, 2.8, 5.0, 3.2,
            2.2, 1.5, -1.5, 2.0, 2.5,
            3.0, 1.5, 5.0, 3.5,
            1.8, 3.0, 2.5, 3.5
        ],
        "Inflation": [
            3.2, 2.5, 2.3, 3.0, 2.0, 3.2, 2.8,
            2.5, 2.3, 3.5, 2.8,
            4.5, 0.5, 45.0, 3.0, 1.5, 4.0, 3.8, 12.0, 9.5, 28.0,
            2.0, 2.5, 2.8, 3.0, 4.5, 35.0,
            4.5, 4.0, 100.0, 7.0, 4.5,
            25.0, 5.0, 6.5, 22.0,
            8.0, 4.5, 3.0, 5.5
        ],
        "Oil_Import_Dep": [
            -5, 95, 98, 85, 90, 95, 100,
            95, 97, -80, -60,
            85, 72, 92, 65, 80, 95, 100, 85, 100, 90,
            -350, -250, -500, -380, -300, -180,
            15, -5, 10, -20, 95,
            -80, 85, 100, 90,
            -250, 96, 97, 80
        ],
        "Current_Account": [
            -3.0, 6.5, -1.5, -3.5, 0.5, 1.0, 8.0,
            3.5, 4.0, 1.5, -1.0,
            -1.8, 1.5, -4.5, -0.5, 5.0, 3.5, -3.0, -2.5, -1.0, -5.0,
            5.0, 12.0, 15.0, 25.0, 8.0, 2.0,
            -2.5, -1.5, -1.0, -3.0, -4.0,
            -0.5, -2.5, -5.0, -3.5,
            5.0, -1.0, 0.5, -6.0
        ],
        "FX_Reserves_Bn": [
            250, 320, 250, 200, 220, 100, 50,
            1250, 420, 60, 100,
            620, 3400, 100, 145, 220, 90, 100, 15, 25, 35,
            450, 180, 50, 50, 100, 30,
            340, 220, 25, 60, 40,
            35, 60, 8, 6,
            480, 180, 160, 60
        ],
        "Debt_GDP": [
            125, 65, 112, 100, 140, 108, 50,
            260, 55, 45, 105,
            85, 80, 35, 40, 62, 37, 60, 75, 40, 92,
            25, 30, 45, 10, 55, 35,
            75, 55, 85, 55, 40,
            40, 72, 70, 80,
            20, 50, 42, 50
        ],
        "Oil_Consumption_mbpd": [
            20.0, 2.1, 1.5, 1.4, 1.2, 1.2, 0.9,
            3.4, 2.7, 1.1, 2.4,
            5.5, 16.0, 1.0, 1.8, 1.3, 0.5, 0.5, 0.6, 0.1, 0.7,
            3.8, 1.2, 0.3, 0.5, 0.8, 1.8,
            3.1, 1.9, 0.5, 0.3, 0.4,
            0.5, 0.6, 0.1, 0.1,
            3.5, 0.6, 0.2, 0.2
        ],
        "Oil_Production_mbpd": [
            13.0, 0.03, 0.01, 0.7, 0.1, 0.01, 0.02,
            0.003, 0.03, 0.3, 5.5,
            0.8, 4.2, 0.07, 0.6, 0.2, 0.01, 0.01, 0.08, 0.0, 0.55,
            12.0, 4.0, 1.8, 2.7, 4.5, 3.5,
            3.3, 2.0, 0.6, 0.75, 0.01,
            1.5, 0.01, 0.0, 0.0,
            10.5, 0.02, 0.003, 0.07
        ],
        "Energy_Subsidy_GDP": [
            0.2, 0.3, 0.2, 0.1, 0.3, 0.2, 0.1,
            0.3, 0.4, 0.1, 0.2,
            2.0, 0.8, 0.5, 1.5, 0.5, 0.3, 0.5, 3.5, 1.5, 6.5,
            5.0, 4.5, 3.0, 6.0, 7.0, 8.0,
            0.8, 1.0, 3.0, 0.5, 0.3,
            2.0, 1.5, 0.5, 0.3,
            1.0, 0.2, 0.2, 0.5
        ],
        "Pop_Mn": [
            335, 84, 68, 68, 59, 48, 18,
            124, 52, 26, 40,
            1430, 1425, 85, 280, 72, 100, 115, 240, 172, 105,
            37, 10, 3, 4, 44, 88,
            216, 130, 46, 52, 20,
            225, 60, 55, 34,
            144, 38, 11, 19
        ],
        "Currency": [
            "USD","EUR","EUR","GBP","EUR","EUR","EUR",
            "JPY","KRW","AUD","CAD",
            "INR","CNY","TRY","IDR","THB","VND","PHP","PKR","BDT","EGP",
            "SAR","AED","QAR","KWD","IQD","IRR",
            "BRL","MXN","ARS","COP","CLP",
            "NGN","ZAR","KES","GHS",
            "RUB","PLN","CZK","RON"
        ],
        "FX_Regime": [
            "Free Float","Free Float","Free Float","Free Float","Free Float","Free Float","Free Float",
            "Free Float","Free Float","Free Float","Free Float",
            "Managed Float","Managed Float","Free Float","Free Float","Managed Float","Managed Float",
            "Free Float","Managed Float","Managed Float","Managed Float",
            "Peg (USD)","Peg (USD)","Peg (USD)","Peg (USD)","Managed Float","Managed Float",
            "Free Float","Free Float","Crawling Peg","Free Float","Free Float",
            "Managed Float","Free Float","Managed Float","Managed Float",
            "Managed Float","Free Float","Free Float","Free Float"
        ]
    }
    return pd.DataFrame(data)


@st.cache_data
def get_strait_hormuz_data():
    """Strait of Hormuz transit data (EIA, 2024 estimates)"""
    return {
        "daily_oil_flow_mbpd": 21.0,
        "pct_global_seaborne_oil": 30,
        "pct_global_lng": 20,
        "key_exporters": ["Saudi Arabia", "Iraq", "UAE", "Kuwait", "Qatar", "Iran"],
        "alternative_routes": {
            "Saudi East-West Pipeline": {"capacity_mbpd": 5.0, "status": "Operational"},
            "UAE Abu Dhabi Pipeline (Habshan-Fujairah)": {"capacity_mbpd": 1.5, "status": "Operational"},
            "Iraq-Turkey (Kirkuk-Ceyhan)": {"capacity_mbpd": 0.9, "status": "Partially operational"},
        },
        "total_bypass_capacity_mbpd": 7.4
    }


@st.cache_data
def get_historical_oil_shocks():
    """Historical oil price shock episodes for context"""
    return pd.DataFrame({
        "Event": [
            "1973 Arab Oil Embargo", "1979 Iranian Revolution", "1990 Gulf War",
            "2003 Iraq Invasion", "2008 Financial Crisis", "2011 Arab Spring",
            "2014 Oil Glut", "2020 COVID + Price War", "2022 Russia-Ukraine War",
            "2026 US-Iran Conflict"
        ],
        "Year": [1973, 1979, 1990, 2003, 2008, 2011, 2014, 2020, 2022, 2026],
        "Peak_Oil_Change_%": [300, 150, 100, 40, -75, 25, -60, -65, 60, None],
        "Global_GDP_Impact_%": [-2.5, -3.0, -1.5, -0.5, -3.5, -0.3, 0.3, -3.1, -0.8, None],
        "Duration_Months": [16, 18, 8, 6, 18, 6, 24, 12, 12, None]
    })

# ──────────────────────────────────────────────────────────────────────────────
# IMPACT MODEL ENGINE
# ──────────────────────────────────────────────────────────────────────────────

def compute_oil_shock_impact(df, oil_price_change_pct, gas_price_change_pct,
                              hormuz_disruption_pct, war_duration_months):
    """
    Multi-layer transmission model.

    Layer 1 → Energy cost shock
    Layer 2 → Inflation pass-through (direct + indirect + second-round)
    Layer 3 → GDP growth impact
    Layer 4 → External sector (current account, FX)
    Layer 5 → Fiscal impact (subsidy burden)
    """
    results = df.copy()
    oil_chg = oil_price_change_pct / 100.0
    gas_chg = gas_price_change_pct / 100.0
    duration_factor = min(war_duration_months / 12.0, 2.0)  # caps at 2 years

    # Net oil import ratio (positive = importer, negative = exporter)
    results["Net_Oil_Import_Ratio"] = results["Oil_Import_Dep"].clip(-100, 100) / 100.0

    # ── Layer 1: Energy Cost Shock ──
    # Cost shock proportional to import dependence and price change
    results["Energy_Cost_Shock_%"] = (
        results["Net_Oil_Import_Ratio"].clip(lower=0) * oil_chg * 100 * 0.6 +
        results["Net_Oil_Import_Ratio"].clip(lower=0) * gas_chg * 100 * 0.4
    )
    # Exporters get revenue boost
    results["Exporter_Revenue_Gain_%"] = (
        (-results["Net_Oil_Import_Ratio"]).clip(lower=0) * oil_chg * 100 * 0.5
    )

    # Hormuz disruption: additional supply shock for Gulf-dependent importers
    hormuz_exposure = results["Country"].map(
        lambda c: 0.8 if c in ["India", "Japan", "South Korea", "China", "Thailand"]
        else (0.5 if c in ["Germany", "France", "Italy", "Spain", "Netherlands",
                           "United Kingdom", "Turkey", "Pakistan", "Bangladesh"]
              else (0.3 if c in ["United States", "Brazil", "Mexico", "Australia"]
                    else (0.9 if c in ["Saudi Arabia", "UAE", "Qatar", "Kuwait", "Iraq", "Iran"]
                          else 0.4)))
    )
    results["Hormuz_Supply_Shock_%"] = hormuz_exposure * (hormuz_disruption_pct / 100.0) * 15

    # ── Layer 2: Inflation Pass-Through ──
    # Direct: fuel/energy prices (immediate)
    direct_inflation = results["Energy_Cost_Shock_%"] * 0.12
    # Indirect: transport, food, manufacturing (lagged 2-4 months)
    indirect_inflation = results["Energy_Cost_Shock_%"] * 0.08 * duration_factor
    # Second-round: wages, expectations (lagged 6-12 months)
    second_round = results["Energy_Cost_Shock_%"] * 0.04 * (duration_factor ** 0.5)
    # Hormuz supply disruption adds extra inflation
    hormuz_inflation = results["Hormuz_Supply_Shock_%"] * 0.15

    results["Inflation_Impact_ppt"] = (
        direct_inflation + indirect_inflation + second_round + hormuz_inflation
    ).round(2)

    # Exporters: mild inflation from demand/spending boom
    exporter_mask = results["Net_Oil_Import_Ratio"] < -0.5
    results.loc[exporter_mask, "Inflation_Impact_ppt"] = (
        results.loc[exporter_mask, "Exporter_Revenue_Gain_%"] * 0.02
    ).round(2)

    results["New_Inflation_%"] = (results["Inflation"] + results["Inflation_Impact_ppt"]).round(1)

    # ── Layer 3: GDP Growth Impact ──
    # Base GDP hit from energy cost shock
    gdp_hit_energy = -results["Energy_Cost_Shock_%"] * 0.035 * duration_factor
    # Investment uncertainty shock (uniform across all countries)
    gdp_hit_uncertainty = -0.3 * duration_factor
    # Consumption squeeze from inflation
    gdp_hit_consumption = -results["Inflation_Impact_ppt"] * 0.08
    # Hormuz supply chain disruption
    gdp_hit_hormuz = -results["Hormuz_Supply_Shock_%"] * 0.04

    results["GDP_Impact_ppt"] = (
        gdp_hit_energy + gdp_hit_uncertainty + gdp_hit_consumption + gdp_hit_hormuz
    ).round(2)

    # Exporters: revenue gain partially offsets
    results.loc[exporter_mask, "GDP_Impact_ppt"] = (
        results.loc[exporter_mask, "Exporter_Revenue_Gain_%"] * 0.02 - 0.2 * duration_factor
    ).round(2)

    results["New_GDP_Growth_%"] = (results["GDP_Growth"] + results["GDP_Impact_ppt"]).round(1)

    # ── Layer 4: External Sector ──
    # Current account deterioration for importers
    ca_hit = (
        results["Net_Oil_Import_Ratio"].clip(lower=0) * oil_chg * 2.5 +
        results["Hormuz_Supply_Shock_%"] * 0.05
    )
    results["CA_Impact_ppt"] = (-ca_hit).round(2)
    results.loc[exporter_mask, "CA_Impact_ppt"] = (
        results.loc[exporter_mask, "Exporter_Revenue_Gain_%"] * 0.06
    ).round(2)
    results["New_CA_%GDP"] = (results["Current_Account"] + results["CA_Impact_ppt"]).round(1)

    # FX depreciation pressure (importers with weak reserves)
    reserve_adequacy = results["FX_Reserves_Bn"] / (results["GDP_Bn"] * 0.3)  # months of imports proxy
    results["FX_Pressure_Score"] = (
        (results["Net_Oil_Import_Ratio"].clip(lower=0) * oil_chg * 30) /
        (reserve_adequacy.clip(lower=0.1) * 10)
    ).clip(0, 100).round(1)

    # Managed/pegged currencies are more stable
    peg_mask = results["FX_Regime"].str.contains("Peg")
    results.loc[peg_mask, "FX_Pressure_Score"] *= 0.3

    # ── Layer 5: Fiscal Impact ──
    results["Fiscal_Cost_Subsidy_%GDP"] = (
        results["Energy_Subsidy_GDP"] * (1 + oil_chg * 0.5) - results["Energy_Subsidy_GDP"]
    ).round(2)

    # ── Composite Vulnerability Score ──
    # Normalize each dimension 0-100 and weight
    norm = lambda s: ((s - s.min()) / (s.max() - s.min() + 1e-9) * 100)

    results["Vulnerability_Score"] = (
        norm(-results["GDP_Impact_ppt"]) * 0.30 +
        norm(results["Inflation_Impact_ppt"]) * 0.25 +
        norm(-results["CA_Impact_ppt"]) * 0.20 +
        norm(results["FX_Pressure_Score"]) * 0.15 +
        norm(results["Fiscal_Cost_Subsidy_%GDP"]) * 0.10
    ).round(1)

    # Exporters get negative vulnerability (net benefit)
    results.loc[exporter_mask, "Vulnerability_Score"] = (
        -results.loc[exporter_mask, "Exporter_Revenue_Gain_%"] * 0.5
    ).clip(-50, 0).round(1)

    # Impact Category
    results["Impact_Category"] = pd.cut(
        results["Vulnerability_Score"],
        bins=[-100, -10, 20, 40, 60, 100],
        labels=["Net Beneficiary", "Low Impact", "Moderate Impact", "High Impact", "Severe Impact"]
    )

    return results


# ──────────────────────────────────────────────────────────────────────────────
# PLOTLY TEMPLATE
# ──────────────────────────────────────────────────────────────────────────────
def mp_layout(fig, title="", height=500):
    fig.update_layout(
        title=dict(text=title, font=dict(color=GOLD, size=16, family="Georgia")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=CARD,
        font=dict(color=TXT, family="Georgia", size=12),
        height=height,
        margin=dict(l=60, r=30, t=60, b=50),
        legend=dict(
            bgcolor="rgba(0,0,0,0.3)", bordercolor=MID,
            font=dict(color=TXT, size=11)
        ),
        xaxis=dict(gridcolor="rgba(136,146,176,0.15)", zerolinecolor=MID),
        yaxis=dict(gridcolor="rgba(136,146,176,0.15)", zerolinecolor=MID),
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR – SCENARIO CONTROLS
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.html(f"""
    <div style="text-align:center; padding:10px 0; user-select:none;">
        <h3 style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:'Playfair Display',Georgia,serif;">
            ⚙️ Scenario Parameters
        </h3>
    </div>
    """)

    scenario_preset = st.selectbox(
        "Scenario Preset",
        ["Custom", "Low Intensity", "Base Case", "Stress (Hormuz Disruption)", "Extreme (Full Blockade)"]
    )

    presets = {
        "Low Intensity":              (10, 5, 5, 3),
        "Base Case":                  (25, 20, 20, 6),
        "Stress (Hormuz Disruption)": (60, 50, 50, 9),
        "Extreme (Full Blockade)":    (100, 80, 80, 12),
    }

    if scenario_preset != "Custom" and scenario_preset in presets:
        p = presets[scenario_preset]
        oil_chg = st.slider("Crude Oil Price Change (%)", -20, 150, p[0])
        gas_chg = st.slider("Natural Gas Price Change (%)", -20, 120, p[1])
        hormuz_pct = st.slider("Hormuz Disruption (%)", 0, 100, p[2])
        duration = st.slider("Conflict Duration (months)", 1, 24, p[3])
    else:
        oil_chg = st.slider("Crude Oil Price Change (%)", -20, 150, 25)
        gas_chg = st.slider("Natural Gas Price Change (%)", -20, 120, 20)
        hormuz_pct = st.slider("Hormuz Disruption (%)", 0, 100, 20)
        duration = st.slider("Conflict Duration (months)", 1, 24, 6)

    st.divider()
    st.html(f"""
    <div style="padding:5px 0; user-select:none;">
        <p style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.8rem;">
            📊 <strong style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE};">Data Sources</strong><br>
            • IMF World Economic Outlook (Apr 2025)<br>
            • World Bank WDI<br>
            • EIA International Energy Statistics<br>
            • BP Statistical Review 2024<br>
            • BIS FX Reserve Data<br>
        </p>
    </div>
    """)

    st.html(f"""
    <div style="padding:5px 0; user-select:none;">
        <p style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.75rem;">
            🛠️ <strong style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE};">Live Data Enhancement</strong><br>
            Deploy to Streamlit Cloud for live feeds from:<br>
            • <code>yfinance</code> — Oil, Gold, FX, Equities<br>
            • <code>wbgapi</code> — World Bank indicators<br>
            • <code>fredapi</code> — US Federal Reserve data<br>
            • <code>imfpy</code> — IMF WEO datasets<br>
            • <code>eia-python</code> — US EIA energy data
        </p>
    </div>
    """)

# ──────────────────────────────────────────────────────────────────────────────
# COMPUTE IMPACTS
# ──────────────────────────────────────────────────────────────────────────────
df_base = get_country_data()
results = compute_oil_shock_impact(df_base, oil_chg, gas_chg, hormuz_pct, duration)

# ──────────────────────────────────────────────────────────────────────────────
# TAB LAYOUT
# ──────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📋 Executive Summary",
    "🌍 Country Impact Matrix",
    "📊 Transmission Channels",
    "🗺️ Regional Analysis",
    "⛽ Hormuz & Energy",
    "📈 Historical Context",
    "📐 Methodology & Data Sources"
])

# ─── TAB 1: EXECUTIVE SUMMARY ───────────────────────────────────────────────
with tabs[0]:
    st.html(f"""
    <div style="background:{CARD}; border:1px solid {MID}; border-radius:10px; padding:18px; margin-bottom:15px; user-select:none;">
        <h3 style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; margin-top:0; font-family:Georgia;">
            Scenario: Oil +{oil_chg}% &nbsp;|&nbsp; Gas +{gas_chg}% &nbsp;|&nbsp; Hormuz {hormuz_pct}% Disrupted &nbsp;|&nbsp; {duration} months
        </h3>
        <p style="color:{TXT}; -webkit-text-fill-color:{TXT}; font-size:0.95rem; margin:0;">
            The shock is fundamentally <strong style="color:{RED}; -webkit-text-fill-color:{RED};">stagflationary for energy-importing economies</strong>,
            combining cost-push inflation, demand compression, and external imbalance deterioration.
            Energy exporters experience <strong style="color:{GRN}; -webkit-text-fill-color:{GRN};">conditional gains</strong>,
            contingent on uninterrupted supply and geopolitical stability.
        </p>
    </div>
    """)

    # Key metrics
    importers = results[results["Net_Oil_Import_Ratio"] > 0.3]
    exporters = results[results["Net_Oil_Import_Ratio"] < -0.5]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        avg_gdp_hit = importers["GDP_Impact_ppt"].mean()
        st.metric("Avg GDP Hit (Importers)", f"{avg_gdp_hit:.1f} ppt", delta=f"{avg_gdp_hit:.1f}%", delta_color="inverse")
    with c2:
        avg_infl = importers["Inflation_Impact_ppt"].mean()
        st.metric("Avg Inflation Rise (Importers)", f"+{avg_infl:.1f} ppt", delta=f"+{avg_infl:.1f}%", delta_color="inverse")
    with c3:
        worst = results.loc[results["GDP_Impact_ppt"].idxmin()]
        st.metric("Most Impacted", worst["Country"], delta=f"{worst['GDP_Impact_ppt']:.1f}% GDP", delta_color="inverse")
    with c4:
        best = results.loc[results["GDP_Impact_ppt"].idxmax()]
        st.metric("Largest Beneficiary", best["Country"], delta=f"+{best['GDP_Impact_ppt']:.1f}% GDP")

    st.markdown("---")

    # Impact classification chart
    impact_counts = results["Impact_Category"].value_counts().reset_index()
    impact_counts.columns = ["Category", "Count"]
    color_map = {
        "Net Beneficiary": GRN,
        "Low Impact": LBLUE,
        "Moderate Impact": GOLD,
        "High Impact": ORANGE,
        "Severe Impact": RED
    }
    fig_cat = go.Figure()
    for _, row in impact_counts.iterrows():
        fig_cat.add_trace(go.Bar(
            x=[row["Category"]], y=[row["Count"]],
            marker_color=color_map.get(row["Category"], MUTED),
            text=[row["Count"]], textposition="outside",
            textfont=dict(color=TXT),
            name=row["Category"]
        ))
    fig_cat = mp_layout(fig_cat, "Country Impact Classification", 350)
    fig_cat.update_layout(showlegend=False, xaxis_title="", yaxis_title="Number of Countries")
    st.plotly_chart(fig_cat, use_container_width=True)

    # Vulnerability Ranking
    top_vulnerable = results.nlargest(10, "Vulnerability_Score")[
        ["Country", "Archetype", "GDP_Impact_ppt", "Inflation_Impact_ppt", "FX_Pressure_Score", "Vulnerability_Score"]
    ].reset_index(drop=True)
    top_vulnerable.index += 1
    st.html(f'<h4 style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">Top 10 Most Vulnerable Economies</h4>')
    st.dataframe(top_vulnerable, use_container_width=True)


# ─── TAB 2: COUNTRY IMPACT MATRIX ───────────────────────────────────────────
with tabs[1]:
    col_filter, col_arch = st.columns(2)
    with col_filter:
        selected_regions = st.multiselect(
            "Filter by Region",
            options=sorted(results["Region"].unique()),
            default=sorted(results["Region"].unique())
        )
    with col_arch:
        selected_archetypes = st.multiselect(
            "Filter by Archetype",
            options=sorted(results["Archetype"].unique()),
            default=sorted(results["Archetype"].unique())
        )

    filtered = results[
        (results["Region"].isin(selected_regions)) &
        (results["Archetype"].isin(selected_archetypes))
    ]

    # Bubble chart: GDP Impact vs Inflation Impact, bubble = GDP size, color = archetype
    arch_colors = {
        "Energy Flexible": LBLUE,
        "Energy Importer (Advanced)": GOLD,
        "Emerging Importer (Fragile FX)": RED,
        "Large Semi-Insulated": PURPLE,
        "Energy Exporter": GRN,
    }

    fig_bubble = go.Figure()
    for arch in filtered["Archetype"].unique():
        sub = filtered[filtered["Archetype"] == arch]
        fig_bubble.add_trace(go.Scatter(
            x=sub["GDP_Impact_ppt"], y=sub["Inflation_Impact_ppt"],
            mode="markers+text",
            marker=dict(
                size=(sub["GDP_Bn"] / sub["GDP_Bn"].max() * 60).clip(8, 60),
                color=arch_colors.get(arch, MUTED),
                opacity=0.75,
                line=dict(color="white", width=1)
            ),
            text=sub["Country"],
            textposition="top center",
            textfont=dict(size=9, color=TXT),
            name=arch,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "GDP Impact: %{x:.1f} ppt<br>"
                "Inflation Impact: %{y:.1f} ppt<br>"
                "<extra></extra>"
            )
        ))

    fig_bubble = mp_layout(fig_bubble, "GDP Growth Impact vs Inflation Pass-Through (bubble = GDP size)", 550)
    fig_bubble.update_xaxes(title="GDP Growth Impact (ppt)")
    fig_bubble.update_yaxes(title="Inflation Impact (ppt)")
    # Add quadrant lines
    fig_bubble.add_shape(type="line", x0=0, x1=0, y0=-2, y1=filtered["Inflation_Impact_ppt"].max()*1.1,
                         line=dict(color=MUTED, dash="dash", width=1))
    fig_bubble.add_shape(type="line", x0=filtered["GDP_Impact_ppt"].min()*1.1,
                         x1=filtered["GDP_Impact_ppt"].max()*1.1, y0=0, y1=0,
                         line=dict(color=MUTED, dash="dash", width=1))
    st.plotly_chart(fig_bubble, use_container_width=True)

    # Full Data Table
    display_cols = [
        "Country", "Region", "Archetype", "GDP_Growth", "New_GDP_Growth_%", "GDP_Impact_ppt",
        "Inflation", "New_Inflation_%", "Inflation_Impact_ppt",
        "Current_Account", "New_CA_%GDP", "CA_Impact_ppt",
        "FX_Pressure_Score", "Vulnerability_Score", "Impact_Category"
    ]
    with st.expander("📋 Full Country Impact Data Table", expanded=False):
        st.dataframe(
            filtered[display_cols].sort_values("Vulnerability_Score", ascending=False).reset_index(drop=True),
            use_container_width=True, height=500
        )


# ─── TAB 3: TRANSMISSION CHANNELS ───────────────────────────────────────────
with tabs[2]:
    st.html(f"""
    <div style="background:{CARD}; border-left:4px solid {GOLD}; padding:15px; margin-bottom:15px; user-select:none; border-radius:5px;">
        <h4 style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; margin:0 0 8px;">Five-Layer Transmission Framework</h4>
        <p style="color:{TXT}; -webkit-text-fill-color:{TXT}; font-size:0.9rem; margin:0;">
            <strong style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE};">Layer 1:</strong> Energy Price Shock (Oil + Gas + Freight) →
            <strong style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE};">Layer 2:</strong> Inflation (Direct + Indirect + Second-Round) →
            <strong style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE};">Layer 3:</strong> Real Economy (IP ↓, Consumption ↓, Investment ↓) →
            <strong style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE};">Layer 4:</strong> External Sector (CA ↓, FX ↓, Reserves ↓) →
            <strong style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE};">Layer 5:</strong> Supply Chain & Shortages (Hormuz chokepoint)
        </p>
    </div>
    """)

    selected_country = st.selectbox("Select Country for Deep Dive", results["Country"].tolist(), index=0)
    cdata = results[results["Country"] == selected_country].iloc[0]

    # Waterfall chart showing layer-by-layer GDP impact
    layers = ["Baseline GDP", "Energy Cost", "Uncertainty", "Inflation Drag", "Hormuz Disruption", "Net GDP Growth"]
    energy_hit = -cdata["Energy_Cost_Shock_%"] * 0.035 * min(duration/12, 2) if cdata["Net_Oil_Import_Ratio"] > 0 else cdata["Exporter_Revenue_Gain_%"] * 0.02
    uncertainty_hit = -0.3 * min(duration/12, 2)
    inflation_hit = -cdata["Inflation_Impact_ppt"] * 0.08
    hormuz_hit = -cdata["Hormuz_Supply_Shock_%"] * 0.04

    vals = [cdata["GDP_Growth"], energy_hit, uncertainty_hit, inflation_hit, hormuz_hit, 0]
    vals[-1] = cdata["GDP_Growth"] + energy_hit + uncertainty_hit + inflation_hit + hormuz_hit

    fig_wf = go.Figure(go.Waterfall(
        x=layers,
        y=[cdata["GDP_Growth"], energy_hit, uncertainty_hit, inflation_hit, hormuz_hit, vals[-1]],
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        connector=dict(line=dict(color=MUTED, width=1)),
        decreasing=dict(marker=dict(color=RED)),
        increasing=dict(marker=dict(color=GRN)),
        totals=dict(marker=dict(color=GOLD)),
        textposition="outside",
        text=[f"{v:+.2f}%" for v in [cdata["GDP_Growth"], energy_hit, uncertainty_hit, inflation_hit, hormuz_hit, vals[-1]]],
        textfont=dict(color=TXT)
    ))
    fig_wf = mp_layout(fig_wf, f"{selected_country}: GDP Growth Waterfall — Layer-by-Layer Transmission", 450)
    fig_wf.update_yaxes(title="GDP Growth (%)")
    st.plotly_chart(fig_wf, use_container_width=True)

    # Inflation decomposition
    c1, c2 = st.columns(2)
    with c1:
        direct = cdata["Energy_Cost_Shock_%"] * 0.12 if cdata["Net_Oil_Import_Ratio"] > 0 else 0
        indirect = cdata["Energy_Cost_Shock_%"] * 0.08 * min(duration/12, 2) if cdata["Net_Oil_Import_Ratio"] > 0 else 0
        second = cdata["Energy_Cost_Shock_%"] * 0.04 * (min(duration/12, 2)**0.5) if cdata["Net_Oil_Import_Ratio"] > 0 else 0
        hormuz_inf = cdata["Hormuz_Supply_Shock_%"] * 0.15

        fig_inf = go.Figure(go.Pie(
            labels=["Direct (fuel/energy)", "Indirect (transport/food)", "Second-Round (wages)", "Hormuz Supply"],
            values=[max(direct, 0.01), max(indirect, 0.01), max(second, 0.01), max(hormuz_inf, 0.01)],
            marker=dict(colors=[RED, ORANGE, GOLD, PURPLE]),
            textfont=dict(color="white"),
            hole=0.4
        ))
        fig_inf = mp_layout(fig_inf, f"{selected_country}: Inflation Channel Decomposition", 350)
        st.plotly_chart(fig_inf, use_container_width=True)

    with c2:
        # Country scorecard
        st.html(f"""
        <div style="background:{CARD}; border:1px solid {MID}; border-radius:8px; padding:15px; user-select:none;">
            <h4 style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Georgia; margin-top:0;">
                {selected_country} — Impact Scorecard
            </h4>
            <table style="width:100%; border-collapse:collapse;">
                <tr><td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:4px;">Archetype</td>
                    <td style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE}; text-align:right; padding:4px;">{cdata['Archetype']}</td></tr>
                <tr><td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:4px;">GDP Growth (Base → New)</td>
                    <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:right; padding:4px;">{cdata['GDP_Growth']:.1f}% → {cdata['New_GDP_Growth_%']:.1f}%</td></tr>
                <tr><td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:4px;">Inflation (Base → New)</td>
                    <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:right; padding:4px;">{cdata['Inflation']:.1f}% → {cdata['New_Inflation_%']:.1f}%</td></tr>
                <tr><td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:4px;">Current Account (Base → New)</td>
                    <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:right; padding:4px;">{cdata['Current_Account']:.1f}% → {cdata['New_CA_%GDP']:.1f}%</td></tr>
                <tr><td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:4px;">FX Pressure Score</td>
                    <td style="color:{'#dc3545' if cdata['FX_Pressure_Score']>50 else '#FFD700'}; -webkit-text-fill-color:{'#dc3545' if cdata['FX_Pressure_Score']>50 else '#FFD700'}; text-align:right; padding:4px;">
                    {cdata['FX_Pressure_Score']:.0f}/100</td></tr>
                <tr><td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:4px;">Oil Import Dependence</td>
                    <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:right; padding:4px;">{cdata['Oil_Import_Dep']:.0f}%</td></tr>
                <tr><td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:4px;">FX Reserves</td>
                    <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:right; padding:4px;">${cdata['FX_Reserves_Bn']:.0f}B</td></tr>
                <tr><td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:4px;">Fiscal Subsidy Cost</td>
                    <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:right; padding:4px;">+{cdata['Fiscal_Cost_Subsidy_%GDP']:.2f}% GDP</td></tr>
                <tr style="border-top:1px solid {MID};">
                    <td style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; padding:8px 4px; font-weight:bold;">Vulnerability Score</td>
                    <td style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:right; padding:8px 4px; font-weight:bold; font-size:1.2rem;">
                    {cdata['Vulnerability_Score']:.0f}</td></tr>
            </table>
        </div>
        """)


# ─── TAB 4: REGIONAL ANALYSIS ───────────────────────────────────────────────
with tabs[3]:
    # Aggregate by region
    region_agg = results.groupby("Region").agg(
        Avg_GDP_Impact=("GDP_Impact_ppt", "mean"),
        Avg_Inflation_Impact=("Inflation_Impact_ppt", "mean"),
        Avg_CA_Impact=("CA_Impact_ppt", "mean"),
        Avg_FX_Pressure=("FX_Pressure_Score", "mean"),
        Total_GDP_Bn=("GDP_Bn", "sum"),
        Avg_Vulnerability=("Vulnerability_Score", "mean"),
        Countries=("Country", "count")
    ).round(2).sort_values("Avg_Vulnerability", ascending=False).reset_index()

    # Grouped bar chart
    fig_reg = go.Figure()
    fig_reg.add_trace(go.Bar(
        x=region_agg["Region"], y=region_agg["Avg_GDP_Impact"],
        name="GDP Impact (ppt)", marker_color=RED, text=region_agg["Avg_GDP_Impact"].apply(lambda x: f"{x:.1f}"),
        textposition="outside", textfont=dict(color=TXT, size=10)
    ))
    fig_reg.add_trace(go.Bar(
        x=region_agg["Region"], y=region_agg["Avg_Inflation_Impact"],
        name="Inflation Impact (ppt)", marker_color=ORANGE, text=region_agg["Avg_Inflation_Impact"].apply(lambda x: f"{x:.1f}"),
        textposition="outside", textfont=dict(color=TXT, size=10)
    ))
    fig_reg.add_trace(go.Bar(
        x=region_agg["Region"], y=region_agg["Avg_CA_Impact"],
        name="CA Impact (ppt)", marker_color=LBLUE, text=region_agg["Avg_CA_Impact"].apply(lambda x: f"{x:.1f}"),
        textposition="outside", textfont=dict(color=TXT, size=10)
    ))
    fig_reg = mp_layout(fig_reg, "Regional Impact Comparison: GDP, Inflation & Current Account", 450)
    fig_reg.update_layout(barmode="group", xaxis_tickangle=-30)
    fig_reg.update_yaxes(title="Impact (percentage points)")
    st.plotly_chart(fig_reg, use_container_width=True)

    # Regional vulnerability heatmap
    arch_agg = results.groupby(["Region", "Archetype"]).agg(
        Avg_Vuln=("Vulnerability_Score", "mean"),
        Count=("Country", "count")
    ).reset_index()

    pivot = arch_agg.pivot_table(index="Region", columns="Archetype", values="Avg_Vuln", fill_value=0)

    fig_heat = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[c[:25] for c in pivot.columns],
        y=pivot.index,
        colorscale=[[0, GRN], [0.3, LBLUE], [0.6, GOLD], [1.0, RED]],
        text=pivot.values.round(1),
        texttemplate="%{text}",
        textfont=dict(color="white", size=11),
        colorbar=dict(title=dict(text="Vulnerability", font=dict(color=GOLD)), tickfont=dict(color=TXT))
    ))
    fig_heat = mp_layout(fig_heat, "Vulnerability Heatmap: Region × Archetype", 400)
    st.plotly_chart(fig_heat, use_container_width=True)

    # Regional data table
    with st.expander("📋 Regional Aggregated Data"):
        st.dataframe(region_agg, use_container_width=True)


# ─── TAB 5: HORMUZ & ENERGY ─────────────────────────────────────────────────
with tabs[4]:
    hormuz = get_strait_hormuz_data()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Daily Oil Flow", f"{hormuz['daily_oil_flow_mbpd']} mbpd")
    with c2:
        st.metric("% Global Seaborne Oil", f"{hormuz['pct_global_seaborne_oil']}%")
    with c3:
        st.metric("% Global LNG", f"{hormuz['pct_global_lng']}%")
    with c4:
        st.metric("Bypass Capacity", f"{hormuz['total_bypass_capacity_mbpd']} mbpd")

    st.markdown("---")

    # Supply disruption scenarios
    disruption_levels = [0, 10, 20, 30, 50, 70, 100]
    supply_loss = [hormuz["daily_oil_flow_mbpd"] * d/100 for d in disruption_levels]
    bypassed = [min(s, hormuz["total_bypass_capacity_mbpd"]) for s in supply_loss]
    net_loss = [s - b for s, b in zip(supply_loss, bypassed)]

    fig_hormuz = go.Figure()
    fig_hormuz.add_trace(go.Bar(
        x=[f"{d}%" for d in disruption_levels], y=bypassed,
        name="Bypassed via Pipelines", marker_color=GRN
    ))
    fig_hormuz.add_trace(go.Bar(
        x=[f"{d}%" for d in disruption_levels], y=net_loss,
        name="Net Supply Lost (mbpd)", marker_color=RED
    ))
    fig_hormuz = mp_layout(fig_hormuz, "Strait of Hormuz: Disruption vs Bypass Capacity", 400)
    fig_hormuz.update_layout(barmode="stack", xaxis_title="Hormuz Disruption Level", yaxis_title="Million Barrels/Day")
    st.plotly_chart(fig_hormuz, use_container_width=True)

    # Alternative routes table
    st.html(f'<h4 style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">Alternative Pipeline Routes</h4>')
    routes_df = pd.DataFrame([
        {"Route": k, "Capacity (mbpd)": v["capacity_mbpd"], "Status": v["status"]}
        for k, v in hormuz["alternative_routes"].items()
    ])
    st.dataframe(routes_df, use_container_width=True, hide_index=True)

    # Oil production/consumption comparison
    fig_oilbal = make_subplots(rows=1, cols=2, subplot_titles=["Top Oil Consumers (mbpd)", "Top Oil Producers (mbpd)"])
    top_consumers = results.nlargest(12, "Oil_Consumption_mbpd")
    top_producers = results.nlargest(12, "Oil_Production_mbpd")

    fig_oilbal.add_trace(go.Bar(
        x=top_consumers["Country"], y=top_consumers["Oil_Consumption_mbpd"],
        marker_color=RED, name="Consumption"
    ), row=1, col=1)
    fig_oilbal.add_trace(go.Bar(
        x=top_producers["Country"], y=top_producers["Oil_Production_mbpd"],
        marker_color=GRN, name="Production"
    ), row=1, col=2)
    fig_oilbal = mp_layout(fig_oilbal, "", 400)
    fig_oilbal.update_xaxes(tickangle=-40)
    st.plotly_chart(fig_oilbal, use_container_width=True)


# ─── TAB 6: HISTORICAL CONTEXT ──────────────────────────────────────────────
with tabs[5]:
    hist = get_historical_oil_shocks()

    fig_hist = go.Figure()
    hist_valid = hist.dropna(subset=["Peak_Oil_Change_%"])

    fig_hist.add_trace(go.Bar(
        x=hist_valid["Event"], y=hist_valid["Peak_Oil_Change_%"],
        marker_color=[RED if v > 0 else GRN for v in hist_valid["Peak_Oil_Change_%"]],
        text=hist_valid["Peak_Oil_Change_%"].apply(lambda x: f"{x:+.0f}%"),
        textposition="outside", textfont=dict(color=TXT),
        name="Oil Price Change %"
    ))
    fig_hist = mp_layout(fig_hist, "Historical Oil Price Shocks — Peak Change (%)", 420)
    fig_hist.update_xaxes(tickangle=-35)
    fig_hist.update_yaxes(title="Peak Oil Price Change (%)")
    st.plotly_chart(fig_hist, use_container_width=True)

    # GDP impact comparison
    fig_gdp_hist = go.Figure()
    fig_gdp_hist.add_trace(go.Scatter(
        x=hist_valid["Peak_Oil_Change_%"], y=hist_valid["Global_GDP_Impact_%"],
        mode="markers+text",
        marker=dict(size=hist_valid["Duration_Months"]*2.5, color=GOLD, opacity=0.7,
                    line=dict(color=TXT, width=1)),
        text=hist_valid["Event"].str.split(" ").str[:2].str.join(" "),
        textposition="top center", textfont=dict(color=TXT, size=9),
        hovertemplate="<b>%{text}</b><br>Oil: %{x:+.0f}%<br>GDP: %{y:.1f}%<br><extra></extra>"
    ))
    fig_gdp_hist = mp_layout(fig_gdp_hist, "Oil Shock Magnitude vs Global GDP Impact (bubble = duration)", 420)
    fig_gdp_hist.update_xaxes(title="Peak Oil Price Change (%)")
    fig_gdp_hist.update_yaxes(title="Global GDP Impact (%)")
    st.plotly_chart(fig_gdp_hist, use_container_width=True)

    with st.expander("📋 Historical Oil Shock Episodes Data"):
        st.dataframe(hist, use_container_width=True, hide_index=True)


# ─── TAB 7: METHODOLOGY & DATA SOURCES ──────────────────────────────────────
with tabs[6]:
    st.html(f"""
    <div style="background:{CARD}; border:1px solid {MID}; border-radius:10px; padding:20px; user-select:none;">
        <h3 style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Georgia; margin-top:0;">
            Analytical Methodology
        </h3>

        <h4 style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE};">A. Multi-Layer Transmission Model</h4>
        <p style="color:{TXT}; -webkit-text-fill-color:{TXT}; font-size:0.92rem;">
            The model uses a five-layer cascade transmission framework calibrated to empirical elasticities
            from IMF Working Papers, BIS studies, and academic research on oil-shock pass-through:
        </p>
        <p style="color:{TXT}; -webkit-text-fill-color:{TXT}; font-size:0.92rem; font-family:monospace; background:#0a192f; padding:12px; border-radius:5px;">
            <strong style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">Layer 1 — Energy Shock:</strong><br>
            &nbsp;&nbsp;Energy_Cost_Shock = Oil_Import_Dep × ΔOil × 0.6 + Oil_Import_Dep × ΔGas × 0.4<br><br>
            <strong style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">Layer 2 — Inflation Pass-Through:</strong><br>
            &nbsp;&nbsp;CPI_t = α + β₁·Oil_t + β₂·FX_t + β₃·OutputGap_t + ε_t<br>
            &nbsp;&nbsp;Direct (β≈0.12) + Indirect (β≈0.08 × duration) + Second-round (β≈0.04 × √duration)<br><br>
            <strong style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">Layer 3 — GDP Impact:</strong><br>
            &nbsp;&nbsp;GDP_t = α − γ₁·OilShock_t − γ₂·Inflation_t + γ₃·Investment_t<br>
            &nbsp;&nbsp;Energy drag + Uncertainty shock (−0.3pp/yr) + Consumption squeeze + Hormuz disruption<br><br>
            <strong style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">Layer 4 — External Sector:</strong><br>
            &nbsp;&nbsp;CA deterioration = f(Oil_Import_Dep, ΔOil, Hormuz_exposure)<br>
            &nbsp;&nbsp;FX Pressure = f(CA_hit, Reserve_adequacy, FX_regime)<br><br>
            <strong style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">Layer 5 — Fiscal:</strong><br>
            &nbsp;&nbsp;Subsidy_cost_increase = Subsidy_base × ΔOil × 0.5
        </p>

        <h4 style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE}; margin-top:20px;">B. Country Archetypes</h4>
        <p style="color:{TXT}; -webkit-text-fill-color:{TXT}; font-size:0.92rem;">
            Countries classified by impact asymmetry drivers: <strong>energy dependence + FX regime + subsidy structure</strong>.
        </p>
        <ul style="color:{TXT}; -webkit-text-fill-color:{TXT}; font-size:0.9rem;">
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};"><strong style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">Energy Importers (Advanced):</strong> Euro Area, Japan, UK, S. Korea — Stagflation (↑ inflation, ↓ growth)</li>
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};"><strong style="color:{RED}; -webkit-text-fill-color:{RED};">Emerging Importers (Fragile FX):</strong> India, Turkey, Thailand, Pakistan — Currency stress + inflation spiral</li>
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};"><strong style="color:{PURPLE}; -webkit-text-fill-color:{PURPLE};">Large Semi-Insulated:</strong> China — Mixed (cost ↑ but buffers exist)</li>
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};"><strong style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE};">Energy Flexible:</strong> US — Moderate inflation, limited recession risk</li>
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};"><strong style="color:{GRN}; -webkit-text-fill-color:{GRN};">Energy Exporters:</strong> MENA, Russia, Canada — Revenue gain (if no disruption)</li>
        </ul>

        <h4 style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE}; margin-top:20px;">C. Vulnerability Score</h4>
        <p style="color:{TXT}; -webkit-text-fill-color:{TXT}; font-size:0.92rem;">
            Composite weighted score (0-100): GDP Impact (30%) + Inflation (25%) + Current Account (20%) + FX Pressure (15%) + Fiscal (10%).
            Negative scores indicate net beneficiaries (energy exporters).
        </p>

        <h4 style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE}; margin-top:20px;">D. Data Sources</h4>
        <table style="width:100%; border-collapse:collapse; margin-top:8px;">
            <tr style="border-bottom:1px solid {MID};">
                <td style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; padding:6px;">Source</td>
                <td style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; padding:6px;">Indicators</td>
                <td style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; padding:6px;">Access Method</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(136,146,176,0.15);">
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">IMF WEO (Apr 2025)</td>
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">GDP, Inflation, CA Balance, Debt/GDP</td>
                <td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:6px;">imfpy / imf.org</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(136,146,176,0.15);">
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">World Bank WDI</td>
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">GDP (current USD), Population, Trade %</td>
                <td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:6px;">wbgapi / data.worldbank.org</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(136,146,176,0.15);">
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">EIA</td>
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">Oil production/consumption, Energy imports</td>
                <td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:6px;">eia-python / eia.gov</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(136,146,176,0.15);">
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">BP Statistical Review</td>
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">Energy mix, Oil trade flows, Hormuz data</td>
                <td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:6px;">bp.com/statisticalreview</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(136,146,176,0.15);">
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">BIS</td>
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">FX Reserves, Exchange rate regimes</td>
                <td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:6px;">bis.org/statistics</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(136,146,176,0.15);">
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">Yahoo Finance (yfinance)</td>
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">Live oil/gold/FX/equity prices</td>
                <td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:6px;">yfinance Python package</td>
            </tr>
            <tr>
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">FRED (St. Louis Fed)</td>
                <td style="color:{TXT}; -webkit-text-fill-color:{TXT}; padding:6px;">US macro (CPI, PCE, yields, spreads)</td>
                <td style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; padding:6px;">fredapi Python package</td>
            </tr>
        </table>

        <h4 style="color:{LBLUE}; -webkit-text-fill-color:{LBLUE}; margin-top:20px;">E. Limitations & Caveats</h4>
        <ul style="color:{TXT}; -webkit-text-fill-color:{TXT}; font-size:0.88rem;">
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};">Pass-through elasticities are calibrated from historical episodes; actual pass-through varies by country monetary framework</li>
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};">Strategic petroleum reserve releases (IEA coordinated) are not modeled</li>
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};">Financial contagion, credit spreads, and equity market feedback loops are simplified</li>
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};">Sanctions, secondary sanctions, and trade rerouting are not explicitly captured</li>
            <li style="color:{TXT}; -webkit-text-fill-color:{TXT};">Model assumes linear pass-through; non-linear threshold effects possible in extreme scenarios</li>
        </ul>
    </div>
    """)


# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.html(f"""
<div style="text-align:center; padding:15px 10px 30px; user-select:none;">
    <p style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.05rem; font-family:'Playfair Display',Georgia,serif; margin-bottom:5px;">
        The Mountain Path — World of Finance
    </p>
    <p style="color:{TXT}; -webkit-text-fill-color:{TXT}; font-size:0.88rem; margin-bottom:3px;">
        Prof. V. Ravichandran &nbsp;|&nbsp;
        Visiting Faculty @ NMIMS Bangalore, BITS Pilani, RV University Bangalore, Goa Institute of Management
    </p>
    <p style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.82rem; margin-bottom:8px;">
        28+ years Corporate Finance & Banking &nbsp;|&nbsp; 10+ years Academia
    </p>
    <p style="margin:0;">
        <a href="https://themountainpathacademy.com" target="_blank"
           style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none; margin:0 10px;">
           🌐 themountainpathacademy.com</a>
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank"
           style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none; margin:0 10px;">
           💼 LinkedIn</a>
        <a href="https://github.com/trichyravis" target="_blank"
           style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none; margin:0 10px;">
           🐙 GitHub</a>
    </p>
</div>
""")
