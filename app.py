from __future__ import annotations

import streamlit as st

from src.dashboard_logic import analyze, build_price_trend, money, percent
from src.state import get_data
from src.ui import apply_theme, metric_card, render_hero, render_sidebar, t


st.set_page_config(
    page_title="Price Match Agent",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
render_sidebar()

products, competitors = get_data()
result = analyze(products, competitors)
summary = (
    result.sort_values("final_comparable_price", na_position="last")
    .drop_duplicates("product_id")
)
matched_rows = result[result["match_status"] == "matched"]
matched_product_count = int(matched_rows["product_id"].nunique())
matched_listing_count = len(matched_rows)
match_count = int(result.loc[result["recommendation"] == "match", "product_id"].nunique())
uncertain_count = int(result.loc[result["recommendation"] == "uncertain", "product_id"].nunique())

render_hero(
    t("overview"),
    t("overview_subtitle"),
)
st.markdown(
    f'<div class="section-kicker">Executive overview</div><div class="section-title">{t("executive")}</div>',
    unsafe_allow_html=True,
)

kpi_cols = st.columns(4)
kpi_cards = [
    (t("self_products"), str(products["product_id"].nunique()), t("current_scope")),
    (t("matched_products"), str(matched_product_count), f"{matched_listing_count} {t('competitor_records')}"),
    (t("match_count"), str(match_count), t("rule_passed")),
    (t("uncertain"), str(uncertain_count), t("need_data")),
]
for column, (label, value, detail) in zip(kpi_cols, kpi_cards):
    with column:
        st.markdown(metric_card(label, value, detail), unsafe_allow_html=True)

st.markdown(
    f'<div class="data-note">{t("dedup_note")}</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1.05, 1.45])
with left:
    st.markdown(f'<div class="section-kicker">Priority action</div><div class="section-title">{t("priority")}</div>', unsafe_allow_html=True)
    focus_rows = summary[summary["recommendation"] == "match"]
    focus = focus_rows.iloc[0] if not focus_rows.empty else summary.iloc[0]
    focus_status = str(focus.get("recommendation", "uncertain"))
    badge_class = {"match": "badge-match", "observe": "badge-observe"}.get(focus_status, "badge-uncertain")
    badge_label = {"match": t("match_badge"), "observe": t("observe_badge")}.get(focus_status, t("uncertain_badge"))
    st.markdown(
        f"""
        <div class="focus-card">
            <span class="badge {badge_class}">{badge_label}</span>
            <div class="focus-title" style="margin-top:.8rem">{focus.get('product_name', '—')}</div>
            <div class="focus-meta">{focus.get('product_id', '—')} · {focus.get('platform', '—')} · {focus.get('size_ml', '—')} ml</div>
            <div class="focus-price">{money(focus.get('final_comparable_price'))}<span>{t('competitor_final')}</span></div>
            <div class="focus-note">{t('our_final')} {money(focus.get('our_final_comparable_price'))} · {t('price_gap')} {percent(focus.get('price_gap_rate'))} · {t('margin_after')} {percent(focus.get('margin_after_match'))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(f'<div class="section-kicker">Market movement</div><div class="section-title">{t("market_trend")}</div>', unsafe_allow_html=True)
    trend = build_price_trend(competitors)
    if trend.empty:
        st.info("当前 CSV 没有可用的 collected_at 日期，暂时无法绘制趋势。")
    else:
        st.line_chart(trend)
        st.markdown(f'<div class="data-note">{t("trend_note")}</div>', unsafe_allow_html=True)

st.markdown(f'<div class="section-kicker">Decision distribution</div><div class="section-title">{t("distribution")}</div>', unsafe_allow_html=True)
chart_col, note_col = st.columns([1.45, 1])
with chart_col:
    st.bar_chart(result["recommendation"].value_counts())
with note_col:
    st.markdown(
        """
        <div class="focus-card">
            <div class="focus-title">{t('rules')}</div>
            <div class="focus-note" style="margin-top:.75rem">{t('rules_text_1')}</div>
            <div class="focus-note" style="margin-top:.65rem">{t('rules_text_2')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
