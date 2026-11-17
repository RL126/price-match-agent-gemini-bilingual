---
name: product-match-skill
description: 判断自有护肤品与美国平台竞品是否为同款。使用品牌、标准化商品名称和规格进行可解释匹配。
---

# Product Match Skill

## Purpose

根据本 Skill 内的模拟商品数据，判断自有商品与竞品商品是否可以确认是同款。

## When to use

当用户询问以下内容时使用本 Skill，并且必须运行匹配脚本：

- 两个商品是否为同款
- 某个自有 SKU 是否匹配某个平台竞品
- 某个竞品是否允许进入后续价格比较

## Execution

运行：

```bash
python3 scripts/match_product.py --product-id P001 --platform "Amazon US" --competitor-product "Vitamin C Serum" --competitor-size-ml 30
```

## Matching rules

1. 品牌、商品名称和规格都一致时，返回 `matched`。
2. 品牌和商品名称一致，但规格不一致时，返回 `uncertain`。
3. 品牌或商品名称明显不一致时，返回 `unmatched`。
4. 不允许因为名称相似就直接确认同款。
5. 匹配结果必须包含匹配方法、分数和证据。

## Output

返回 JSON，字段包括：

- `match_status`
- `product_id`
- `competitor_product`
- `match_score`
- `match_method`
- `evidence`
- `same_brand`
- `same_name`
- `same_size`
- `competitor_size_ml`

只有 `matched` 才允许进入自动价格比较；`uncertain` 必须交由人工确认。
