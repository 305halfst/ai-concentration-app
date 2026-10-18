"""Page-level text: title, introduction, contents, limitations and sources."""

TITLE = "Is cutting-edge AI becoming something only big tech can do?"

INTRO = (
    "This page asks who owns the world's computing power, for **a university research funding body deciding whether to "
    "fund shared compute for academics**. It uses two open datasets: the TOP500 list of supercomputers (June 2026) and "
    "Epoch AI's database of AI data centres (October 2026). Each chart is introduced by what to look for and followed by "
    "what it shows, and each section ends by leading into the next."
)

CONTENTS = [
    ("section-1", "1 · Who our audience could be, and how they relate"),
    ("section-2", "2 · Where the compute sits"),
    ("section-3", "3 · Who is paying for frontier AI data centres"),
    ("section-4", "4 · What the data cannot show"),
    ("sources", "Sources"),
]

ANSWER = (
    "**Short answer:** building frontier-scale AI data centres is already a big-tech game: five companies account for most of "
    "the spending, and no university or public research body appears among the named owners. Measured supercomputing is not: the public sector "
    "holds most of the TOP500's compute. But the TOP500 measures Linpack speed, not AI training, and universities hold only a "
    "small part of it. For the funder, the question is less whether public compute exists than whether academics can reach it."
)

REFRESH = ("Data: TOP500 list, June 2026 · Epoch AI data centres, October 2026 update · "
           "last data refresh 11/10/2026 (both raw files downloaded that day). Sources are listed at the end of the page.")


def headline(segments, owners) -> list[tuple[str, str, str]]:
    """Three facts about the whole of both datasets, shown on the opening screen."""
    a = segments.set_index("segment")
    public = segments[segments["sector_group"] == "Public"]["rmax_share_pct"].sum()
    total = owners["capital_cost_2025usd_bn"].sum()
    big5 = owners[owners["owner"].isin(["Google", "Meta", "Amazon", "Microsoft", "SpaceXAI"])]["capital_cost_2025usd_bn"].sum()
    return [
        ("Public sector's share of TOP500 compute", f"{public:.1f}%",
         "Universities, research labs and government; % of the list's combined Rmax, June 2026"),
        ("Universities' share of TOP500 compute", f"{a.loc['Academic', 'rmax_share_pct']:.1f}%",
         f"versus {a.loc['Academic', 'system_share_pct']:.1f}% of the 500 machines, June 2026"),
        ("Five owners' share of AI data-centre spending", f"{big5 / total * 100:.1f}%",
         f"of ${total:.1f}B (2025 US dollars) across {int(owners['n_datacenters'].sum())} sites, Epoch AI, October 2026"),
    ]


LIMITS = (
    "- **TOP500 measures Linpack (HPL) performance, not AI-training capacity.** A high TOP500 position does not mean a facility can train frontier models.\n"
    "- **China has under-reported to TOP500 since 2023**, so non-Western public compute is undercounted.\n"
    "- **Epoch covers only 93 data centres.** Owner means the operator of a site, not the developer whose models are trained there, and 9 sites (11.8% of capex) have no known owner.\n"
    "- **Neither dataset measures how much compute any group needs.** They show what each group holds (TOP500) or has spent (Epoch), not its demand.\n"
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
REFRESH_SHORT = "Last data refresh: 11/10/2026 (TOP500 June 2026 list; Epoch AI October 2026 update)."
SOURCE_COLUMNS = ["App file (data/processed/)", "What it holds", "Raw file (data/sources/)", "Publisher", "Licence", "Raw MD5"]
SOURCE_NOTE = (
    "Both raw files were downloaded on 11/10/2026 and left unedited. `python data/build_processed.py` checks both MD5s and "
    "writes the three app files. Map shapes: Natural Earth 1:110m via world-atlas 2.0.2 (ISC licence). Citations: Epoch AI, "
    "‘Data on AI data centers’, published online at epoch.ai · TOP500.org, TOP500 List June 2026."
)
