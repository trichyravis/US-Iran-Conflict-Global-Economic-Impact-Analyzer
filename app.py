
"""
===============================================================================
THE MOUNTAIN PATH - WORLD OF FINANCE
US–Iran Conflict: Global Economic Impact Analyzer
Prof. V. Ravichandran  |  themountainpathacademy.com
===============================================================================

Multi-layer transmission model: Energy Shock → Inflation → Growth → External Sector → Supply Chains
Country archetypes: Energy Importers (Advanced), Emerging Importers, Semi-Insulated, Energy Flexible, Exporters

Run:   streamlit run app.py
Deps:  pip install streamlit numpy pandas plotly scipy
"""

import math
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Mountain Path - US–Iran Economic Impact Analyzer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# MOUNTAIN PATH DESIGN SYSTEM  (matching Probability & Distributions app)
# ============================================================================
DARKBLUE  = "#003366"
LIGHTBLUE = "#ADD8E6"
GOLD      = "#FFD700"
ACCENTRED = "#B22234"
EXCEL_GRN = "#217346"
PY_DARK   = "#1E3250"
OFFWHITE  = "#F7FAFC"
GRN       = "#28a745"
RED       = "#dc3545"
ORANGE    = "#ff8c00"
PURPLE    = "#9b59b6"
MID       = "#004d80"

MOUNTAIN_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+Pro:wght@400;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Source Serif Pro', Georgia, 'Times New Roman', serif;
}}

.block-container {{
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}}

/* Sidebar styling */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {DARKBLUE} 0%, #001f3d 100%);
}}
[data-testid="stSidebar"] * {{
    color: #ffffff !important;
}}
[data-testid="stSidebar"] .stRadio > label > div {{
    color: #ffffff !important;
}}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
    color: {GOLD} !important;
    font-family: 'Playfair Display', serif;
}}

