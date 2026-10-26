# Data dictionary and reproducibility record

This document describes every dataset read by the deployed app.  It is also a
record of the exact source material currently committed to this repository.
Do not overwrite a processed file merely by downloading a newer source release:
the app analyses the June 2026 TOP500 list and an Epoch AI snapshot documented
as 11 October 2026.

## Source material

| Source | Committed file | Source URL | Licence / attribution | Snapshot used by the app | Primary key |
|---|---|---|---|---|---|
| TOP500 List, June 2026 | `sources/top500/TOP500_202606.xlsx` | `https://www.top500.org/lists/top500/2026/06/` | Copyright TOP500.org; no licence grant stated, used with attribution | June 2026 | `rank` |
| Our World in Data, from Epoch AI notable AI systems | `sources/owid/affiliation-researchers-building-artificial-intelligence-systems-all.csv` | `https://ourworldindata.org/grapher/affiliation-researchers-building-artificial-intelligence-systems-all` | CC BY 4.0 | 1950–2025 used (2026 incomplete), downloaded 11/10/2026; MD5 `9c5bdd24852b8a3d9b06c17e7f61df98` | `Entity` + `Year` |
| Epoch AI, Data on AI Data Centers | `sources/epoch/data_centers.csv` | `https://epoch.ai/data/data-centers-documentation/downloads` | CC BY 4.0 | October 2026 update, downloaded 11/10/2026; MD5 `ea246ddea0bf7f561f99c1639662be23`; 93 rows | `Name` |

All three raw files were downloaded on 11/10/2026 and are committed unedited.
`data/build_processed.py` checks their MD5s (TOP500 `26d72ecb9eb8fcdcefb0df3a1b215f79`,
Epoch `ea246ddea0bf7f561f99c1639662be23`, OWID `9c5bdd24852b8a3d9b06c17e7f61df98`) before writing anything.  Epoch's website
now serves a later release, so a fresh download will not match and must not replace
the committed file.

## Processed files used by the app

### `processed/top500_systems_clean.csv`

- **Grain / primary key:** one row per TOP500 system; `rank` is unique (500 rows).
- **Time coverage / latest observation:** TOP500 June 2026 list (latest observation June 2026); latest observed
  system in this cross-sectional list is June 2026.
- **Source:** `sources/top500/TOP500_202606.xlsx`.
- **Transform:** select the fields below from the TOP500 list; convert Rmax and
  Rpeak from PFlop/s to TFlop/s by multiplying by 1,000; retain power in kW;
  add the group's documented organisation classification (`segment` and
  `sector_group`) for narrative comparison.  The classification mapping is
  represented in this committed processed table and should be reviewed before
  any refresh.

| Column | Meaning and unit |
|---|---|
| `rank` | TOP500 rank; integer primary key |
| `name`, `site`, `manufacturer` | system, installation site and vendor text |
| `country` | installation country; categorical |
| `install_year` | installation year; year |
| `segment` | `Research`, `Industry`, `Academic`, `Vendor`, `Others` or `Government` |
| `sector_group` | narrative grouping: `Public`, `Private` or `Other` |
| `rmax_tflops`, `rpeak_tflops` | LINPACK sustained / theoretical performance; TFlop/s |
| `power_kw` | listed power; kW |
| `total_cores` | processor cores; count |

### `processed/fig4_top500_by_segment.csv`

- **Grain / primary key:** one row per organisation `segment` (six rows).
- **Time coverage / latest observation:** derived from the June 2026 TOP500 list; latest observation June 2026.
- **Transform:** group `top500_systems_clean.csv` by `segment` and
  `sector_group`; count rows as `n_systems`; sum `rmax_tflops`; divide each
  group by the all-segment totals to calculate the two percentage columns.

| Column | Meaning and unit |
|---|---|
| `sector_group`, `segment` | classification fields described above |
| `n_systems` | TOP500 systems; count |
| `rmax_tflops` | combined sustained LINPACK performance; TFlop/s |
| `system_share_pct`, `rmax_share_pct` | share of all 500 systems / combined Rmax; percent |

### `processed/datacenters_by_owner_country.csv`

- **Grain / primary key:** one row per named owner in the app's documented
  11 October 2026 Epoch snapshot; `owner` is unique (20 rows = 19 named owners + `Unknown`).
- **Time coverage / latest observation:** the snapshot is October 2026.  It is
  not a time series.
- **Source:** `sources/epoch/data_centers.csv` (93 site rows, 11/10/2026 snapshot).
- **Transform:** strip the `#confident` / `#likely` / `#speculative` tags from
  `Owner`; a missing owner becomes `Unknown` (9 sites); round H100 equivalents to
  0 dp, power to 1 dp and capital cost to 3 dp per site; group the sites by owner;
  `country` = the owner's listed site countries, de-duplicated and joined with
  `|`; `n_countries` = how many; sum site counts, capital cost, power and H100
  equivalents; `capex_share_pct` = owner capital cost / total x 100, 2 dp.

