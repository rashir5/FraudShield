"""
📊 FraudShield — Analytics Dashboard V2
Enterprise analytics featuring 50-city national fraud heatmap and high-density KPI grids.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import pandas as pd
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dashboard.services.api_client import get_analytics
from dashboard.services.geo_utils import get_coords

# ── Plotly Theme Defaults ───────────────────────────────
_PLC_THEME = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94A3B8", family="Inter"),
    margin=dict(l=10, r=10, t=30, b=10),
)

st.title("📊 National Fraud Analytics")
st.markdown("Providing visibility across 50+ regions in the Indian banking network.")

with st.spinner("Compiling national data…"):
    analytics = get_analytics()

if "error" in analytics:
    st.error(f"⚠️ Service unavailable: {analytics['error']}")
    st.stop()

# ── Data Extraction ──────────────────────────────────────────
risk_dist = analytics.get("risk_distribution", [])
fraud_trends = analytics.get("fraud_trends", [])
category_data = analytics.get("category_breakdown", [])
merchant_data = analytics.get("top_flagged_merchants", [])
geo_data = analytics.get("geo_distribution", [])

# ── KPI Section ──────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
total_txns = sum(r.get("count", 0) for r in risk_dist)
flagged_txns = sum(r.get("count", 0) for r in risk_dist if r.get("risk_level") in ("MEDIUM", "HIGH"))
fraud_rate = (flagged_txns / total_txns * 100) if total_txns else 0

col1.metric("National Volume", f"{total_txns:,}", delta="Real-time")
col2.metric("Flagged Activity", f"{flagged_txns:,}", delta=f"{fraud_rate:.1f}% Rate", delta_color="inverse")
col3.metric("Monitored Cities", f"{len(geo_data)}", delta="Full Coverage")
avg_scores = [c.get("average_risk_score", 0) for c in category_data]
col4.metric("Network Risk Index", f"{(sum(avg_scores)/len(avg_scores)):.1f}" if avg_scores else "0.0")

st.markdown("---")

# ── Geospatial Heatmap Row ──────────────────────────────────
st.markdown("### 🗺️ National Fraud Density Heatmap")
if geo_data:
    # Prepare data for pydeck
    map_points = []
    for g in geo_data:
        coords = get_coords(g["city"])
        map_points.append({
            "city": g["city"],
            "lat": coords[0],
            "lon": coords[1],
            "weight": g["flagged_count"]
        })
    map_df = pd.DataFrame(map_points)
    
    view_state = pdk.ViewState(latitude=20.5937, longitude=78.9629, zoom=4, pitch=30)
    
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=map_df,
        get_position=["lon", "lat"],
        get_weight="weight",
        radius_pixels=60,
        intensity=1,
        threshold=0.05,
        color_range=[
            [67, 56, 202, 50],   # Indigo light
            [79, 70, 229, 100],
            [99, 102, 241, 150],
            [139, 92, 246, 200], # Purple
            [167, 139, 250, 240],
            [239, 68, 68, 255]    # Red hot
        ]
    )
    
    st.pydeck_chart(pdk.Deck(
        layers=[heatmap_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v11",
        tooltip={"text": "{city}: {weight} flagged transactions"}
    ))
else:
    st.info("Insufficient geographic data for heatmap.")

st.markdown("---")

# ── Trend & Merchant Row ────────────────────────────────────
chart_1, chart_2 = st.columns(2)

with chart_1:
    st.markdown("##### 📈 Daily Network Pulse")
    if fraud_trends:
        dates = [f["period"] for f in fraud_trends]
        totals = [f["total_transactions"] for f in fraud_trends]
        flagged = [f["flagged_count"] for f in fraud_trends]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=totals, name="Volume", line=dict(color="#6366F1", width=3)))
        fig.add_trace(go.Scatter(x=dates, y=flagged, name="Flagged", fill="tozeroy", line=dict(color="#EF4444", width=2, dash="dot")))
        fig.update_layout(**_PLC_THEME, legend=dict(orientation="h", x=0, y=1.2))
        st.plotly_chart(fig, use_container_width=True)

with chart_2:
    st.markdown("##### 🏪 High-Risk Merchant Exposure")
    if merchant_data:
        names = [m["merchant_name"] for m in merchant_data]
        counts = [m["flagged_count"] for m in merchant_data]
        scores = [m["average_risk_score"] for m in merchant_data]
        
        fig = px.bar(x=counts, y=names, orientation="h", color=scores, 
                     color_continuous_scale=["#6366F1", "#F59E0B", "#EF4444"])
        fig.update_layout(**_PLC_THEME, coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
