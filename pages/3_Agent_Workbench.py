from __future__ import annotations

import os

import streamlit as st

from src.agent import run_agent
from src.dashboard_logic import analyze
from src.state import get_data
from src.ui import apply_theme, render_hero, render_sidebar, t, current_language


st.set_page_config(page_title="Agent 工作台 · Price Match", page_icon="✦", layout="wide")
apply_theme()
render_sidebar()
products, competitors = get_data()
result = analyze(products, competitors)

render_hero(t("agent"), t("agent_subtitle"), "TOOL-CALLING ASSISTANT")

if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
    st.markdown(f'<div class="data-note">{t("agent_note")}</div>', unsafe_allow_html=True)
    question = st.text_area(
        t("question"),
        value=(
            "Analyze whether P001 should match Amazon US Vitamin C Serum 30 ml."
            if current_language() == "en"
            else "分析 P001 在 Amazon US 的 Vitamin C Serum 30 ml 是否值得跟价。"
        ),
        height=130,
    )
    if st.button(t("run_agent")):
        try:
            with st.spinner(t("agent_spinner")):
                answer, steps = run_agent(question, result, current_language())
            st.markdown(f'<div class="section-kicker">Final answer</div><div class="section-title">{t("final_answer")}</div>', unsafe_allow_html=True)
            st.write(answer)
            with st.expander(t("trace")):
                for step in steps:
                    st.json(step)
        except Exception as error:
            st.error(str(error))
else:
    st.markdown(
        f'<div class="focus-card"><div class="focus-title">{t("agent_offline_title")}</div><div class="focus-note">{t("agent_offline_note")}</div></div>',
        unsafe_allow_html=True,
    )
