# Study guide: Retail Sales Explorer

## Read in this order

1. Try the demo and change several inputs.
2. Read the question, method, and limitations in README.md.
3. Run every cell of notebooks/analysis.ipynb.
4. Trace a displayed result back to src/pipeline.py and its raw data.
5. Read the tests and change one assumption in a new experiment.

## Be ready to explain

- Why are positive sales different from net revenue and profit?
- How do missing customer IDs affect sales totals and unique-customer counts differently?
- Why should distinct customers not be summed across months?
- What assumption makes exact-row deduplication valid, and when could it be wrong?
- Why is December 2011 not comparable with a complete month?
- How does the SQLite result reconcile with the dashboard?

## Make it your own

Write a one-page interpretation in your own words, implement one of the notebook extension ideas, and record both what improved and what did not. Keep a new test period for any supervised model changes. Do not claim business impact, accuracy, or independent authorship that the evidence does not support.
