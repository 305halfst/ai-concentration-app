"""Page-level text: title, navigation, limitations and documented sources."""

TITLE = "Is cutting-edge AI becoming something only big tech can do?"

CONTENTS = [
    ("question", "Our answer"),
    ("section-1", "1 · Universities have been squeezed out of frontier AI"),
    ("section-2", "2 · Five companies own most of the tracked AI infrastructure"),
    ("section-3", "3 · Public institutions won the last race, not this one"),
    ("section-4", "4 · Universities and Australia barely register"),
    ("section-5", "5 · What it would take, and our ask"),
    ("limits", "What the data cannot show · Sources"),
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
    from charts.common import read

    gdp = read("au_gdp.csv").sort_values("year").iloc[-1]
    sites = read("datacenters_by_country.csv")

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
        "gdp_bn": float(gdp["gdp_usd_bn"]),
        "gdp_year": int(gdp["year"]),
        "n_sites": int(sites["n_datacenters"].sum()),
        "n_estimated": int(sites["n_estimated"].sum()),
    }


QUESTION_EXPLAINED = (
    "*Cutting-edge AI* means the most capable AI systems and the AI-specific data centres they are trained in. "
    "*Only big tech* means a handful of companies build and own almost all of it."
)


def hero(f: dict) -> list[tuple[str, str, str]]:
    """Three numbers that cover the whole of the three datasets, for the opening screen."""
    return [
        (f"Universities' share of notable AI systems, {f['t_last']}", f"{f['t_uni_last']:.1f}%",
         f"{f['t_uni_last'] - f['t_uni_first']:+.1f} points since {f['t_first']} ({f['t_uni_first']:.0f}%)"),
        ("Tracked AI chips owned by five companies", f"{f['big5_h100']:.1f}%",
         "estimated H100 equivalents, Epoch AI data centres, October 2026"),
        ("Universities or public labs among the owners", "0",
         f"of {f['named']} named owners of those AI data centres"),
    ]


def answer(f: dict) -> str:
    return (
        "### Yes. Frontier AI is becoming big tech's game.\n"
        f"The one piece of evidence against it, that public institutions run {f['public_rmax']:.1f}% of TOP500 "
        "supercomputing, measures general supercomputers' Linpack speed, not the AI-specific data centres where frontier "
        "models are trained (section 3)."
    )


AUDIENCE = ("**For:** an Australian Government officer deciding whether to fund shared AI computing for universities.")


def calculator(f: dict, target_pct: float) -> dict:
    """Chips a new public owner would need for `target_pct` of the tracked total, if other owners did not grow."""
    need = target_pct / (100 - target_pct) * f["h100_total"]
    return {"chips": need, "cost_bn": need * f["cost_per_h100"] / 1e9, "times_au": need / f["au_h100_n"],
            "gdp_pct": need * f["cost_per_h100"] / 1e9 / f["gdp_bn"] * 100}


def conclusion(f: dict) -> str:
    return (
        f"- Universities went from **{f['t_uni_first']:.0f}%** to **{f['t_uni_last']:.1f}%** of notable AI systems "
        f"({f['t_first']}–{f['t_last']}).\n"
        f"- Five companies own **{f['big5_h100']:.1f}%** of the tracked AI chips; no named owner is a university or public lab.\n"
        f"- Australia: **{f['au_top500']:.1f}%** of TOP500 compute, **{f['au_h100']:.1f}%** of the tracked AI chips."
    )


def recommendation(f: dict) -> str:
    one = calculator(f, 1.0)
    return (
        "### Fund shared GPU capacity for Australian universities, built on public research facilities such as Setonix "
        "(Pawsey).\n"
        f"Even 1% of today's tracked AI chips means about **{one['chips']:,.0f}** H100 equivalents, roughly "
        f"**${one['cost_bn']:.1f}B**: a national investment, not a university one. Alternatives we weighed: cloud credits "
        "(capacity stays private) and a larger AI share of existing machines (competes with current users). "
        "*This is our recommendation, not a finding of the data.*"
    )


def limits(ai_systems, owners) -> str:
    years = ai_systems[ai_systems["year"] >= 2010].groupby("year")["total_year"].first()
    unknown = owners.loc[owners["owner"] == "Unknown"]
    from charts.common import read
    sites = read("datacenters_by_country.csv")
    n_sites, n_est = int(sites["n_datacenters"].sum()), int(sites["n_estimated"].sum())
    return (
        "- **TOP500 measures Linpack speed, not AI training,** and only lists machines whose owners submit a result.\n"
        f"- **Notable AI systems are counted, not weighted:** {years.min()}–{years.max()} a year, so single systems move "
        "a share; recent years may be revised as Epoch adds systems.\n"
        f"- **Epoch tracks large AI data centres only.** {n_sites - n_est} of {n_sites} sites have no current "
        f"estimate; {int(unknown['n_datacenters'].sum())} sites ({unknown['capex_share_pct'].sum():.1f}% of estimated cost) "
        "have no known owner; owner means operator, not the model developer.\n"
        "- **Epoch estimates cost from power,** so cost and power are not independent.\n"
        "- **No dataset measures demand** or who may use a machine, and TOP500 and Epoch are snapshots.\n"
        "- **The calculator is an order of magnitude** (other owners held fixed, Epoch's average cost per chip), and the "
        "**recommendation is ours.**"
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
    ["au_gdp.csv", "5 rows, Australia's GDP 2021–2025 (US$ bn); used only for the calculator's share of GDP",
     "worldbank/MKTGDPAUA646NWDB.csv", "World Bank, GDP (current US$) NY.GDP.MKTP.CD, via FRED series MKTGDPAUA646NWDB "
     "(retrieved 26/10/2026)", "CC BY 4.0", "40729543b2a721515a3df7e20fb41f7b"],
    ["ai_systems_by_sector.csv", "305 rows, sector x year, 1950–2025", "owid/affiliation-researchers-building-artificial-intelligence-systems-all.csv",
     "Our World in Data, from Epoch AI notable AI systems (2026)", "CC BY 4.0", "9c5bdd24852b8a3d9b06c17e7f61df98"],
]

REFRESH_SHORT = ("Last data refresh: 11/10/2026 (TOP500 June 2026 list; Epoch AI October 2026 update; Our World in Data "
                 "notable AI systems); 26/10/2026 (World Bank GDP for Australia, calculator only).")
SOURCE_NOTE = (
    "The TOP500, Epoch AI and Our World in Data files were downloaded on 11/10/2026 and the World Bank GDP observations "
    "were copied from FRED on 26/10/2026; all four are kept unedited in `data/sources/`. `python data/build_processed.py` "
    "checks their MD5s and regenerates every processed file the app reads. Map shapes: Natural Earth 1:110m via "
    "world-atlas 2.0.2 (ISC licence)."
)
