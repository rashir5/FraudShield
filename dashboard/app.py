"""
🛡️ FraudShield Enterprise V2 — High-End Fintech Dashboard
Main Streamlit Application Entry Point
"""
import streamlit as st
import time

# ── Page config must be the very first Streamlit call ────────
st.set_page_config(
    page_title="FraudShield Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

_PREMIUM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* ── Root & Typography ──────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: radial-gradient(circle at top left, #1E1B4B 0%, #0F172A 40%, #020617 100%);
    color: #F8FAFC;
}

/* ── Sidebar — High-End Glassmorphism ─────────── */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.8) !important;
    backdrop-filter: blur(20px) saturate(180%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
    color: #A5B4FC !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
}

/* ── Live Ticker Styling ──────────────────────── */
.ticker-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 8px;
    transition: all 0.3s ease;
}
.ticker-card:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateX(4px);
}
.pulse-red {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #EF4444;
    box-shadow: 0 0 0 rgba(239, 68, 68, 0.4);
    animation: pulse 1.5s infinite;
    margin-right: 8px;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

/* ── Metric cards — hover lift ────────────────── */
div[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 1.25rem !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.3s cubic-bezier(.4,0,.2,1) !important;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-8px) scale(1.02) !important;
    background: rgba(255, 255, 255, 0.06) !important;
    border-color: rgba(99, 102, 241, 0.3) !important;
}

/* ── Transitions & Entry ──────────────────────── */
.main .block-container {
    animation: slideUpFade 0.6s cubic-bezier(.4,0,.2,1);
}
@keyframes slideUpFade {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ── Table Styling V2 ─────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
}

/* ── Buttons — vibrant gradient ──────────────── */
.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.5) !important;
}

/* ── Custom Scrollbar ────────────────────────── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.3); border-radius: 10px; }
</style>
"""

def inject_v2_css():
    """Inject V2 high-end Fintech styling."""
    st.html(_PREMIUM_CSS)

@st.fragment(run_every="10s")
def render_sidebar_ticker():
    """Real-time transaction ticker with 10s refresh pulse."""
    st.markdown("---")
    st.markdown("### 📡 Live Engine Feed")
    
    from dashboard.services.api_client import get_transactions
    
    # Try to fetch latest transactions
    res = get_transactions(page=1, page_size=5)
    
    if "error" in res:
        st.caption("⚠️ Feed Offline")
        return

    txns = res.get("transactions", [])
    if not txns:
        st.caption("No incoming traffic...")
        return

    for t in txns:
        is_risk = t.get("is_flagged", False)
        # Using st.html to ensure the stylized ticker cards render perfectly
        st.html(f'''
        <div class="ticker-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.75rem; color: #94A3B8;">{t["timestamp"][11:19]}</span>
                {f'<span class="pulse-red"></span>' if is_risk else ''}
            </div>
            <div style="font-weight: 600; font-size: 0.9rem; margin-top: 4px; color: #F8FAFC;">
                ₹{t["amount"]:,.2f}
            </div>
            <div style="font-size: 0.7rem; color: #64748B;">
                {t["merchant_name"]} • {t["city"]}
            </div>
        </div>
        ''')

def render_hero():
    st.title("🛡️ FraudShield Enterprise V2")
    st.markdown(
        "A sophisticated National Fraud Monitoring System for Indian Banking. "
        "Powered by Rule-Based Heuristics and Gemini AI Analysis."
    )
    st.markdown("---")

def render_status_overview():
    from dashboard.services.api_client import get_transactions
    col1, col2, col3 = st.columns(3)
    
    res = get_transactions(page=1, page_size=1)
    api_ok = "error" not in res
    
    with col1:
        st.metric("System Status", "ONLINE" if api_ok else "OFFLINE", 
                  delta="Connected" if api_ok else "Disconnected", 
                  delta_color="normal" if api_ok else "inverse")
    with col2:
        st.metric("Active Regions", "50 Cities" if api_ok else "0", delta="National Scope")
    with col3:
        total = res.get("total", 0) if api_ok else 0
        st.metric("Historical Data", f"{total:,}", delta="+Batches Available")

def main():
    inject_v2_css()
    render_hero()
    render_status_overview()
    with st.sidebar:
        render_sidebar_ticker()

if __name__ == "__main__":
    main()
