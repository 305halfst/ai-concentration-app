"""Page-level text: title, introduction, contents, limitations and sources."""

TITLE = "Is cutting-edge AI becoming something only big tech can do?"

INTRO = (
    "This page asks who owns the world's computing power, for **a university research funding body deciding whether to "
    "fund shared compute for academics**. It uses two open datasets: the TOP500 list of supercomputers (June 2026) and "
    "Epoch AI's database of AI data centres (October 2026). Each chart is introduced by what to look for and followed by "
    "what it shows, and each section ends by leading into the next."
)

CONTENTS = [
    ("section-1", "1 · Who our audience is"),
    ("section-2", "2 · Where the compute sits"),
    ("section-3", "3 · Who is paying for frontier AI data centres"),
    ("section-4", "4 · What the data cannot show"),
    ("sources", "Sources"),
]

ANSWER = (
    "**Short answer:** building frontier-scale AI data centres is already a big-tech game. Public supercomputing is not, but it "
    "was not built for AI training, and universities hold only a small part of it. For the funder, the question is less whether "
    "public compute exists than whether academics can reach compute that fits AI work."
)

LIMITS = (
    "- **TOP500 measures Linpack (HPL) performance, not AI-training capacity.** A high TOP500 position does not mean a facility can train frontier models.\n"
    "- **China has under-reported to TOP500 since 2023**, so non-Western public compute is undercounted.\n"
    "- **Epoch covers only 93 data centres.** Owner means operator, not model developer (Anthropic trains on Amazon and SpaceXAI sites), and 9 sites (11.8% of capex) have no known owner.\n"
    "- **Both datasets are snapshots** (TOP500 June 2026, Epoch October 2026), not trends."
)

SOURCES = [
    ["fig4_top500_by_segment.csv", "6 rows: systems and Rmax share per segment", "top500/TOP500_202606.xlsx",
     "TOP500.org, TOP500 List June 2026", "No licence grant; © 1993–2026 TOP500.org, cited with attribution", "26d72ecb9eb8fcdcefb0df3a1b215f79"],
    ["top500_systems_clean.csv", "500 rows, one per supercomputer; 11 of 38 columns + sector_group", "top500/TOP500_202606.xlsx",
     "TOP500.org, TOP500 List June 2026", "as above", "26d72ecb9eb8fcdcefb0df3a1b215f79"],
    ["datacenters_by_owner_country.csv", "20 rows, one per data-centre owner", "epoch/data_centers.csv",
     "Epoch AI, ‘Data on AI data centers’ (Oct 2026)", "CC BY 4.0", "ea246ddea0bf7f561f99c1639662be23"],
]
SOURCE_COLUMNS = ["App file (data/processed/)", "What it holds", "Raw file (data/sources/)", "Publisher", "Licence", "Raw MD5"]
SOURCE_NOTE = (
    "Both raw files were downloaded on 11/10/2026 and left unedited. `python data/build_processed.py` checks both MD5s and "
    "writes the three app files. Map shapes: Natural Earth 1:110m via world-atlas 2.0.2 (ISC licence). Citations: Epoch AI, "
    "‘Data on AI data centers’, published online at epoch.ai · TOP500.org, TOP500 List June 2026."
)
