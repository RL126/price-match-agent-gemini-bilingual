from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard_logic import analyze
from src.state import get_data, reset_demo_data, set_data
from src.ui import apply_theme, render_hero, render_sidebar, t


st.set_page_config(page_title="数据管理 · Price Match", page_icon="✦", layout="wide")
apply_theme()
render_sidebar()

render_hero(t("data"), t("data_subtitle"), "DATA MANAGEMENT")

current_products, current_competitors = get_data()
st.markdown(f'<div class="section-kicker">Import data</div><div class="section-title">{t("import_data")}</div>', unsafe_allow_html=True)
products_file = st.file_uploader(t("own_csv"), type="csv", key="products_upload")
competitors_file = st.file_uploader(t("competitor_csv"), type="csv", key="competitors_upload")

if st.button(t("apply_upload")):
    if products_file is None or competitors_file is None:
        st.warning(t("upload_both"))
    else:
        try:
            new_products = pd.read_csv(products_file)
            new_competitors = pd.read_csv(competitors_file)
            analyze(new_products, new_competitors)
            set_data(new_products, new_competitors)
            current_products, current_competitors = new_products, new_competitors
            st.success(t("data_updated"))
        except Exception as error:
            st.error(f"{t('data_failed')}：{error}")

if st.button(t("reset_demo")):
    reset_demo_data()
    current_products, current_competitors = get_data()
    st.success(t("demo_restored"))

st.markdown(f'<div class="section-kicker">Current dataset</div><div class="section-title">{t("preview")}</div>', unsafe_allow_html=True)
preview_col1, preview_col2 = st.columns(2)
with preview_col1:
    st.markdown(f"**{t('own_products')}**")
    st.dataframe(current_products.head(8), hide_index=True)
with preview_col2:
    st.markdown(f"**{t('competitors')}**")
    st.dataframe(current_competitors.head(8), hide_index=True)
