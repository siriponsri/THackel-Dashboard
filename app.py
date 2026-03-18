
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Household Income Dashboard",
    page_icon="📊",
    layout="wide"
)

# ══════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════

COLOR_PRIMARY = "#1E293B"
COLOR_TEXT    = "#334155"

CHART_COLORS = [
    "#4F46E5", "#0EA5E9", "#10B981", "#F59E0B",
    "#EF4444", "#8B5CF6", "#EC4899", "#06B6D4",
    "#14B8A6", "#F97316"
]

PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, Segoe UI, sans-serif", color=COLOR_TEXT, size=12),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FAFBFC",
    title=dict(font=dict(size=15, color=COLOR_PRIMARY, weight=600), x=0, xanchor="left"),
    margin=dict(l=10, r=10, t=52, b=20),
    legend=dict(
        orientation="h", yanchor="bottom", y=-0.25,
        xanchor="center", x=0.5,
        font=dict(size=10.5, color="#64748B"), bgcolor="rgba(0,0,0,0)"
    ),
    xaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0",
              title_font=dict(color="#64748B", size=11),
              tickfont=dict(color="#64748B", size=10)),
    yaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0",
              title_font=dict(color="#64748B", size=11),
              tickfont=dict(color="#64748B", size=10)),
)

def styled_fig(fig, **kwargs):
    layout = {**PLOTLY_LAYOUT, **kwargs}
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#F1F5F9")
    fig.update_yaxes(showgrid=False)
    return fig

# ---------- CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif !important; }

