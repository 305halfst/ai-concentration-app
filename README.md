# Is cutting-edge AI becoming something only big tech can do?

36104 Data Visualisation and Narratives · Assignment 3 · Group 8 · Streamlit data narrative.

- **Repository:** https://github.com/305halfst/ai-concentration-app
- **Deployed app:** https://ai-concentration.streamlit.app
- **Assessed version:** release tag `a3-final` (the commit hash is also given in the submission PDF)

## Question

**Is cutting-edge AI becoming something only big tech can do?**

The question is arguable because the same data supports both answers. Five companies (Google, Meta, Amazon, Microsoft
and SpaceXAI) account for 72.2% of the $524.0B capital cost of the 93 largest AI data centres, which says yes. The public
sector (universities, research labs and government) holds 71.3% of TOP500 supercomputing compute, which says no.

## Persona

**A university research funding body deciding whether to fund shared compute for academics.** The app serves that
decision: whether academics can reach compute that fits AI work through public facilities, or whether frontier-scale
compute now sits only with big tech. The evidence contrasts the TOP500 supercomputer list with Epoch AI's database of
large AI data centres.

## User stories

1. **As a** research funding officer, **I want** to compare universities' share of TOP500 machines with their share of
   compute, **so that** I can judge whether academics already have access to large-scale compute.
   *Walk-through:* section 1. Chart A has a measure toggle; Chart C filters organisation segments.
2. **As a** research funding officer, **I want** to see which countries hold public and private supercomputing capacity,
   **so that** I can compare Australia with overseas capacity.
   *Walk-through:* section 2. Chart D switches between all, public and private systems.
3. **As a** research funding officer, **I want** to see who is paying for the largest AI data centres and whether any have
   a site in Australia, **so that** I can assess whether capacity might be leased rather than built publicly.
   *Walk-through:* section 3. Chart B provides a top-N slider and country highlight selector.
4. **As a** research funding officer, **I want** to compare reported investment, power capacity and estimated H100-equivalent
   scale for AI data-centre owners, **so that** I can distinguish a high-spend owner from one with a larger listed physical footprint.
   *Walk-through:* section 4. Chart E filters by listed site country and owner, then presents KPI cards, a bubble chart and
   an accessible owner table.

## Run

Python 3.11 or newer, from this folder:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

## Charts

| Chart | Visual vocabulary | Purpose and interaction |
|---|---|---|
| A | Part-to-whole / magnitude | 100% stacked or paired bars comparing TOP500 systems and Rmax shares by organisation segment. |
| C | Distribution | Heatmap of TOP500 machine counts by size band and organisation; segment filter. |
| D | Spatial / ranking | Choropleth and labelled top-10 bar chart of national Rmax shares; system-group selector. |
| B | Ranking | Sorted bars of AI data-centre capital cost by owner; top-N slider and country highlight. |
| E | Relationship | Bubble scatterplot relating owner capital cost, listed power capacity and estimated H100 equivalents; country and owner filters. |

## Chart E design decision and contribution

Chart E, **AI Data-centre Scale versus Investment**, is the assigned dashboard contribution. A scatterplot was chosen
instead of another bar chart because Chart B already ranks owners by capital cost. Scatterplot position makes the
relationship between reported capital cost and listed power capacity visible at once, while bubble area adds the dataset's
estimated H100-equivalent measure. It supports comparison without claiming that investment causes power or chip capacity.

The dashboard includes country and owner filters, KPI cards, an owner-labelled chart, an accessible table, an empty state
and a filtered CSV download. It cannot show utilisation, energy efficiency, university access, model-training output, or
a causal relationship between the three measures.

## Repository layout

| Path | Purpose |
|---|---|
| `app.py` | Streamlit narrative page, controls, chart cards, downloads and source captions. |
| `charts/chart_a_segments.py` | Chart A: organisation shares of TOP500 systems and Rmax. |
| `charts/chart_c_sizes.py` | Chart C: TOP500 machines by Rmax size band and organisation. |
| `charts/chart_d_map.py` | Chart D: TOP500 Rmax share by country. |
| `charts/chart_b_capex.py` | Chart B: AI data-centre capital-cost ranking by owner. |
| `charts/chart_e_scale.py` | Chart E: AI data-centre scale versus investment bubble scatterplot. |
| `charts/common.py` | Processed-data reader, palette and shared Altair styling. |
| `data/sources/` | The two raw files, unedited: `top500/TOP500_202606.xlsx` and `epoch/data_centers.csv` (both downloaded 11/10/2026). |
| `data/build_processed.py` | Checks both raw files' MD5s and regenerates every file in `data/processed/`. |
| `data/processed/` | The three CSV files used by the app, plus `MANIFEST.csv` (rows, source, transform and MD5 per file). |
| `data/data_dictionary_en.md` | Data dictionary: source, URL, licence, columns and units, primary key, time coverage, latest observation, transform. |
| `PROVENANCE.md`, `DISCLOSURE.md` | AI provenance matrix; data and AI disclosure statement. |
| `requirements.txt` | Python package versions. |

## Data and regeneration

The app reads only the three files in `data/processed/`. They are regenerated from the two raw files in `data/sources/`
with:

```bash
python data/build_processed.py
```

The script stops if either raw file's MD5 differs from the 11/10/2026 snapshot (TOP500 `26d72ecb9eb8fcdcefb0df3a1b215f79`,
Epoch `ea246ddea0bf7f561f99c1639662be23`), then writes the three CSVs and `MANIFEST.csv`. Running it reproduces the committed
processed files byte for byte.

## Design rules

- No hover is required to identify a value: charts use labels or explanatory text, and Chart E includes an accessible table.
- Public-sector categories use blues, private categories use oranges and other/unknown categories use grey.
- Source/date captions identify the verified documentation supporting each chart's processed data.
