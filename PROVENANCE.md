# AI provenance matrix

One row per substantive AI use. Every member owns at least one row. Each verification names a check that could have
failed, and the outcome says what happened.

| Artefact | Who | Tool | What was asked | What came back | How it was verified (a check that could have failed) | Outcome |
|---|---|---|---|---|---|---|
| `data/build_processed.py` + `data/processed/` | Kimkim | Claude | Clean the raw TOP500 and Epoch files into the tables the app reads | Cleaning script, processed CSVs and data dictionary section | Recomputed 59.88% (TOP500 Research share of Rmax) and $524.0B (Epoch total capital cost) in Excel from the raw files; the script asserts the source MD5s and primary-key uniqueness | Matched; kept. One bug found and fixed (the country lookup used a de-duplicated list) |
| `app.py` + `charts/` (page structure, charts A–D) | Kimkim | Claude | Build the Streamlit narrative from the three processed files, in the Session 2 page order, with no hover | App code, chart modules and an HTML preview | Summed `rmax_share_pct` for the Public rows of `fig4_top500_by_segment.csv` (59.88 + 10.04 + 1.34 = 71.26) and compared it with the app's 71.3%; cleared the Segments filter on chart C and checked that a message, not an error, appeared | Matched; kept. Chart C changed from a log-scale strip plot to a size-band heatmap after review, and a claim the data could not support was removed |
| <artefact> | <Member B> | <tool> | <what was asked> | <what came back> | <a check that could have failed> | <outcome> |
| <artefact> | <Member C> | <tool> | <what was asked> | <what came back> | <a check that could have failed> | <outcome> |
| <artefact> | <Member D> | <tool> | <what was asked> | <what came back> | <a check that could have failed> | <outcome> |

Add a row for any other tool the group used (for example, the dataset search in Part 1).
