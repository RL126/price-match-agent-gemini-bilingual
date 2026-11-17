from __future__ import annotations

import pandas as pd


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return " ".join(str(value).lower().strip().split())


def analyze(products: pd.DataFrame, competitors: pd.DataFrame) -> pd.DataFrame:
    products = products.copy()
    competitors = competitors.copy()
    required_products = {
        "product_id", "brand", "product_name", "size_ml", "cost_price",
        "our_price", "minimum_margin_rate",
    }
    required_competitors = {
        "platform", "brand", "competitor_product_name", "size_ml",
        "listed_price", "discount_price", "shipping_fee", "tax_fee",
    }
    missing_products = required_products - set(products.columns)
    missing_competitors = required_competitors - set(competitors.columns)
    if missing_products or missing_competitors:
        raise ValueError(
            f"自有商品缺少字段：{sorted(missing_products)}；"
            f"竞品数据缺少字段：{sorted(missing_competitors)}"
        )

    for column in ["our_shipping_fee", "our_tax_fee"]:
        if column not in products.columns:
            products[column] = 0.0

    products["brand_key"] = products["brand"].map(normalize_text)
    products["name_key"] = products["product_name"].map(normalize_text)
    competitors["brand_key"] = competitors["brand"].map(normalize_text)
    competitors["name_key"] = competitors["competitor_product_name"].map(normalize_text)
    result = products.merge(
        competitors,
        on=["brand_key", "name_key", "size_ml"],
        how="left",
        suffixes=("_our", "_competitor"),
    )
    result["match_status"] = result["platform"].notna().map(
        {True: "matched", False: "uncertain"}
    )
    result["match_score"] = result["match_status"].map(
        {"matched": 1.0, "uncertain": 0.0}
    )
    result["competitor_price"] = result["discount_price"].fillna(
        result["listed_price"]
    )
    result["final_comparable_price"] = (
        result["competitor_price"] + result["shipping_fee"] + result["tax_fee"]
    ).round(2)
    result["our_final_comparable_price"] = (
        result["our_price"] + result["our_shipping_fee"] + result["our_tax_fee"]
    ).round(2)
    result["matched_net_price"] = (
        result["final_comparable_price"]
        - result["our_shipping_fee"]
        - result["our_tax_fee"]
    ).round(2)
    result["price_gap_rate"] = (
        (result["our_final_comparable_price"] - result["final_comparable_price"])
        / result["final_comparable_price"]
    ).round(4)
    result["margin_after_match"] = (
        (result["matched_net_price"] - result["cost_price"])
        / result["matched_net_price"]
    ).where(result["matched_net_price"] > 0).round(4)

    def recommendation(row: pd.Series) -> str:
        if row["match_status"] != "matched":
            return "uncertain"
        if (
            pd.isna(row["final_comparable_price"])
            or pd.isna(row["cost_price"])
            or pd.isna(row["margin_after_match"])
        ):
            return "uncertain"
        if row["margin_after_match"] < row["minimum_margin_rate"]:
            return "do_not_match"
        if row["price_gap_rate"] >= 0.10:
            return "match"
        return "observe"

    result["recommendation"] = result.apply(recommendation, axis=1)
    reasons = {
        "match": "同品牌、同商品名和同规格已匹配，且跟价后利润率达标。",
        "observe": "同款已匹配，但价格差异未达到 10% 跟价阈值。",
        "do_not_match": "跟价后利润率低于最低要求。",
        "uncertain": "无法确认同款或缺少关键价格数据。",
    }
    result["reason"] = result["recommendation"].map(reasons)
    return result


