from __future__ import annotations

import os
from typing import Any

import pandas as pd
from dotenv import load_dotenv

from src.tools.price_tools import calculate_price_recommendation_from_analysis


load_dotenv()


SYSTEM_INSTRUCTIONS = """
你是跨境电商 Price Match Agent。

当用户询问具体商品、平台和竞品价格时，必须调用
calculate_price_recommendation 工具。这个工具会依次完成同款匹配、竞品价格查询、
最终可比价格、价格差异率、利润率和跟价规则判断。

严格规则：
1. 不要自行计算价格、利润率或价格差异率，只能使用工具返回的数字。
2. 如果 match_status 不是 matched，必须输出 uncertain，不得建议跟价。
3. 如果工具返回数据不足，必须说明缺少哪些数据，不得编造价格或利润率。
4. 最终可比价格用于消费者价格比较；利润率使用跟价后的到手价扣除我方运费和税费。
5. 只返回一份最终结果，避免重复查询或重复结论。
6. 只能使用当前 Streamlit 分析结果；如果数据来自 simulated_data，必须说明它不是实时平台价格。
""".strip()


def _build_analysis_tool(analysis: pd.DataFrame, steps: list[dict[str, Any]]):
    """Create a tool bound to the current uploaded/analyzed dataset."""

    def calculate_price_recommendation(
        product_id: str,
        platform: str,
        competitor_product_name: str,
        competitor_size_ml: float,
    ) -> dict[str, Any]:
        result = calculate_price_recommendation_from_analysis(
            analysis=analysis,
            product_id=product_id,
            platform=platform,
            competitor_product_name=competitor_product_name,
            competitor_size_ml=competitor_size_ml,
        )
        steps.append(
            {
                "step": "tool_call",
                "tool": "calculate_price_recommendation",
                "arguments": {
                    "product_id": product_id,
                    "platform": platform,
                    "competitor_product_name": competitor_product_name,
                    "competitor_size_ml": competitor_size_ml,
                },
                "source": "current_streamlit_analysis",
                "result": result,
            }
        )
        return result

    calculate_price_recommendation.__name__ = "calculate_price_recommendation"
    calculate_price_recommendation.__doc__ = (
        "根据当前上传 CSV 的分析结果，执行同款匹配、价格差异、利润率和跟价规则。"
        "所有数字由 Python 计算，不读取独立的模拟数据。"
    )
    return calculate_price_recommendation


def run_agent(
    question: str, analysis: pd.DataFrame, language: str = "zh"
) -> tuple[str, list[dict[str, Any]]]:
    """Run Gemini with a tool bound to the current Streamlit analysis result."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "未检测到 GEMINI_API_KEY。请在 .env 中填入 Google AI Studio API Key。"
        )

    # Google 官方新 Python SDK：google-genai。
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    steps: list[dict[str, Any]] = []
    analysis_tool = _build_analysis_tool(analysis, steps)
    language_instruction = (
        "请使用中文回答用户，保留 recommendation、match_status 等字段名。"
        if language != "en"
        else "Answer the user entirely in English. Keep field names such as recommendation and match_status when useful."
    )

    response = client.models.generate_content(
        model=model,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=f"{SYSTEM_INSTRUCTIONS}\n{language_instruction}",
            # SDK 会把这个 Python 函数转换为工具声明，并在模型请求时调用它。
            # 计算仍然发生在本地 Python，不交给模型心算。
            tools=[analysis_tool],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                maximum_remote_calls=2
            ),
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini 没有返回可读文本，请检查模型名称或 API 配额。")
    steps.insert(
        0,
        {
            "step": "agent_request",
            "model": model,
            "data_source": "current_streamlit_analysis",
        },
    )
    return response.text, steps
