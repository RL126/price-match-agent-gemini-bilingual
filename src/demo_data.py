import pandas as pd


def demo_products() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "product_id": "P001",
                "brand": "GlowLab",
                "product_name": "Vitamin C Serum",
                "size_ml": 30,
                "cost_price": 10.00,
                "our_price": 24.99,
                "our_shipping_fee": 0.00,
                "our_tax_fee": 2.00,
                "minimum_margin_rate": 0.20,
            },
            {
                "product_id": "P002",
                "brand": "GlowLab",
                "product_name": "Hydrating Face Cream",
                "size_ml": 50,
                "cost_price": 16.00,
                "our_price": 29.99,
                "our_shipping_fee": 0.00,
                "our_tax_fee": 2.40,
                "minimum_margin_rate": 0.20,
            },
            {
                "product_id": "P003",
                "brand": "PureSkin",
                "product_name": "Niacinamide Serum",
                "size_ml": 30,
                "cost_price": 8.00,
                "our_price": 19.99,
                "our_shipping_fee": 0.00,
                "our_tax_fee": 1.60,
                "minimum_margin_rate": 0.20,
            },
        ]
    )


def demo_competitors() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "platform": "Amazon US",
                "brand": "GlowLab",
                "competitor_product_name": "Vitamin C Serum",
                "size_ml": 30,
                "listed_price": 21.99,
                "discount_price": 18.99,
                "shipping_fee": 0.00,
                "tax_fee": 1.52,
                "collected_at": "2026-11-15",
            },
            {
                "platform": "Amazon US",
                "brand": "GlowLab",
                "competitor_product_name": "Vitamin C Serum",
                "size_ml": 30,
                "listed_price": 20.99,
                "discount_price": 18.49,
                "shipping_fee": 0.00,
                "tax_fee": 1.48,
                "collected_at": "2026-11-16",
            },
            {
                "platform": "Amazon US",
                "brand": "GlowLab",
                "competitor_product_name": "Vitamin C Serum",
                "size_ml": 30,
                "listed_price": 19.99,
                "discount_price": 17.99,
                "shipping_fee": 0.00,
                "tax_fee": 1.44,
                "collected_at": "2026-11-17",
            },
            {
                "platform": "Walmart US",
                "brand": "GlowLab",
                "competitor_product_name": "Hydrating Face Cream",
                "size_ml": 50,
                "listed_price": 24.99,
                "discount_price": 22.99,
                "shipping_fee": 2.99,
                "tax_fee": 1.84,
                "collected_at": "2026-11-17",
            },
            {
                "platform": "Amazon US",
                "brand": "OtherBrand",
                "competitor_product_name": "Niacinamide Serum",
                "size_ml": 30,
                "listed_price": 12.99,
                "discount_price": 11.99,
                "shipping_fee": 0.00,
                "tax_fee": 0.96,
                "collected_at": "2026-11-17",
            },
        ]
    )
