# Findings

- 541,909 original rows; 524,878 positive-sale rows after cleaning.
- £10,642,110.80 in positive sales across 19,960 invoices.
- 4,338 identifiable customers; missing IDs remain in sales totals.
- UK sales account for 84.6% of the total.
- December 2011 is partial, ending on 9 December.

## How to interpret this

Positive sales exclude refunds and costs, so they are neither net revenue nor profit. Service/postage codes are included. Duplicate removal is a documented assumption. This single historical retailer is not representative of all ecommerce.

Reproduce with `python -m src.pipeline`. Source hash and methodology are in `DATA.md` and `README.md`.
