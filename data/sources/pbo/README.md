# Australian Government total expenses, 2025-26

- **File:** `2025-26_Medium-Term_Budget_Outlook_-_Beyond_the_Budget_-_Data.xlsx`, the data workbook published with the
  Parliamentary Budget Office's *2025-26 Medium-term budget outlook: Beyond the Budget*, unedited.
  https://www.pbo.gov.au/publications-and-data/publications/2025-26-Medium-term-budget-outlook
- **Used:** sheet `Table B-2` (Comparison of expense programs), row `Total expenses`, 2025-26: 27.3% of GDP and
  A$785.7 billion. `data/build_processed.py` asserts the column headers before reading them.
- **Licence:** Commonwealth of Australia; PBO publications are released under Creative Commons Attribution 4.0
  International (PBO copyright notice). Attribution: "Based on Commonwealth of Australia data."
- **Downloaded:** 26/10/2026.
- **Used for:** only Calculator K's "share of federal spending" = (cost as % of GDP) ÷ 27.3%. Using the
  percentage-of-GDP form keeps US-dollar costs and Australian-dollar budgets comparable without an exchange rate.
