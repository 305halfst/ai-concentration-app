# Is cutting-edge AI becoming something only big tech can do?

36104 Data Visualisation and Narratives · Assignment 3 · Group 8 · Streamlit data narrative.

- **Repository:** https://github.com/305halfst/ai-concentration-app
- **Deployed app:** https://ai-concentration.streamlit.app
- **Assessed version:** release tag `a3-final` (the commit hash is also given in the submission PDF)

## Question and audience

The app asks whether cutting-edge AI is becoming something only big tech can do. It is written for a university research
funding body deciding whether academics need publicly funded shared compute, or could obtain suitable capacity elsewhere.
The evidence contrasts the TOP500 supercomputer list with Epoch AI's database of large AI data centres.

## User stories

1. **As a** research funding officer, **I want** to compare universities' share of TOP500 machines with their share of
   compute, **so that** I can judge whether academics already have access to large-scale compute.
   *Walk-through:* section 1. Chart A has a measure toggle; Chart C filters organisation segments.
2. **As a** research funding officer, **I want** to see which countries hold public and private supercomputing capacity,
   **so that** I can compare Australia with overseas capacity.
   *Walk-through:* section 2. Chart D switches between all, public and private systems; the "Compare a country" selector
   (default Australia) states its rank and share, outlines it on the map and adds it to the bar.
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
| D | Spatial / ranking | Choropleth, labelled top-10 bar chart and full country table of national Rmax shares; system-group selector and compared-country selector. |
| B | Ranking | Sorted bars of AI data-centre capital cost by owner; top-N slider and country highlight. |
| E | Relationship | Bubble scatterplot relating owner capital cost, listed power capacity and estimated H100 equivalents; country and owner filters. |

## Chart D design decision and contribution

Chart D, **Where the compute sits**, is Purvesh Ribadiya's dashboard contribution. A choropleth was kept for the spatial
overview, rather than a proportional-symbol (bubble) map, because bubbles for Germany, Italy, Switzerland, France and the
United Kingdom overlap in Europe and hide each other. A map alone cannot carry exact values, and the persona's own country
is easy to miss: Australia ranks 28 of 47 countries with 0.3% of TOP500 Rmax, below the labelled top ten. Chart D therefore
adds a "Compare a country" selector (default Australia) that states the country's rank, systems, Rmax and share, outlines it
on the map and always adds it to the bar, plus a table of every country so no value needs hovering. Singapore has no shape at
the 1:110m map scale, so the table is the only place its value appears. When the compared country has no system in the
selection (for example Australia with private systems only), a message replaces its line.

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
| `data/processed/` | The three CSV files used by the app. |
| `requirements.txt` | Python package versions. |

## Data availability and traceability

The app reads these available processed files:

- `fig4_top500_by_segment.csv` — organisation-level TOP500 system and Rmax shares.
- `top500_systems_clean.csv` — 500 TOP500 systems, including country, year, sector, Rmax, power and cores.
- `datacenters_by_owner_country.csv` — 20 AI data-centre owner records, including country, data-centre count, capital cost,
  power, H100 equivalents and capex share.

Existing project documentation identifies TOP500 List June 2026 and Epoch AI's October 2026 data-centre update, with a
last documented refresh of 11 October 2026. It also refers to `data/sources/`, `data/build_processed.py`, and
`data/data_dictionary_en.md`; none is present in this checkout. Therefore the app can trace displayed values to the three
processed CSVs, but the raw-data transformation path cannot be independently verified or regenerated from this branch.

## Design rules

- No hover is required to identify a value: charts use labels or explanatory text, and Chart E includes an accessible table.
- Public-sector categories use blues, private categories use oranges and other/unknown categories use grey.
- Source/date captions identify the verified documentation supporting each chart's processed data.
