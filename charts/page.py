"""Page-level text: title, navigation, limitations and documented sources."""

TITLE = "Is cutting-edge AI becoming something only big tech can do?"

CONTENTS = [
    ("question", "The question, and our answer"),
    ("section-1", "1 · Frontier AI is becoming an industry game"),
    ("section-2", "2 · Who owns the AI infrastructure today"),
    ("section-3", "3 · Strong in the old race, absent from the new one"),
    ("section-4", "4 · Universities and Australia"),
    ("section-5", "5 · What it would take, and our recommendation"),
    ("limits", "6 · What the data cannot show"),
    ("sources", "Sources"),
]

BIG_FIVE = ["Google", "Meta", "Amazon", "Microsoft", "SpaceXAI"]

QUESTION_FOR_READER = (
    "Would you accept a future in which a handful of companies control a critical technology? "
    "This page shows how close that future already is for AI, and what Australia could do about it."
)


def figures(segments, systems, owners, ai_systems) -> dict:
    """Every number used in the opening, conclusion and recommendation, computed from data/processed/."""
    from charts.chart_d_map import by_country
    from charts.chart_t_time import facts

    h100 = owners["h100_equivalents"].sum()
    countries = by_country(systems, "All systems").set_index("country")["share_pct"]
    australia = owners[owners["country"].str.split("|").map(lambda places: "Australia" in places)]
    seg = segments.set_index("segment")
    return {
        **{"t_" + k: v for k, v in facts(ai_systems).items()},
        "public_rmax": segments[segments["sector_group"] == "Public"]["rmax_share_pct"].sum(),
        "big5_h100": owners[owners["owner"].isin(BIG_FIVE)]["h100_equivalents"].sum() / h100 * 100,
        "named": int((owners["owner"] != "Unknown").sum()),
        "unknown_sites": int(owners.loc[owners["owner"] == "Unknown", "n_datacenters"].sum()),
        "uni_systems": seg.loc["Academic", "system_share_pct"],
        "uni_rmax": seg.loc["Academic", "rmax_share_pct"],
        "au_top500": countries.get("Australia", 0),
        "au_owner": ", ".join(australia["owner"]),
        "au_h100_n": australia["h100_equivalents"].sum(),
        "au_h100": australia["h100_equivalents"].sum() / h100 * 100,
        "h100_total": h100,
        "cost_per_h100": owners["capital_cost_2025usd_bn"].sum() * 1e9 / h100,
    }


QUESTION_EXPLAINED = (
    "**What we mean.** *Cutting-edge AI* is the frontier: the most capable AI systems, and the AI-specific data centres "
    "they are trained in. *Only big tech can do it* would mean that a handful of companies build and own almost all of "
    "it, so that universities and public institutions cannot. The question is open: public institutions still run most of "
    "the world's measured supercomputing, so the same data can be read both ways."
)


def answer(f: dict) -> str:
    return (
        "### Big tech is building the AI factories. None of the named owners is a university or public lab.\n\n"
        f"**Our answer: for frontier AI, largely yes.** Industry built **{f['t_ind_last']:.1f}%** of notable AI systems in "
        f"{f['t_last']} (universities: {f['t_uni_first']:.0f}% in {f['t_first']}, {f['t_uni_last']:.1f}% in {f['t_last']}), and "
        f"five companies hold **{f['big5_h100']:.1f}%** of the estimated AI chips in the data centres Epoch AI tracks. "
        f"Public institutions still run **{f['public_rmax']:.1f}%** of TOP500 supercomputing, but that list measures "
        "Linpack speed, not AI training."
    )


AUDIENCE = (
    "**Who this page is for:** a policy officer in the Australian Government who funds research infrastructure and must "
    "decide whether to invest in shared AI computing capacity for universities. The sections answer, in order: *Is AI "
    "really becoming an industry activity?* (1) *Who owns the infrastructure?* (2, 3) *Where do universities and Australia "
    "stand?* (4) *What should we do, and what would it cost?* (5)"
)


def calculator(f: dict, target_pct: float) -> dict:
    """Chips a new public owner would need for `target_pct` of the tracked total, if other owners did not grow."""
    need = target_pct / (100 - target_pct) * f["h100_total"]
    return {"chips": need, "cost_bn": need * f["cost_per_h100"] / 1e9, "times_au": need / f["au_h100_n"]}


