from __future__ import annotations

from html import escape

import streamlit as st


TRANSLATIONS = {
    "zh": {
        "language": "语言 / Language",
        "zh": "中文",
        "en": "English",
        "us_market": "美国市场 · USD",
        "nav_hint": "使用左侧页面导航切换功能",
        "simulated": "模拟数据",
        "overview": "跨境电商竞品价格监控",
        "overview_subtitle": "让每一次跟价决策，都有同款匹配、到手价格和利润率作为依据。",
        "details": "商品明细",
        "details_subtitle": "逐个查看同款匹配、最终可比价格、利润率和跟价依据。",
        "agent": "Agent 工作台",
        "agent_subtitle": "让 Gemini 理解问题，让本地 Python 工具负责事实和计算。",
        "data": "数据管理",
        "data_subtitle": "上传自有商品和竞品价格 CSV，系统会在当前会话中同步到所有页面。",
        "executive": "今日价格洞察",
        "self_products": "自有商品",
        "matched_products": "匹配商品",
        "competitor_records": "条竞品记录",
        "match_count": "建议跟价",
        "rule_passed": "满足价差与利润规则",
        "uncertain": "无法判断",
        "need_data": "需要补充数据",
        "current_scope": "当前分析范围",
        "dedup_note": "匹配记录可能包含同一商品在多个平台或多个日期的记录，顶部指标按商品去重。",
        "priority": "优先处理商品",
        "match_badge": "建议跟价",
        "observe_badge": "继续观察",
        "uncertain_badge": "需要确认",
        "competitor_final": "竞品最终可比价",
        "our_final": "我方最终可比价",
        "price_gap": "价格差异",
        "margin_after": "跟价后利润率",
        "market_trend": "竞品最终可比价格趋势",
        "trend_note": "按平台/商品展示每日最低最终可比价格；模拟数据仅用于演示。",
        "distribution": "跟价建议分布",
        "rules": "规则摘要",
        "rules_text_1": "同款匹配成功后，系统比较双方最终可比价格，并检查跟价后的利润率是否达到最低要求。",
        "rules_text_2": "价格差异使用含运费和税费的到手口径；利润率会扣除我方运费和税费。",
        "filter_product": "筛选商品",
        "all_products": "全部商品",
        "amount_note": "金额单位：USD。跟价后净价 = 竞品最终可比价 − 我方运费 − 我方税费。",
        "download_csv": "下载当前 CSV",
        "download_report": "下载分析报告",
        "agent_note": "当前 Agent 会读取本次会话中的分析结果，不会回到旧的模拟数据。",
        "question": "输入问题",
        "run_agent": "运行 Agent",
        "agent_spinner": "Agent 正在读取当前分析结果并调用价格工具…",
        "final_answer": "最终分析",
        "trace": "查看 Agent 调用过程",
        "agent_offline_title": "Agent 尚未连接",
        "agent_offline_note": "在项目根目录的 .env 中配置 GEMINI_API_KEY，然后重启 Streamlit。Dashboard 和价格计算不受影响。",
        "import_data": "更新分析数据",
        "own_csv": "自有商品 CSV",
        "competitor_csv": "竞品价格 CSV",
        "apply_upload": "应用上传数据",
        "upload_both": "请同时上传两个 CSV 文件。",
        "data_updated": "数据已更新，概览、商品明细和 Agent 页面会使用这批数据。",
        "data_failed": "数据校验失败",
        "reset_demo": "恢复内置模拟数据",
        "demo_restored": "已恢复内置模拟数据。",
        "preview": "当前数据预览",
        "own_products": "自有商品",
        "competitors": "竞品价格",
    },
    "en": {
        "language": "Language / 语言",
        "zh": "中文",
        "en": "English",
        "us_market": "US market · USD",
        "nav_hint": "Use the sidebar to switch pages",
        "simulated": "SIMULATED DATA",
        "overview": "Cross-border price monitoring",
        "overview_subtitle": "Make every price-match decision with product, landed-price, and margin evidence.",
        "details": "Product details",
        "details_subtitle": "Inspect product matching, comparable prices, margin, and recommendation evidence.",
        "agent": "Agent workbench",
        "agent_subtitle": "Gemini understands the question; local Python tools own the facts and calculations.",
        "data": "Data management",
        "data_subtitle": "Upload owned-product and competitor CSV files and sync them across this session.",
        "executive": "Today’s pricing insight",
        "self_products": "Owned products",
        "matched_products": "Matched products",
        "competitor_records": "competitor records",
        "match_count": "Price-match advice",
        "rule_passed": "Gap and margin rules passed",
        "uncertain": "Needs review",
        "need_data": "More data required",
        "current_scope": "Current scope",
        "dedup_note": "Records may include multiple platforms or dates for one product; headline metrics are deduplicated by product.",
        "priority": "Priority action",
        "match_badge": "MATCH",
        "observe_badge": "OBSERVE",
        "uncertain_badge": "REVIEW",
        "competitor_final": "Competitor landed price",
        "our_final": "Our landed price",
        "price_gap": "Price gap",
        "margin_after": "Post-match margin",
        "market_trend": "Competitor landed-price trend",
        "trend_note": "Daily minimum landed price by platform/product; simulated data for demonstration only.",
        "distribution": "Recommendation distribution",
        "rules": "Rule summary",
        "rules_text_1": "After a same-product match, the system compares landed prices and checks the post-match margin against the minimum requirement.",
        "rules_text_2": "Price gap uses shipping-and-tax-inclusive landed prices; margin deducts our shipping and tax costs.",
        "filter_product": "Filter product",
        "all_products": "All products",
        "amount_note": "Currency: USD. Post-match net price = competitor landed price − our shipping − our tax.",
        "download_csv": "Download current CSV",
        "download_report": "Download analysis report",
        "agent_note": "The Agent reads the current session analysis result rather than falling back to old demo data.",
        "question": "Ask a question",
        "run_agent": "Run Agent",
        "agent_spinner": "Agent is reading the current analysis and calling the pricing tool…",
        "final_answer": "Final analysis",
        "trace": "View Agent tool trace",
        "agent_offline_title": "Agent not connected",
        "agent_offline_note": "Add GEMINI_API_KEY to .env in the project root and restart Streamlit. The dashboard and calculations still work offline.",
        "import_data": "Update analysis data",
        "own_csv": "Owned products CSV",
        "competitor_csv": "Competitor prices CSV",
        "apply_upload": "Apply uploaded data",
        "upload_both": "Please upload both CSV files.",
        "data_updated": "Data updated. Overview, product details, and Agent pages now use this dataset.",
        "data_failed": "Data validation failed",
        "reset_demo": "Restore demo data",
        "demo_restored": "Demo data restored.",
        "preview": "Current data preview",
        "own_products": "Owned products",
        "competitors": "Competitor prices",
    },
}


