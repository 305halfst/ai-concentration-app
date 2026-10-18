# Is cutting-edge AI becoming something only big tech can do?

A3 Streamlit data narrative. **Persona:** a university research funding body deciding whether to fund
shared compute for academics.

## Run

Python 3.11, from this folder:

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

## Layout

| Path | Purpose |
|---|---|
| `app.py` | Page in the course-session order: purpose, "On this page", short answer, sections 1–4, sources |
| `charts/page.py` | Title, introduction, contents, short answer, limitations, sources table |
| `charts/chart_a_segments.py` | **A** (section 1) · 100% stacked bars, share of systems vs share of compute (Rmax) by segment; toggle to paired bars |
| `charts/chart_c_sizes.py` | **C** (section 1) · heatmap of machines per size band by segment; *Segments* filter; empty selection shows a message |
| `charts/chart_d_map.py` | **D** (section 2) · choropleth of Rmax share by country (+ labelled top-10 bar); *Systems included* toggle |
| `charts/chart_b_capex.py` | **B** (section 3) · sorted horizontal bars, AI data-centre capex by owner; *Top-N* slider and *Highlight a country* (always shown) |
| `charts/common.py` | Data reading, colours, chart styling |

Section order: **1 · Who our audience is** (A, then C explains why universities hold so little compute) →
**2 · Where the compute sits** (D) → **3 · Who is paying for frontier AI data centres** (B) →
**4 · What the data cannot show** → **Sources**. Each section runs lead text → chart → how to read it →
what it shows → a bridge into the next section.
| `data/processed/` | The three app files written by `data/build_processed.py` |
| `static/countries-110m.json` | Country shapes (world-atlas 2.0.2, Natural Earth 1:110m, ISC licence), served by Streamlit static serving |

Each chart lives in its own file, so each member's commit touches only their chart. Put the member names
in `OWNERS` at the top of `app.py`.

## Design rules used

- **No hover.** Every value the reader needs is printed on the chart or in the text below it; no tooltips are defined.
- **One colour meaning throughout:** public = blue, private = orange, other = grey.
- **Values are computed from the processed files at run time.** The 59.88% (Research share of Rmax) and $120.4B
  (Google capex) can be traced live back to the raw files, as set out in the recording prep.
