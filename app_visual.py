import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import plotly.graph_objects as go
from data_loader import load_and_consolidate, CSV_DASHBOARD_PATH
from train_model import select_features, MODEL_PATH

FEATURES_PATH = "model_features.json"

st.set_page_config(
    page_title="Camp Nou Dynamic Pricing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── OPTIMIZED CSS (FCB THEME + GLASSMORPHISM) ────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #004d98 0%, #a50044 100%);
        color: white;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #ffed00;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }
    
    h1, h2, h3 {
        color: white !important;
    }
    
    .stButton>button {
        background-color: #ffed00 !important;
        color: #004d98 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        transition: transform 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────

@st.cache_resource
def load_assets():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(FEATURES_PATH):
        return None, None
    model = joblib.load(MODEL_PATH)
    with open(FEATURES_PATH, "r") as f:
        features = json.load(f)
    return model, features

def run_optimization(model, features, context_row, price_range):
    base_p = float(context_row["base_price"])
    horizon = float(context_row["horizon_days"])
    
    # Calcular coeficiente de elasticidad dinámico basado en las condiciones
    occ = float(context_row.get('occupancy_rate', 0.5))
    days = float(context_row.get('days_to_match', 30))
    
    # E base: 2.5 (Demanda muy elástica). 
    # A mayor ocupación, menor elasticidad (más rígido, la gente paga más).
    E = 2.8 - (occ * 1.8)
    if days < 7:
        E -= 0.5 # Cerca del partido, los fans están más desesperados (inelástico)
        
    E = max(0.1, E) # Seguridad matemática
    
    sweep_results = []
    for price in price_range:
        temp_row = context_row.copy()
        temp_row["current_price"] = price
        temp_row["price_vs_base"] = price / base_p
        
        input_df = pd.DataFrame([temp_row])
        X = select_features(input_df)
        X = X.reindex(columns=features, fill_value=0)
        
        # 1. Obtenemos la tasa base general que predice el AI
        base_rate = max(0, model.predict(X)[0])
        
        # 2. Inyectamos la Elasticidad Dinámica
        price_ratio = price / base_p
        elasticity_factor = 1.0 - (price_ratio - 1.0) * E 
        
        # 3. Calculamos la tasa final
        rate = max(0, base_rate * elasticity_factor)
        
        q = rate * horizon
        rev = price * q
        
        sweep_results.append({
            "Price": price,
            "SalesRate": rate,
            "Revenue": rev,
            "Demand": q
        })
    return pd.DataFrame(sweep_results)

# ─── SIDEBAR (CONTROL PANEL) ──────────────────────────────────────────────────

with st.sidebar:
    st.image("https://www.fcbarcelona.com/fcbarcelona/photo/2018/10/01/21626601-26dd-4d7a-ba92-70b12bc85496/FCB_Logo.png", width=100)
    st.title("Admin Console")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Actualizar Template (CSV)", type=["csv"])
    
    st.subheader("Model Settings")
    auto_refresh = st.checkbox("Live Optimization", value=True)
    confidence_threshold = st.slider("Confidence Buffer", 0.0, 0.2, 0.05)

# ─── MAIN CONTENT ──────────────────────────────────────────────────────────────

st.title("📊 Camp Nou: Dynamic Pricing Dashboard")
st.markdown("Real-time revenue optimization engine for FC Barcelona Matchday tickets.")

model, model_features = load_assets()

if not model or not model_features:
    st.error("Model assets not found. Please run the training pipeline first.")
    st.stop()

# Data Loading
df = load_and_consolidate(CSV_DASHBOARD_PATH) if not uploaded_file else pd.read_csv(uploaded_file, sep=";")

if df is not None:
    # Match Selector logic
    if "match_name" not in df.columns:
        df["match_name"] = "FC Barcelona vs " + df["opponent"].astype(str)
    
    selected_sector = st.selectbox("Select Sector Context", df["sector_name"].unique())
    row = df[df["sector_name"] == selected_sector].iloc[0].copy()

    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Base Price", f"€{row['base_price']:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_m2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("Match Context")
        st.write(f"**Opponent:** {row['opponent']}")
        st.write(f"**Ranking:** {row['opponent_ranking']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_m3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("Current State")
        st.write(f"**Days to Match:** {row['days_to_match']}")
        st.write(f"**Occupancy:** {row['occupancy_rate']*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    # Sliders for real-time simulation
    st.markdown("---")
    st.subheader("Simulate Market Conditions")
    c1, c2, c3 = st.columns(3)
    sim_days = c1.slider("Days to Match", 0, 180, int(row['days_to_match']))
    sim_occ = c2.slider("Simulated Occupancy", 0.0, 1.0, float(row['occupancy_rate']))
    sim_vel = c3.slider("Sales Velocity", 0.0, 1.0, float(row.get('sales_velocity', 0.1)))

    row['days_to_match'] = sim_days
    row['occupancy_rate'] = sim_occ
    row['sales_velocity'] = sim_vel

    # Run Optimization Sweep
    price_range = np.linspace(float(row['base_price']) * 0.5, float(row['base_price']) * 1.5, 40)
    sweep_df = run_optimization(model, model_features, row, price_range)
    
    optimal_row = sweep_df.loc[sweep_df["Revenue"].idxmax()]
    current_price = float(row.get("current_price", row["base_price"]))
    
    # ─── RESULTS METRICS ───
    st.markdown("---")
    res_c1, res_c2, res_c3, res_c4 = st.columns(4)
    res_c1.metric("Optimal Price", f"€{optimal_row['Price']:.2f}", 
                  f"{((optimal_row['Price']/row['base_price'])-1)*100:+.1f}% vs Base")
    res_c2.metric("Projected Revenue", f"€{optimal_row['Revenue']:,.2f}")
    res_c3.metric("Projected Sales Rate", f"{optimal_row['SalesRate']:.2f} tix/day")
    res_c4.metric("Total Projected Demand", f"{optimal_row['Demand']:.0f} units")

    # ─── CHARTS (PLOTLY) ───
    st.markdown("### Optimization Analytics")
    chart_c1, chart_c2 = st.columns(2)
    
    # Revenue Chart
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(x=sweep_df["Price"], y=sweep_df["Revenue"], 
                                mode='lines+markers', name='Projected Revenue',
                                line=dict(color='#ffed00', width=3)))
    fig_rev.add_vline(x=optimal_row["Price"], line_dash="dash", line_color="white", 
                      annotation_text="Optimal Price")
    fig_rev.update_layout(title="Revenue vs Price Curve", 
                          xaxis_title="Simulation Price (€)", 
                          yaxis_title="Expected Revenue (€)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font=dict(color="white"))
    chart_c1.plotly_chart(fig_rev, use_container_width=True)

    # Sales Rate Chart
    fig_rate = go.Figure()
    fig_rate.add_trace(go.Scatter(x=sweep_df["Price"], y=sweep_df["SalesRate"], 
                                 line=dict(color='#00ff00', dash='dot'), 
                                 name='Sales Rate'))
    fig_rate.update_layout(title="Predicted Sales Rate Decay", 
                           xaxis_title="Simulation Price (€)", 
                           yaxis_title="Expected Sales Rate (units/day)",
                           paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font=dict(color="white"))
    chart_c2.plotly_chart(fig_rate, use_container_width=True)

    st.markdown("---")
    with st.expander("Show Raw Optimization Table"):
        st.dataframe(sweep_df.style.highlight_max(axis=0, subset=['Revenue']))
else:
    st.info("Please load a data file or template to begin analysis.")
