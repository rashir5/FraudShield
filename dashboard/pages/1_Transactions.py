"""
💳 FraudShield — Transaction Monitoring Page V2
Enterprise monitoring grid with AI-powered investigation modals and geospatial context.
"""
import streamlit as st
import pandas as pd
import pydeck as pdk
import sys, os

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dashboard.services.api_client import (
    get_transactions,
    generate_transactions,
    analyze_transaction,
)
from dashboard.services.geo_utils import get_coords

# ── Investigation Dialog ───────────────────────────────────
@st.dialog("🧠 AI Fraud Investigation", width="large")
def show_investigation(txn_id, city_name):
    """Investigation modal with Gemini AI reasoning and Map context."""
    st.caption(f"Transaction ID: {txn_id} • Location: {city_name}")
    
    col_map, col_ai = st.columns([1, 1])
    
    with col_map:
        st.markdown("##### 📍 Geospatial Context")
        coords = get_coords(city_name)
        # Render Pydeck Point Map
        view_state = pdk.ViewState(latitude=coords[0], longitude=coords[1], zoom=10, pitch=45)
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": coords[0], "lon": coords[1], "name": city_name}],
            get_position=["lon", "lat"],
            get_color=[99, 102, 241, 200], # Indigo
            get_radius=1000,
        )
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/dark-v11"))
        st.caption(f"Coordinates: {coords[0]:.4f}, {coords[1]:.4f}")

    with col_ai:
        with st.spinner("Gemini AI is analyzing patterns…"):
            res = analyze_transaction(txn_id)
            
        if "error" in res:
            st.error(f"AI Service unavailable: {res['error']}")
        else:
            st.markdown("##### 🧬 AI Pattern Analysis")
            st.info(res.get("pattern_explanation", "No explanation available."))
            
            st.markdown("##### 🚨 Key Risk Factors")
            st.warning(res.get("top_risk_factors", "None identified."))
            
            st.markdown("##### 💡 Recommendation")
            st.success(res.get("recommendation", "Proceed with caution."))
            
            if res.get("response_time_ms"):
                st.caption(f"Inference: {res['response_time_ms']:.0f}ms")

# ── Sidebar Filters ──────────────────────────────────────────
st.sidebar.markdown("### 🔎 Search Filters")
risk_filter = st.sidebar.selectbox("Risk Level", ["All", "HIGH", "MEDIUM", "LOW"])
_flagged_map = {"All": None, "Flagged Only": True, "Unflagged Only": False}
flagged_filter = st.sidebar.selectbox("Status", list(_flagged_map.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Admin Controls")
gen_count = st.sidebar.number_input("Bulk Generate", min_value=10, max_value=5000, value=100, step=50)
if st.sidebar.button("⚡ Generate Transactions", use_container_width=True):
    with st.spinner("Processing..."):
        res = generate_transactions(gen_count)
        if "error" not in res:
            st.sidebar.success(f"Generated {gen_count} rows")
            st.rerun()

# ── Main Monitoring Grid ─────────────────────────────────────
st.markdown("## 💳 Enterprise Transaction Monitor")
st.markdown("Select a row to launch the deep-AI investigation module.")

data = get_transactions(
    page=1, page_size=100,
    risk_level=risk_filter if risk_filter != "All" else None,
    is_flagged=_flagged_map[flagged_filter]
)

if "error" in data:
    st.error(f"Connectivity Error: {data['error']}")
    st.stop()

txns = data.get("transactions", [])
if not txns:
    st.info("Zero transactions found matching criteria.")
    st.stop()

df = pd.DataFrame(txns)
# Align backend 'city' with frontend 'location' and 'id' with 'txn_id'
rename_cols = {"id": "txn_id", "city": "location"}
df = df.rename(columns={k: v for k, v in rename_cols.items() if k in df.columns})

# Define preferred enterprise columns
preferred = ["txn_id", "timestamp", "amount", "account_holder", "merchant_name", "location", "is_flagged"]
# Only select columns that actually exist to avoid KeyError
available_cols = [c for c in preferred if c in df.columns]
display_df = df[available_cols].copy()

# Add a simpler 'Investigation' selection
event = st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
        "is_flagged": st.column_config.CheckboxColumn("Flagged"),
        "timestamp": st.column_config.DatetimeColumn("Created At"),
        "txn_id": "ID",
        "location": "City"
    }
)

# Handle selection event
if event and event["selection"]["rows"]:
    selected_idx = event["selection"]["rows"][0]
    row = display_df.iloc[selected_idx]
    # Ensure txn_id exists for modal
    t_id = row.get("txn_id", "")
    t_loc = row.get("location", "Unknown")
    show_investigation(t_id, t_loc)
