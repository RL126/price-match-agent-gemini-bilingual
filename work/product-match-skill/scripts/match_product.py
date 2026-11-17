import argparse
import json
from pathlib import Path


def normalize(value: str) -> str:
    return " ".join(value.lower().strip().split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-id", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--competitor-product", required=True)
    parser.add_argument("--competitor-size-ml", type=float)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    products = json.loads((root / "data" / "products.json").read_text(encoding="utf-8"))
    competitors = json.loads(
        (root / "data" / "competitor_products.json").read_text(encoding="utf-8")
    )

    own = next((item for item in products if item["product_id"] == args.product_id), None)
    if own is None:
        print(json.dumps({"match_status": "uncertain", "message": "Unknown product_id."}))
        return

    candidates = [
        item
        for item in competitors
        if item["platform"].lower() == args.platform.lower()
        and item["product_name"].lower() == args.competitor_product.lower()
        and (
            args.competitor_size_ml is None
            or item["size_ml"] == args.competitor_size_ml
        )
    ]

    if not candidates:
        result = {
            "match_status": "unmatched",
            "product_id": own["product_id"],
            "competitor_product": args.competitor_product,
            "match_score": 0.0,
            "match_method": "no_candidate",
            "evidence": "No candidate with the same platform and product name was found.",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    candidate = candidates[0]
    same_brand = normalize(own["brand"]) == normalize(candidate["brand"])
    same_name = normalize(own["product_name"]) == normalize(candidate["product_name"])
    same_size = own["size_ml"] == candidate["size_ml"]
    score = round((0.4 if same_brand else 0) + (0.4 if same_name else 0) + (0.2 if same_size else 0), 2)

    if same_brand and same_name and same_size:
        status = "matched"
        evidence = "Brand, normalized product name, and normalized size are identical."
    elif same_brand and same_name:
        status = "uncertain"
        evidence = "Brand and product name match, but the package size is different."
    else:
        status = "unmatched"
        evidence = "Brand or product name does not match."

    result = {
        "match_status": status,
        "product_id": own["product_id"],
        "competitor_product": candidate["product_name"],
        "match_score": score,
        "match_method": "brand_name_size_rule",
        "evidence": evidence,
        "same_brand": same_brand,
        "same_name": same_name,
        "same_size": same_size,
        "competitor_size_ml": candidate["size_ml"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
