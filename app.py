import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Spend & Pray | Marketing Attribution",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).parent
orders = pd.read_csv(BASE / "orders.csv", parse_dates=["Order_Date"])
mkt = pd.read_csv(BASE / "marketing_activity.csv", parse_dates=["Activity_Date"])

# ---------------- Theme ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
    background:
      radial-gradient(circle at 84% 8%, rgba(212,160,23,.10), transparent 23%),
      radial-gradient(circle at 8% 80%, rgba(38,59,93,.08), transparent 28%),
      #f7f5f0;
    color: #17202a;
}
.block-container { max-width: 1450px; padding-top: 1.2rem; padding-bottom: 4rem; }
h1,h2,h3 { font-family: 'Playfair Display', serif !important; }

/* sidebar */
section[data-testid="stSidebar"] { background:#14213d; }
section[data-testid="stSidebar"] * { color:#f7f5f0 !important; }
.side-title { font-family:'Playfair Display',serif; font-size:1.65rem; line-height:1.05; margin:4px 0 8px; }
.side-note { color:rgba(255,255,255,.68) !important; font-size:.82rem; line-height:1.55; }
.story-pill { padding:10px 12px; border:1px solid rgba(255,255,255,.12); border-radius:12px; margin:7px 0; font-size:.82rem; }

/* hero */
.hero {
    min-height: 520px; border-radius: 32px; padding: 56px 60px;
    background: linear-gradient(135deg,#14213d 0%,#263b5d 55%,#405a78 100%);
    color: white; position: relative; overflow: hidden;
    box-shadow: 0 25px 70px rgba(20,33,61,.18);
}
.hero:before {
    content:""; position:absolute; width:510px; height:510px; border-radius:50%;
    border:1px solid rgba(255,255,255,.13); right:-135px; top:-145px;
    box-shadow: -40px 40px 0 -39px rgba(255,209,102,.85),
                -78px 78px 0 -77px rgba(255,209,102,.55),
                -116px 116px 0 -115px rgba(255,209,102,.35);
}
.hero:after {
    content:""; position:absolute; width:260px; height:260px; border:1px solid rgba(255,209,102,.24);
    border-radius:50%; right:90px; bottom:-180px;
}
.hero-content { position:relative; z-index:2; max-width:850px; }
.kicker { text-transform:uppercase; letter-spacing:.18em; font-size:.73rem; font-weight:700; opacity:.72; }
.hero h1 { font-size:clamp(3.2rem,7vw,6.8rem); line-height:.92; margin:.3rem 0 1.25rem; color:white; }
.hero p { font-size:1.2rem; line-height:1.7; max-width:760px; color:rgba(255,255,255,.82); }
.question { margin-top:34px; font-family:'Playfair Display',serif; font-size:1.55rem; color:#ffd166; max-width:760px; }

/* layout */
.section { padding: 72px 8px 20px; }
.section-kicker { color:#173F5F; text-transform:uppercase; letter-spacing:.12em; font-size:1.08rem; font-weight:900; border-left:6px solid #C88719; padding-left:13px; line-height:1.1; margin-bottom:8px; }
.section h2 { font-family:'DM Sans',sans-serif !important; font-size:3rem; font-weight:800; letter-spacing:-.035em; margin:.22rem 0 .75rem; color:#101820; }
.section p { color:#394650; font-size:1.06rem; max-width:820px; line-height:1.65; }

.metric {
    background:rgba(255,255,255,.82); border:1px solid rgba(23,32,42,.07);
    border-radius:22px; padding:23px; min-height:132px;
    box-shadow:0 10px 30px rgba(23,32,42,.05);
}
.metric-label { font-size:.82rem; text-transform:uppercase; letter-spacing:.12em; color:#394650; font-weight:800; }
.metric-value { font-family:'DM Sans',sans-serif; font-size:2.75rem; font-weight:800; margin-top:7px; letter-spacing:-.02em; }
.metric-note { color:#7b858e; font-size:.82rem; margin-top:6px; line-height:1.4; }
.insight { border-left:4px solid #d4a017; background:#fffdf7; padding:19px 23px; border-radius:0 18px 18px 0; margin:20px 0; color:#4e5962; line-height:1.6; }
.insight strong { font-family:'DM Sans',sans-serif; font-size:1.18rem; font-weight:800; color:#101820; }
.card { border-radius:24px; padding:27px; background:#fff; border:1px solid #e6e1d7; height:100%; box-shadow:0 8px 24px rgba(23,32,42,.035); }
.card h3 { font-size:1.45rem; margin:.35rem 0 .7rem; }
.card p, .card li { color:#59636d; line-height:1.7; }
.card ul { padding-left:20px; }
.smallcaps { font-size:.69rem; letter-spacing:.12em; text-transform:uppercase; font-weight:700; color:#8a7442; }

/* story rail */
.rail { display:flex; gap:7px; margin:22px 0 4px; align-items:center; }
.rail-step { flex:1; height:7px; background:#dfddd7; border-radius:99px; }
.rail-step.on { background:#d4a017; }
.rail-labels { display:flex; justify-content:space-between; color:#737b82; font-size:.69rem; text-transform:uppercase; letter-spacing:.08em; }

/* funnel */
.funnel-wrap { display:flex; flex-direction:column; align-items:center; gap:5px; margin:28px 0 8px; }
.funnel-step { text-align:center; padding:16px 12px; color:white; font-weight:700; border-radius:12px; box-shadow:0 8px 18px rgba(23,32,42,.08); }
.funnel-small { width:44%; background:#0F766E; }
.funnel-mid { width:58%; background:#173F5F; }
.funnel-wide { width:72%; background:#101820; }
.funnel-missing { width:84%; background:#fffdf7; color:#8a7442; border:2px dashed #d4a017; }

/* ending */
.final { border-radius:30px; padding:48px; background:linear-gradient(135deg,#14213d,#314967); color:white; position:relative; overflow:hidden; }
.final h2 { color:white; font-size:3rem; margin:.35rem 0 1rem; }
.final p { color:rgba(255,255,255,.78); max-width:800px; line-height:1.7; font-size:1.08rem; }
.footer { margin-top:65px; padding:30px; text-align:center; color:#737b82; border-top:1px solid #dedbd4; }

@media (max-width: 800px) {
  .hero { padding:38px 28px; min-height:480px; }
  .section h2 { font-size:2.15rem; }
  .funnel-small,.funnel-mid,.funnel-wide,.funnel-missing { width:92%; }
}
</style>
""", unsafe_allow_html=True)


def money(x):
    return f"${x:,.2f}"


def metric_card(label, value, note):
    return f'''<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>'''

# ---------------- Derived data ----------------
total_revenue = orders["Net_Revenue"].sum()
total_orders = orders["Order_ID"].nunique()
total_spend = mkt["Activity_Cost"].fillna(0).sum()
total_clicks = int(mkt["Clicks"].fillna(0).sum())

monthly = orders.groupby(orders["Order_Date"].dt.to_period("M")).agg(
    Orders=("Order_ID", "nunique"), Revenue=("Net_Revenue", "sum")
).reset_index()
monthly["Month"] = monthly["Order_Date"].dt.strftime("%b")
max_m = monthly.loc[monthly["Orders"].idxmax()]
min_m = monthly.loc[monthly["Orders"].idxmin()]

ch = mkt.groupby("Channel").agg(
    Activities=("Activity_ID", "nunique"), Cost=("Activity_Cost", "sum"),
    Impressions=("Impressions", "sum"), Clicks=("Clicks", "sum")
).reset_index()

paid = mkt[mkt["Channel"].eq("Paid Social")].copy()
paid_imp = int(paid["Impressions"].fillna(0).sum())
paid_clicks = int(paid["Clicks"].fillna(0).sum())
paid_ctr = paid_clicks / paid_imp if paid_imp else 0

# ---------------- Navigation ----------------
st.sidebar.markdown('<div class="side-title">Spend &amp; Pray</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="side-note">Interactive marketing-attribution story · Team 8 · 2025</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
story = st.sidebar.radio(
    "Jump to story",
    [
        "00 · The Question",
        "01 · Sales",
        "02 · Marketing",
        "03 · Timing",
        "04 · Engagement",
        "05 · Attribution Gap",
        "06 · Measure & Improve",
    ],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="side-note"><b>Reading rule</b><br>Timing can show association. It does not prove that a marketing activity caused an order.</div>', unsafe_allow_html=True)

# ---------------- Hero ----------------
st.markdown("""
<div class="hero">
  <div class="hero-content">
    <div class="kicker">Team 8 · Marketing Attribution · 2025</div>
    <h1>Spend &amp; Pray</h1>
    <p>We know what we spent. We know what people clicked. But can we connect those activities to the sales they generated?</p>
    <div class="question">Follow the evidence: sales → marketing → timing → engagement → attribution gap → next step.</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="rail">
  <div class="rail-step on"></div><div class="rail-step on"></div><div class="rail-step on"></div>
  <div class="rail-step on"></div><div class="rail-step on"></div><div class="rail-step on"></div><div class="rail-step on"></div>
</div>
<div class="rail-labels"><span>Question</span><span>Sales</span><span>Marketing</span><span>Timing</span><span>Engagement</span><span>Gap</span><span>Next step</span></div>
""", unsafe_allow_html=True)

# ---------------- Snapshot ----------------
st.markdown('<div class="section" id="snapshot"><div class="section-kicker">The business snapshot</div><h2>What we know.</h2><p>The current-state dataset gives us reliable sales outcomes and separately recorded marketing activity. The important distinction is that these two facts are not directly connected at the order level.</p></div>', unsafe_allow_html=True)
cols = st.columns(4)
metrics = [
    ("Net Revenue", money(total_revenue), "2025 sales outcome"),
    ("Orders", f"{total_orders:,}", "completed online orders"),
    ("Marketing Activity Cost", money(total_spend), "recorded activity cost"),
    ("Paid Social Clicks", f"{total_clicks:,}", "measurable engagement"),
]
for c, (lab, val, note) in zip(cols, metrics):
    c.markdown(metric_card(lab, val, note), unsafe_allow_html=True)

# ---------------- Story 1 ----------------
if story in ["00 · The Question", "01 · Sales"]:
    st.markdown('<div class="section"><div class="section-kicker">01 · Sales</div><h2>Sales move over time.</h2><p>Monthly sales are not constant. October records the highest order count, while June records the lowest.</p></div>', unsafe_allow_html=True)

    # High-contrast monthly sales chart: direct labels, highlighted months, no overlapping callouts.
    fig = go.Figure()
    bar_colors = ["#173F5F" if m not in {max_m["Month"], min_m["Month"]} else ("#C88719" if m == max_m["Month"] else "#0F766E") for m in monthly["Month"]]
    fig.add_trace(go.Bar(
        x=monthly["Month"], y=monthly["Revenue"],
        text=[f"<b>${v:,.0f}</b><br>{int(o):,} orders" for v, o in zip(monthly["Revenue"], monthly["Orders"])],
        textposition="outside",
        textfont=dict(size=14, color="#101820", family="DM Sans"),
        marker=dict(color=bar_colors, line=dict(width=0)),
        customdata=monthly[["Orders"]],
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<br>Orders: %{customdata[0]:,}<extra></extra>",
        cliponaxis=False,
    ))
    fig.update_layout(
        height=555, margin=dict(l=78,r=35,t=70,b=72),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False, bargap=.30,
        font=dict(family="DM Sans", size=15, color="#101820"),
        xaxis_title="Month", yaxis_title="Net revenue (USD)",
    )
    fig.update_xaxes(showgrid=False, tickfont=dict(size=15, color="#101820"), title_font=dict(size=16, color="#101820"), fixedrange=True)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(23,63,95,.14)", zeroline=False,
                     tickprefix="$", tickformat=",.0f", tickfont=dict(size=14, color="#101820"), title_font=dict(size=16, color="#101820"), nticks=6)
    st.plotly_chart(fig, use_container_width=True)

    h1, h2 = st.columns(2)
    with h1:
        st.markdown(f"""<div class=\"metric\" style=\"border-top:5px solid #C88719; min-height:110px;\"><div class=\"metric-label\">Highest monthly orders</div><div class=\"metric-value\" style=\"font-size:2.15rem;\">{int(max_m['Orders']):,}</div><div class=\"metric-note\">{max_m['Month']} · highlighted in gold</div></div>""", unsafe_allow_html=True)
    with h2:
        st.markdown(f"""<div class=\"metric\" style=\"border-top:5px solid #0F766E; min-height:110px;\"><div class=\"metric-label\">Lowest monthly orders</div><div class=\"metric-value\" style=\"font-size:2.15rem;\">{int(min_m['Orders']):,}</div><div class=\"metric-note\">{min_m['Month']} · highlighted in teal</div></div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="insight"><strong>What stands out:</strong> {max_m["Month"]} has the most orders ({int(max_m["Orders"]):,}); {min_m["Month"]} has the fewest ({int(min_m["Orders"]):,}). This gives us a sales timeline to compare against marketing activity.</div>', unsafe_allow_html=True)

# ---------------- Story 2 ----------------
if story in ["00 · The Question", "02 · Marketing"]:
    st.markdown('<div class="section"><div class="section-kicker">02 · Marketing</div><h2>Marketing moves too.</h2><p>The channels operate at very different activity and cost levels. That difference matters before we talk about attribution.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.55, 1])
    with c1:
        ch_plot = ch.copy()
        ch_plot["Cost_Display"] = ch_plot["Cost"].fillna(0)
        fig = go.Figure(go.Bar(
            x=ch_plot["Cost_Display"], y=ch_plot["Channel"], orientation="h",
            text=[money(x) if x > 0 else "N/A" for x in ch_plot["Cost_Display"]], textposition="outside",
            textfont=dict(size=16, color="#101820", family="DM Sans"), cliponaxis=False,
            customdata=ch_plot[["Activities","Clicks"]].fillna(0),
            marker=dict(color=["#173F5F", "#C88719", "#0F766E"], line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>Recorded cost: $%{x:,.2f}<br>Activities: %{customdata[0]:,.0f}<br>Clicks: %{customdata[1]:,.0f}<extra></extra>"
        ))
        fig.update_layout(height=430, margin=dict(l=15,r=95,t=35,b=65), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          xaxis_title="Recorded activity cost (USD)", yaxis_title="Marketing channel", showlegend=False,
                          font=dict(family="DM Sans", size=14, color="#17202a"))
        fig.update_xaxes(showgrid=True, gridcolor="rgba(23,32,42,.10)", zeroline=False, tickprefix="$", tickformat=",.0f",
                         tickfont=dict(size=14, color="#101820"), title_font=dict(size=16, color="#101820"), nticks=5)
        fig.update_yaxes(showgrid=False, categoryorder="array", categoryarray=["Paid Social","Influencer","Offline Event"],
                         tickfont=dict(size=16, color="#101820"), title_font=dict(size=16, color="#101820"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        for _, r in ch.iterrows():
            imp = int(r["Impressions"]) if pd.notna(r["Impressions"]) else 0
            clicks = int(r["Clicks"]) if pd.notna(r["Clicks"]) else 0
            ctr = clicks / imp if imp else None
            cost_text = money(r["Cost"]) if pd.notna(r["Cost"]) else "N/A"
            ctr_text = f"{ctr:.2%} CTR" if ctr is not None else "CTR not applicable"
            st.markdown(metric_card(r["Channel"], f"{int(r['Activities']):,} activities", f"{cost_text} recorded cost · {clicks:,} clicks · {ctr_text}"), unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="insight"><strong>Read carefully:</strong> cost and engagement differ by channel, but those differences do not tell us which channel generated revenue.</div>', unsafe_allow_html=True)

# ---------------- Story 3 ----------------
if story in ["00 · The Question", "03 · Timing"]:
    st.markdown('<div class="section"><div class="section-kicker">03 · Timing</div><h2>Do sales and marketing activity happen together?</h2><p>We can compare dates. We cannot treat that timing as proof that an activity caused a purchase.</p></div>', unsafe_allow_html=True)

    # Use monthly timing so the full year is readable at a glance. Marketing activity is shown as labeled markers.
    monthly_activity = mkt.assign(Month=mkt["Activity_Date"].dt.to_period("M")).groupby("Month").agg(Activities=("Activity_ID","nunique")).reset_index()
    monthly_activity["Month"] = monthly_activity["Month"].dt.strftime("%b")
    timing = monthly[["Month","Revenue","Orders"]].merge(monthly_activity, on="Month", how="left").fillna({"Activities":0})
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timing["Month"], y=timing["Revenue"], mode="lines+markers+text", name="Net revenue",
        text=[f"${v:,.0f}" for v in timing["Revenue"]], textposition="top center",
        textfont=dict(size=13, color="#101820", family="DM Sans"), marker=dict(size=10, color="#173F5F", line=dict(width=2, color="#FFFFFF")), line=dict(width=5, color="#173F5F", shape="spline"),
        customdata=timing[["Orders","Activities"]],
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<br>Orders: %{customdata[0]:,}<br>Marketing activities: %{customdata[1]:,}<extra></extra>"
    ))
    # Label months with activity counts beneath the timeline.
    for _, r in timing.iterrows():
        if r["Activities"] > 0:
            fig.add_annotation(x=r["Month"], y=0, yref="y", text=f"{int(r['Activities'])} activities",
                               showarrow=False, yshift=-28, font=dict(size=12, color="#7a4f00", family="DM Sans"))
    fig.update_layout(
        height=520, margin=dict(l=70,r=35,t=45,b=90), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False, font=dict(family="DM Sans", size=14, color="#17202a"),
        xaxis_title="Month", yaxis_title="Net revenue (USD)"
    )
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linecolor="#101820",
        linewidth=2,
        tickcolor="#101820",
        tickfont=dict(size=16, color="#101820", family="DM Sans"),
        title_font=dict(size=17, color="#101820", family="DM Sans"),
        fixedrange=True
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(23,32,42,.16)",
        gridwidth=1,
        showline=True,
        linecolor="#101820",
        linewidth=2,
        tickcolor="#101820",
        zeroline=False,
        tickprefix="$",
        tickformat=",.0f",
        tickfont=dict(size=16, color="#101820", family="DM Sans"),
        title_font=dict(size=17, color="#101820", family="DM Sans"),
        nticks=6
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight"><strong>Association ≠ Attribution:</strong> a sales spike occurring near a campaign, influencer promotion, or event is a timing relationship. The current-state data does not reliably identify the marketing source of each order.</div>', unsafe_allow_html=True)

# ---------------- Story 4 ----------------
if story in ["00 · The Question", "04 · Engagement"]:
    st.markdown('<div class="section"><div class="section-kicker">04 · Engagement</div><h2>Attention is measurable.</h2><p>Paid Social gives us observable impressions, clicks, cost, and CTR. That tells us about engagement—not which orders it generated.</p></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for c, lab, val, note in [
        (c1, "Impressions", f"{paid_imp:,}", "paid-social deliveries"),
        (c2, "Clicks", f"{paid_clicks:,}", "tracked engagement"),
        (c3, "Overall CTR", f"{paid_ctr:.2%}", "clicks ÷ impressions"),
    ]:
        c.markdown(metric_card(lab, val, note), unsafe_allow_html=True)

    st.markdown("""
    <div class="funnel-wrap">
      <div class="funnel-step funnel-small">193,116 · IMPRESSIONS</div>
      <div>↓</div>
      <div class="funnel-step funnel-mid">3,222 · CLICKS</div>
      <div>↓</div>
      <div class="funnel-step funnel-wide">1.67% · CTR</div>
      <div>↓</div>
      <div class="funnel-step funnel-missing">??? · PURCHASES ATTRIBUTED TO PAID SOCIAL</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="insight"><strong>The missing link:</strong> engagement is observable, but conversion to an order cannot be assigned to Paid Social from this dataset.</div>', unsafe_allow_html=True)

    with st.expander("See the paid-social cost vs. clicks detail", expanded=False):
        fig = go.Figure(go.Scatter(x=paid["Activity_Cost"], y=paid["Clicks"], mode="markers", text=paid["Activity_Name"], marker=dict(size=9, opacity=.68), hovertemplate="<b>%{text}</b><br>Cost: $%{x:.2f}<br>Clicks: %{y:,}<extra></extra>"))
        fig.update_layout(height=360, margin=dict(l=15,r=20,t=20,b=15), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Activity cost", yaxis_title="Clicks", showlegend=False)
        fig.update_xaxes(showgrid=True, gridcolor="rgba(23,32,42,.10)", tickprefix="$", tickformat=",.0f", tickfont=dict(size=14, color="#101820"), title_font=dict(size=16, color="#101820"))
        fig.update_yaxes(showgrid=True, gridcolor="rgba(23,32,42,.10)", tickformat=",.0f", tickfont=dict(size=14, color="#101820"), title_font=dict(size=16, color="#101820"))
        st.plotly_chart(fig, use_container_width=True)

# ---------------- Story 5 ----------------
if story in ["00 · The Question", "05 · Attribution Gap"]:
    st.markdown('<div class="section"><div class="section-kicker">05 · The attribution gap</div><h2>We have the beginning and the end. The connection is missing.</h2><p>The dataset preserves the current-state limitation: orders remain unlinked to a specific marketing channel.</p></div>', unsafe_allow_html=True)

    a, b = st.columns(2)
    with a:
        st.markdown("""
        <div class="card">
          <div class="smallcaps">Measurable now</div>
          <h3>What the data supports</h3>
          <ul>
            <li>Orders and net revenue</li>
            <li>Marketing activity and recorded cost</li>
            <li>Paid-social impressions and clicks</li>
            <li>CTR and CPC where inputs exist</li>
            <li>Sales and activity timing</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.markdown("""
        <div class="card">
          <div class="smallcaps">Not measurable yet</div>
          <h3>What we cannot claim</h3>
          <ul>
            <li>Channel-level conversion</li>
            <li>Attributed revenue by channel</li>
            <li>CAC by channel</li>
            <li>ROAS by channel</li>
            <li>Channel profit or causal sales lift</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="insight"><strong>Bottom line:</strong> the limitation is not a lack of sales data or marketing data. It is the missing traceable connection between a marketing touchpoint and an order.</div>', unsafe_allow_html=True)

# ---------------- Story 6 ----------------
if story in ["00 · The Question", "06 · Measure & Improve"]:
    st.markdown('<div class="section"><div class="section-kicker">06 · Measure & improve</div><h2>Build the missing connection.</h2><p>The next measurement system should connect marketing touchpoints to orders using traceable evidence.</p></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="padding:30px;">
      <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center;">
        <div class="metric" style="min-width:150px;text-align:center;"><div class="metric-label">Marketing</div><div class="metric-value" style="font-size:1.5rem;">Campaign</div></div>
        <div style="font-size:2rem;color:#8a7442;">→</div>
        <div class="metric" style="min-width:150px;text-align:center;"><div class="metric-label">Tracking</div><div class="metric-value" style="font-size:1.5rem;">UTM / QR</div></div>
        <div style="font-size:2rem;color:#8a7442;">→</div>
        <div class="metric" style="min-width:150px;text-align:center;"><div class="metric-label">Customer</div><div class="metric-value" style="font-size:1.5rem;">Order ID</div></div>
        <div style="font-size:2rem;color:#8a7442;">→</div>
        <div class="metric" style="min-width:150px;text-align:center;"><div class="metric-label">Outcome</div><div class="metric-value" style="font-size:1.5rem;">Conversion</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="final" style="margin-top:28px;">
      <div class="kicker">Final takeaway</div>
      <h2>From Spend &amp; Pray → Measure &amp; Improve</h2>
      <p>The current data shows sales and marketing patterns. Better tracking is the missing link needed to accurately connect marketing activity to sales attribution.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer">Spend &amp; Pray · Team 8 · Current-state marketing attribution analysis · Timing comparisons are associative, not causal.</div>', unsafe_allow_html=True)
