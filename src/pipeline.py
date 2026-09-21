"""Build retail KPIs using SQLite and export an offline dashboard."""

import json, sqlite3
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .data import ROOT, load_data, clean_sales, save_json

MONTH_SQL = """
SELECT Month AS month, ROUND(SUM(Sales),2) AS sales,
       COUNT(DISTINCT InvoiceNo) AS orders, COUNT(*) AS line_items
FROM sales GROUP BY Month ORDER BY Month
"""


def summarize(df):
    if df.empty:
        return {
            "sales": 0,
            "orders": 0,
            "customers": 0,
            "line_items": 0,
            "aov": 0,
            "products": [],
        }
    total = float(df.Sales.sum())
    orders = int(df.InvoiceNo.nunique())
    products = (
        df.groupby("StockCode", dropna=False)
        .agg(sales=("Sales", "sum"), description=("Description", "first"))
        .sort_values("sales", ascending=False)
        .head(8)
        .reset_index()
    )
    return {
        "sales": round(total, 2),
        "orders": orders,
        "customers": int(df.CustomerID.nunique()),
        "line_items": int(len(df)),
        "aov": round(total / orders, 2),
        "products": [
            {
                "code": str(r.StockCode),
                "name": r.description,
                "sales": round(r.sales, 2),
            }
            for r in products.itertuples()
        ],
    }


def main():
    raw, digest = load_data()
    df, audit = clean_sales(raw)
    with sqlite3.connect(":memory:") as conn:
        df[["Month", "Sales", "InvoiceNo"]].to_sql("sales", conn, index=False)
        monthly = pd.read_sql_query(MONTH_SQL, conn)
    countries = sorted(df.Country.unique().tolist())
    months = sorted(df.Month.unique().tolist())
    slices, trends = {}, {}
    for country in ["All countries"] + countries:
        sub = df if country == "All countries" else df.loc[df.Country == country]
        slices[country] = {"All months": summarize(sub)}
        for month, g in sub.groupby("Month"):
            slices[country][month] = summarize(g)
        trend = sub.groupby("Month").Sales.sum().reindex(months, fill_value=0)
        trends[country] = [
            {"month": m, "sales": round(float(v), 2)} for m, v in trend.items()
        ]
    data = {
        "project": "retail",
        "source": "UCI Online Retail",
        "sha256": digest,
        "audit": audit,
        "start": str(df.InvoiceDate.min().date()),
        "end": str(df.InvoiceDate.max().date()),
        "countries": countries,
        "months": months,
        "slices": slices,
        "trends": trends,
    }
    save_json(ROOT / "reports/analysis.json", data)
    monthly.to_csv(ROOT / "reports/monthly_sales.csv", index=False)
    plt.rcParams.update(
        {"font.size": 11, "axes.spines.top": False, "axes.spines.right": False}
    )
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.bar(monthly.month, monthly.sales / 1e6, color="#2458e6")
    ax.set(
        ylabel="Positive sales (GBP millions)",
        title="Online Retail: monthly positive sales (refunds excluded)",
    )
    ax.tick_params(axis="x", rotation=45)
    ax.text(
        0.99,
        0.95,
        "December 2011 ends on the 9th",
        transform=ax.transAxes,
        ha="right",
        color="#555",
    )
    fig.tight_layout()
    fig.savefig(ROOT / "reports/monthly_sales.png", dpi=160)
    plt.close(fig)
    (ROOT / "demo/data.js").write_text(
        "window.PROJECT_DATA=" + json.dumps(data, allow_nan=False) + ";",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"audit": audit, "overall": slices["All countries"]["All months"]}, indent=2
        )
    )
    return data


if __name__ == "__main__":
    main()