/* Mountain Path brand banner */
.mp-brand-banner {{
    background: linear-gradient(135deg, {DARKBLUE} 0%, #001f3d 100%);
    color: #ffffff;
    padding: 22px 30px;
    border-radius: 8px;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    border-bottom: 4px solid {GOLD};
}}
.mp-brand-banner h1 {{
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    margin: 0;
    font-size: 2.2rem;
    letter-spacing: 2px;
    color: #ffffff;
}}
.mp-brand-banner .sub {{
    font-style: italic;
    color: {LIGHTBLUE};
    font-size: 1.05rem;
}}
.mp-brand-banner .dot {{
    color: {GOLD};
    font-weight: bold;
}}

/* Page title */
.mp-title {{
    font-family: 'Playfair Display', serif;
    color: {DARKBLUE};
    font-size: 2.0rem;
    font-weight: 900;
    margin: 18px 0 4px 0;
    padding-bottom: 8px;
    border-bottom: 3px solid {GOLD};
}}
.mp-subtitle {{
    color: {DARKBLUE};
    font-size: 1.05rem;
    font-style: italic;
    margin-bottom: 18px;
}}

/* Section header */
.mp-section {{
    font-family: 'Playfair Display', serif;
    color: {DARKBLUE};
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 8px;
    padding-left: 10px;
    border-left: 5px solid {GOLD};
}}

/* Definition box (blue) */
.defn-box {{
    background: {LIGHTBLUE}33;
    border: 1.5px solid {DARKBLUE};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 10px 0 14px 0;
}}
.defn-box .head {{
    background: {DARKBLUE};
    color: #ffffff;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
    font-size: 0.95rem;
    letter-spacing: 1px;
}}

/* Example / illustration box (gold) */
.ex-box {{
    background: #fffbe6;
    border: 1.5px solid {GOLD};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 10px 0 14px 0;
}}
.ex-box .head {{
    background: {GOLD};
    color: {DARKBLUE};
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
    font-size: 0.95rem;
    letter-spacing: 1px;
}}

/* Data source box (green) */
.xl-box {{
    background: #eaf7ef;
    border: 1.5px solid {EXCEL_GRN};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 10px 0 14px 0;
    font-size: 0.95rem;
}}
.xl-box .head {{
    background: {EXCEL_GRN};
    color: #ffffff;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
    font-family: 'Source Serif Pro', serif;
    font-size: 0.95rem;
    letter-spacing: 1px;
}}

/* Warning/alert box (red tint) */
.warn-box {{
    background: #fff0f0;
    border: 1.5px solid {RED};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 10px 0 14px 0;
}}
.warn-box .head {{
    background: {RED};
    color: #ffffff;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
    font-size: 0.95rem;
    letter-spacing: 1px;
}}

/* Summary box (gold tint) */
.sum-box {{
    background: #fff7d1;
    border: 1.5px solid {DARKBLUE};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 12px 0;
}}

/* Stat chip row */
.stat-chip {{
    background: {DARKBLUE};
    color: #ffffff;
    padding: 10px 16px;
    border-radius: 6px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}}
.stat-chip .label {{
    color: {GOLD};
    font-size: 0.82rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
.stat-chip .val {{
    font-size: 1.35rem;
    font-weight: 700;
}}

/* Footer */
.mp-footer {{
    margin-top: 40px;
    padding: 14px;
    background: {DARKBLUE};
    color: #ffffff;
    text-align: center;
    border-top: 4px solid {GOLD};
    border-radius: 6px;
    font-size: 0.9rem;
}}
.mp-footer .gold {{ color: {GOLD}; font-weight: 700; }}

/* Streamlit widget overrides */
.stRadio [role="radiogroup"] label {{
    background: transparent !important;
}}
[data-testid="stMetric"] {{
    background: #ffffff;
    border: 1px solid {DARKBLUE}33;
    border-radius: 6px;
    padding: 8px 10px;
}}
[data-testid="stMetricLabel"] {{
    color: {DARKBLUE} !important;
    font-weight: 600 !important;
}}

/* Tables */
.dataframe th {{
    background: {DARKBLUE} !important;
    color: #ffffff !important;
}}

/* Buttons */
.stButton>button {{
    background: {DARKBLUE};
    color: #ffffff;
    border: 1.5px solid {GOLD};
    border-radius: 6px;
    font-weight: 600;
}}
.stButton>button:hover {{
    background: {GOLD};
    color: {DARKBLUE};
    border: 1.5px solid {DARKBLUE};
}}
</style>
"""

st.markdown(MOUNTAIN_CSS, unsafe_allow_html=True)

# ============================================================================
# HELPERS  (matching probability app style)
# ============================================================================
def brand_banner():
    st.markdown(
        f"""
        <div class="mp-brand-banner">
            <h1>THE MOUNTAIN PATH</h1>
            <div class="sub">World of Finance <span class="dot">•</span> themountainpathacademy.com</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def page_title(title, subtitle=""):
    st.markdown(f'<div class="mp-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="mp-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def section(text):
    st.markdown(f'<div class="mp-section">{text}</div>', unsafe_allow_html=True)

def defn_box(title, body_md):
    st.markdown(
        f"""<div class="defn-box"><span class="head">{title}</span><br>{body_md}</div>""",
        unsafe_allow_html=True,
    )

def ex_box(title, body_md):
    st.markdown(
        f"""<div class="ex-box"><span class="head">{title}</span><br>{body_md}</div>""",
        unsafe_allow_html=True,
    )

def xl_box(title, body_md):
    st.markdown(
        f"""<div class="xl-box"><span class="head">{title}</span><br>{body_md}</div>""",
        unsafe_allow_html=True,
    )

def warn_box(title, body_md):
    st.markdown(
        f"""<div class="warn-box"><span class="head">{title}</span><br>{body_md}</div>""",
        unsafe_allow_html=True,
    )

def sum_box(body_md):
    st.markdown(f"""<div class="sum-box">{body_md}</div>""", unsafe_allow_html=True)

def stat_chip_row(items):
    cols = st.columns(len(items))
    for c, (lbl, val) in zip(cols, items):
        with c:
            st.markdown(
                f'<div class="stat-chip"><div class="label">{lbl}</div>'
                f'<div class="val">{val}</div></div>',
                unsafe_allow_html=True,
            )

def mp_plot_layout(fig, title, xaxis="x", yaxis="y", height=420):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Playfair Display", size=18, color=DARKBLUE)),
        xaxis=dict(title=xaxis, linecolor=DARKBLUE, gridcolor="#e6eaf0"),
        yaxis=dict(title=yaxis, linecolor=DARKBLUE, gridcolor="#e6eaf0"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Source Serif Pro", color=DARKBLUE),
        height=height,
        margin=dict(l=60, r=20, t=60, b=50),
        showlegend=True,
        legend=dict(bgcolor="#ffffff", bordercolor=DARKBLUE, borderwidth=1),
    )
    return fig

LINKEDIN_URL = "https://www.linkedin.com/in/trichyravis/"
GITHUB_URL   = "https://github.com/trichyravis"

def footer():
    st.markdown(
        f"""
        <div class="mp-footer">
            <span class="gold">The Mountain Path — World of Finance</span> &nbsp;•&nbsp;
            Prof. V. Ravichandran &nbsp;•&nbsp;
            Visiting Faculty @ NMIMS Bangalore, BITS Pilani, RV University Bangalore, Goa Institute of Management &nbsp;•&nbsp;
            <a href="https://themountainpathacademy.com" target="_blank" style="color:#FFD700;text-decoration:none;">themountainpathacademy.com</a> &nbsp;•&nbsp;
            <a href="{LINKEDIN_URL}" target="_blank" style="color:#FFD700;text-decoration:none;">LinkedIn</a> &nbsp;•&nbsp;
            <a href="{GITHUB_URL}" target="_blank" style="color:#FFD700;text-decoration:none;">GitHub</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# COMPREHENSIVE DATA LAYER
# Sources: IMF WEO (Apr 2025), World Bank WDI, EIA, BP Statistical Review
# ============================================================================
@st.cache_data
def get_country_data():
    data = {
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
        "GDP_Bn": [28800,4520,3130,3500,2260,1580,1090,4230,1710,1800,2240,3940,18500,1080,1420,515,450,410,340,460,400,1100,510,220,165,265,390,2170,1790,640,340,350,390,400,115,80,2000,840,340,370],
        "GDP_Growth": [2.3,0.8,1.1,1.3,0.7,2.1,1.0,1.0,2.2,2.0,1.8,6.5,4.5,3.0,5.1,2.8,6.0,5.8,2.5,5.5,3.8,3.5,4.0,2.5,2.8,5.0,3.2,2.2,1.5,-1.5,2.0,2.5,3.0,1.5,5.0,3.5,1.8,3.0,2.5,3.5],
        "Inflation": [3.2,2.5,2.3,3.0,2.0,3.2,2.8,2.5,2.3,3.5,2.8,4.5,0.5,45.0,3.0,1.5,4.0,3.8,12.0,9.5,28.0,2.0,2.5,2.8,3.0,4.5,35.0,4.5,4.0,100.0,7.0,4.5,25.0,5.0,6.5,22.0,8.0,4.5,3.0,5.5],
        "Oil_Import_Dep": [-5,95,98,85,90,95,100,95,97,-80,-60,85,72,92,65,80,95,100,85,100,90,-350,-250,-500,-380,-300,-180,15,-5,10,-20,95,-80,85,100,90,-250,96,97,80],
        "Current_Account": [-3.0,6.5,-1.5,-3.5,0.5,1.0,8.0,3.5,4.0,1.5,-1.0,-1.8,1.5,-4.5,-0.5,5.0,3.5,-3.0,-2.5,-1.0,-5.0,5.0,12.0,15.0,25.0,8.0,2.0,-2.5,-1.5,-1.0,-3.0,-4.0,-0.5,-2.5,-5.0,-3.5,5.0,-1.0,0.5,-6.0],
        "FX_Reserves_Bn": [250,320,250,200,220,100,50,1250,420,60,100,620,3400,100,145,220,90,100,15,25,35,450,180,50,50,100,30,340,220,25,60,40,35,60,8,6,480,180,160,60],
        "Debt_GDP": [125,65,112,100,140,108,50,260,55,45,105,85,80,35,40,62,37,60,75,40,92,25,30,45,10,55,35,75,55,85,55,40,40,72,70,80,20,50,42,50],
        "Oil_Consumption_mbpd": [20.0,2.1,1.5,1.4,1.2,1.2,0.9,3.4,2.7,1.1,2.4,5.5,16.0,1.0,1.8,1.3,0.5,0.5,0.6,0.1,0.7,3.8,1.2,0.3,0.5,0.8,1.8,3.1,1.9,0.5,0.3,0.4,0.5,0.6,0.1,0.1,3.5,0.6,0.2,0.2],
        "Oil_Production_mbpd": [13.0,0.03,0.01,0.7,0.1,0.01,0.02,0.003,0.03,0.3,5.5,0.8,4.2,0.07,0.6,0.2,0.01,0.01,0.08,0.0,0.55,12.0,4.0,1.8,2.7,4.5,3.5,3.3,2.0,0.6,0.75,0.01,1.5,0.01,0.0,0.0,10.5,0.02,0.003,0.07],
        "Energy_Subsidy_GDP": [0.2,0.3,0.2,0.1,0.3,0.2,0.1,0.3,0.4,0.1,0.2,2.0,0.8,0.5,1.5,0.5,0.3,0.5,3.5,1.5,6.5,5.0,4.5,3.0,6.0,7.0,8.0,0.8,1.0,3.0,0.5,0.3,2.0,1.5,0.5,0.3,1.0,0.2,0.2,0.5],
        "Pop_Mn": [335,84,68,68,59,48,18,124,52,26,40,1430,1425,85,280,72,100,115,240,172,105,37,10,3,4,44,88,216,130,46,52,20,225,60,55,34,144,38,11,19],
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
    return {
        "daily_oil_flow_mbpd": 21.0, "pct_global_seaborne_oil": 30, "pct_global_lng": 20,
        "key_exporters": ["Saudi Arabia","Iraq","UAE","Kuwait","Qatar","Iran"],
        "alternative_routes": {
            "Saudi East-West Pipeline": {"capacity_mbpd": 5.0, "status": "Operational"},
            "UAE Habshan-Fujairah Pipeline": {"capacity_mbpd": 1.5, "status": "Operational"},
            "Iraq-Turkey (Kirkuk-Ceyhan)": {"capacity_mbpd": 0.9, "status": "Partially operational"},
        },
        "total_bypass_capacity_mbpd": 7.4
    }

@st.cache_data
def get_historical_oil_shocks():
    return pd.DataFrame({
        "Event": ["1973 Arab Oil Embargo","1979 Iranian Revolution","1990 Gulf War","2003 Iraq Invasion","2008 Financial Crisis","2011 Arab Spring","2014 Oil Glut","2020 COVID + Price War","2022 Russia-Ukraine War","2026 US-Iran Conflict"],
        "Year": [1973,1979,1990,2003,2008,2011,2014,2020,2022,2026],
        "Peak_Oil_Change_%": [300,150,100,40,-75,25,-60,-65,60,None],
        "Global_GDP_Impact_%": [-2.5,-3.0,-1.5,-0.5,-3.5,-0.3,0.3,-3.1,-0.8,None],
        "Duration_Months": [16,18,8,6,18,6,24,12,12,None]
    })


# ============================================================================
# IMPACT MODEL ENGINE
# ============================================================================
def compute_oil_shock_impact(df, oil_price_change_pct, gas_price_change_pct,
                              hormuz_disruption_pct, war_duration_months):
    results = df.copy()
    oil_chg = oil_price_change_pct / 100.0
    gas_chg = gas_price_change_pct / 100.0
    duration_factor = min(war_duration_months / 12.0, 2.0)

    results["Net_Oil_Import_Ratio"] = results["Oil_Import_Dep"].clip(-100, 100) / 100.0

    # Layer 1: Energy Cost Shock
    results["Energy_Cost_Shock_%"] = (
        results["Net_Oil_Import_Ratio"].clip(lower=0) * oil_chg * 100 * 0.6 +
        results["Net_Oil_Import_Ratio"].clip(lower=0) * gas_chg * 100 * 0.4
    )
    results["Exporter_Revenue_Gain_%"] = (
        (-results["Net_Oil_Import_Ratio"]).clip(lower=0) * oil_chg * 100 * 0.5
    )

    hormuz_exposure = results["Country"].map(
        lambda c: 0.8 if c in ["India","Japan","South Korea","China","Thailand"]
        else (0.5 if c in ["Germany","France","Italy","Spain","Netherlands","United Kingdom","Turkey","Pakistan","Bangladesh"]
              else (0.3 if c in ["United States","Brazil","Mexico","Australia"]
                    else (0.9 if c in ["Saudi Arabia","UAE","Qatar","Kuwait","Iraq","Iran"] else 0.4)))
    )
    results["Hormuz_Supply_Shock_%"] = hormuz_exposure * (hormuz_disruption_pct / 100.0) * 15

    # Layer 2: Inflation Pass-Through
    direct_inflation = results["Energy_Cost_Shock_%"] * 0.12
    indirect_inflation = results["Energy_Cost_Shock_%"] * 0.08 * duration_factor
    second_round = results["Energy_Cost_Shock_%"] * 0.04 * (duration_factor ** 0.5)
    hormuz_inflation = results["Hormuz_Supply_Shock_%"] * 0.15

    results["Inflation_Impact_ppt"] = (direct_inflation + indirect_inflation + second_round + hormuz_inflation).round(2)

    exporter_mask = results["Net_Oil_Import_Ratio"] < -0.5
    results.loc[exporter_mask, "Inflation_Impact_ppt"] = (results.loc[exporter_mask, "Exporter_Revenue_Gain_%"] * 0.02).round(2)
    results["New_Inflation_%"] = (results["Inflation"] + results["Inflation_Impact_ppt"]).round(1)

    # Layer 3: GDP Growth Impact
    gdp_hit_energy = -results["Energy_Cost_Shock_%"] * 0.035 * duration_factor
    gdp_hit_uncertainty = -0.3 * duration_factor
    gdp_hit_consumption = -results["Inflation_Impact_ppt"] * 0.08
    gdp_hit_hormuz = -results["Hormuz_Supply_Shock_%"] * 0.04

    results["GDP_Impact_ppt"] = (gdp_hit_energy + gdp_hit_uncertainty + gdp_hit_consumption + gdp_hit_hormuz).round(2)
    results.loc[exporter_mask, "GDP_Impact_ppt"] = (results.loc[exporter_mask, "Exporter_Revenue_Gain_%"] * 0.02 - 0.2 * duration_factor).round(2)
    results["New_GDP_Growth_%"] = (results["GDP_Growth"] + results["GDP_Impact_ppt"]).round(1)

    # Layer 4: External Sector
    ca_hit = results["Net_Oil_Import_Ratio"].clip(lower=0) * oil_chg * 2.5 + results["Hormuz_Supply_Shock_%"] * 0.05
    results["CA_Impact_ppt"] = (-ca_hit).round(2)
    results.loc[exporter_mask, "CA_Impact_ppt"] = (results.loc[exporter_mask, "Exporter_Revenue_Gain_%"] * 0.06).round(2)
    results["New_CA_%GDP"] = (results["Current_Account"] + results["CA_Impact_ppt"]).round(1)

    reserve_adequacy = results["FX_Reserves_Bn"] / (results["GDP_Bn"] * 0.3)
    results["FX_Pressure_Score"] = ((results["Net_Oil_Import_Ratio"].clip(lower=0) * oil_chg * 30) / (reserve_adequacy.clip(lower=0.1) * 10)).clip(0, 100).round(1)
    peg_mask = results["FX_Regime"].str.contains("Peg")
    results.loc[peg_mask, "FX_Pressure_Score"] *= 0.3

    # Layer 5: Fiscal Impact
    results["Fiscal_Cost_Subsidy_%GDP"] = (results["Energy_Subsidy_GDP"] * (1 + oil_chg * 0.5) - results["Energy_Subsidy_GDP"]).round(2)

    # Composite Vulnerability Score
    norm = lambda s: ((s - s.min()) / (s.max() - s.min() + 1e-9) * 100)
    results["Vulnerability_Score"] = (
        norm(-results["GDP_Impact_ppt"]) * 0.30 + norm(results["Inflation_Impact_ppt"]) * 0.25 +
        norm(-results["CA_Impact_ppt"]) * 0.20 + norm(results["FX_Pressure_Score"]) * 0.15 +
        norm(results["Fiscal_Cost_Subsidy_%GDP"]) * 0.10
    ).round(1)
    results.loc[exporter_mask, "Vulnerability_Score"] = (-results.loc[exporter_mask, "Exporter_Revenue_Gain_%"] * 0.5).clip(-50, 0).round(1)
    results["Impact_Category"] = pd.cut(results["Vulnerability_Score"], bins=[-100,-10,20,40,60,100],
                                         labels=["Net Beneficiary","Low Impact","Moderate Impact","High Impact","Severe Impact"])
    return results


# ============================================================================
# SIDEBAR  (matching probability app layout)
# ============================================================================
with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center; padding:16px 0; border-bottom:2px solid {GOLD};">
            <div style="font-family:'Playfair Display',serif; font-size:1.3rem; font-weight:900; color:{GOLD};">
                THE MOUNTAIN PATH
            </div>
            <div style="color:{LIGHTBLUE}; font-style:italic; font-size:0.85rem;">World of Finance</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### ⚙️ Scenario Parameters")

    scenario_preset = st.selectbox("Scenario Preset",
        ["Custom","Low Intensity","Base Case","Stress (Hormuz Disruption)","Extreme (Full Blockade)"])

    presets = {"Low Intensity":(10,5,5,3), "Base Case":(25,20,20,6),
               "Stress (Hormuz Disruption)":(60,50,50,9), "Extreme (Full Blockade)":(100,80,80,12)}

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

    st.markdown("---")
    st.markdown("**Prof. V. Ravichandran**")
    st.caption("28+ yrs Corporate Finance & Banking")
    st.caption("Financial Risk Modelling • Quant Finance")


# ============================================================================
# COMPUTE & RENDER
# ============================================================================
brand_banner()

df_base = get_country_data()
results = compute_oil_shock_impact(df_base, oil_chg, gas_chg, hormuz_pct, duration)

page_title("US–Iran Conflict: Global Economic Impact Analyzer",
           "Multi-layer transmission model — Energy Shock → Inflation → Growth → External Sector → Supply Chains")

tabs = st.tabs(["📋 Executive Summary","🌍 Country Impact Matrix","📊 Transmission Channels",
                 "🗺️ Regional Analysis","⛽ Hormuz & Energy","📈 Historical Context","📐 Methodology & Data"])

# ─── TAB 1: EXECUTIVE SUMMARY ───────────────────────────────────────────────
with tabs[0]:
    sum_box(
        f"<b>Scenario: Oil +{oil_chg}% &nbsp;|&nbsp; Gas +{gas_chg}% &nbsp;|&nbsp; "
        f"Hormuz {hormuz_pct}% Disrupted &nbsp;|&nbsp; {duration} months</b><br><br>"
        f"The shock is fundamentally <b style='color:{RED}'>stagflationary for energy-importing economies</b>, "
        f"combining cost-push inflation, demand compression, and external imbalance deterioration. "
        f"Energy exporters experience <b style='color:{GRN}'>conditional gains</b>, "
        f"contingent on uninterrupted supply and geopolitical stability."
    )

    importers = results[results["Net_Oil_Import_Ratio"] > 0.3]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        avg_gdp = importers["GDP_Impact_ppt"].mean()
        st.metric("Avg GDP Hit (Importers)", f"{avg_gdp:.1f} ppt", delta=f"{avg_gdp:.1f}%", delta_color="inverse")
    with c2:
        avg_inf = importers["Inflation_Impact_ppt"].mean()
        st.metric("Avg Inflation Rise", f"+{avg_inf:.1f} ppt", delta=f"+{avg_inf:.1f}%", delta_color="inverse")
    with c3:
        worst = results.loc[results["GDP_Impact_ppt"].idxmin()]
        st.metric("Most Impacted", worst["Country"], delta=f"{worst['GDP_Impact_ppt']:.1f}% GDP", delta_color="inverse")
    with c4:
        best = results.loc[results["GDP_Impact_ppt"].idxmax()]
        st.metric("Largest Beneficiary", best["Country"], delta=f"+{best['GDP_Impact_ppt']:.1f}% GDP")

    section("Impact Classification")
    impact_counts = results["Impact_Category"].value_counts().reset_index()
    impact_counts.columns = ["Category","Count"]
    cmap = {"Net Beneficiary":GRN,"Low Impact":LIGHTBLUE,"Moderate Impact":GOLD,"High Impact":ORANGE,"Severe Impact":RED}
    fig = go.Figure()
    for _, row in impact_counts.iterrows():
        fig.add_trace(go.Bar(x=[row["Category"]], y=[row["Count"]], marker_color=cmap.get(row["Category"],"#888"),
                             text=[row["Count"]], textposition="outside", name=row["Category"]))
    mp_plot_layout(fig, "Country Impact Classification", "Category", "Number of Countries", 380)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    section("Top 10 Most Vulnerable Economies")
    top10 = results.nlargest(10,"Vulnerability_Score")[
        ["Country","Archetype","GDP_Impact_ppt","Inflation_Impact_ppt","FX_Pressure_Score","Vulnerability_Score"]
    ].reset_index(drop=True)
    top10.index += 1
    st.dataframe(top10, use_container_width=True)


# ─── TAB 2: COUNTRY IMPACT MATRIX ───────────────────────────────────────────
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        sel_reg = st.multiselect("Filter by Region", sorted(results["Region"].unique()), default=sorted(results["Region"].unique()))
    with c2:
        sel_arch = st.multiselect("Filter by Archetype", sorted(results["Archetype"].unique()), default=sorted(results["Archetype"].unique()))

    filtered = results[(results["Region"].isin(sel_reg)) & (results["Archetype"].isin(sel_arch))]

    arch_colors = {"Energy Flexible":LIGHTBLUE, "Energy Importer (Advanced)":GOLD,
                   "Emerging Importer (Fragile FX)":RED, "Large Semi-Insulated":PURPLE, "Energy Exporter":GRN}

    fig = go.Figure()
    for arch in filtered["Archetype"].unique():
        sub = filtered[filtered["Archetype"]==arch]
        fig.add_trace(go.Scatter(
            x=sub["GDP_Impact_ppt"], y=sub["Inflation_Impact_ppt"], mode="markers+text",
            marker=dict(size=(sub["GDP_Bn"]/sub["GDP_Bn"].max()*60).clip(8,60),
                        color=arch_colors.get(arch,"#888"), opacity=0.75, line=dict(color=DARKBLUE, width=1)),
            text=sub["Country"], textposition="top center", textfont=dict(size=9, color=DARKBLUE),
            name=arch, hovertemplate="<b>%{text}</b><br>GDP: %{x:.1f}ppt<br>Infl: %{y:.1f}ppt<extra></extra>"
        ))
    mp_plot_layout(fig, "GDP Growth Impact vs Inflation Pass-Through (bubble = GDP size)",
                   "GDP Growth Impact (ppt)", "Inflation Impact (ppt)", 550)
    fig.add_shape(type="line",x0=0,x1=0,y0=-2,y1=filtered["Inflation_Impact_ppt"].max()*1.1,line=dict(color="#ccc",dash="dash",width=1))
    fig.add_shape(type="line",x0=filtered["GDP_Impact_ppt"].min()*1.1,x1=filtered["GDP_Impact_ppt"].max()*1.1,y0=0,y1=0,line=dict(color="#ccc",dash="dash",width=1))
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Full Country Impact Data Table"):
        dcols = ["Country","Region","Archetype","GDP_Growth","New_GDP_Growth_%","GDP_Impact_ppt",
                 "Inflation","New_Inflation_%","Inflation_Impact_ppt","Current_Account","New_CA_%GDP",
                 "CA_Impact_ppt","FX_Pressure_Score","Vulnerability_Score","Impact_Category"]
        st.dataframe(filtered[dcols].sort_values("Vulnerability_Score",ascending=False).reset_index(drop=True), use_container_width=True, height=500)


# ─── TAB 3: TRANSMISSION CHANNELS ───────────────────────────────────────────
with tabs[2]:
    defn_box("FIVE-LAYER TRANSMISSION FRAMEWORK",
             "<b>Layer 1:</b> Energy Price Shock (Oil + Gas + Freight) → "
             "<b>Layer 2:</b> Inflation (Direct + Indirect + Second-Round) → "
             "<b>Layer 3:</b> Real Economy (IP ↓, Consumption ↓, Investment ↓) → "
             "<b>Layer 4:</b> External Sector (CA ↓, FX ↓, Reserves ↓) → "
             "<b>Layer 5:</b> Supply Chain & Shortages (Hormuz chokepoint)")

    selected_country = st.selectbox("Select Country for Deep Dive", results["Country"].tolist(), index=0)
    cd = results[results["Country"]==selected_country].iloc[0]

    energy_hit = -cd["Energy_Cost_Shock_%"]*0.035*min(duration/12,2) if cd["Net_Oil_Import_Ratio"]>0 else cd["Exporter_Revenue_Gain_%"]*0.02
    unc_hit = -0.3*min(duration/12,2)
    inf_hit = -cd["Inflation_Impact_ppt"]*0.08
    hor_hit = -cd["Hormuz_Supply_Shock_%"]*0.04
    total = cd["GDP_Growth"]+energy_hit+unc_hit+inf_hit+hor_hit

    fig = go.Figure(go.Waterfall(
        x=["Baseline GDP","Energy Cost","Uncertainty","Inflation Drag","Hormuz","Net GDP Growth"],
        y=[cd["GDP_Growth"],energy_hit,unc_hit,inf_hit,hor_hit,total],
        measure=["absolute","relative","relative","relative","relative","total"],
        connector=dict(line=dict(color="#ccc",width=1)),
        decreasing=dict(marker=dict(color=RED)), increasing=dict(marker=dict(color=GRN)),
        totals=dict(marker=dict(color=GOLD)),
        textposition="outside",
        text=[f"{v:+.2f}%" for v in [cd["GDP_Growth"],energy_hit,unc_hit,inf_hit,hor_hit,total]],
    ))
    mp_plot_layout(fig, f"{selected_country}: GDP Growth Waterfall — Layer-by-Layer", "", "GDP Growth (%)", 450)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        direct = cd["Energy_Cost_Shock_%"]*0.12 if cd["Net_Oil_Import_Ratio"]>0 else 0
        indirect = cd["Energy_Cost_Shock_%"]*0.08*min(duration/12,2) if cd["Net_Oil_Import_Ratio"]>0 else 0
        second = cd["Energy_Cost_Shock_%"]*0.04*(min(duration/12,2)**0.5) if cd["Net_Oil_Import_Ratio"]>0 else 0
        hormuz_inf = cd["Hormuz_Supply_Shock_%"]*0.15

        fig = go.Figure(go.Pie(
            labels=["Direct (fuel)","Indirect (transport/food)","Second-Round (wages)","Hormuz Supply"],
            values=[max(direct,0.01),max(indirect,0.01),max(second,0.01),max(hormuz_inf,0.01)],
            marker=dict(colors=[RED,ORANGE,GOLD,PURPLE]), hole=0.4
        ))
        mp_plot_layout(fig, f"{selected_country}: Inflation Decomposition", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fx_clr = RED if cd['FX_Pressure_Score']>50 else DARKBLUE
        ex_box(f"COUNTRY SCORECARD — {selected_country}",
               f"<b>Archetype:</b> {cd['Archetype']}<br>"
               f"<b>GDP Growth:</b> {cd['GDP_Growth']:.1f}% → {cd['New_GDP_Growth_%']:.1f}%<br>"
               f"<b>Inflation:</b> {cd['Inflation']:.1f}% → {cd['New_Inflation_%']:.1f}%<br>"
               f"<b>Current Account:</b> {cd['Current_Account']:.1f}% → {cd['New_CA_%GDP']:.1f}%<br>"
               f"<b>FX Pressure:</b> <span style='color:{fx_clr}'>{cd['FX_Pressure_Score']:.0f}/100</span><br>"
               f"<b>Oil Import Dep:</b> {cd['Oil_Import_Dep']:.0f}%<br>"
               f"<b>FX Reserves:</b> ${cd['FX_Reserves_Bn']:.0f}B<br>"
               f"<b>Fiscal Subsidy Cost:</b> +{cd['Fiscal_Cost_Subsidy_%GDP']:.2f}% GDP<br>"
               f"<hr style='border-color:{GOLD}'>"
               f"<b style='font-size:1.1rem'>Vulnerability Score: {cd['Vulnerability_Score']:.0f}</b>")


# ─── TAB 4: REGIONAL ANALYSIS ───────────────────────────────────────────────
with tabs[3]:
    ragg = results.groupby("Region").agg(
        Avg_GDP=("GDP_Impact_ppt","mean"), Avg_Infl=("Inflation_Impact_ppt","mean"),
        Avg_CA=("CA_Impact_ppt","mean"), Avg_FX=("FX_Pressure_Score","mean"),
        GDP_Total=("GDP_Bn","sum"), Avg_Vuln=("Vulnerability_Score","mean"), N=("Country","count")
    ).round(2).sort_values("Avg_Vuln", ascending=False).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=ragg["Region"], y=ragg["Avg_GDP"], name="GDP Impact (ppt)", marker_color=RED))
    fig.add_trace(go.Bar(x=ragg["Region"], y=ragg["Avg_Infl"], name="Inflation Impact (ppt)", marker_color=ORANGE))
    fig.add_trace(go.Bar(x=ragg["Region"], y=ragg["Avg_CA"], name="CA Impact (ppt)", marker_color=LIGHTBLUE))
    mp_plot_layout(fig, "Regional Impact Comparison", "Region", "Impact (ppt)", 450)
    fig.update_layout(barmode="group", xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    aa = results.groupby(["Region","Archetype"]).agg(V=("Vulnerability_Score","mean")).reset_index()
    pv = aa.pivot_table(index="Region", columns="Archetype", values="V", fill_value=0)
    fig = go.Figure(go.Heatmap(
        z=pv.values, x=[c[:25] for c in pv.columns], y=pv.index,
        colorscale=[[0,GRN],[0.3,LIGHTBLUE],[0.6,GOLD],[1.0,RED]],
        text=pv.values.round(1), texttemplate="%{text}", textfont=dict(size=11),
        colorbar=dict(title=dict(text="Vulnerability",font=dict(color=DARKBLUE)), tickfont=dict(color=DARKBLUE))
    ))
    mp_plot_layout(fig, "Vulnerability Heatmap: Region × Archetype", height=400)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Regional Aggregated Data"):
        st.dataframe(ragg, use_container_width=True)


# ─── TAB 5: HORMUZ & ENERGY ─────────────────────────────────────────────────
with tabs[4]:
    hormuz = get_strait_hormuz_data()
    stat_chip_row([("Daily Oil Flow",f"{hormuz['daily_oil_flow_mbpd']} mbpd"),
                   ("% Global Seaborne Oil",f"{hormuz['pct_global_seaborne_oil']}%"),
                   ("% Global LNG",f"{hormuz['pct_global_lng']}%"),
                   ("Bypass Capacity",f"{hormuz['total_bypass_capacity_mbpd']} mbpd")])
    st.markdown("---")

    dlevels = [0,10,20,30,50,70,100]
    sloss = [hormuz["daily_oil_flow_mbpd"]*d/100 for d in dlevels]
    bypassed = [min(s, hormuz["total_bypass_capacity_mbpd"]) for s in sloss]
    nloss = [s-b for s,b in zip(sloss, bypassed)]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=[f"{d}%" for d in dlevels], y=bypassed, name="Bypassed", marker_color=GRN))
    fig.add_trace(go.Bar(x=[f"{d}%" for d in dlevels], y=nloss, name="Net Supply Lost", marker_color=RED))
    mp_plot_layout(fig, "Strait of Hormuz: Disruption vs Bypass Capacity", "Disruption Level","mbpd", 400)
    fig.update_layout(barmode="stack")
    st.plotly_chart(fig, use_container_width=True)

    section("Alternative Pipeline Routes")
    rdf = pd.DataFrame([{"Route":k,"Capacity (mbpd)":v["capacity_mbpd"],"Status":v["status"]} for k,v in hormuz["alternative_routes"].items()])
    st.dataframe(rdf, use_container_width=True, hide_index=True)

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Top Oil Consumers","Top Oil Producers"])
    tc = results.nlargest(12,"Oil_Consumption_mbpd"); tp = results.nlargest(12,"Oil_Production_mbpd")
    fig.add_trace(go.Bar(x=tc["Country"],y=tc["Oil_Consumption_mbpd"],marker_color=RED,name="Consumption"),row=1,col=1)
    fig.add_trace(go.Bar(x=tp["Country"],y=tp["Oil_Production_mbpd"],marker_color=GRN,name="Production"),row=1,col=2)
    mp_plot_layout(fig,"",height=400); fig.update_xaxes(tickangle=-40)
    st.plotly_chart(fig, use_container_width=True)


# ─── TAB 6: HISTORICAL CONTEXT ──────────────────────────────────────────────
with tabs[5]:
    hist = get_historical_oil_shocks(); hv = hist.dropna(subset=["Peak_Oil_Change_%"])

    fig = go.Figure(go.Bar(x=hv["Event"], y=hv["Peak_Oil_Change_%"],
        marker_color=[RED if v>0 else GRN for v in hv["Peak_Oil_Change_%"]],
        text=hv["Peak_Oil_Change_%"].apply(lambda x: f"{x:+.0f}%"), textposition="outside"))
    mp_plot_layout(fig, "Historical Oil Price Shocks — Peak Change (%)","","Peak Change (%)", 420)
    fig.update_xaxes(tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure(go.Scatter(x=hv["Peak_Oil_Change_%"], y=hv["Global_GDP_Impact_%"], mode="markers+text",
        marker=dict(size=hv["Duration_Months"]*2.5, color=GOLD, opacity=0.7, line=dict(color=DARKBLUE, width=1)),
        text=hv["Event"].str.split(" ").str[:2].str.join(" "),
        textposition="top center", textfont=dict(color=DARKBLUE, size=9)))
    mp_plot_layout(fig, "Oil Shock Magnitude vs Global GDP Impact (bubble = duration)",
                   "Peak Oil Price Change (%)","Global GDP Impact (%)", 420)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Historical Oil Shock Episodes"):
        st.dataframe(hist, use_container_width=True, hide_index=True)


# ─── TAB 7: METHODOLOGY & DATA ──────────────────────────────────────────────
with tabs[6]:
    section("A. Multi-Layer Transmission Model")
    defn_box("ECONOMETRIC STRUCTURE",
             "<b>Layer 1 — Energy Shock:</b><br>"
             "Energy_Cost_Shock = Oil_Import_Dep × ΔOil × 0.6 + Oil_Import_Dep × ΔGas × 0.4<br><br>"
             "<b>Layer 2 — Inflation Pass-Through:</b><br>"
             "CPI_t = α + β₁·Oil_t + β₂·FX_t + β₃·OutputGap_t + ε_t<br>"
             "Direct (β≈0.12) + Indirect (β≈0.08 × duration) + Second-round (β≈0.04 × √duration)<br><br>"
             "<b>Layer 3 — GDP Impact:</b><br>"
             "GDP_t = α − γ₁·OilShock_t − γ₂·Inflation_t + γ₃·Investment_t<br><br>"
             "<b>Layer 4 — External Sector:</b><br>"
             "CA deterioration = f(Oil_Import_Dep, ΔOil, Hormuz_exposure)<br>"
             "FX Pressure = f(CA_hit, Reserve_adequacy, FX_regime)<br><br>"
             "<b>Layer 5 — Fiscal:</b><br>"
             "Subsidy_cost_increase = Subsidy_base × ΔOil × 0.5")

    section("B. Country Archetypes")
    ex_box("CLASSIFICATION LOGIC",
           f"• <b style='color:{GOLD}'>Energy Importers (Advanced):</b> Euro Area, Japan, UK — Stagflation<br>"
           f"• <b style='color:{RED}'>Emerging Importers (Fragile FX):</b> India, Turkey, Pakistan — Currency stress<br>"
           f"• <b style='color:{PURPLE}'>Large Semi-Insulated:</b> China — Mixed impact<br>"
           f"• <b style='color:{LIGHTBLUE}'>Energy Flexible:</b> US — Moderate inflation, limited recession risk<br>"
           f"• <b style='color:{GRN}'>Energy Exporters:</b> MENA, Russia, Canada — Conditional gains")

    section("C. Vulnerability Score")
    defn_box("COMPOSITE SCORE (0-100)",
             "GDP Impact (30%) + Inflation (25%) + Current Account (20%) + FX Pressure (15%) + Fiscal (10%)")

    section("D. Data Sources")
    xl_box("DATA SOURCES & ACCESS METHODS",
           "<b>IMF WEO (Apr 2025)</b> — GDP, Inflation, CA Balance, Debt/GDP — <code>imfpy</code><br>"
           "<b>World Bank WDI</b> — GDP (current USD), Population — <code>wbgapi</code><br>"
           "<b>EIA</b> — Oil production/consumption — <code>eia-python</code><br>"
           "<b>BP Statistical Review 2024</b> — Energy mix, Hormuz data<br>"
           "<b>BIS</b> — FX Reserves, Exchange rate regimes<br>"
           "<b>Yahoo Finance</b> — Live oil/gold/FX/equity prices — <code>yfinance</code><br>"
           "<b>FRED</b> — US macro (CPI, PCE, yields) — <code>fredapi</code>")

    section("E. Limitations & Caveats")
    warn_box("IMPORTANT CAVEATS",
             "• Pass-through elasticities calibrated from historical episodes; actual values vary<br>"
             "• Strategic petroleum reserve releases (IEA coordinated) not modeled<br>"
             "• Financial contagion and equity feedback loops simplified<br>"
             "• Sanctions and trade rerouting not explicitly captured<br>"
             "• Linear pass-through assumed; non-linear threshold effects possible in extreme scenarios")


# ============================================================================
# FOOTER
# ============================================================================
footer()
