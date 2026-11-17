from __future__ import annotations

from typing import Any

from src.demo_data import demo_competitors, demo_products


def _text(value: Any) -> str:
    return " ".join(str(value).lower().strip().split())


def _json_value(value: Any) -> Any:
    """Convert pandas/numpy scalar values into JSON-safe Python values."""
    if value is None:
        return None
    try:
        if value != value:  # NaN
            return None
    except (TypeError, ValueError):
        pass
    return value.item() if hasattr(value, "item") else value


def _product(product_id: str) -> dict[str, Any] | None:
    rows = demo_products().to_dict(orient="records")
    return next((row for row in rows if row["product_id"] == product_id), None)


def _competitor_rows(
    platform: str, competitor_product_name: str, size_ml: float
) -> list[dict[str, Any]]:
    rows = demo_competitors().to_dict(orient="records")
    return [
        row
        for row in rows
        if _text(row["platform"]) == _text(platform)
        and _text(row["competitor_product_name"]) == _text(competitor_product_name)
        and float(row["size_ml"]) == float(size_ml)
    ]


def match_product(
    product_id: str,
    platform: str,
    competitor_product_name: str,
    competitor_size_ml: float,
) -> dict[str, Any]:
    """Match an owned product to a competitor listing using deterministic rules."""
    own = _product(product_id)
    if own is None:
        return {
            "match_status": "uncertain",
            "product_id": product_id,
            "evidence": "Unknown product_id.",
        }

    rows = _competitor_rows(platform, competitor_product_name, competitor_size_ml)
    if not rows:
        return {
            "match_status": "unmatched",
            "product_id": product_id,
            "platform": platform,
            "competitor_product_name": competitor_product_name,
            "evidence": "No competitor record matched the platform, name, and size.",
        }

    row = rows[0]
    same_brand = _text(own["brand"]) == _text(row["brand"])
    same_name = _text(own["product_name"]) == _text(row["competitor_product_name"])
    same_size = float(own["size_ml"]) == float(row["size_ml"])
    status = "matched" if same_brand and same_name and same_size else "uncertain"
    score = round(
        (0.4 if same_brand else 0)
        + (0.4 if same_name else 0)
        + (0.2 if same_size else 0),
        2,
    )
    return {
        "match_status": status,
        "product_id": product_id,
        "platform": platform,
        "competitor_product_name": competitor_product_name,
        "match_score": score,
        "same_brand": same_brand,
        "same_name": same_name,
        "same_size": same_size,
        "evidence": "Brand, normalized product name, and size were compared by code.",
    }


def get_competitor_price(
    platform: str, competitor_product_name: str, size_ml: float
) -> dict[str, Any]:
    """Return the lowest final comparable price among matching simulated listings."""
    rows = _competitor_rows(platform, competitor_product_name, size_ml)
    if not rows:
        return {
            "status": "not_found",
            "platform": platform,
            "competitor_product_name": competitor_product_name,
        }

    enriched = []
    for row in rows:
        item_price = row["discount_price"] or row["listed_price"]
        final_price = round(item_price + row["shipping_fee"] + row["tax_fee"], 2)
        enriched.append({**row, "competitor_price": item_price, "final_comparable_price": final_price})
    selected = min(enriched, key=lambda row: row["final_comparable_price"])
    return {
        "status": "found",
        "platform": selected["platform"],
        "competitor_product_name": selected["competitor_product_name"],
        "brand": selected["brand"],
        "size_ml": selected["size_ml"],
        "competitor_price": selected["competitor_price"],
        "shipping_fee": selected["shipping_fee"],
        "tax_fee": selected["tax_fee"],
        "final_comparable_price": selected["final_comparable_price"],
        "records_found": len(rows),
        "collected_at": selected["collected_at"],
        "source": "simulated_data",
    }


