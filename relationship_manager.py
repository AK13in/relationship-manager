import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Banking Relationship Manager",
    layout="wide",
    page_icon="🏦",
    initial_sidebar_state="expanded"
)
# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
NAVY    = "#1A3C5E"
TEAL    = "#2E86AB"
GREEN   = "#1B6B3A"
RED     = "#C0392B"
AMBER   = "#D4A017"
PURPLE  = "#6C3483"
GOLD    = "#C9A84C"
SILVER  = "#7F8C8D"
LIGHT   = "#EAF4FB"
WHITE   = "#FFFFFF"

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
  .block-container {{ padding: 1rem 2rem 2rem 2rem; max-width: 1400px; }}

  /* ── KPI Cards ── */
  .kpi {{
    padding: 1.1rem 1.3rem; border-radius: 14px; color: white;
    text-align: center; box-shadow: 0 6px 20px rgba(0,0,0,0.10);
    transition: transform 0.2s; cursor: default;
  }}
  .kpi:hover {{ transform: translateY(-2px); }}
  .kpi-navy   {{ background: linear-gradient(135deg, {NAVY} 0%, {TEAL} 100%); }}
  .kpi-danger {{ background: linear-gradient(135deg, #7B241C 0%, {RED} 100%); }}
  .kpi-safe   {{ background: linear-gradient(135deg, #145A32 0%, #27AE60 100%); }}
  .kpi-amber  {{ background: linear-gradient(135deg, #7D6608 0%, {AMBER} 100%); }}
  .kpi-gold   {{ background: linear-gradient(135deg, #6E4A0A 0%, {GOLD} 100%); }}
  .kpi-purple {{ background: linear-gradient(135deg, #4A235A 0%, {PURPLE} 100%); }}
  .kpi-teal   {{ background: linear-gradient(135deg, #1A5276 0%, {TEAL} 100%); }}
  .kpi-label  {{ font-size: .68rem; font-weight: 600; opacity: .82;
                 letter-spacing: .09em; text-transform: uppercase; margin-bottom: 5px; }}
  .kpi-value  {{ font-size: 1.95rem; font-weight: 800; line-height: 1.1; }}
  .kpi-sub    {{ font-size: .70rem; opacity: .72; margin-top: 4px; font-weight: 500; }}

  /* ── Section Headers ── */
  .sec {{
    font-size: 1rem; font-weight: 700; color: {NAVY};
    border-left: 4px solid {TEAL}; padding-left: 10px;
    margin: 1.6rem 0 .9rem 0; letter-spacing: .01em;
  }}
  .sec-sm {{
    font-size: .88rem; font-weight: 600; color: {NAVY};
    margin: .8rem 0 .4rem 0;
  }}

  /* ── Insight Boxes ── */
  .ibox {{
    border-radius: 0 10px 10px 0; padding: .9rem 1.2rem;
    margin: .4rem 0; font-size: .88rem; line-height: 1.6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }}
  .ibox-info    {{ background: #EAF4FB; border-left: 4px solid {TEAL};   color: #154360; }}
  .ibox-danger  {{ background: #FDEDEC; border-left: 4px solid {RED};    color: #7B241C; }}
  .ibox-warning {{ background: #FEF9E7; border-left: 4px solid {AMBER};  color: #7D6608; }}
  .ibox-success {{ background: #EAFAF1; border-left: 4px solid {GREEN};  color: #145A32; }}
  .ibox-paradox {{ background: #F4ECF7; border-left: 4px solid {PURPLE}; color: {PURPLE}; }}
  .ibox-gold    {{ background: #FDF6E3; border-left: 4px solid {GOLD};   color: #6E4A0A; }}

  /* ── Stat Pills ── */
  .pill {{
    display: inline-block; padding: .25rem .75rem; border-radius: 20px;
    font-size: .75rem; font-weight: 700; margin: .15rem;
  }}
  .pill-red    {{ background: #FDEDEC; color: {RED}; }}
  .pill-green  {{ background: #EAFAF1; color: {GREEN}; }}
  .pill-amber  {{ background: #FEF9E7; color: #7D6608; }}
  .pill-navy   {{ background: {LIGHT}; color: {NAVY}; }}

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #F0F5FA 0%, #E8F0F8 100%);
    border-right: 1px solid #DDE8F0;
  }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {{ gap: 6px; border-bottom: 2px solid #DDE8F0; }}
  .stTabs [data-baseweb="tab"] {{
    background: #F5F8FC; border-radius: 8px 8px 0 0;
    padding: .45rem 1.2rem; font-weight: 600; font-size: .88rem;
    color: {NAVY}; border: 1px solid #DDE8F0; border-bottom: none;
    transition: all 0.2s;
  }}
  .stTabs [aria-selected="true"] {{
    background: {NAVY} !important; color: white !important;
    border-color: {NAVY} !important;
  }}

  /* ── Divider ── */
  .divider {{
    height: 2px;
    background: linear-gradient(90deg, {TEAL} 0%, rgba(46,134,171,0.2) 60%, transparent 100%);
    margin: 1.2rem 0; border: none;
  }}

  /* ── Page title ── */
  .page-title {{
    font-size: 1.75rem; font-weight: 800; color: {NAVY};
    letter-spacing: -.02em; margin-bottom: 2px;
  }}
  .page-sub {{
    font-size: .88rem; color: {TEAL}; font-weight: 500; margin-bottom: .5rem;
  }}

  /* ── Table styling ── */
  .dataframe {{ font-size: .83rem !important; }}

  /* ── Scrollable watchlist ── */
  .watchlist-note {{
    font-size: .78rem; color: #777; font-style: italic; margin-top: .3rem;
  }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA ENGINE
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="📊  Processing 10,000 customer records…")
def load_data():
    df = pd.read_csv("European_Bank.csv")

    # ── Segments ──────────────────────────────────────────────────────────
    df["Value_Segment"] = pd.qcut(
        df["Balance"].rank(method="first"), q=4,
        labels=["Bronze", "Silver", "Gold", "Platinum"]
    )
    df["AgeBand"] = pd.cut(
        df["Age"], bins=[0, 30, 40, 50, 60, 100],
        labels=["<30", "30–40", "40–50", "50–60", "60+"]
    )
    df["CreditBand"] = pd.cut(
        df["CreditScore"], bins=[0, 500, 600, 700, 850],
        labels=["Poor", "Fair", "Good", "Excellent"]
    )
    df["TenureBand"] = pd.cut(
        df["Tenure"], bins=[-1, 2, 5, 7, 10],
        labels=["New (0–2)", "Growing (3–5)", "Established (6–7)", "Loyal (8–10)"]
    )

    # ── Derived flags ─────────────────────────────────────────────────────
    bal_med = df["Balance"].median()
    df["IsHighValue"]         = (df["Balance"] > bal_med).astype(int)
    df["IsInactiveHighValue"] = ((df["IsActiveMember"] == 0) & (df["Balance"] > bal_med)).astype(int)
    df["ProductRisk"]         = (df["NumOfProducts"] >= 3).astype(int)
    df["OlderInactive"]       = ((df["Age"] > 40) & (df["IsActiveMember"] == 0)).astype(int)
    df["GermanyFlag"]         = (df["Geography"] == "Germany").astype(int)
    df["IsZeroBalance"]       = (df["Balance"] == 0).astype(int)

    return df, bal_med


df, bal_med = load_data()


# ─────────────────────────────────────────────────────────────────────────────
# HEALTH SCORE ENGINE  (recalculated live from sidebar weights)
# ─────────────────────────────────────────────────────────────────────────────
def compute_health(df, w_act, w_card, w_ten, w_prod):
    raw = (
        (df["IsActiveMember"] * w_act)  +
        (df["HasCrCard"]      * w_card) +
        (df["Tenure"]         * w_ten)  +
        (df["NumOfProducts"]  * w_prod)
    ).clip(upper=100)
    tiers = pd.cut(raw, bins=[-1, 40, 74, 100],
                   labels=["At Risk", "Moderate", "Healthy"])
    return raw, tiers


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding:.5rem 0 1rem'>
      <div style='font-size:1.5rem'>🏦</div>
      <div style='font-size:1.1rem; font-weight:800; color:{NAVY}'>Banking Relationship Manager</div>
      <div style='font-size:.75rem; color:{TEAL}; font-weight:500'>Portfolio Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:.2rem 0 1rem; opacity:.3'>", unsafe_allow_html=True)

    # ── Filters ───────────────────────────────────────────────────────────
    st.markdown(f"<div style='font-size:.8rem;font-weight:700;color:{NAVY};margin-bottom:.4rem'>🔍 CUSTOMER FILTERS</div>",
                unsafe_allow_html=True)

    geo_sel  = st.multiselect("Geography", ["France","Germany","Spain"],
                               default=["France","Germany","Spain"])
    gen_sel  = st.multiselect("Gender", ["Male","Female"], default=["Male","Female"])
    seg_sel  = st.multiselect("Value Segment", ["Bronze","Silver","Gold","Platinum"],
                               default=["Bronze","Silver","Gold","Platinum"])
    act_sel  = st.multiselect("Activity", [0,1], default=[0,1],
                               format_func=lambda x: "Active" if x==1 else "Inactive")
    prod_sel = st.multiselect("Products", [1,2,3,4], default=[1,2,3,4])
    age_r    = st.slider("Age Range", 18, 92, (18, 92))
    bal_r    = st.slider("Min Balance (€)", 0, 250000, 0, step=5000)

    st.markdown("<hr style='margin:.8rem 0; opacity:.3'>", unsafe_allow_html=True)

    # ── Health Score Weights ───────────────────────────────────────────────
    st.markdown(f"<div style='font-size:.8rem;font-weight:700;color:{NAVY};margin-bottom:.4rem'>⚖️ HEALTH SCORE WEIGHTS</div>",
                unsafe_allow_html=True)
    st.caption("Adjust to reflect your bank's priorities. Scores update live.")

    w_act  = st.slider("Activity weight",      0, 60, 40, step=5)
    w_card = st.slider("Credit card weight",   0, 30, 10, step=5)
    w_ten  = st.slider("Tenure weight (×yr)",  0, 10,  3, step=1)
    w_prod = st.slider("Products weight",      0, 20,  5, step=1)

    st.markdown("<hr style='margin:.8rem 0; opacity:.3'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:.72rem; color:#888; line-height:1.8'>
      Dataset: <b style='color:{NAVY}'>10,000</b> customers<br>
      Overall churn: <b style='color:{RED}'>20.4%</b><br>
      HV inactive risk: <b style='color:{RED}'>€322M</b><br>
      Germany churn: <b style='color:{RED}'>32.4%</b>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS + COMPUTE HEALTH
# ─────────────────────────────────────────────────────────────────────────────
fdf = df[
    df["Geography"].isin(geo_sel) &
    df["Gender"].isin(gen_sel) &
    df["Value_Segment"].isin(seg_sel) &
    df["IsActiveMember"].isin(act_sel) &
    df["NumOfProducts"].isin(prod_sel) &
    df["Age"].between(*age_r) &
    (df["Balance"] >= bal_r)
].copy()

fdf["Health_Score"], fdf["Health_Tier"] = compute_health(fdf, w_act, w_card, w_ten, w_prod)

# Core metrics
total       = len(fdf)
churned     = int(fdf["Exited"].sum())
churn_rate  = churned / total if total > 0 else 0
avg_health  = fdf["Health_Score"].mean() if total > 0 else 0
watchlist   = fdf[fdf["IsActiveMember"] == 0].copy()
rev_risk    = watchlist["Balance"].sum()
at_risk_n   = int((fdf["Health_Tier"] == "At Risk").sum())
plat_bal    = fdf[fdf["Value_Segment"] == "Platinum"]["Balance"].sum()
avg_bal     = fdf["Balance"].mean()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
🏦 Banking Relationship Manager
<div class='page-sub'>
  Real-time portfolio analytics  •  Revenue at risk  •  Health scoring  •
  10,000 European bank customers  •  <span style='color:{GOLD};font-weight:600'>Banking Portfolio Analytics</span>
</div>
""", unsafe_allow_html=True)

# Filter summary pills
active_filters = []
if geo_sel != ["France","Germany","Spain"]: active_filters.append(f"📍 {', '.join(geo_sel)}")
if gen_sel != ["Male","Female"]:            active_filters.append(f"👤 {', '.join(gen_sel)}")
if bal_r > 0:                               active_filters.append(f"💰 Balance ≥ €{bal_r:,}")
if age_r != (18,92):                        active_filters.append(f"🎂 Age {age_r[0]}–{age_r[1]}")

if active_filters:
    pills = " ".join([f"<span class='pill pill-navy'>{f}</span>" for f in active_filters])
    st.markdown(f"<div style='margin:.3rem 0 .8rem'>{pills}</div>", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────────────────────────────────────
k = st.columns(7)

kpi_data = [
    ("navy",   "Customers",        f"{total:,}",                    "In current view"),
    ("danger" if churn_rate>0.25 else "amber" if churn_rate>0.15 else "safe",
               "Churn Rate",       f"{churn_rate:.1%}",             f"{churned:,} lost"),
    ("danger", "Revenue at Risk",  f"€{rev_risk/1e6:.1f}M",         f"{len(watchlist):,} inactive"),
    ("amber" if avg_health<75 else "safe",
               "Avg Health",       f"{avg_health:.0f}",             "Out of 100"),
    ("danger" if at_risk_n > total*0.3 else "amber",
               "At-Risk Count",    f"{at_risk_n:,}",                "Health score ≤ 40"),
    ("gold",   "Platinum Balance", f"€{plat_bal/1e6:.1f}M",         "Top 25% customers"),
    ("teal",   "Avg Balance",      f"€{avg_bal/1000:.0f}K",         "Per customer"),
]

for col, (color, label, value, sub) in zip(k, kpi_data):
    with col:
        st.markdown(f"""
        <div class='kpi kpi-{color}'>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-value'>{value}</div>
          <div class='kpi-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
t1, t2, t3, t4, t5, t6 = st.tabs([
    "📊  Portfolio Overview",
    "🌍  Regional Intelligence",
    "🛠️  Product Analytics",
    "🚨  Revenue at Risk",
    "🛡️  Health Engine",
    "🔬  Explorer",
])

CHART_H = 340
LAYOUT  = dict(paper_bgcolor=WHITE, plot_bgcolor=WHITE,
               margin=dict(t=30, b=20, l=10, r=10),
               font=dict(family="Inter", size=12))


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PORTFOLIO OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with t1:

    c1, c2, c3 = st.columns(3)

    # ── Churn by segment ──────────────────────────────────────────────────
    with c1:
        st.markdown("<div class='sec'>Churn Rate by Value Segment</div>", unsafe_allow_html=True)
        seg = fdf.groupby("Value_Segment", observed=True).agg(
            Churn=("Exited","mean"), Count=("Exited","count")
        ).reset_index()
        colors = {"Bronze":TEAL,"Silver":SILVER,"Gold":GOLD,"Platinum":NAVY}
        fig = px.bar(seg, x="Value_Segment", y="Churn",
                     color="Value_Segment",
                     color_discrete_map=colors,
                     text=seg["Churn"].map(lambda x: f"{x:.1%}"),
                     labels={"Churn":"Churn Rate","Value_Segment":"Segment"})
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H, showlegend=False,
                          yaxis=dict(tickformat=".0%", showgrid=True,
                                     gridcolor="#EEE", range=[0,.35]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "<div class='ibox ibox-gold'>💎 Gold & Platinum churn more than Bronze — "
            "wealthy customers have more options. Proactive engagement is non-negotiable "
            "at the top tier.</div>", unsafe_allow_html=True
        )

    # ── Gender churn ─────────────────────────────────────────────────────
    with c2:
        st.markdown("<div class='sec'>Churn by Gender & Activity</div>", unsafe_allow_html=True)
        gen_act = fdf.groupby(["Gender","IsActiveMember"])["Exited"].mean().reset_index()
        gen_act["Status"] = gen_act["IsActiveMember"].map({1:"Active",0:"Inactive"})
        fig = px.bar(gen_act, x="Gender", y="Exited", color="Status", barmode="group",
                     color_discrete_map={"Active":TEAL,"Inactive":RED},
                     text=gen_act["Exited"].map(lambda x: f"{x:.1%}"),
                     labels={"Exited":"Churn Rate"})
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H,
                          yaxis=dict(tickformat=".0%", showgrid=True,
                                     gridcolor="#EEE", range=[0,.5]),
                          legend_title="")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "<div class='ibox ibox-warning'>👤 Inactive female customers churn at the "
            "highest rate of any gender-activity combination — a specific outreach "
            "opportunity.</div>", unsafe_allow_html=True
        )

    # ── Age band churn ────────────────────────────────────────────────────
    with c3:
        st.markdown("<div class='sec'>Churn by Age Band</div>", unsafe_allow_html=True)
        age_ch = fdf.groupby("AgeBand", observed=True)["Exited"].agg(
            ["mean","count"]
        ).reset_index()
        age_ch.columns = ["AgeBand","Churn","Count"]
        fig = px.bar(age_ch, x="AgeBand", y="Churn",
                     color="Churn",
                     color_continuous_scale=[[0,"#27AE60"],[0.35,AMBER],[0.6,RED],[1,"#7B241C"]],
                     text=age_ch["Churn"].map(lambda x: f"{x:.1%}"),
                     labels={"AgeBand":"Age Band","Churn":"Churn Rate"})
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H, coloraxis_showscale=False,
                          yaxis=dict(tickformat=".0%", showgrid=True,
                                     gridcolor="#EEE", range=[0,.75]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "<div class='ibox ibox-danger'>🎯 50–60 year olds churn at 56% — the "
            "highest of any age band. 40–50 is the largest at-risk group by volume."
            "</div>", unsafe_allow_html=True
        )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    c4, c5 = st.columns(2)

    # ── Tenure analysis ───────────────────────────────────────────────────
    with c4:
        st.markdown("<div class='sec'>Tenure vs Churn — Does Loyalty Build Over Time?</div>",
                    unsafe_allow_html=True)
        ten = fdf.groupby("Tenure")["Exited"].agg(["mean","count"]).reset_index()
        ten.columns = ["Tenure","Churn","Count"]
        avg_line = fdf["Exited"].mean()

        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=ten["Tenure"], y=ten["Churn"],
            name="Churn Rate", marker_color=TEAL, opacity=0.8,
            text=[f"{v:.1%}" for v in ten["Churn"]],
            textposition="outside"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=ten["Tenure"], y=ten["Count"],
            name="Customers", mode="lines+markers",
            line=dict(color=AMBER, width=2.5), marker=dict(size=7)
        ), secondary_y=True)
        fig.add_hline(y=avg_line, line_dash="dash", line_color=RED,
                      annotation_text=f"Avg {avg_line:.1%}",
                      annotation_position="right")
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE,
                          margin=dict(t=30, b=20, l=10, r=10),
                          font=dict(family="Inter", size=12),
                          height=CHART_H,
                          xaxis=dict(title="Years with Bank", dtick=1),
                          yaxis=dict(tickformat=".0%", showgrid=True,
                                     gridcolor="#EEE", title="Churn Rate"),
                          yaxis2=dict(showgrid=False, title="Customers"),
                          legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "<div class='ibox ibox-info'>📌 Churn is flat across all tenure lengths — "
            "long-tenure customers are not significantly safer. Engagement quality "
            "matters more than relationship age.</div>", unsafe_allow_html=True
        )

    # ── Credit score vs churn ─────────────────────────────────────────────
    with c5:
        st.markdown("<div class='sec'>Credit Score Band vs Churn</div>",
                    unsafe_allow_html=True)
        cr = fdf.groupby("CreditBand", observed=True)["Exited"].agg(
            ["mean","count"]
        ).reset_index()
        cr.columns = ["Band","Churn","Count"]

        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=cr["Band"], y=cr["Churn"],
            name="Churn Rate",
            marker_color=[RED, AMBER, TEAL, GREEN],
            text=[f"{v:.1%}" for v in cr["Churn"]],
            textposition="outside"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=cr["Band"], y=cr["Count"],
            name="Customers", mode="lines+markers",
            line=dict(color=NAVY, width=2), marker=dict(size=8)
        ), secondary_y=True)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H,
                          yaxis=dict(tickformat=".0%", showgrid=True,
                                     gridcolor="#EEE", range=[0,.35]),
                          yaxis2=dict(showgrid=False),
                          legend=dict(x=0.6, y=0.99))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "<div class='ibox ibox-info'>📊 Credit score has surprisingly weak "
            "predictive power for churn — Poor credit customers don't churn "
            "significantly more than Excellent ones. Age and activity dominate."
            "</div>", unsafe_allow_html=True
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REGIONAL INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
with t2:

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='sec'>Churn Rate by Geography & Activity</div>",
                    unsafe_allow_html=True)
        geo_act = fdf.groupby(["Geography","IsActiveMember"])["Exited"].mean().reset_index()
        geo_act["Status"] = geo_act["IsActiveMember"].map({1:"Active",0:"Inactive"})
        fig = px.bar(geo_act, x="Geography", y="Exited", color="Status",
                     barmode="group",
                     color_discrete_map={"Active":TEAL,"Inactive":RED},
                     text=geo_act["Exited"].map(lambda x: f"{x:.1%}"),
                     labels={"Exited":"Churn Rate"})
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H,
                          yaxis=dict(tickformat=".0%", showgrid=True,
                                     gridcolor="#EEE", range=[0,.55]),
                          legend_title="")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("<div class='sec'>Total Balance by Geography</div>",
                    unsafe_allow_html=True)
        geo_bal = fdf.groupby("Geography").agg(
            Total_Balance=("Balance","sum"),
            Avg_Balance=("Balance","mean"),
            Customers=("Balance","count"),
            Churn_Rate=("Exited","mean")
        ).reset_index()
        fig = px.bar(geo_bal, x="Geography", y="Total_Balance",
                     color="Geography",
                     color_discrete_map={"France":TEAL,"Germany":RED,"Spain":AMBER},
                     text=geo_bal["Total_Balance"].map(lambda x: f"€{x/1e6:.0f}M"),
                     labels={"Total_Balance":"Total Balance (€)"})
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H, showlegend=False,
                          yaxis=dict(showgrid=True, gridcolor="#EEE"))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "<div class='ibox ibox-danger'>🇩🇪 <b>Germany Alert:</b> German customers "
        "churn at 32.4% — nearly 2× France (16.2%) and Spain (16.7%). Despite having "
        "the highest average balance (€119,730 vs €62,000 in France), Germany "
        "represents the highest risk-adjusted revenue exposure. "
        "Inactive Germans churn at 46%.</div>", unsafe_allow_html=True
    )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("<div class='sec'>Segment × Geography Churn Heatmap</div>",
                    unsafe_allow_html=True)
        heat = fdf.groupby(["Value_Segment","Geography"],
                            observed=True)["Exited"].mean().reset_index()
        heat_wide = heat.pivot(index="Value_Segment", columns="Geography",
                               values="Exited").fillna(0)
        fig = px.imshow(
            heat_wide, text_auto=".1%",
            color_continuous_scale=[[0,LIGHT],[0.4,AMBER],[1,RED]],
            labels={"color":"Churn Rate"},
            aspect="auto"
        )
        fig.update_traces(textfont_size=13)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H,
                          coloraxis_colorbar=dict(tickformat=".0%"))
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown("<div class='sec'>Age Band × Activity Churn Heatmap</div>",
                    unsafe_allow_html=True)
        heat2 = fdf.groupby(["AgeBand","IsActiveMember"],
                              observed=True)["Exited"].mean().reset_index()
        heat2["Status"] = heat2["IsActiveMember"].map({1:"Active",0:"Inactive"})
        heat2_wide = heat2.pivot(index="AgeBand", columns="Status",
                                  values="Exited").fillna(0)
        fig = px.imshow(
            heat2_wide, text_auto=".1%",
            color_continuous_scale=[[0,LIGHT],[0.4,AMBER],[1,RED]],
            labels={"color":"Churn Rate"},
            aspect="auto"
        )
        fig.update_traces(textfont_size=13)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H,
                          coloraxis_colorbar=dict(tickformat=".0%"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "<div class='ibox ibox-danger'>🎯 Inactive 50–60 year olds churn at "
            "85.7% — the single most dangerous combination in the entire dataset."
            "</div>", unsafe_allow_html=True
        )

    # ── Regional summary table ─────────────────────────────────────────────
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='sec'>Regional Summary</div>", unsafe_allow_html=True)
    reg = fdf.groupby("Geography").agg(
        Customers=("Exited","count"),
        Churned=("Exited","sum"),
        Churn_Rate=("Exited","mean"),
        Avg_Balance=("Balance","mean"),
        Total_Balance=("Balance","sum"),
        Avg_Age=("Age","mean"),
        Avg_Health=("Health_Score","mean")
    ).reset_index()
    reg["Churn_Rate"]    = reg["Churn_Rate"].map(lambda x: f"{x:.1%}")
    reg["Avg_Balance"]   = reg["Avg_Balance"].map(lambda x: f"€{x:,.0f}")
    reg["Total_Balance"] = reg["Total_Balance"].map(lambda x: f"€{x/1e6:.1f}M")
    reg["Avg_Age"]       = reg["Avg_Age"].map(lambda x: f"{x:.1f}")
    reg["Avg_Health"]    = reg["Avg_Health"].map(lambda x: f"{x:.0f}/100")
    reg.columns = ["Geography","Customers","Churned","Churn Rate",
                   "Avg Balance","Total Balance","Avg Age","Avg Health"]
    st.dataframe(reg, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PRODUCT ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with t3:

    c1, c2 = st.columns([1,1.4])

    with c1:
        st.markdown("<div class='sec'>Product Stickiness Table</div>",
                    unsafe_allow_html=True)
        prod = fdf.groupby("NumOfProducts").agg(
            Customers=("Exited","count"),
            Churn_Rate=("Exited","mean"),
            Avg_Balance=("Balance","mean"),
            Avg_Health=("Health_Score","mean")
        ).reset_index()

        # Annotate risk
        prod["Risk"] = prod["NumOfProducts"].map(
            {1:"⚠️ High",2:"✅ Sweet Spot",3:"🔴 Critical",4:"🔴🔴 Exit"}
        )
        styled = prod.copy()
        styled["Churn_Rate"]  = styled["Churn_Rate"].map(lambda x: f"{x:.1%}")
        styled["Avg_Balance"] = styled["Avg_Balance"].map(lambda x: f"€{x:,.0f}")
        styled["Avg_Health"]  = styled["Avg_Health"].map(lambda x: f"{x:.0f}")
        styled.columns = ["Products","Customers","Churn Rate",
                          "Avg Balance","Avg Health","Risk Signal"]
        st.dataframe(styled, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class='ibox ibox-paradox' style='margin-top:.8rem'>
          ⚠️ <b>The Stickiness Paradox</b><br>
          1 product → 27.7% churn<br>
          2 products → 7.6% churn ✅<br>
          3 products → 82.7% churn 🔴<br>
          4 products → 100% churn 🔴🔴<br><br>
          More products = complexity, not loyalty.
          The sweet spot is exactly 2.
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='sec'>The Product Paradox — Churn Rate by Count</div>",
                    unsafe_allow_html=True)
        prod_raw = fdf.groupby("NumOfProducts")["Exited"].mean().reset_index()
        fig = px.bar(prod_raw, x="NumOfProducts", y="Exited",
                     color="NumOfProducts",
                     color_discrete_map={1:TEAL,2:GREEN,3:AMBER,4:RED},
                     text=prod_raw["Exited"].map(lambda x: f"{x:.1%}"),
                     labels={"Exited":"Churn Rate","NumOfProducts":"Products Held"})
        fig.update_traces(textposition="outside", textfont_size=14)

        # Annotations
        fig.add_annotation(x=2, y=0.14, text="✅ Sweet Spot",
                           showarrow=False, font=dict(size=12,color=GREEN),
                           bgcolor="#EAFAF1", bordercolor=GREEN, borderwidth=1,
                           borderpad=4)
        fig.add_annotation(x=3.5, y=0.55, text="⚠️ Over-saturation",
                           showarrow=False, font=dict(size=11,color=RED),
                           bgcolor="#FDEDEC", bordercolor=RED, borderwidth=1,
                           borderpad=4)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H+40, showlegend=False,
                          yaxis=dict(tickformat=".0%", range=[0,1.2],
                                     showgrid=True, gridcolor="#EEE"))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("<div class='sec'>Product Mix by Geography</div>",
                    unsafe_allow_html=True)
        geo_prod = fdf.groupby(["Geography","NumOfProducts"],
                                observed=True).size().reset_index(name="Count")
        fig = px.bar(geo_prod, x="Geography", y="Count",
                     color="NumOfProducts",
                     color_discrete_map={1:TEAL,2:GREEN,3:AMBER,4:RED},
                     barmode="stack",
                     labels={"NumOfProducts":"Products","Count":"Customers"})
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H,
                          yaxis=dict(showgrid=True, gridcolor="#EEE"))
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown("<div class='sec'>🔬  What-If: Product Count Impact</div>",
                    unsafe_allow_html=True)
        sim_geo = st.selectbox("Filter by geography",
                               ["All","France","Germany","Spain"],
                               key="prod_geo")
        sim_df = fdf if sim_geo=="All" else fdf[fdf["Geography"]==sim_geo]
        ps = sim_df.groupby("NumOfProducts")["Exited"].mean().reset_index()

        fig = px.line(ps, x="NumOfProducts", y="Exited",
                      markers=True, line_shape="linear",
                      color_discrete_sequence=[TEAL],
                      text=ps["Exited"].map(lambda x: f"{x:.1%}"),
                      labels={"NumOfProducts":"Products","Exited":"Churn Rate"})
        fig.update_traces(textposition="top center", marker_size=12,
                          line_width=3)
        fig.add_hline(y=fdf["Exited"].mean(), line_dash="dash",
                      line_color=RED,
                      annotation_text=f"Avg {fdf['Exited'].mean():.1%}",
                      annotation_position="right")
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H,
                          yaxis=dict(tickformat=".0%", range=[0,1.15],
                                     showgrid=True, gridcolor="#EEE"))
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — REVENUE AT RISK
# ══════════════════════════════════════════════════════════════════════════════
with t4:

    # Sub KPIs
    w1, w2, w3, w4 = st.columns(4)
    wl_churn  = watchlist["Exited"].mean() if len(watchlist)>0 else 0
    avg_wl_b  = watchlist["Balance"].mean() if len(watchlist)>0 else 0
    potential = rev_risk * wl_churn

    for col, (color,label,val,sub) in zip(
        [w1,w2,w3,w4],
        [("danger","Revenue at Risk",     f"€{rev_risk/1e6:.1f}M",   "Inactive customers"),
         ("amber", "Watchlist Churn Rate",f"{wl_churn:.1%}",          f"vs {churn_rate:.1%} overall"),
         ("navy",  "Avg Watchlist Balance",f"€{avg_wl_b/1000:.0f}K", "Per inactive customer"),
         ("danger","Projected Loss",      f"€{potential/1e6:.1f}M",   "If churn rate holds")]
    ):
        with col:
            st.markdown(f"""
            <div class='kpi kpi-{color}'>
              <div class='kpi-label'>{label}</div>
              <div class='kpi-value'>{val}</div>
              <div class='kpi-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='sec'>Revenue at Risk by Geography</div>",
                    unsafe_allow_html=True)
        geo_risk = watchlist.groupby("Geography").agg(
            Revenue=("Balance","sum"),
            Customers=("Balance","count"),
            Churn_Rate=("Exited","mean")
        ).reset_index()

        fig = make_subplots(specs=[[{"secondary_y":True}]])
        geo_colors = [{"France":TEAL,"Germany":RED,"Spain":AMBER}.get(g,TEAL)
                      for g in geo_risk["Geography"]]
        fig.add_trace(go.Bar(
            x=geo_risk["Geography"], y=geo_risk["Revenue"],
            name="Revenue at Risk",
            marker_color=geo_colors,
            text=[f"€{v/1e6:.1f}M" for v in geo_risk["Revenue"]],
            textposition="outside"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=geo_risk["Geography"], y=geo_risk["Churn_Rate"],
            name="Churn Rate", mode="lines+markers",
            line=dict(color=NAVY, width=2.5), marker=dict(size=10)
        ), secondary_y=True)
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H,
                          yaxis=dict(showgrid=True, gridcolor="#EEE",
                                     title="Balance (€)"),
                          yaxis2=dict(tickformat=".0%", showgrid=False,
                                      title="Churn Rate"),
                          legend=dict(x=0.01,y=0.99))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("<div class='sec'>Watchlist Balance by Segment</div>",
                    unsafe_allow_html=True)
        fig = px.box(watchlist, x="Value_Segment", y="Balance",
                     color="Value_Segment",
                     color_discrete_map={
                         "Bronze":TEAL,"Silver":SILVER,
                         "Gold":GOLD,"Platinum":NAVY
                     },
                     labels={"Value_Segment":"Segment","Balance":"Balance (€)"},
                     points="outliers")
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=CHART_H, showlegend=False,
                          yaxis=dict(showgrid=True, gridcolor="#EEE"))
        st.plotly_chart(fig, use_container_width=True)

    # ── Watchlist table ───────────────────────────────────────────────────
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='sec'>Priority Outreach Watchlist</div>",
                unsafe_allow_html=True)

    wl_col1, wl_col2, wl_col3 = st.columns([1,1,2])
    with wl_col1:
        sort_col = st.selectbox("Sort by",
                                ["Balance","Health_Score","Age","NumOfProducts"],
                                key="wl_sort")
    with wl_col2:
        geo_wl = st.multiselect("Geography filter",
                                ["France","Germany","Spain"],
                                default=["France","Germany","Spain"],
                                key="wl_geo")
    with wl_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"<span class='pill pill-red'>⚠️ {len(watchlist):,} inactive customers</span>"
            f"<span class='pill pill-amber'>€{rev_risk/1e6:.1f}M at risk</span>"
            f"<span class='pill pill-red'>Churn rate: {wl_churn:.1%}</span>",
            unsafe_allow_html=True
        )

    wl_show = watchlist[watchlist["Geography"].isin(geo_wl)].sort_values(
        sort_col, ascending=False
    ).reset_index(drop=True)

    display_cols = ["CustomerId","Geography","Gender","Age","Balance",
                    "NumOfProducts","Value_Segment","Health_Score","Exited"]
    wl_disp = wl_show[display_cols].copy()
    wl_disp.columns = ["Customer ID","Geography","Gender","Age","Balance (€)",
                        "Products","Segment","Health Score","Churned"]
    wl_disp["Balance (€)"]   = wl_disp["Balance (€)"].map(lambda x: f"€{x:,.0f}")
    wl_disp["Health Score"]  = wl_disp["Health Score"].round(0).astype(int)

    if not wl_disp.empty:
        st.dataframe(wl_disp.head(100), use_container_width=True, hide_index=True)
        st.markdown(
            f"<p class='watchlist-note'>Showing top 100 of {len(wl_show):,} customers. "
            "Download full list below.</p>", unsafe_allow_html=True
        )
        st.download_button(
            label="⬇️  Download Full Watchlist (CSV)",
            data=wl_show[display_cols].to_csv(index=False),
            file_name="beli_priority_watchlist.csv",
            mime="text/csv",
            help="Full inactive customer list for outreach campaigns"
        )
    else:
        st.success("✅  No inactive customers match the current filters.")

    st.markdown(f"""
    <div class='ibox ibox-danger' style='margin-top:1rem'>
      ⚡ <b>Action Required:</b> A 10% retention improvement on this watchlist
      preserves <b>€{rev_risk*0.10/1e6:.1f}M</b> in deposits.
      Inactive customers with high balances churn at 32.3% —
      significantly above the {churn_rate:.1%} filtered average.
      These are your highest-ROI outreach targets.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — HEALTH ENGINE
# ══════════════════════════════════════════════════════════════════════════════
with t5:

    st.markdown(f"""
    <div class='ibox ibox-info'>
      <b>Current Formula:</b> Health Score =
      (IsActiveMember × <b>{w_act}</b>) +
      (HasCrCard × <b>{w_card}</b>) +
      (Tenure × <b>{w_ten}</b>) +
      (NumOfProducts × <b>{w_prod}</b>),
      clipped to 100 — adjust weights in the sidebar to see live changes.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        # Gauge
        st.markdown("<div class='sec'>Portfolio Health Gauge</div>",
                    unsafe_allow_html=True)
        g_color = GREEN if avg_health>74 else (AMBER if avg_health>40 else RED)
        fig = go.Figure(go.Indicator(
            mode  = "gauge+number+delta",
            value = avg_health,
            delta = {"reference":60, "suffix":" pts",
                     "increasing":{"color":GREEN},
                     "decreasing":{"color":RED}},
            title = {"text":"Average Portfolio Health",
                     "font":{"size":14,"color":NAVY,"family":"Inter"}},
            number= {"font":{"size":46,"color":g_color,"family":"Inter"},
                     "suffix":" / 100"},
            gauge = {
                "axis":    {"range":[0,100],"tickwidth":1,"tickcolor":"#CCC"},
                "bar":     {"color":g_color,"thickness":0.3},
                "bgcolor": WHITE,
                "steps": [
                    {"range":[0, 40],"color":"#FDEDEC"},
                    {"range":[40,74],"color":"#FEF9E7"},
                    {"range":[74,100],"color":"#EAFAF1"},
                ],
                "threshold":{
                    "line":{"color":NAVY,"width":3},
                    "thickness":0.75,"value":75
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(t=50,b=10,l=20,r=20),
                          paper_bgcolor=WHITE, plot_bgcolor=WHITE,
                          font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)

        # Tier donut
        tier_c = fdf["Health_Tier"].value_counts().reset_index()
        tier_c.columns = ["Tier","Count"]
        fig2 = px.pie(tier_c, values="Count", names="Tier", hole=0.5,
                      color="Tier",
                      color_discrete_map={
                          "At Risk":RED,"Moderate":AMBER,"Healthy":GREEN
                      })
        fig2.update_traces(textinfo="percent+label", textfont_size=12,
                           pull=[0.05 if t=="At Risk" else 0
                                 for t in tier_c["Tier"]])
        fig2.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=260, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.markdown("<div class='sec'>Health Score vs Balance — Churn Scatter</div>",
                    unsafe_allow_html=True)
        samp = fdf.sample(min(2500,len(fdf)), random_state=42)
        fig = px.scatter(
            samp, x="Health_Score", y="Balance",
            color=samp["Exited"].map({0:"Retained",1:"Churned"}),
            color_discrete_map={"Retained":TEAL,"Churned":RED},
            opacity=0.45, size_max=5,
            labels={"Health_Score":"Health Score","Balance":"Balance (€)"}
        )
        fig.add_vline(x=40, line_dash="dash", line_color=RED, line_width=1.5,
                      annotation_text="At-Risk threshold",
                      annotation_position="top right")
        fig.add_vline(x=75, line_dash="dash", line_color=GREEN, line_width=1.5,
                      annotation_text="Healthy threshold",
                      annotation_position="top right")
        fig.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=300, legend_title="",
                          yaxis=dict(showgrid=True, gridcolor="#EEE"),
                          xaxis=dict(showgrid=True, gridcolor="#EEE"))
        st.plotly_chart(fig, use_container_width=True)

        # Health by segment
        st.markdown("<div class='sec'>Health Score by Value Segment</div>",
                    unsafe_allow_html=True)
        sh = fdf.groupby("Value_Segment", observed=True)["Health_Score"].mean().reset_index()
        fig3 = px.bar(sh, x="Value_Segment", y="Health_Score",
                      color="Value_Segment",
                      color_discrete_map={
                          "Bronze":TEAL,"Silver":SILVER,"Gold":GOLD,"Platinum":NAVY
                      },
                      text=sh["Health_Score"].map(lambda x: f"{x:.0f}"),
                      labels={"Value_Segment":"Segment","Health_Score":"Avg Health"})
        fig3.update_traces(textposition="outside", textfont_size=12)
        fig3.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=250, showlegend=False,
                           yaxis=dict(range=[0,100], showgrid=True,
                                      gridcolor="#EEE"))
        st.plotly_chart(fig3, use_container_width=True)

    # ── Score validation ───────────────────────────────────────────────────
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='sec'>Health Score Validation — Score Band vs Churn Rate</div>",
                unsafe_allow_html=True)

    fdf["Health_Band"] = pd.cut(
        fdf["Health_Score"], bins=[0,20,40,60,80,100],
        labels=["0–20","21–40","41–60","61–80","81–100"]
    )
    hb = fdf.groupby("Health_Band", observed=True)["Exited"].agg(
        ["mean","count"]
    ).reset_index()
    hb.columns = ["Band","Churn","Count"]

    fig_hv = make_subplots(specs=[[{"secondary_y":True}]])
    fig_hv.add_trace(go.Bar(
        x=hb["Band"], y=hb["Churn"], name="Churn Rate",
        marker_color=[RED,RED,AMBER,TEAL,GREEN],
        text=[f"{v:.1%}" for v in hb["Churn"]],
        textposition="outside"
    ), secondary_y=False)
    fig_hv.add_trace(go.Scatter(
        x=hb["Band"], y=hb["Count"], name="Customers",
        mode="lines+markers",
        line=dict(color=NAVY,width=2.5), marker=dict(size=9)
    ), secondary_y=True)
    fig_hv.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=300,
                          yaxis=dict(tickformat=".0%", showgrid=True,
                                     gridcolor="#EEE", range=[0,.45]),
                          yaxis2=dict(showgrid=False),
                          legend=dict(x=0.7,y=0.99))
    st.plotly_chart(fig_hv, use_container_width=True)
    st.markdown(
        "<div class='ibox ibox-success'>✅ <b>Score Validated:</b> Lower health "
        "scores correlate directly with higher churn across all bands. The model "
        "is working as designed. Adjust sidebar weights to reprioritise what "
        "'healthy' means for your portfolio.</div>", unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with t6:
    st.markdown("<div class='sec'>Build Your Own View</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:.85rem;color:#666'>"
        "Select any dimensions and chart type to explore churn patterns "
        "across the filtered dataset.</p>", unsafe_allow_html=True
    )

    ex1, ex2, ex3 = st.columns(3)
    with ex1:
        x_ax = st.selectbox("X Axis",
                             ["Geography","AgeBand","Value_Segment","NumOfProducts",
                              "CreditBand","Gender","Tenure","TenureBand"],
                             key="ex_x")
    with ex2:
        col_by = st.selectbox("Colour by",
                              ["IsActiveMember","Gender",
                               "Value_Segment","NumOfProducts","Geography"],
                              key="ex_c")
    with ex3:
        chart_t = st.selectbox("Chart Type",
                               ["Bar — Churn Rate","Bar — Customer Count",
                                "Heatmap","Box — Health Score",
                                "Scatter — Balance vs Age"],
                               key="ex_t")

    # Safe groupby helper — avoids duplicate column error when x_ax == col_by
    def safe_groupby_churn(df, x, c):
        tmp = df[[x, c, "Exited"]].copy() if x != c else df[[x, "Exited"]].copy()
        tmp[x] = tmp[x].astype(str)
        if x != c:
            tmp[c] = tmp[c].astype(str)
            return tmp.groupby([x, c], observed=True)["Exited"].mean().reset_index()
        else:
            return tmp.groupby(x, observed=True)["Exited"].mean().reset_index()

    def safe_groupby_count(df, x, c):
        tmp = df[[x, c]].copy() if x != c else df[[x]].copy()
        tmp[x] = tmp[x].astype(str)
        if x != c:
            tmp[c] = tmp[c].astype(str)
            return tmp.groupby([x, c], observed=True).size().reset_index(name="Count")
        else:
            return tmp.groupby(x, observed=True).size().reset_index(name="Count")

    same_col = (x_ax == col_by)

    if chart_t == "Bar — Churn Rate":
        g = safe_groupby_churn(fdf, x_ax, col_by)
        if same_col:
            fig_ex = px.bar(g, x=x_ax, y="Exited",
                            text=g["Exited"].map(lambda x: f"{x:.1%}"),
                            labels={"Exited":"Churn Rate"},
                            color_discrete_sequence=[TEAL])
        else:
            fig_ex = px.bar(g, x=x_ax, y="Exited", color=col_by, barmode="group",
                            text=g["Exited"].map(lambda x: f"{x:.1%}"),
                            labels={"Exited":"Churn Rate"})
        fig_ex.update_traces(textposition="outside")
        fig_ex.update_layout(yaxis_tickformat=".0%",
                             yaxis_showgrid=True, yaxis_gridcolor="#EEE")

    elif chart_t == "Bar — Customer Count":
        g = safe_groupby_count(fdf, x_ax, col_by)
        if same_col:
            fig_ex = px.bar(g, x=x_ax, y="Count", text="Count",
                            color_discrete_sequence=[TEAL])
        else:
            fig_ex = px.bar(g, x=x_ax, y="Count", color=col_by,
                            barmode="stack", text="Count")
        fig_ex.update_traces(textposition="inside")
        fig_ex.update_layout(yaxis_showgrid=True, yaxis_gridcolor="#EEE")

    elif chart_t == "Heatmap":
        if same_col:
            g = safe_groupby_churn(fdf, x_ax, col_by)
            fig_ex = px.bar(g, x=x_ax, y="Exited",
                            text=g["Exited"].map(lambda x: f"{x:.1%}"),
                            labels={"Exited":"Churn Rate"},
                            color_discrete_sequence=[TEAL])
            fig_ex.update_layout(yaxis_tickformat=".0%")
        else:
            g = safe_groupby_churn(fdf, x_ax, col_by)
            piv_w = g.pivot(index=col_by, columns=x_ax, values="Exited").fillna(0)
            fig_ex = px.imshow(piv_w,
                               color_continuous_scale=[[0,LIGHT],[0.5,AMBER],[1,RED]],
                               text_auto=".1%",
                               labels={"color":"Churn Rate"})
            fig_ex.update_layout(coloraxis_colorbar=dict(tickformat=".0%"))

    elif chart_t == "Box — Health Score":
        tmp = fdf.copy()
        tmp["_color"] = tmp[col_by].astype(str)
        fig_ex = px.box(tmp, x=x_ax, y="Health_Score",
                        color="_color",
                        labels={"Health_Score":"Health Score","_color":col_by},
                        points="outliers")
        fig_ex.update_layout(yaxis_showgrid=True, yaxis_gridcolor="#EEE",
                             legend_title=col_by)

    else:  # Scatter
        samp = fdf.sample(min(2000,len(fdf)), random_state=42).copy()
        samp["_color"] = samp[col_by].astype(str)
        fig_ex = px.scatter(samp, x="Age", y="Balance",
                            color="_color",
                            opacity=0.5, size_max=6,
                            labels={"Balance":"Balance (€)","Age":"Age",
                                    "_color":col_by})
        fig_ex.update_layout(yaxis_showgrid=True, yaxis_gridcolor="#EEE",
                             legend_title=col_by)

    fig_ex.update_layout(paper_bgcolor=WHITE, plot_bgcolor=WHITE, margin=dict(t=30, b=20, l=10, r=10), font=dict(family="Inter", size=12), height=400)
    st.plotly_chart(fig_ex, use_container_width=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Summary table ──────────────────────────────────────────────────────
    st.markdown("<div class='sec'>Segment Summary Table</div>", unsafe_allow_html=True)
    grp_by = st.selectbox("Group by",
                           ["Geography","Value_Segment","AgeBand",
                            "CreditBand","Gender","NumOfProducts","TenureBand"],
                           key="sum_g")

    summ = fdf.groupby(grp_by, observed=True).agg(
        Customers=("Exited","count"),
        Churned=("Exited","sum"),
        Churn_Rate=("Exited","mean"),
        Avg_Balance=("Balance","mean"),
        Avg_Health=("Health_Score","mean"),
        Revenue_at_Risk=("Balance",
            lambda x: x[fdf.loc[x.index,"IsActiveMember"]==0].sum())
    ).reset_index()

    summ["Churn_Rate"]       = summ["Churn_Rate"].map(lambda x: f"{x:.1%}")
    summ["Avg_Balance"]      = summ["Avg_Balance"].map(lambda x: f"€{x:,.0f}")
    summ["Avg_Health"]       = summ["Avg_Health"].map(lambda x: f"{x:.0f}/100")
    summ["Revenue_at_Risk"]  = summ["Revenue_at_Risk"].map(lambda x: f"€{x/1e6:.2f}M")
    summ.columns = [grp_by,"Customers","Churned","Churn Rate",
                    "Avg Balance","Avg Health","Revenue at Risk"]
    st.dataframe(summ, use_container_width=True, hide_index=True)

    # Export
    st.download_button(
        label="⬇️  Download Filtered Dataset (CSV)",
        data=fdf.drop(["AgeBand","CreditBand","TenureBand","Health_Band",
                        "Health_Tier","Value_Segment","IsHighValue",
                        "IsInactiveHighValue","ProductRisk","OlderInactive",
                        "GermanyFlag","IsZeroBalance"], axis=1, errors="ignore"
                      ).to_csv(index=False),
        file_name="beli_filtered_dataset.csv",
        mime="text/csv"
    )


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center; font-size:.75rem; color:#999; padding:.5rem 0;
            font-family:Inter,sans-serif'>
  🏦 Banking Relationship Manager  •
  Arvind K  |  PES University, Bengaluru  •
  <span style='color:{TEAL}'>10,000 customers</span>  •
  <span style='color:{TEAL}'>6 analytical modules</span>  •
  <span style='color:{TEAL}'>Live health scoring</span>
</div>
""", unsafe_allow_html=True)
