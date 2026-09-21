import json, unittest
from pathlib import Path
import pandas as pd
from src.pipeline import summarize

ROOT = Path(__file__).resolve().parents[1]


class AnalysisTests(unittest.TestCase):
    def test_orders_and_customers_are_distinct(self):
        df = pd.DataFrame(
            {
                "InvoiceNo": ["A", "A", "B"],
                "CustomerID": [1, 1, 1],
                "Sales": [10.0, 15.0, 5.0],
                "StockCode": ["X", "Y", "X"],
                "Description": ["x", "y", "x"],
            }
        )
        s = summarize(df)
        self.assertEqual(s["orders"], 2)
        self.assertEqual(s["customers"], 1)
        self.assertEqual(s["aov"], 15)

    def test_empty_selection(self):
        self.assertEqual(summarize(pd.DataFrame())["sales"], 0)

    def test_exported_aggregates_reconcile(self):
        d = json.loads((ROOT / "reports/analysis.json").read_text())
        overall = d["slices"]["All countries"]["All months"]["sales"]
        self.assertAlmostEqual(
            sum(r["sales"] for r in d["trends"]["All countries"]), overall, places=2
        )
        self.assertAlmostEqual(
            sum(d["slices"][c]["All months"]["sales"] for c in d["countries"]),
            overall,
            places=2,
        )
        self.assertEqual(
            d["audit"]["raw_rows"],
            sum(
                d["audit"][k]
                for k in [
                    "duplicate_rows",
                    "cancellation_or_negative_rows",
                    "nonpositive_or_invalid_rows",
                    "clean_rows",
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