def calculate_price_recommendation(
    product_id: str,
    platform: str,
    competitor_product_name: str,
    competitor_size_ml: float,
) -> dict[str, Any]:
    """Run the deterministic match, price, gap, and margin rules."""
    own = _product(product_id)
    match = match_product(product_id, platform, competitor_product_name, competitor_size_ml)
    if own is None or match["match_status"] != "matched":
        return {"match": match, "recommendation": "uncertain"}

    price = get_competitor_price(platform, competitor_product_name, competitor_size_ml)
    if price["status"] != "found":
        return {"match": match, "price": price, "recommendation": "uncertain"}

    competitor_price = price["competitor_price"]
    our_final_price = own["our_price"] + own["our_shipping_fee"] + own["our_tax_fee"]
    competitor_final_price = price["final_comparable_price"]
    price_gap_rate = round(
        (our_final_price - competitor_final_price) / competitor_final_price, 4
    )
    matched_net_price = competitor_final_price - own["our_shipping_fee"] - own["our_tax_fee"]
    margin_after_match = round(
        (matched_net_price - own["cost_price"]) / matched_net_price, 4
    ) if matched_net_price > 0 else None
    if margin_after_match is None:
        return {
            "match": match,
            "price": price,
            "our_final_comparable_price": round(our_final_price, 2),
            "matched_net_price": round(matched_net_price, 2),
            "recommendation": "uncertain",
            "calculation_note": "跟价后的利润率无法计算：我方到手价扣除运费和税费后不大于 0。",
        }
    if margin_after_match < own["minimum_margin_rate"]:
        recommendation = "do_not_match"
    elif price_gap_rate >= 0.10:
        recommendation = "match"
    else:
        recommendation = "observe"

    return {
        "match": match,
        "price": price,
        "our_final_comparable_price": round(our_final_price, 2),
        "matched_net_price": round(matched_net_price, 2),
        "price_gap_rate": price_gap_rate,
        "margin_after_match": margin_after_match,
        "minimum_margin_rate": own["minimum_margin_rate"],
        "recommendation": recommendation,
        "calculation_note": (
            "税费用于消费者最终价格比较；利润率使用跟价后的到手价扣除我方运费和税费。"
        ),
    }


def calculate_price_recommendation_from_analysis(
    analysis: Any,
    product_id: str,
    platform: str,
    competitor_product_name: str,
    competitor_size_ml: float,
) -> dict[str, Any]:
    """Query the current Streamlit analysis result, not the demo dataset."""
    rows = analysis[
        (analysis["product_id"].astype(str) == str(product_id))
        & (analysis["platform"].map(_text) == _text(platform))
        & (
            analysis["competitor_product_name"].map(_text)
            == _text(competitor_product_name)
        )
        & (analysis["size_ml"].astype(float) == float(competitor_size_ml))
    ].copy()
    if rows.empty:
        return {
            "match": {
                "match_status": "uncertain",
                "product_id": product_id,
                "platform": platform,
                "competitor_product_name": competitor_product_name,
                "evidence": "当前上传数据中没有找到对应的商品、平台和规格。",
            },
            "recommendation": "uncertain",
            "source": "current_streamlit_analysis",
        }

    row = rows.sort_values("final_comparable_price", na_position="last").iloc[0]
    match_status = _json_value(row.get("match_status"))
    result: dict[str, Any] = {
        "match": {
            "match_status": match_status,
            "product_id": _json_value(row.get("product_id")),
            "platform": _json_value(row.get("platform")),
            "competitor_product_name": _json_value(row.get("competitor_product_name")),
            "match_score": _json_value(row.get("match_score")),
            "evidence": "当前上传数据按品牌、标准化名称和规格完成匹配。",
        },
        "price": {
            "competitor_price": _json_value(row.get("competitor_price")),
            "shipping_fee": _json_value(row.get("shipping_fee")),
            "tax_fee": _json_value(row.get("tax_fee")),
            "final_comparable_price": _json_value(row.get("final_comparable_price")),
            "records_found": int(len(rows)),
            "source": "current_streamlit_analysis",
        },
        "our_final_comparable_price": _json_value(row.get("our_final_comparable_price")),
        "matched_net_price": _json_value(row.get("matched_net_price")),
        "price_gap_rate": _json_value(row.get("price_gap_rate")),
        "margin_after_match": _json_value(row.get("margin_after_match")),
        "minimum_margin_rate": _json_value(row.get("minimum_margin_rate")),
        "recommendation": _json_value(row.get("recommendation")),
        "calculation_note": "利润率使用跟价后的到手价扣除我方运费和税费；价格差异使用双方最终可比价格。",
        "source": "current_streamlit_analysis",
    }
    if match_status != "matched":
        result["recommendation"] = "uncertain"
    return result