def build_price_trend(competitors: pd.DataFrame) -> pd.DataFrame:
    if "collected_at" not in competitors.columns:
        return pd.DataFrame()
    trend = competitors.copy()
    trend["collected_at"] = pd.to_datetime(trend["collected_at"], errors="coerce")
    trend["item_price"] = trend["discount_price"].fillna(trend["listed_price"])
    trend["final_comparable_price"] = (
        trend["item_price"] + trend["shipping_fee"] + trend["tax_fee"]
    ).round(2)
    trend = trend.dropna(subset=["collected_at", "final_comparable_price"])
    if trend.empty:
        return pd.DataFrame()
    trend["series"] = (
        trend["platform"].astype(str)
        + " / "
        + trend["competitor_product_name"].astype(str)
    )
    trend = trend.groupby(["collected_at", "series"], as_index=False)[
        "final_comparable_price"
    ].min()
    return trend.pivot(
        index="collected_at", columns="series", values="final_comparable_price"
    ).sort_index()


def build_markdown_report(result: pd.DataFrame, language: str = "zh") -> str:
    english = language == "en"
    reason_map = {
        "同品牌、同商品名和同规格已匹配，且跟价后利润率达标。": "Brand, product name, and size match; post-match margin meets the requirement.",
        "同款已匹配，但价格差异未达到 10% 跟价阈值。": "The same product is matched, but the price gap is below the 10% threshold.",
        "跟价后利润率低于最低要求。": "Post-match margin is below the minimum requirement.",
        "无法确认同款或缺少关键价格数据。": "The same product is uncertain or key price data is missing.",
    }
    report_rows = (
        result.sort_values("final_comparable_price", na_position="last")
        .drop_duplicates("product_id")
    )
    if english:
        lines = [
            "# Price Match Analysis Report", "",
            "> Source: CSV/demo data; not live marketplace pricing.", "",
            f"- Owned products: {result['product_id'].nunique()}",
            f"- Matched products: {result.loc[result['match_status'] == 'matched', 'product_id'].nunique()}",
            f"- Products recommended for matching: {result.loc[result['recommendation'] == 'match', 'product_id'].nunique()}",
            "", "## Product conclusions", "",
        ]
    else:
        lines = [
            "# Price Match 分析报告", "",
            "> 数据来源：CSV/模拟数据；不代表实时平台价格。", "",
            f"- 自有商品数：{result['product_id'].nunique()}",
            f"- 匹配商品数：{result.loc[result['match_status'] == 'matched', 'product_id'].nunique()}",
            f"- 建议跟价商品数：{result.loc[result['recommendation'] == 'match', 'product_id'].nunique()}",
            "", "## 商品结论", "",
        ]
    for _, row in report_rows.iterrows():
        final_price = f"${row['final_comparable_price']:.2f}" if pd.notna(row["final_comparable_price"]) else "无法计算"
        gap = f"{row['price_gap_rate']:.1%}" if pd.notna(row["price_gap_rate"]) else "无法计算"
        margin = f"{row['margin_after_match']:.1%}" if pd.notna(row["margin_after_match"]) else "无法计算"
        if english:
            lines.extend([
                f"### {row['product_id']} — {row['product_name']}",
                f"- Platform: {row.get('platform', '-')}",
                f"- Competitor landed price: {final_price}",
                f"- Price gap: {gap}",
                f"- Post-match margin: {margin}",
                f"- Recommendation: {row['recommendation']}",
                f"- Evidence: {reason_map.get(str(row['reason']), row['reason'])}", "",
            ])
        else:
            lines.extend([
                f"### {row['product_id']} — {row['product_name']}",
                f"- 平台：{row.get('platform', '-')}",
                f"- 竞品最终可比价格：{final_price}",
                f"- 价格差异率：{gap}",
                f"- 跟价后利润率：{margin}",
                f"- 建议：{row['recommendation']}",
                f"- 依据：{row['reason']}", "",
            ])
    return "\n".join(lines)


def money(value: object) -> str:
    return f"${float(value):,.2f}" if pd.notna(value) else "—"


def percent(value: object) -> str:
    return f"{float(value):.1%}" if pd.notna(value) else "—"