.stApp { background: #F8FAFC !important; }

.block-container {
    padding: 1.2rem 2rem 2rem !important;
    max-width: 1160px;
}

/* ═══ HEADER ═══ */
.dash-hero {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 60%, #1a1a2e 100%);
    border-radius: 16px;
    padding: 2.2rem 2.5rem 1.8rem;
    margin-bottom: 1.4rem;
    position: relative;
    overflow: hidden;
}
.dash-hero::before {
    content: '';
    position: absolute;
    top: -40%; right: -10%;
    width: 340px; height: 340px;
    background: radial-gradient(circle, rgba(79,70,229,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.dash-hero h1 {
    color: #FFFFFF !important;
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 0.25rem;
    position: relative;
}
.dash-hero .subtitle {
    color: #94A3B8 !important;
    font-size: 0.85rem;
    font-weight: 400;
    position: relative;
}
.dash-hero .badge {
    display: inline-block;
    background: rgba(79,70,229,0.25);
    color: #A5B4FC;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    margin-bottom: 0.7rem;
    letter-spacing: 0.04em;
    position: relative;
}

/* ═══ METRIC CARDS ═══ */
.kpi-row { display: flex; gap: 0.9rem; margin-bottom: 1.2rem; }
.kpi-card {
    flex: 1;
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.3rem 1.2rem 1.15rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04), 0 4px 12px rgba(15,23,42,0.03);
    border: 1px solid #F1F5F9;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-card.c1::after { background: linear-gradient(90deg, #4F46E5, #818CF8); }
.kpi-card.c2::after { background: linear-gradient(90deg, #0EA5E9, #67E8F9); }
.kpi-card.c3::after { background: linear-gradient(90deg, #10B981, #6EE7B7); }
.kpi-card.c4::after { background: linear-gradient(90deg, #F59E0B, #FCD34D); }

.kpi-card .kpi-icon {
    font-size: 1.5rem;
    margin-bottom: 0.25rem;
}
.kpi-card .kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #94A3B8 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
}
.kpi-card .kpi-value {
    font-size: 1.85rem;
    font-weight: 800;
    color: #1E293B !important;
    line-height: 1.15;
    letter-spacing: -0.02em;
}
.kpi-card .kpi-unit {
    font-size: 0.72rem;
    color: #94A3B8 !important;
    margin-top: 0.15rem;
}

/* ═══ CHART WRAPPER ═══ */
.chart-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.2rem 1.2rem 0.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04), 0 4px 12px rgba(15,23,42,0.03);
    border: 1px solid #F1F5F9;
}
.chart-card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1E293B !important;
    margin: 0 0 0.2rem;
}
.chart-card-desc {
    font-size: 0.78rem;
    color: #94A3B8 !important;
    margin: 0 0 0.8rem;
}

/* ═══ SECTION TITLE ═══ */
.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #1E293B !important;
    border-left: 3px solid #4F46E5;
    padding-left: 0.7rem;
    margin: 1.4rem 0 0.8rem;
}

h1, h2, h3 { color: #1E293B !important; font-weight: 700; }

/* ═══ TABS ═══ */
[data-baseweb="tab-list"] {
    gap: 0 !important;
    background: #FFFFFF;
    border-radius: 10px;
    padding: 0.25rem;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04);
    border: 1px solid #F1F5F9;
    margin-bottom: 1rem;
}
button[data-baseweb="tab"] {
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    color: #64748B !important;
    background: transparent !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    border: none !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    background: #4F46E5 !important;
}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {
    display: none !important;
}

/* ═══ SIDEBAR ═══ */
section[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #F1F5F9 !important;
}
.sidebar-brand {
    text-align: center;
    padding: 0.6rem 0 1rem;
    border-bottom: 1px solid #F1F5F9;
    margin-bottom: 1rem;
}
.sidebar-brand .logo {
    font-size: 1.7rem;
    margin-bottom: 0.2rem;
}
.sidebar-brand .brand-name {
    font-size: 0.82rem;
    font-weight: 700;
    color: #1E293B !important;
    letter-spacing: -0.01em;
}
.sidebar-brand .brand-sub {
    font-size: 0.68rem;
    color: #94A3B8 !important;
}
section[data-testid="stSidebar"] label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: #475569 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background: #EEF2FF !important;
    color: #4F46E5 !important;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 500;
    border: 1px solid #C7D2FE !important;
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] span[role="presentation"] {
    color: #4F46E5 !important;
}

/* ═══ DATAFRAME ═══ */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04);
    border: 1px solid #F1F5F9;
}

/* ═══ DIVIDER ═══ */
hr {
    border: none !important;
    height: 1px !important;
    background: #F1F5F9 !important;
    margin: 1rem 0 !important;
}

/* ═══ POLICY CARDS ═══ */
.policy-card {
    background: #FFFFFF;
    border: 1px solid #F1F5F9;
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04);
}
.policy-card h4 {
    font-size: 0.92rem;
    font-weight: 700;
    color: #1E293B !important;
    margin: 0 0 0.45rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.policy-card p, .policy-card li {
    font-size: 0.82rem;
    color: #475569 !important;
    line-height: 1.7;
}
.policy-card strong {
    color: #1E293B !important;
    font-weight: 600;
}
.policy-card ul { padding-left: 1.2rem; margin: 0; }

/* ═══ MISC ═══ */
[data-testid="stMetricValue"] { color: #1E293B !important; }
</style>
""", unsafe_allow_html=True)


def kpi_card(icon: str, label: str, value: str, unit: str, color_class: str) -> str:
    unit_html = f'<div class="kpi-unit">{unit}</div>' if unit else ""
    return f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {unit_html}
    </div>
    """

# ---------- Load ----------
@st.cache_data
def load_data():
    avg_income = pd.read_csv("avg_income.csv")
    pct_house = pd.read_csv("pct_house.csv")

    # Standardize missing text
    for col in avg_income.select_dtypes(include="object").columns:
        avg_income[col] = avg_income[col].astype(str).str.strip()

    for col in pct_house.select_dtypes(include="object").columns:
        pct_house[col] = pct_house[col].astype(str).str.strip()

    avg_income = avg_income.replace({"": np.nan, "nan": np.nan, "None": np.nan, "NaN": np.nan})
    pct_house = pct_house.replace({"": np.nan, "nan": np.nan, "None": np.nan, "NaN": np.nan})

    # Rename columns
    avg_income = avg_income.rename(columns={
        "source_income1": "income_source_level1",
        "source_income2": "income_source_level2",
        "source_income3": "income_source_level3",
        "soc_eco_class1": "occupation_group_main",
        "soc_eco_class2": "occupation_group_detail",
        "value": "average_income",
        "unit": "income_unit",
        "attribute": "attribute_note",
        "source": "data_source"
    })

    pct_house = pct_house.rename(columns={
        "hh_size": "household_size_group",
        "income": "income_range",
        "value": "household_share",
        "unit": "share_unit",
        "attribute": "attribute_note",
        "source": "data_source"
    })

    # Numeric
    avg_income["year"] = pd.to_numeric(avg_income["year"], errors="coerce")
    avg_income["average_income"] = pd.to_numeric(avg_income["average_income"], errors="coerce")
    pct_house["year"] = pd.to_numeric(pct_house["year"], errors="coerce")
    pct_house["household_share"] = pd.to_numeric(pct_house["household_share"], errors="coerce")

    # Required columns only
    avg_income_required_cols = [
        "year", "province", "occupation_group_main",
        "occupation_group_detail", "income_source_level3", "average_income"
    ]
    pct_house_required_cols = [
        "year", "province", "household_size_group",
        "income_range", "household_share"
    ]

    avg_income = avg_income.dropna(subset=avg_income_required_cols).copy()
    pct_house = pct_house.dropna(subset=pct_house_required_cols).copy()

    # Remove exact duplicates in pct_house
    pct_house = pct_house.drop_duplicates().copy()

    # Keep only valid share values
    pct_house = pct_house[
        (pct_house["household_share"] >= 0) &
        (pct_house["household_share"] <= 100)
    ].copy()

    # Subset for total income
    total_income_df = avg_income[
        avg_income["income_source_level3"] == "รายได้ทั้งสิ้นต่อเดือน"
    ].copy()

    total_income_df = total_income_df[
        total_income_df["average_income"] >= 0
    ].copy()

    return avg_income, pct_house, total_income_df

avg_income, pct_house, total_income_df = load_data()

# ---------- Sidebar ----------
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="logo">📊</div>
    <div class="brand-name">Income Dashboard</div>
    <div class="brand-sub">THackle DataViz 2566</div>
</div>
""", unsafe_allow_html=True)

selected_main_groups = st.sidebar.multiselect(
    "เลือกกลุ่มอาชีพหลัก",
    sorted(total_income_df["occupation_group_main"].dropna().unique().tolist()),
    default=sorted(total_income_df["occupation_group_main"].dropna().unique().tolist())
)

filtered_total = total_income_df[
    total_income_df["occupation_group_main"].isin(selected_main_groups)
].copy()

# ── Header ──
st.markdown("""
<div class="dash-hero">
    <div class="badge">THACKLE DATAVIZ CHALLENGE</div>
    <h1>Household Income Dashboard</h1>
    <div class="subtitle">รายได้เฉลี่ยต่อเดือนของครัวเรือนไทย พ.ศ. 2566 &mdash; สำนักงานสถิติแห่งชาติ</div>
</div>
""", unsafe_allow_html=True)

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Income by Occupation",
    "Regional Inequality",
    "Income Structure",
    "Policy Insights"
])

# ═══  Tab 1 — Overview  ═══
with tab1:
    # KPI cards as raw HTML row for pixel-perfect control
    st.markdown(f"""
    <div class="kpi-row">
        {kpi_card("🗺️", "จังหวัด", str(filtered_total['province'].nunique()), "provinces", "c1")}
        {kpi_card("👥", "กลุ่มอาชีพหลัก", str(filtered_total['occupation_group_main'].nunique()), "groups", "c2")}
        {kpi_card("🏷️", "กลุ่มอาชีพย่อย", str(filtered_total['occupation_group_detail'].nunique()), "sub-groups", "c3")}
        {kpi_card("💰", "รายได้เฉลี่ย", f"{filtered_total['average_income'].mean():,.0f}", "บาท / เดือน", "c4")}
    </div>
    """, unsafe_allow_html=True)

    income_cap = filtered_total["average_income"].quantile(0.99)

    st.markdown("""
    <div class="chart-card">
        <div class="chart-card-title">Distribution of Average Monthly Household Income</div>
        <div class="chart-card-desc">Filtered by selected occupation groups · capped at 99th percentile</div>
    </div>
    """, unsafe_allow_html=True)

    fig = px.histogram(
        filtered_total[filtered_total["average_income"] <= income_cap],
        x="average_income",
        nbins=20,
        color_discrete_sequence=["#4F46E5"],
        labels={
            "average_income": "Average Income (Baht / month)",
            "count": "Number of Records"
        }
    )
    fig.update_traces(marker_line_width=0, opacity=0.9)
    styled_fig(fig, height=400, bargap=0.12)
    fig.update_layout(title="")
    st.plotly_chart(fig, use_container_width=True)

    income_band_summary = pd.DataFrame({
        "Income Band": [
            "ต่ำกว่า 10,000 บาท",
            "10,000 – 19,999 บาท",
            "20,000 – 29,999 บาท",
            "30,000 – 39,999 บาท",
            "40,000 บาทขึ้นไป"
        ],
        "Count": [
            (filtered_total["average_income"] < 10000).sum(),
            ((filtered_total["average_income"] >= 10000) & (filtered_total["average_income"] < 20000)).sum(),
            ((filtered_total["average_income"] >= 20000) & (filtered_total["average_income"] < 30000)).sum(),
            ((filtered_total["average_income"] >= 30000) & (filtered_total["average_income"] < 40000)).sum(),
            (filtered_total["average_income"] >= 40000).sum()
        ]
    })
    income_band_summary["Share (%)"] = (
        income_band_summary["Count"] / income_band_summary["Count"].sum() * 100
    ).round(2)

    st.markdown('<div class="section-title">Income Band Summary</div>', unsafe_allow_html=True)
    st.dataframe(income_band_summary, use_container_width=True, hide_index=True)

# ═══  Tab 2 — Income by Occupation  ═══
with tab2:
    st.markdown('<div class="section-title">Who Earns What?</div>', unsafe_allow_html=True)

    q1_detail = (
        filtered_total
        .groupby(["occupation_group_main", "occupation_group_detail"], as_index=False)
        .agg(avg_monthly_income=("average_income", "mean"))
    )

    q1_plot = q1_detail.copy()
    q1_plot["occupation_display"] = (
        q1_plot["occupation_group_detail"] + "  |  " + q1_plot["occupation_group_main"]
    )
    q1_plot = q1_plot.sort_values("avg_monthly_income", ascending=True)

    fig = px.bar(
        q1_plot,
        x="avg_monthly_income",
        y="occupation_display",
        color="occupation_group_main",
        orientation="h",
        text="avg_monthly_income",
        color_discrete_sequence=CHART_COLORS,
        labels={
            "avg_monthly_income": "Average Income (Baht / month)",
            "occupation_display": "",
            "occupation_group_main": "Occupation Group"
        },
    )
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                      marker_line_width=0, opacity=0.92)
    styled_fig(fig, height=680)
    fig.update_layout(title="Average Monthly Household Income by Occupation",
                      plot_bgcolor="#FAFBFC")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    q1_gap = (
        q1_detail
        .groupby("occupation_group_main", as_index=False)
        .agg(
            n_detail=("occupation_group_detail", "nunique"),
            max_income=("avg_monthly_income", "max"),
            min_income=("avg_monthly_income", "min")
        )
    )
    q1_gap["income_gap"] = q1_gap["max_income"] - q1_gap["min_income"]
    q1_gap["gap_ratio"] = (q1_gap["max_income"] / q1_gap["min_income"]).round(2)
    q1_gap_plot = q1_gap[q1_gap["n_detail"] >= 2].copy().sort_values("income_gap", ascending=True)

    fig2 = px.bar(
        q1_gap_plot,
        x="income_gap",
        y="occupation_group_main",
        orientation="h",
        text="income_gap",
        color_discrete_sequence=[CHART_COLORS[1]],
        labels={
            "income_gap": "Income Gap (Baht / month)",
            "occupation_group_main": ""
        },
    )
    fig2.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                       marker_line_width=0)
    styled_fig(fig2, height=380)
    fig2.update_layout(title="Income Gap Within Each Main Occupation Group")
    st.plotly_chart(fig2, use_container_width=True)

# ═══  Tab 3 — Regional Inequality  ═══
with tab3:
    st.markdown('<div class="section-title">Where Is Inequality?</div>', unsafe_allow_html=True)

    q2_province_occ = (
        filtered_total
        .groupby(["province", "occupation_group_detail"], as_index=False)
        .agg(avg_monthly_income=("average_income", "mean"))
    )

    q2_province_occ_valid = q2_province_occ[q2_province_occ["avg_monthly_income"] > 0].copy()

    q2_province_gap = (
        q2_province_occ_valid
        .groupby("province")
        .agg(
            n_detail=("occupation_group_detail", "nunique"),
            avg_income=("avg_monthly_income", "mean"),
            max_income=("avg_monthly_income", "max"),
            min_income=("avg_monthly_income", "min"),
            p90_income=("avg_monthly_income", lambda s: s.quantile(0.90)),
            p10_income=("avg_monthly_income", lambda s: s.quantile(0.10))
        )
        .reset_index()
    )

    q2_province_gap = q2_province_gap[q2_province_gap["n_detail"] >= 2].copy()
    q2_province_gap["income_gap"] = q2_province_gap["max_income"] - q2_province_gap["min_income"]
    q2_province_gap["robust_gap"] = q2_province_gap["p90_income"] - q2_province_gap["p10_income"]
    q2_province_gap["normalized_gap"] = (q2_province_gap["robust_gap"] / q2_province_gap["avg_income"]).round(2)

    pct_total = pct_house[pct_house["household_size_group"] == "รวมทั้งสิ้น"].copy()
    pct_total = pct_total[
        ~pct_total["income_range"].isin([
            "รายได้ทั้งสิ้นเฉลี่ยต่อเดือนต่อคน",
            "รายได้ทั้งสิ้นเฉลี่ยต่อเดือนต่อครัวเรือน"
        ])
    ].copy()

    income_range_map = {
        "1,500 - 3,000 บาท": "1,501 - 3,000 บาท",
        "ต่ำกว่า 500 บาท": "ต่ำกว่า 1,500 บาท",
        "500 - 1,500 บาท": "ต่ำกว่า 1,500 บาท"
    }
    pct_total["income_range_clean"] = pct_total["income_range"].replace(income_range_map)

    low_income_bins = [
        "ต่ำกว่า 1,500 บาท",
        "1,501 - 3,000 บาท",
        "3,001 - 5,000 บาท",
        "5,001 - 10,000 บาท"
    ]

    high_income_bins = [
        "50,001 - 100,000 บาท",
        "มากกว่า 100,000 บาท"
    ]

    low_share = (
        pct_total[pct_total["income_range_clean"].isin(low_income_bins)]
        .groupby("province", as_index=False)
        .agg(low_income_share=("household_share", "sum"))
    )

    high_share = (
        pct_total[pct_total["income_range_clean"].isin(high_income_bins)]
        .groupby("province", as_index=False)
        .agg(high_income_share=("household_share", "sum"))
    )

    q2_profile = (
        q2_province_gap
        .merge(low_share, on="province", how="left")
        .merge(high_share, on="province", how="left")
        .fillna(0)
    )

    q2_profile["polarization_score"] = q2_profile["low_income_share"] + q2_profile["high_income_share"]

    q2_top_gap = q2_province_gap.sort_values("robust_gap", ascending=False).head(15).copy()
    q2_top_gap_plot = q2_top_gap.sort_values("robust_gap", ascending=True)

    fig = px.bar(
        q2_top_gap_plot,
        x="robust_gap",
        y="province",
        orientation="h",
        text="robust_gap",
        color_discrete_sequence=[CHART_COLORS[3]],
        labels={
            "robust_gap": "Robust Income Gap (Baht / month)",
            "province": ""
        },
    )
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                      marker_line_width=0)
    styled_fig(fig, height=620)
    fig.update_layout(title="Top Provinces with the Largest Robust Income Gap")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    fig2 = px.scatter(
        q2_profile,
        x="avg_income",
        y="robust_gap",
        size="polarization_score",
        hover_name="province",
        color_discrete_sequence=[CHART_COLORS[0]],
        labels={
            "avg_income": "Average Income (Baht / month)",
            "robust_gap": "Robust Income Gap (Baht / month)"
        },
    )
    fig2.update_traces(marker=dict(line_width=0.5, line_color="white", opacity=0.8))
    styled_fig(fig2, height=580)
    fig2.update_layout(title="Province Profile: Income vs Internal Gap")
    st.plotly_chart(fig2, use_container_width=True)

# ═══  Tab 4 — Income Structure  ═══
with tab4:
    st.markdown('<div class="section-title">What Is the Income Structure?</div>', unsafe_allow_html=True)

    q3_component_sources = [
        "ค่าจ้างและเงินเดือน",
        "กำไรสุทธิจากการทำธุรกิจ",
        "กำไรสุทธิจากการทำการเกษตร",
        "รายได้จากทรัพย์สิน",
        "เงินที่ได้รับเป็นการช่วยเหลือ",
        "รายได้ที่ไม่เป็นตัวเงิน",
        "รายได้ไม่ประจำ (ที่เป็นตัวเงิน)"
    ]

    q3_raw = avg_income[
        avg_income["income_source_level3"].isin(q3_component_sources)
    ].copy()

    q3_positive = q3_raw[q3_raw["average_income"] > 0].copy()

    q3_structure = (
        q3_positive
        .groupby(["occupation_group_main", "income_source_level3"], as_index=False)
        .agg(avg_monthly_income=("average_income", "mean"))
    )

    q3_structure["share_pct"] = (
        q3_structure
        .groupby("occupation_group_main")["avg_monthly_income"]
        .transform(lambda s: s / s.sum() * 100)
    )

    fig = px.bar(
        q3_structure,
        x="share_pct",
        y="occupation_group_main",
        color="income_source_level3",
        orientation="h",
        text="share_pct",
        color_discrete_sequence=CHART_COLORS,
        labels={
            "share_pct": "Share (%)",
            "occupation_group_main": "",
            "income_source_level3": "Income Source"
        },
    )
    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="inside",
        marker_line_width=0
    )
    styled_fig(fig, height=500, xaxis_range=[0, 100])
    fig.update_layout(title="Income Structure by Main Occupation Group")
    st.plotly_chart(fig, use_container_width=True)

    q3_dominant = (
        q3_structure
        .sort_values(["occupation_group_main", "share_pct"], ascending=[True, False])
        .groupby("occupation_group_main", as_index=False)
        .first()
        .rename(columns={
            "income_source_level3": "main_income_source",
            "share_pct": "main_source_share"
        })
    )

    vulnerable_sources = [
        "เงินที่ได้รับเป็นการช่วยเหลือ",
        "รายได้ไม่ประจำ (ที่เป็นตัวเงิน)"
    ]

    q3_vulnerable_share = (
        q3_structure[q3_structure["income_source_level3"].isin(vulnerable_sources)]
        .groupby("occupation_group_main", as_index=False)
        .agg(vulnerable_source_share=("share_pct", "sum"))
    )

    q3_dominant = q3_dominant.merge(q3_vulnerable_share, on="occupation_group_main", how="left")
    q3_dominant["vulnerable_source_share"] = q3_dominant["vulnerable_source_share"].fillna(0).round(2)
    q3_dominant["main_source_share"] = q3_dominant["main_source_share"].round(2)

    st.markdown('<div class="section-title">Dominant & Vulnerable Sources</div>', unsafe_allow_html=True)
    st.dataframe(
        q3_dominant[[
            "occupation_group_main",
            "main_income_source",
            "main_source_share",
            "vulnerable_source_share"
        ]],
        use_container_width=True,
        hide_index=True
    )

# ═══  Tab 5 — Policy Insights  ═══
with tab5:
    st.markdown('<div class="section-title">Key Policy Implications</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
<div class="policy-card">
    <h4>📌 1. Occupational Inequality</h4>
    <ul>
        <li>กลุ่มลูกจ้างมีช่องว่างรายได้ภายในกลุ่มสูงที่สุด</li>
        <li>นโยบายควรมุ่งเพิ่มโอกาสเข้าถึงงานคุณภาพ และยกระดับทักษะแรงงาน</li>
    </ul>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="policy-card">
    <h4>🗺️ 2. Spatial Inequality</h4>
    <ul>
        <li>บางจังหวัดมี robust internal income gap สูง ขณะที่บางจังหวัดมี polarization สูง</li>
        <li>นโยบายระดับพื้นที่ควรแยกเป้าหมาย: "ยกระดับรายได้โดยรวม" vs "ลดช่องว่างภายในจังหวัด"</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
<div class="policy-card">
    <h4>⚠️ 3. Income Structure Vulnerability</h4>
    <ul>
        <li><strong>ลูกจ้าง</strong> — พึ่งพาค่าจ้างเป็นหลัก</li>
        <li><strong>ผู้ประกอบธุรกิจ</strong> — พึ่งพากำไรธุรกิจเป็นหลัก</li>
        <li><strong>ผู้ถือครองทำการเกษตร</strong> — พึ่งพากำไรเกษตรเป็นหลัก</li>
        <li><strong>ผู้ไม่ได้ปฏิบัติงานเชิงเศรษฐกิจ</strong> — พึ่งพาเงินช่วยเหลือและรายได้ไม่ประจำ ในสัดส่วนสูง</li>
    </ul>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="policy-card">
    <h4>📋 4. Data Source</h4>
    <p>ข้อมูลจาก สำนักงานสถิติแห่งชาติ พ.ศ. 2566<br>
    Survey of Household Socio-Economic Status</p>
</div>
""", unsafe_allow_html=True)

