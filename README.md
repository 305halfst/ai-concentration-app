# Is cutting-edge AI becoming something only big tech can do?

36104 Data Visualisation and Narratives · Assignment 3 · Group 8 · Streamlit data narrative.

- **Repository:** https://github.com/305halfst/ai-concentration-app
- **Deployed app:** https://ai-concentration.streamlit.app
- **Assessed version:** release tag `a3-final` (the commit hash is also given in the submission PDF)

## Question

**Is cutting-edge AI becoming something only big tech can do?**

The question is arguable because the same data supports both answers. Five companies (Google, Meta, Amazon, Microsoft
and SpaceXAI) account for 72.2% of the $524.0B capital cost of the 93 largest AI data centres, which says yes. The
public sector (universities, research labs and government) holds 71.3% of TOP500 supercomputing compute, which says no.

## Persona

**A university research funding body** (for example a university research office or a national research council)
**deciding whether to fund shared compute for academics.** The app serves that decision: whether academics can reach
compute that fits AI work through public facilities, or whether frontier-scale compute now sits only with big tech.

## User stories

1. **As a** research funding officer, **I want** to compare universities' share of TOP500 machines with their share of
   its compute, **so that** I can judge whether academics already have access to large-scale compute.
   *Walk-through:* section 1. Chart A (toggle *Measure* between the stacked bars and the paired bars), then chart C
   (use the *Segments* filter to compare universities with public research labs).
2. **As a** research funding officer, **I want** to see which countries hold public and private supercomputing
   capacity, **so that** I can see how much of it is in Australia compared with overseas.
   *Walk-through:* section 2. Chart D (switch *Systems included* between all, public and private systems; read
   Australia's share in the text below the chart).
3. **As a** research funding officer, **I want** to see who is paying for the largest AI data centres and whether any
   of them has a site in Australia, **so that** I can decide whether shared academic compute has to be funded
   publicly or could be leased from the owners.
   *Walk-through:* section 3. Chart B (move the *Owners shown* slider; pick a country in *Highlight a country*;
   owners with a site there stay on the chart).

## Run

Python 3.11 or newer, from this folder:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

## Repository layout

| Path | Purpose |
|---|---|
| `app.py` | The page, in the course-session order: "On this page", short answer, sections 1–4, sources |
| `charts/page.py` | Title, contents, short answer, limitations, sources |
| `charts/chart_a_segments.py` | **A** (section 1) · 100% stacked bars, share of systems vs share of compute (Rmax) by segment; toggle to paired bars |
| `charts/chart_c_sizes.py` | **C** (section 1) · heatmap of machines per size band by segment; *Segments* filter; an empty selection shows a message |
| `charts/chart_d_map.py` | **D** (section 2) · choropleth of Rmax share by country, plus a labelled top-10 bar; *Systems included* toggle |
| `charts/chart_b_capex.py` | **B** (section 3) · sorted horizontal bars, AI data-centre capital cost by owner; *Owners shown* slider and *Highlight a country* |
| `charts/common.py` | Data reading, colours, chart styling |
| `data/sources/` | Raw source files, unedited (TOP500 June 2026 spreadsheet; Epoch AI data centres CSV) |
| `data/processed/` | The three files the app reads, written by `data/build_processed.py` |
| `data/build_processed.py` | Checks the raw files' MD5s and regenerates every file in `data/processed/` |
| `data/data_dictionary_en.md` | Data dictionary: source, URL, licence, columns and units, primary key, time coverage, latest observation, transform |
| `PROVENANCE.md` | AI provenance matrix, one row or more per member |
| `DISCLOSURE.md` | Data and AI disclosure statement |
| `static/countries-110m.json` | Country shapes (world-atlas 2.0.2, Natural Earth 1:110m, ISC licence), served by Streamlit static serving |

Regenerate the processed files with `python data/build_processed.py`.

Each chart lives in its own file.

## Design rules

- **No hover.** Every value is printed on the chart or in the text below it; no tooltips are defined.
- **One colour meaning throughout:** public sector = blues, private sector = oranges, other = grey; teal marks the
  highlighted country in chart B. All palettes were checked under simulated deuteranopia, protanopia and tritanopia.
- **Numbers are computed from the processed files when the app runs**, so every number on screen can be traced back
  to `data/processed/` and from there to `data/sources/`.