def current_language() -> str:
    return st.session_state.get("language", "zh")


def t(key: str) -> str:
    return TRANSLATIONS[current_language()].get(key, key)


def recommendation_label(value: object) -> str:
    labels = {
        "zh": {"match": "建议跟价", "observe": "观察", "do_not_match": "不建议跟价", "uncertain": "无法判断"},
        "en": {"match": "MATCH", "observe": "OBSERVE", "do_not_match": "DO NOT MATCH", "uncertain": "REVIEW"},
    }
    return labels[current_language()].get(str(value), str(value))


def reason_label(value: object) -> str:
    reasons = {
        "同品牌、同商品名和同规格已匹配，且跟价后利润率达标。": {"zh": "同品牌、同商品名和同规格已匹配，且跟价后利润率达标。", "en": "Brand, product name, and size match; post-match margin meets the requirement."},
        "同款已匹配，但价格差异未达到 10% 跟价阈值。": {"zh": "同款已匹配，但价格差异未达到 10% 跟价阈值。", "en": "The same product is matched, but the price gap is below the 10% threshold."},
        "跟价后利润率低于最低要求。": {"zh": "跟价后利润率低于最低要求。", "en": "Post-match margin is below the minimum requirement."},
        "无法确认同款或缺少关键价格数据。": {"zh": "无法确认同款或缺少关键价格数据。", "en": "The same product is uncertain or key price data is missing."},
    }
    return reasons.get(str(value), {}).get(current_language(), str(value))


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root { --ink:#f4fbf7; --muted:#99b3ad; --line:rgba(193,251,212,.16); --mint:#c1fbd4; --pistachio:#d4f9e0; --surface:#1e2c31; }
        [data-testid="stAppViewContainer"] { background:#000; background-image:radial-gradient(circle at 88% 2%,rgba(193,251,212,.10),transparent 27rem),radial-gradient(circle at 3% 30%,rgba(30,44,49,.50),transparent 25rem); color:var(--ink); }
        [data-testid="stHeader"] { background:transparent; }
        [data-testid="stSidebar"] { background:#0a0a0a; border-right:1px solid var(--line); }
        [data-testid="stSidebar"] * { color:var(--ink); }
        .block-container { max-width:1480px; padding:2.2rem 3.4rem 4rem; }
        .brand { display:flex; align-items:center; gap:.65rem; margin:.4rem 0 1.4rem; }
        .brand-mark { width:38px; height:38px; border-radius:9999px; background:var(--mint); display:grid; place-items:center; color:#000; font-weight:850; }
        .brand-name { font-weight:750; font-size:1.05rem; }
        .brand-sub { color:#99b3ad; font-size:.72rem; }
        .hero { padding:1.7rem 2rem 1.8rem; border:1px solid rgba(193,251,212,.20); border-radius:20px; background:linear-gradient(112deg,#0a0a0a,#101616 55%,#0d1c1d); box-shadow:0 24px 70px rgba(0,0,0,.24); margin-bottom:1.2rem; }
        .hero-top { display:flex; justify-content:space-between; align-items:center; gap:1rem; }
        .eyebrow,.section-kicker { color:var(--mint); font-size:.72rem; letter-spacing:.15em; font-weight:700; text-transform:uppercase; }
        .hero h1 { color:#fff; font-family:"Helvetica Neue",Helvetica,Arial,sans-serif; font-size:2.55rem; font-weight:350; letter-spacing:-.045em; margin:.45rem 0 .35rem; }
        .hero p { color:#b8c9c1; margin:0; font-size:1rem; }
        .live-pill { border:1px solid rgba(193,251,212,.35); color:var(--mint); background:rgba(193,251,212,.08); border-radius:999px; padding:.46rem .76rem; font-size:.78rem; white-space:nowrap; }
        .metric-card { background:linear-gradient(145deg,rgba(30,44,49,.92),rgba(10,10,10,.96)); border:1px solid var(--line); border-radius:12px; padding:1.1rem 1.15rem; min-height:118px; box-shadow:0 12px 28px rgba(0,0,0,.22); }
        .metric-card:before { content:""; display:block; width:32px; height:3px; border-radius:99px; margin-bottom:.8rem; background:var(--mint); }
        .metric-label { color:var(--muted); font-size:.82rem; }.metric-value { color:#fff; font-size:1.75rem; font-weight:750; letter-spacing:-.04em; margin:.25rem 0; }.metric-detail { color:#829b93; font-size:.76rem; }
        .section-title { color:#fff; font-size:1.28rem; font-weight:650; margin:.25rem 0 1rem; }.section-kicker { margin-top:1.3rem; font-size:.68rem; }
        .focus-card { border:1px solid rgba(193,251,212,.25); border-radius:12px; background:linear-gradient(135deg,rgba(30,44,49,.96),rgba(10,10,10,.98)); padding:1.25rem 1.35rem; min-height:190px; }
        .focus-title { color:#fff; font-size:1.1rem; font-weight:720; }.focus-meta { color:var(--muted); font-size:.84rem; margin-top:.25rem; }.focus-price { color:#fff; font-size:2rem; font-weight:780; margin:.7rem 0 .25rem; }.focus-price span { color:var(--mint); font-size:.85rem; font-weight:600; margin-left:.35rem; }.focus-note,.data-note { color:#9bb1a8; font-size:.8rem; line-height:1.55; }.data-note { font-size:.78rem; padding:.65rem 0 .2rem; }
        .badge { display:inline-block; border-radius:999px; padding:.28rem .62rem; font-size:.73rem; font-weight:700; }.badge-match { color:#c1fbd4; background:rgba(193,251,212,.14); border:1px solid rgba(193,251,212,.28); }.badge-observe { color:#f6d38b; background:rgba(246,211,139,.13); border:1px solid rgba(246,211,139,.28); }.badge-uncertain { color:#cbd5e1; background:rgba(148,163,184,.13); border:1px solid rgba(148,163,184,.24); }
        div[data-testid="stTabs"] button { color:#99b3ad; font-weight:650; } div[data-testid="stTabs"] button[aria-selected="true"] { color:#fff; }
        .stButton > button,.stDownloadButton > button { border-radius:9999px; border:1px solid rgba(193,251,212,.45); background:var(--mint); color:#000; font-weight:650; padding:.55rem 1.2rem; }.stButton > button:hover,.stDownloadButton > button:hover { border-color:#fff; background:var(--pistachio); color:#000; }
        div[data-testid="stFileUploader"] { border:1px dashed rgba(193,251,212,.25); border-radius:12px; padding:.25rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            '<div class="brand"><div class="brand-mark">PM</div><div><div class="brand-name">Price Match</div><div class="brand-sub">Pricing intelligence</div></div></div>',
            unsafe_allow_html=True,
        )
        selected = st.selectbox(
            t("language"),
            ["中文", "English"],
            index=0 if current_language() == "zh" else 1,
        )
        st.session_state.language = "en" if selected == "English" else "zh"
        st.caption(t("us_market"))
        st.caption(t("nav_hint"))


def render_hero(title: str, subtitle: str, eyebrow: str = "CROSS-BORDER PRICING INTELLIGENCE") -> None:
    st.markdown(
        f'<div class="hero"><div class="hero-top"><div class="eyebrow">{escape(eyebrow)}</div><div class="live-pill">● {escape(t("simulated"))}</div></div><h1>{escape(title)}</h1><p>{escape(subtitle)}</p></div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, detail: str) -> str:
    return f'<div class="metric-card"><div class="metric-label">{escape(label)}</div><div class="metric-value">{escape(value)}</div><div class="metric-detail">{escape(detail)}</div></div>'
