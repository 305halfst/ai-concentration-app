# Australia's GDP (current US$)

- **File:** `MKTGDPAUA646NWDB.csv`, in FRED's `fredgraph.csv` layout (`observation_date`, value).
- **Publisher:** World Bank, World Development Indicators, indicator `NY.GDP.MKTP.CD` ("GDP (current US$)").
  Distributed by FRED (Federal Reserve Bank of St. Louis) as series `MKTGDPAUA646NWDB`, last updated 7 July 2026.
- **Licence:** CC BY 4.0 (World Bank). Citation: World Bank, Gross Domestic Product for Australia [MKTGDPAUA646NWDB],
  retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/MKTGDPAUA646NWDB, 26/10/2026.
- **How it was obtained:** our build environment's network blocked the CSV download, so the five most recent annual
  observations (2021–2025) were copied digit for digit from the FRED series page on 26/10/2026 into FRED's own CSV layout.
  To replace it with the full download, save https://fred.stlouisfed.org/graph/fredgraph.csv?id=MKTGDPAUA646NWDB here
  under the same name and update its MD5 in `data/build_processed.py`.
- **Used for:** only the calculator's "share of Australia's GDP" (2025 value).
