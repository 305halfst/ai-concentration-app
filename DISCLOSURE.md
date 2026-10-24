# Data and AI disclosure statement

## Data

The app uses two public datasets. The data dictionary records the source URLs, fields, units, keys, time coverage and
transforms. The TOP500 source below is the exact committed June 2026 XLSX. Epoch's publisher now serves a later CSV
release, so the committed Epoch file is a source sample retrieved on 24/10/2026 rather than a false claim that it is the
app's earlier 11/10/2026 snapshot:

- **TOP500.org, TOP500 List June 2026** (`data/sources/top500/TOP500_202606.xlsx`, MD5 `26d72ecb9eb8fcdcefb0df3a1b215f79`).
  No licence grant; © 1993–2026 TOP500.org, cited with attribution.
- **Epoch AI, ‘Data on AI data centers’** (`data/sources/epoch/data_centers.csv`,
  MD5 `1cf2924b3775c599761b397edb0a2b17`, retrieved 24/10/2026). CC BY 4.0. Published online at epoch.ai.

Map shapes come from Natural Earth 1:110m via world-atlas 2.0.2 (ISC licence). The three files in `data/processed/`
are documented in `data/data_dictionary_en.md`. The original 11/10/2026 Epoch snapshot and build script are not in this
checkout, so they must be restored before claiming the processed Epoch aggregation is fully reproducible.

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
