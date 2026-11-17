from __future__ import annotations

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.demo_data import demo_competitors, demo_products


load_dotenv()


def get_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    if "products_df" not in st.session_state:
        st.session_state.products_df = demo_products()
    if "competitors_df" not in st.session_state:
        st.session_state.competitors_df = demo_competitors()
    return st.session_state.products_df, st.session_state.competitors_df


def set_data(products: pd.DataFrame, competitors: pd.DataFrame) -> None:
    st.session_state.products_df = products.copy()
    st.session_state.competitors_df = competitors.copy()


def reset_demo_data() -> None:
    set_data(demo_products(), demo_competitors())
