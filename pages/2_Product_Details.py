from __future__ import annotations

import streamlit as st

from src.dashboard_logic import analyze, build_markdown_report, percent
from src.state import get_data
from src.ui import apply_theme, current_language, reason_label, recommendation_label, render_hero, render_sidebar, t


st.set_page_config(page_title="商品明细 · Price Match", page_icon="✦", layout="wide")
apply_theme()
render_sidebar()
products, competitors = get_data()
result = analyze(products, competitors)

render_hero(t("details"), t("details_subtitle"), "PRODUCT-LEVEL ANALYSIS")

product_options = [t("all_products")] + sorted(result["product_id"].dropna().astype(str).unique().tolist())
selected_product = st.selectbox(t("filter_product"), product_options)
filtered = result if selected_product == t("all_products") else result[result["product_id"].astype(str) == selected_product]

display_columns = [
    "product_id", "product_name", "platform", "our_final_comparable_price",
    "final_comparable_price", "matched_net_price", "price_gap_rate",
    "margin_after_match", "recommendation", "reason",
]
display = filtered[display_columns].copy()
display["price_gap_rate"] = display["price_gap_rate"].map(percent)
display["margin_after_match"] = display["margin_after_match"].map(percent)
display["recommendation"] = display["recommendation"].map(recommendation_label)
display["reason"] = display["reason"].map(reason_label)
column_names = {
    "product_id": "Product ID" if current_language() == "en" else "商品ID",
    "product_name": "Product" if current_language() == "en" else "商品",
    "platform": "Platform" if current_language() == "en" else "平台",
    "our_final_comparable_price": "Our landed price" if current_language() == "en" else "我方最终可比价",
    "final_comparable_price": "Competitor landed price" if current_language() == "en" else "竞品最终可比价",
    "matched_net_price": "Post-match net price" if current_language() == "en" else "跟价后净价",
    "price_gap_rate": "Price gap" if current_language() == "en" else "价格差异率",
    "margin_after_match": "Post-match margin" if current_language() == "en" else "跟价后利润率",
    "recommendation": "Recommendation" if current_language() == "en" else "建议",
    "reason": "Evidence" if current_language() == "en" else "依据",
}
display = display.rename(columns=column_names)
st.dataframe(display, hide_index=True)
st.caption(t("amount_note"))

csv_data = filtered.to_csv(index=False).encode("utf-8-sig")
report_data = build_markdown_report(filtered, current_language()).encode("utf-8")
download_col1, download_col2 = st.columns(2)
with download_col1:
    st.download_button(t("download_csv"), data=csv_data, file_name="price_match_analysis.csv", mime="text/csv")
with download_col2:
    st.download_button(t("download_report"), data=report_data, file_name="price_match_report.md", mime="text/markdown")
