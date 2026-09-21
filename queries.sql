-- Run after loading cleaned sales into a table named sales.
-- Sales = Quantity * UnitPrice. Cancellations, negatives and zero-price rows excluded.
SELECT Month, ROUND(SUM(Sales), 2) AS positive_sales_gbp,
       COUNT(DISTINCT InvoiceNo) AS orders,
       ROUND(SUM(Sales) / COUNT(DISTINCT InvoiceNo), 2) AS average_order_value_gbp
FROM sales GROUP BY Month ORDER BY Month;

SELECT Country, COUNT(DISTINCT CustomerID) AS known_customers,
       ROUND(SUM(Sales), 2) AS positive_sales_gbp
FROM sales GROUP BY Country ORDER BY positive_sales_gbp DESC;