def conclusion(f: dict) -> str:
    return (
        f"- **AI is becoming an industry activity:** universities built {f['t_uni_first']:.0f}% of notable AI systems in "
        f"{f['t_first']} and {f['t_uni_last']:.1f}% in {f['t_last']}; industry overtook them in {f['t_cross']}.\n"
        f"- **The infrastructure is concentrated:** five companies hold {f['big5_h100']:.1f}% of the estimated AI chips, and "
        f"none of the {f['named']} named owners is a university or public research body ({f['unknown_sites']} sites have no "
        "known owner).\n"
        f"- **Public capacity exists, but it is a different kind:** the public sector runs {f['public_rmax']:.1f}% of TOP500 "
        f"supercomputing (Linpack). Universities run {f['uni_systems']:.1f}% of those machines but hold {f['uni_rmax']:.1f}% "
        "of the compute.\n"
        f"- **Australia is a small player in both:** {f['au_top500']:.1f}% of TOP500 compute, and its only listed AI data "
        f"centre ({f['au_owner']}) holds {f['au_h100']:.1f}% of the estimated AI chips.\n\n"
        "*Our reading (an interpretation, not a finding of the data):* if nothing changes, the AI-specific computing that "
        "Australian researchers depend on will be built and owned by a handful of overseas companies."
    )


def recommendation(f: dict) -> str:
    one = calculator(f, 1.0)
    return (
        "**Fund dedicated, shared GPU capacity for Australian university researchers, building on existing public research "
        "facilities such as Setonix at the Pawsey Supercomputing Centre.**\n\n"
        f"- **Why:** universities' share of notable AI systems fell to {f['t_uni_last']:.1f}%; none of the {f['named']} named "
        f"owners of large AI data centres is a university or public research body; Australia's only listed site holds "
        f"{f['au_h100']:.1f}% of the estimated AI chips.\n"
        f"- **Scale:** even 1% of today's tracked AI chips would mean about {one['chips']:,.0f} H100 equivalents, roughly "
        f"${one['cost_bn']:.1f}B at Epoch's average cost — a national, not a single-university, investment.\n"
        "- **Alternatives we considered:** research compute credits from cloud providers (faster to start, but the capacity "
        "stays in private hands); a larger AI share of existing national facilities (quicker, but AI work would compete with "
        "existing users for the same machines).\n"
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
    "- **Notable AI systems are counted, not weighted.** Each year has 10–106 systems, so one or two systems move a share by several points; the trend matters more than any single year.\n"
    "- **The calculator is an order of magnitude, not a budget.** It assumes other owners do not grow and uses Epoch's average estimated cost per chip.\n"
    "- **TOP500 and the Epoch data centres are snapshots** (June 2026, October 2026); only the notable-systems series shows change over time."
)


SOURCES = [
    ["fig4_top500_by_segment.csv", "6 rows: systems and Rmax share per segment", "top500/TOP500_202606.xlsx",
     "TOP500.org, TOP500 List June 2026", "No licence grant; © 1993–2026 TOP500.org, cited with attribution", "26d72ecb9eb8fcdcefb0df3a1b215f79"],
    ["top500_systems_clean.csv", "500 rows, one per supercomputer; 11 of 38 columns plus sector_group", "top500/TOP500_202606.xlsx",
     "TOP500.org, TOP500 List June 2026", "as above", "26d72ecb9eb8fcdcefb0df3a1b215f79"],
    ["datacenters_by_owner_country.csv", "20 rows, one per data-centre owner", "epoch/data_centers.csv",
     "Epoch AI, Data on AI data centers (October 2026 update)", "CC BY 4.0", "ea246ddea0bf7f561f99c1639662be23"],
    ["datacenters_by_country.csv", "12 rows, one per site country", "epoch/data_centers.csv",
     "Epoch AI, Data on AI data centers (October 2026 update)", "CC BY 4.0", "ea246ddea0bf7f561f99c1639662be23"],
    ["ai_systems_by_sector.csv", "305 rows, sector x year, 1950–2025", "owid/affiliation-researchers-building-artificial-intelligence-systems-all.csv",
     "Our World in Data, from Epoch AI notable AI systems (2026)", "CC BY 4.0", "9c5bdd24852b8a3d9b06c17e7f61df98"],
]

REFRESH_SHORT = "Last data refresh: 11/10/2026 (TOP500 June 2026 list; Epoch AI October 2026 update; Our World in Data notable AI systems)."
SOURCE_NOTE = (
    "All three raw files were downloaded on 11/10/2026 and kept unedited in `data/sources/`. `python data/build_processed.py` "
    "checks their MD5s and regenerates every processed file the app reads. Map shapes: Natural Earth 1:110m via "
    "world-atlas 2.0.2 (ISC licence)."
)
