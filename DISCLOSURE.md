# Data and AI disclosure statement

## Data

The app uses five public sources, kept unedited in `data/sources/`:

- **TOP500.org, TOP500 List June 2026** (`data/sources/top500/TOP500_202606.xlsx`, MD5 `26d72ecb9eb8fcdcefb0df3a1b215f79`).
  No licence grant; © 1993–2026 TOP500.org, cited with attribution.
- **Epoch AI, ‘Data on AI data centers’, October 2026 update** (`data/sources/epoch/data_centers.csv`,
  MD5 `ea246ddea0bf7f561f99c1639662be23`). CC BY 4.0. Published online at epoch.ai.
- **Our World in Data, from Epoch AI's notable AI systems** (`data/sources/owid/affiliation-researchers-building-artificial-intelligence-systems-all.csv`,
  MD5 `9c5bdd24852b8a3d9b06c17e7f61df98`). CC BY 4.0. Citation: Epoch AI (2026), with major processing by Our World in Data.
- **World Bank, GDP (current US$) for Australia, NY.GDP.MKTP.CD, via FRED series MKTGDPAUA646NWDB**
  (`data/sources/worldbank/MKTGDPAUA646NWDB.csv`, MD5 `40729543b2a721515a3df7e20fb41f7b`). CC BY 4.0. The 2021–2025
  observations were copied from the FRED series page on 26/10/2026 because the CSV download was blocked in our build
  environment; used only for the calculator's share of GDP.
- **Parliamentary Budget Office, 2025-26 Medium-term budget outlook, Table B-2** (`data/sources/pbo/mtbo_2025-26_total_expenses.csv`,
  MD5 `15870a60749a7b71e429ea3468bf4223`). CC BY 4.0. Australian Government total expenses 2025-26 (A$785.7B, 27.3% of
  GDP), copied from the PBO page on 26/10/2026; used only for the calculator's share of federal spending.

The first three were downloaded on 11/10/2026.

Map shapes come from Natural Earth 1:110m via world-atlas 2.0.2 (ISC licence). The seven files in `data/processed/`
are produced only by `data/build_processed.py`, which checks all five MD5s; the transforms are documented in
`data/data_dictionary_en.md` and `data/processed/MANIFEST.csv`. Epoch's website now serves a later release of its CSV,
so the committed 11/10/2026 file, not a fresh download, is the source for the app's figures.

## AI

We used generative AI tools during this project. Every substantive use is recorded in `PROVENANCE.md`, one row per
use, with what was asked, what came back and the check we ran on it; each member owns at least one row.

- **Claude (Anthropic)** was used to write the data-cleaning script `data/build_processed.py` and the Streamlit app
  code (`app.py`, `charts/`). Other tools used by members are listed in their rows of `PROVENANCE.md`.
- No AI output was accepted unchecked. The cleaning script refuses to run if a raw file's MD5 changes; the headline
  numbers (59.88%, 71.3%, $524.0B, $120.4B) were recomputed from the source and processed files; and the app was run
  and tested by the group, including the empty-filter state.
- The question, persona, choice of datasets, chart choices and final wording were decided by the group, and the group
  is responsible for every claim in the app.

### Additional AI Tool Usage

**Huajin Wen**

* DeepSeek: Assisted with finding information, identifying relevant datasets, and summarising research.
* Claude Code: Assisted with project design, planning, and code implementation.
* Gemini: Provided feedback and suggestions.
* DeepSeek and Claude Code: Assisted with validation and submission checks.

**Yifan Wu**

* GitHub Copilot: Assisted with understanding project requirements, reviewing dashboard improvements, and troubleshooting.
* GitHub Copilot: Assisted with dashboard implementation, Streamlit app improvements, and debugging.
