import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", required=True)
    parser.add_argument("--product", required=True)
    args = parser.parse_args()

    data_path = Path(__file__).resolve().parents[1] / "data" / "competitor_prices.json"
    records = json.loads(data_path.read_text(encoding="utf-8"))

    matches = [
        record
        for record in records
        if record["platform"].lower() == args.platform.lower()
        and record["product_name"].lower() == args.product.lower()
    ]

    if not matches:
        result = {
            "status": "not_found",
            "platform": args.platform,
            "product_name": args.product,
            "message": "No simulated competitor price was found.",
        }
    else:
        record = matches[0]
        competitor_price = record["discount_price"] or record["listed_price"]
        final_comparable_price = round(
            competitor_price + record["shipping_fee"] + record["tax_fee"],
            2,
        )
        result = {
            "status": "found",
            "platform": record["platform"],
            "product_name": record["product_name"],
            "brand": record["brand"],
            "size": record["size"],
            "competitor_price": competitor_price,
            "listed_price": record["listed_price"],
            "shipping_fee": record["shipping_fee"],
            "tax_fee": record["tax_fee"],
            "final_comparable_price": final_comparable_price,
            "calculation": (
                f"{competitor_price:.2f} + {record['shipping_fee']:.2f} + "
                f"{record['tax_fee']:.2f} = {final_comparable_price:.2f} USD"
            ),
            "currency": record["currency"],
            "collected_at": record["collected_at"],
            "source": record["source"],
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
