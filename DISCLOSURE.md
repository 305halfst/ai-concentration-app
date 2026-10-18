# Data and AI disclosure statement

## Data

The app uses two public datasets, both downloaded on 11/10/2026 and kept unedited in `data/sources/`:

- **TOP500.org, TOP500 List June 2026** (`data/sources/top500/TOP500_202606.xlsx`, MD5 `26d72ecb9eb8fcdcefb0df3a1b215f79`).
  No licence grant; © 1993–2026 TOP500.org, cited with attribution.
- **Epoch AI, ‘Data on AI data centers’, October 2026 update** (`data/sources/epoch/data_centers.csv`,
  MD5 `ea246ddea0bf7f561f99c1639662be23`). CC BY 4.0. Published online at epoch.ai.

Map shapes come from Natural Earth 1:110m via world-atlas 2.0.2 (ISC licence). The three files in `data/processed/`
are produced only by `data/build_processed.py`; the transforms are documented in `data/data_dictionary_en.md`.

## AI

<Edit to match what the group actually did.> We used generative AI tools during this project. Each substantive use
is recorded in `PROVENANCE.md`, with what was asked, what came back and the check we ran on it. Claude was used to
write the data-cleaning script and the Streamlit app code; <other tools and members>. We did not accept any AI output
without checking it: numbers shown in the app were recomputed from the source files, and the app was run and tested
by the group. The question, persona, choice of datasets, chart choices and final wording are the group's own, and the
group is responsible for every claim in the app.
