"""Page-level text: title, navigation, limitations and documented sources."""

TITLE = "Is cutting-edge AI becoming something only big tech can do?"

CONTENTS = [
    ("audience", "Who this page is for"),
    ("section-1", "1 · Who owns frontier AI infrastructure"),
    ("section-2", "2 · What the public sector holds"),
    ("conclusion", "3 · Conclusion"),
    ("recommendation", "4 · Our recommendation"),
    ("section-5", "5 · What the data cannot show"),
    ("sources", "Sources"),
]

BIG_FIVE = ["Google", "Meta", "Amazon", "Microsoft", "SpaceXAI"]


def _figures(segments, systems, owners) -> dict:
    """Every number used in the opening, conclusion and recommendation, computed from data/processed/."""
    from charts.chart_d_map import by_country

    h100 = owners["h100_equivalents"].sum()
    countries = by_country(systems, "All systems").set_index("country")["share_pct"]
    australia = owners[owners["country"].str.split("|").map(lambda places: "Australia" in places)]
    seg = segments.set_index("segment")
    return {
        "public_rmax": segments[segments["sector_group"] == "Public"]["rmax_share_pct"].sum(),
        "big5_h100": owners[owners["owner"].isin(BIG_FIVE)]["h100_equivalents"].sum() / h100 * 100,
        "named": int((owners["owner"] != "Unknown").sum()),
        "unknown_sites": int(owners.loc[owners["owner"] == "Unknown", "n_datacenters"].sum()),
        "sites": int(owners["n_datacenters"].sum()),
        "uni_systems": seg.loc["Academic", "system_share_pct"],
        "uni_rmax": seg.loc["Academic", "rmax_share_pct"],
        "au_top500": countries.get("Australia", 0),
        "au_owner": ", ".join(australia["owner"]),
        "au_h100": australia["h100_equivalents"].sum() / h100 * 100,
    }


QUESTION_FOR_READER = (
    "Would you accept a future in which a handful of companies control a critical technology? "
    "This page shows how close that future already is for AI, and what Australia could do about it."
)


def opening(segments, systems, owners) -> str:
    f = _figures(segments, systems, owners)
    return (
        "### Big tech is building the AI factories. None of the named owners is a university or public lab.\n\n"
        f"**Short answer: for AI-specific infrastructure, largely yes.** Five companies hold **{f['big5_h100']:.1f}%** of the "
        f"estimated AI chips in the data centres Epoch tracks; public institutions still run **{f['public_rmax']:.1f}%** of "
        "TOP500 supercomputing, which measures Linpack speed, not AI training."
    )


AUDIENCE = (
    "A policy officer in the Australian Government who funds research infrastructure and must "
    "decide whether to invest in shared AI computing capacity for universities. The page answers the three questions they "
    "would ask, in order:\n\n"
    "1. **Who owns the infrastructure that frontier AI runs on?** (section 1)\n"
    "2. **What does the public sector, including Australia, already hold?** (section 2)\n"
    "3. **What should we do?** (sections 3 and 4)"
)


def conclusion(segments, systems, owners) -> str:
    f = _figures(segments, systems, owners)
    return (
        f"- **AI-specific capacity is concentrated:** five companies hold {f['big5_h100']:.1f}% of the estimated AI chips, and "
        f"none of the {f['named']} named owners is a university or public research body ({f['unknown_sites']} sites have no "
        "known owner).\n"
        f"- **Public capacity exists, but it is a different kind:** the public sector runs {f['public_rmax']:.1f}% of TOP500 "
        f"supercomputing, measured by Linpack speed. Universities run {f['uni_systems']:.1f}% of those machines but hold "
        f"{f['uni_rmax']:.1f}% of the compute.\n"
        f"- **Australia is a small player in both:** {f['au_top500']:.1f}% of TOP500 compute, and its only listed AI data "
        f"centre ({f['au_owner']}) holds {f['au_h100']:.1f}% of the estimated AI chips.\n\n"
        "*Our reading (an interpretation, not a finding of the data):* if nothing changes, the AI-specific computing that "
        "Australian researchers depend on will be owned by a handful of overseas companies."
    )


def recommendation(segments, systems, owners) -> str:
    f = _figures(segments, systems, owners)
    return (
        "**Fund dedicated, shared GPU capacity for Australian university researchers, building on existing public research "
        "facilities such as Setonix at the Pawsey Supercomputing Centre.**\n\n"
        f"- **Why:** none of the {f['named']} named owners of large AI data centres is a university or public research body, "
        f"and Australia's only listed site holds {f['au_h100']:.1f}% of the estimated AI chips.\n"
        "- **Alternatives we considered:** negotiating research compute credits with cloud providers (faster to start, but "
        "leaves capacity in private hands); giving AI work a larger share of existing national facilities (quicker to start, but "
        "AI work would compete with existing users for the same machines).\n"
        "- **What the data cannot tell us:** how much compute researchers need, which option is cheapest, or whether "
        "commercial facilities would open to universities.\n\n"
        "*This is our recommendation, not a finding of the data.*"
    )


LIMITS = (
    "- **TOP500 measures Linpack (HPL) performance, not AI-training capacity.** A high TOP500 position does not mean a facility can train frontier models.\n"
    "- **China has under-reported to TOP500 since 2023**, so non-Western public compute is undercounted.\n"
    "- **Epoch tracks 93 large AI data centres, not every one.** Owner means the operator of a site, not the developer whose models are trained there, and 9 sites (11.8% of capex) have no known owner.\n"
    "- **Neither dataset measures how much compute any group needs or can access.** They show what each group holds (TOP500) or the estimated cost of what it owns (Epoch), not demand or who may use the machines.\n"
    "- **Epoch estimates capital cost from power,** so cost and power are not independent measures; 20 of the 93 sites it tracks have no current estimate yet.\n"
    "- **The recommendation is ours.** The data shows the gap; it does not show the best way to close it.\n"
    "- **Both datasets are snapshots** (TOP500 June 2026, Epoch October 2026), not trends."
)


SOURCES = [
    ["fig4_top500_by_segment.csv", "6 rows: systems and Rmax share per segment", "top500/TOP500_202606.xlsx",
     "TOP500.org, TOP500 List June 2026", "No licence grant; © 1993–2026 TOP500.org, cited with attribution", "26d72ecb9eb8fcdcefb0df3a1b215f79"],
    ["top500_systems_clean.csv", "500 rows, one per supercomputer; 11 of 38 columns plus sector_group", "top500/TOP500_202606.xlsx",
     "TOP500.org, TOP500 List June 2026", "as above", "26d72ecb9eb8fcdcefb0df3a1b215f79"],
    ["datacenters_by_owner_country.csv", "20 rows, one per data-centre owner", "epoch/data_centers.csv",
     "Epoch AI, Data on AI data centers (October 2026 update)", "CC BY 4.0", "ea246ddea0bf7f561f99c1639662be23"],
]

REFRESH_SHORT = "Last documented data refresh: 11 October 2026 (TOP500 June 2026 list; Epoch AI October 2026 update)."
SOURCE_NOTE = (
    "Both raw files were downloaded on 11/10/2026 and kept unedited in `data/sources/`. `python data/build_processed.py` "
    "checks both MD5s and regenerates the three processed files the app reads. Map shapes: Natural Earth 1:110m via "
    "world-atlas 2.0.2 (ISC licence)."
)
