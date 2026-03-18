
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

# — Palette —
COLOR_PRIMARY   = "#0F172A"   # Dark navy
COLOR_ACCENT    = "#3B82F6"   # Blue accent
COLOR_BG_CARD   = "#F8FAFC"   # Very light gray
COLOR_BORDER    = "#E2E8F0"   # Subtle border
COLOR_TEXT      = "#334155"   # Slate text
COLOR_MUTED     = "#94A3B8"   # Muted

# — Chart colors (accessible & cohesive) —
CHART_COLORS = [
    "#3B82F6", "#10B981", "#F59E0B", "#EF4444",
    "#8B5CF6", "#06B6D4", "#F97316", "#EC4899",
    "#14B8A6", "#6366F1"
]

# — Plotly template —
PLOTLY_LAYOUT = dict(
    font=dict(family="Segoe UI, Tahoma, sans-serif", color=COLOR_TEXT, size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    title=dict(font=dict(size=17, color=COLOR_PRIMARY), x=0.5, xanchor="center"),
    margin=dict(l=20, r=20, t=60, b=30),
    legend=dict(
        orientation="h", yanchor="bottom", y=-0.22,
        xanchor="center", x=0.5,
        font=dict(size=11), bgcolor="rgba(0,0,0,0)"
    ),
    xaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0"),
    yaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0"),
)

def styled_fig(fig, **kwargs):
    """Apply consistent theme to any Plotly figure."""
    layout = {**PLOTLY_LAYOUT, **kwargs}
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#F1F5F9")
    fig.update_yaxes(showgrid=False)
    return fig

# ---------- CSS ----------
st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* ── Header ── */
.dashboard-header {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: white;
    padding: 2rem 2.5rem 1.6rem;
    border-radius: 16px;
    margin-bottom: 1.8rem;
}
.dashboard-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0 0 0.3rem;
    letter-spacing: -0.02em;
}
.dashboard-header p {
    color: #94A3B8;
    font-size: 0.92rem;
    margin: 0;
}

/* ── Metric cards ── */
.metric-card {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: box-shadow 0.2s;
}
.metric-card:hover {
    box-shadow: 0 4px 12px rgba(15,23,42,0.07);
}
.metric-card .label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.35rem;
}
.metric-card .value {
    font-size: 1.65rem;
    font-weight: 700;
    color: #0F172A;
}
.metric-card .unit {
    font-size: 0.75rem;
    color: #94A3B8;
    margin-top: 0.15rem;
}

/* ── Section titles ── */
h2, h3 {
    color: #0F172A;
    font-weight: 600;
    letter-spacing: -0.01em;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #0F172A;
    border-left: 4px solid #3B82F6;
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem;
}

/* ── Tabs ── */
button[data-baseweb="tab"] {
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    color: #64748B !important;
    padding: 0.6rem 1.2rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #0F172A !important;
    font-weight: 600 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #F8FAFC;
    border-right: 1px solid #E2E8F0;
}
section[data-testid="stSidebar"] h1 {
    font-size: 1.05rem;
    font-weight: 600;
    color: #0F172A;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* ── Divider ── */
hr { border-color: #E2E8F0; margin: 1.2rem 0; }

/* ── Policy cards ── */
.policy-card {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.policy-card h4 {
    font-size: 1rem;
    font-weight: 600;
    color: #0F172A;
    margin: 0 0 0.5rem;
}
.policy-card p, .policy-card li {
    font-size: 0.88rem;
    color: #475569;
    line-height: 1.65;
}
</style>
""", unsafe_allow_html=True)


def metric_card(label: str, value: str, unit: str = "") -> str:
    """Return HTML for a styled metric card."""
    unit_html = f'<div class="unit">{unit}</div>' if unit else ""
    return f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
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
st.sidebar.title("Filters")
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
<div class="dashboard-header">
    <h1>Household Income Dashboard</h1>
    <p>THackle DataViz Challenge — Average Monthly Household Income in Thailand (2566)</p>
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
    st.markdown('<div class="section-title">Key Figures</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card(
            "จังหวัด",
            f"{filtered_total['province'].nunique()}",
            "provinces"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card(
            "กลุ่มอาชีพหลัก",
            f"{filtered_total['occupation_group_main'].nunique()}",
            "groups"
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card(
            "กลุ่มอาชีพย่อย",
            f"{filtered_total['occupation_group_detail'].nunique()}",
            "sub-groups"
        ), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card(
            "รายได้เฉลี่ย",
            f"{filtered_total['average_income'].mean():,.0f}",
            "บาท / เดือน"
        ), unsafe_allow_html=True)

    st.markdown("")
    income_cap = filtered_total["average_income"].quantile(0.99)

    fig = px.histogram(
        filtered_total[filtered_total["average_income"] <= income_cap],
        x="average_income",
        nbins=20,
        color_discrete_sequence=[CHART_COLORS[0]],
        labels={
            "average_income": "Average Income (Baht / month)",
            "count": "Number of Records"
        }
    )
    styled_fig(fig, height=420, bargap=0.1)
    fig.update_layout(title="Distribution of Average Monthly Household Income")
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
                      marker_line_width=0)
    styled_fig(fig, height=680)
    fig.update_layout(title="Average Monthly Household Income by Occupation")
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
    <h4>1. Occupational Inequality</h4>
    <ul>
        <li>กลุ่มลูกจ้างมีช่องว่างรายได้ภายในกลุ่มสูงที่สุด</li>
        <li>นโยบายควรมุ่งเพิ่มโอกาสเข้าถึงงานคุณภาพ และยกระดับทักษะแรงงาน</li>
    </ul>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="policy-card">
    <h4>2. Spatial Inequality</h4>
    <ul>
        <li>บางจังหวัดมี robust internal income gap สูง ขณะที่บางจังหวัดมี polarization สูง</li>
        <li>นโยบายระดับพื้นที่ควรแยกเป้าหมาย: "ยกระดับรายได้โดยรวม" vs "ลดช่องว่างภายในจังหวัด"</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
<div class="policy-card">
    <h4>3. Income Structure Vulnerability</h4>
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
    <h4>4. Data Source</h4>
    <p>ข้อมูลจาก สำนักงานสถิติแห่งชาติ พ.ศ. 2566<br>
    Survey of Household Socio-Economic Status</p>
</div>
""", unsafe_allow_html=True)

