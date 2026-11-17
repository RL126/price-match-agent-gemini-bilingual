# Cross-Border Price Match Agent

<img width="1191" height="737" alt="截屏2026-11-17 下午4 58 01" src="https://github.com/user-attachments/assets/eac2b6de-aa7f-4d90-a9f6-a0998a1fac0b" />

<img width="1189" height="734" alt="截屏2026-11-17 下午4 58 26" src="https://github.com/user-attachments/assets/a3888abd-7e7d-44dd-8f3a-b0c6dc6748db" />

A lightweight pricing intelligence dashboard and tool-calling Agent for cross-border e-commerce teams.

The application helps operators compare owned products with simulated competitor listings from Amazon US, Walmart US, and Shopify-style stores. It standardizes product information, calculates landed comparable prices, checks margin rules, and generates a price-match recommendation.

> This is a portfolio MVP using CSV/demo data. It does not scrape websites, connect to real marketplace APIs, or change product prices.

## Product idea

Cross-border sellers often cannot compare competitor prices directly because product names, sizes, discounts, shipping fees, taxes, and margin policies are inconsistent.

This project turns that workflow into a traceable decision process:

```text
User question
    ↓
Gemini Agent understands the request
    ↓
Local Python tool reads the current analysis result
    ↓
Product matching → comparable price → price gap → margin rule
    ↓
Recommendation with evidence and data-source disclaimer
```

The LLM interprets the request and explains the result. Python owns the calculations and business rules.

## Features

- CSV upload for owned products and competitor prices
- Built-in simulated skincare and cosmetics dataset
- Product matching by brand, normalized product name, and size
- Landed comparable price calculation, including shipping and tax
- Price gap calculation between owned and competitor prices
- Post-match margin calculation after deducting owned shipping and tax costs
- Rule-based recommendations: `match`, `observe`, `do_not_match`, or `uncertain`
- Multi-page Streamlit dashboard
- Price trend visualization
- Product-level analysis table with filters
- CSV and Markdown report downloads
- Gemini function calling through Google AI Studio
- Agent tool trace showing the current dataset, arguments, and calculated result
- Chinese/English language switch in the sidebar
- Offline dashboard mode when no API key is configured

## Pages

| Page | Purpose |
|---|---|
| Overview | KPI cards, priority product, price trend, and recommendation distribution |
| Product Details | Filterable product analysis, evidence, CSV export, and Markdown report |
| Agent Workbench | Natural-language questions, Gemini tool calling, and execution trace |
| Data Management | Upload CSV files, validate data, preview records, and restore demo data |

## Architecture

```text
Streamlit UI
├── app.py                         Overview dashboard
├── pages/2_Product_Details.py     Product analysis
├── pages/3_Agent_Workbench.py     Gemini Agent interface
└── pages/4_Data_Management.py     CSV upload and validation

Application logic
├── src/dashboard_logic.py         Matching, pricing, margin, and reports
├── src/state.py                   Session-level data shared across pages
├── src/ui.py                      Theme, translations, and reusable UI helpers
├── src/agent.py                   Gemini function-calling Agent
└── src/tools/price_tools.py       Deterministic pricing tools
```

## Pricing logic

The app keeps customer price comparison and seller profitability separate.

### Competitor landed comparable price

```text
competitor item price
+ competitor shipping fee
+ competitor tax fee
= competitor final comparable price
```

The discounted price is used when available; otherwise the listed price is used.

### Owned final comparable price

```text
owned price
+ owned shipping fee
+ owned tax fee
= owned final comparable price
```

### Price gap rate

```text
(owned final comparable price - competitor final comparable price)
/ competitor final comparable price
```

### Post-match margin

```text
matched net price = competitor final comparable price
                   - owned shipping fee
                   - owned tax fee

post-match margin =
(matched net price - cost price) / matched net price
```

Tax and shipping are included in landed-price comparison, while owned tax and shipping are deducted again when estimating the seller's post-match margin.

## Recommendation rules

- If the product cannot be matched confidently, return `uncertain`.
- If required price, size, or cost data is missing, return `uncertain`.
- If post-match margin is below the product's minimum margin, return `do_not_match`.
- If the owned price is at least 10% higher than the competitor's final comparable price and margin passes, return `match`.
- Otherwise, return `observe`.

## Data format

### Owned products CSV

Required columns:

```text
product_id
brand
product_name
size_ml
cost_price
our_price
minimum_margin_rate
```

Optional columns:

```text
our_shipping_fee
our_tax_fee
```

If the optional columns are missing, the app defaults them to `0.0`.

### Competitor prices CSV

Required columns:

```text
platform
brand
competitor_product_name
size_ml
listed_price
discount_price
shipping_fee
tax_fee
```

Optional column for the trend chart:

```text
collected_at
```

All first-version prices are assumed to be in USD for the US market.

## Local setup

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Gemini Agent mode

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
GEMINI_API_KEY=your_google_ai_studio_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Do not commit `.env` or expose the API key in screenshots, GitHub, or chat messages.

The dashboard and deterministic calculations work without an API key. Only the natural-language Agent requires Gemini access.

### 4. Run the app

```bash
python -m streamlit run app.py
```

If the virtual environment is not activated, use the project interpreter explicitly:

```bash
./.venv/bin/python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Example Agent questions

```text
Analyze whether P001 should match Amazon US Vitamin C Serum 30 ml.
```

```text
Why is P002 not recommended for price matching?
```

```text
Compare the competitor landed price and our post-match margin for P001.
```

The Agent is instructed to use the current Streamlit analysis result. It must not invent prices, margins, or product records.

## Reliability and safety design

- Deterministic calculations are implemented in Python.
- The Agent calls a local function tool instead of performing mental arithmetic.
- The tool is bound to the current session's analyzed data, including uploaded CSV data.
- Uncertain matches cannot receive a price-match recommendation.
- External product text is treated as data, not as system instructions.
- Tool calls and returned values can be expanded in the Agent Workbench.
- Simulated data is clearly labeled and is never presented as live marketplace pricing.

## Current limitations

- Uses simulated CSV data only
- No live Amazon, Walmart, or Shopify API connection
- Matching is rule-based rather than vector-model based
- No user authentication or permissions
- No scheduled jobs or automated alerts
- No DuckDB persistence yet; current uploaded data is held in the Streamlit session

## Future roadmap

1. Add DuckDB persistence and data-quality reports
2. Add richer historical trend analysis
3. Add RAG for pricing policy and promotion rules
4. Add SQL and natural-language analytics safely
5. Add embedding-based product matching with human review
6. Add compliant marketplace APIs and scheduled monitoring
7. Add alerts and automated operating reports