| Column | Meaning and unit |
|---|---|
| `owner` | site owner / operator; text primary key |
| `country` | pipe-separated listed site countries |
| `n_countries`, `n_datacenters` | counts |
| `capital_cost_2025usd_bn` | estimated capital cost; billions of 2025 US dollars |
| `power_mw` | listed power capacity; MW |
| `h100_equivalents` | Epoch's estimated H100-equivalent chips; count |
| `capex_share_pct` | owner's share of all processed capital cost; percent |

### `processed/ai_systems_by_sector.csv`

- **Source:** `sources/owid/affiliation-researchers-building-artificial-intelligence-systems-all.csv` (Our World in
  Data, from Epoch AI's notable AI systems; CC BY 4.0; https://ourworldindata.org/grapher/affiliation-researchers-building-artificial-intelligence-systems-all;
  MD5 `9c5bdd24852b8a3d9b06c17e7f61df98`; downloaded 11/10/2026).
- **Grain / primary key:** one row per (`sector`, `year`); 305 rows. **Time coverage:** 1950–2025; latest observation
  2025 (2026 is incomplete in the source and dropped).
- **Transform:** rename columns; drop years after 2025; fill sector-years with no systems as 0; `total_year` = sum over
  sectors; `share_pct` = `n_systems` / `total_year` x 100, 2 dp.

| Column | Meaning and unit |
|---|---|
| `sector` | Academia; Academia and industry collaboration; Industry; Not specified; Other |
| `year` | year of publication |
| `n_systems`, `total_year` | notable AI systems; count |
| `share_pct` | share of that year's notable systems; percent |

### `processed/datacenters_by_country.csv`

- **Source:** `sources/epoch/data_centers.csv` (as above). **Grain / primary key:** one row per `country` (12 rows).
  **Time coverage:** October 2026 snapshot.
- **Transform:** group the 93 sites by `Country`; `n_datacenters` = sites; `n_estimated` = sites with a current H100
  estimate; `h100_equivalents` = sum (blank = 0); `h100_share_pct` = share of the total, 2 dp.
  **Latest observation:** October 2026 snapshot.

| Column | Meaning and unit |
|---|---|
| `country` | country of the site; text primary key |
| `n_datacenters` | tracked sites in that country; count |
| `n_estimated` | of those, sites with a current H100 estimate; count |
| `h100_equivalents` | sum of current estimated H100 equivalents; count of chips |
| `h100_share_pct` | country's share of all estimated H100 equivalents; percent |

## Values computed in the app (no extra processed file)

- **Chart T:** years 2010–2025 only; "Other" and "Not specified" are drawn together as "Other / not specified".
- **Calculator K:** chips needed = target / (100 − target) × total current H100 equivalents (other owners held
  fixed); rough cost = chips × (total estimated capital cost ÷ total H100 equivalents), about $36,400 per chip; copies of Firmus = chips ÷ 46,488; share of GDP = rough cost ÷ Australia's 2025 GDP
  (US$1,798.52B, World Bank NY.GDP.MKTP.CD via FRED MKTGDPAUA646NWDB, retrieved 26/10/2026; a constant in `charts/page.py`).

- **Chart F, owner groups (Epoch bar):** shares of `h100_equivalents` in `datacenters_by_owner_country.csv`.
  *Five largest named owners* = Google, Meta, Amazon, Microsoft, SpaceXAI (the top five named owners by estimated
  capital cost; also the top five by H100 equivalents). *Unknown* = sites with no owner in Epoch. *Other companies* =
  the remaining named owners. *Public sector* = 0: the group classified each of the 19 named owners by name, and
  none is a university or public research body (G42 is counted as a company although it has state backing).
- **Chart F, sector groups (TOP500 bar):** sums of `rmax_share_pct` by `sector_group` in `fig4_top500_by_segment.csv`.
- **Sites without a current estimate:** in `sources/epoch/data_centers.csv`, 20 of the 93 sites have a current H100
  equivalent of 0 or blank (and therefore no cost or power estimate). Every Epoch share and the $524.0B total cover the
  73 sites with estimates. Check: `(df["Current H100 equivalents"].fillna(0) == 0).sum()` → 20.
- **Australia's TOP500 systems:** rows of `top500_systems_clean.csv` with `country == "Australia"` (4 systems).

## Rebuild

Run `python data/build_processed.py` from the repository root (needs pandas and
openpyxl).  It stops on an MD5 mismatch, then writes the five processed files
and `processed/MANIFEST.csv` (rows, source, transform and MD5 of each output).
On the committed sources it reproduces the committed processed files byte for
byte.
