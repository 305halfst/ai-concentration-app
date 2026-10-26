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
| Epoch AI, Data on AI Data Centers | `sources/epoch/data_centers.csv` | `https://epoch.ai/data/data-centers-documentation/downloads` | CC BY 4.0 | October 2026 update, downloaded 11/10/2026; MD5 `ea246ddea0bf7f561f99c1639662be23`; 93 rows | `Name` |

Both raw files were downloaded on 11/10/2026 and are committed unedited.
`data/build_processed.py` checks their MD5s (TOP500 `26d72ecb9eb8fcdcefb0df3a1b215f79`,
Epoch `ea246ddea0bf7f561f99c1639662be23`) before writing anything.  Epoch's website
now serves a later release, so a fresh download will not match and must not replace
the committed file.

## Processed files used by the app

### `processed/top500_systems_clean.csv`

- **Grain / primary key:** one row per TOP500 system; `rank` is unique (500 rows).
- **Time coverage / latest observation:** TOP500 June 2026 list; latest observed
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
- **Time coverage:** derived from the June 2026 TOP500 list.
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
  11 October 2026 Epoch snapshot; `owner` is unique (20 rows).
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

## Rebuild

Run `python data/build_processed.py` from the repository root (needs pandas and
openpyxl).  It stops on an MD5 mismatch, then writes the three processed files
and `processed/MANIFEST.csv` (rows, source, transform and MD5 of each output).
On the committed sources it reproduces the committed processed files byte for
byte.
