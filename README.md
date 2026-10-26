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

**A policy officer in the Australian Government who funds research infrastructure and must decide whether to invest
in shared AI computing capacity for universities.** The app serves that decision. It shows who owns the infrastructure
frontier AI runs on (Epoch AI's database of large AI data centres), what the public sector and Australia already hold
(the TOP500 supercomputer list), and ends with a conclusion and one recommendation, labelled as ours.

## User stories

1. **As a** research-infrastructure policy officer, **I want** to see whether frontier AI is shifting from universities
   to industry and who owns the AI infrastructure today, **so that** I can judge whether public institutions are being
   left behind.
   *Walk-through:* section 1, Chart T (Play button and year slider); section 2, Charts W, B (top-N slider and country
   highlight) and E (country and owner filters); section 3, Chart F.
2. **As a** research-infrastructure policy officer, **I want** to compare how much compute universities, public labs and
   Australia hold, **so that** I know what public capacity already exists.
   *Walk-through:* section 4: Chart A (measure toggle), Chart C (segment filter; an empty selection shows a message),
   Chart D (all / public / private systems) and Chart M.
3. **As a** research-infrastructure policy officer, **I want** to see what a meaningful public share would cost and a
   clear recommendation with its limits, **so that** I can decide whether to fund shared GPU capacity for universities.
   *Walk-through:* section 5: Calculator K (target-share slider), conclusion and recommendation; then "What the data cannot show".

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
| T | Change over time | Animated 100% stacked area (React + D3 inside Streamlit): share of notable AI systems by sector, 2010–2025; Play button and year slider; every value for the selected year is printed. |
| W | Part-to-whole | Unit chart, 100 squares: owners of the estimated AI chips in Epoch's data centres. |
| B | Ranking | AI data-centre owners by estimated capital cost; top-N slider and country highlight. |
| E | Relationship | Owner capital cost vs power, bubble = estimated AI chips; country and owner filters. |
| F | Part-to-whole | Two 100% bars: public share of TOP500 Rmax vs of estimated AI chips. |
| A | Part-to-whole / magnitude | TOP500 share of systems and of Rmax by organisation type; measure toggle. |
| C | Distribution | TOP500 machines by size band and organisation; segment filter. |
| D | Spatial | TOP500 Rmax by country; all / public / private toggle. |
| M | Spatial | Estimated AI chips by country (Epoch). |
| K | Calculator | Chips and rough cost for a chosen public share; target slider. |

## Chart E design decision and contribution

Chart E (Yifan Wu) is the owner-level dashboard: country and owner filters, KPI cards, a labelled bubble chart, an
accessible table, an empty state and a filtered CSV download. A scatterplot was chosen instead of another bar chart
because Chart B already ranks owners by cost. The first version plotted capital cost against power; because Epoch
estimates cost from power (about $0.038B per MW for every owner), those axes carried the same information, so the
y-axis now shows estimated AI chips (H100 equivalents), an independent measure, and bubble size shows the number of
data centres. Both axes use log scales so small owners do not pile up at the origin.

## Repository layout

| Path | Purpose |
|---|---|
| `app.py` | Streamlit narrative page, controls, chart cards, downloads and source captions. |
| `charts/chart_a_segments.py` | Chart A: organisation shares of TOP500 systems and Rmax. |
| `charts/chart_c_sizes.py` | Chart C: TOP500 machines by Rmax size band and organisation. |
| `charts/chart_d_map.py` | Chart D: TOP500 Rmax share by country. |
| `charts/chart_b_capex.py` | Chart B: AI data-centre capital-cost ranking by owner. |
| `charts/chart_t_time.py`, `charts/js/chart_t_template.html` | Chart T: React + D3 animated time chart; numbers computed in Python, libraries loaded from cdnjs at exact versions. |
| `charts/chart_w_waffle.py`, `charts/chart_f_two_worlds.py`, `charts/chart_m_ai_map.py` | Charts W, F and M. |
| `charts/chart_e_scale.py` | Chart E: AI data-centre scale versus investment bubble scatterplot. |
| `charts/common.py` | Processed-data reader, palette and shared Altair styling. |
| `data/sources/` | The three raw files, unedited (all downloaded 11/10/2026): `top500/TOP500_202606.xlsx`, `epoch/data_centers.csv`, `owid/affiliation-researchers-building-artificial-intelligence-systems-all.csv` (+ its metadata). |
| `data/build_processed.py` | Checks both raw files' MD5s and regenerates every file in `data/processed/`. |
| `data/processed/` | The five CSV files used by the app, plus `MANIFEST.csv` (rows, source, transform and MD5 per file). |
| `data/data_dictionary_en.md` | Data dictionary: source, URL, licence, columns and units, primary key, time coverage, latest observation, transform. |
| `PROVENANCE.md`, `DISCLOSURE.md` | AI provenance matrix; data and AI disclosure statement. |
| `requirements.txt` | Python package versions. |

## Data and regeneration

The app reads only the five files in `data/processed/`. They are regenerated from the three raw files in `data/sources/`
with:

```bash
python data/build_processed.py
```

The script stops if any raw file's MD5 differs from the 11/10/2026 snapshot (TOP500 `26d72ecb9eb8fcdcefb0df3a1b215f79`,
Epoch `ea246ddea0bf7f561f99c1639662be23`, OWID `9c5bdd24852b8a3d9b06c17e7f61df98`), then writes the five CSVs and `MANIFEST.csv`. Running it reproduces the committed
processed files byte for byte.

## Design rules

- No hover is required to identify a value: charts use labels or explanatory text, and Chart E includes an accessible table.
- Public-sector categories use blues, private categories use oranges and other/unknown categories use grey.
- Source/date captions identify the verified documentation supporting each chart's processed data.
