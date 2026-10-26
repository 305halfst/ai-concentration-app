"""Page-level text: title, navigation, limitations and documented sources."""

TITLE = "Is cutting-edge AI becoming something only big tech can do?"

CONTENTS = [
    ("question", "Our answer"),
    ("section-1", "1 · Universities have been squeezed out of frontier AI"),
    ("section-2", "2 · Five companies own most of the tracked AI infrastructure"),
    ("section-3", "3 · Public institutions won the last race, not this one"),
    ("section-4", "4 · Universities and Australia barely register"),
    ("section-5", "5 · What it would take, and our ask"),
    ("limits", "What the data cannot show"),
    ("summary", "In summary · Sources"),
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
    budget = read("au_budget.csv").iloc[0]
    firmus = owners.set_index("owner").loc["Firmus"]

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
        "fed_pct_gdp": float(budget["pct_gdp"]),
        "fed_aud_bn": float(budget["aud_bn"]),
        "fed_year": str(budget["year"]),
        "firmus_h100": float(firmus["h100_equivalents"]),
        "firmus_cost_bn": float(firmus["capital_cost_2025usd_bn"]),
        "firmus_mw": float(firmus["power_mw"]),
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
    """A public share `target_pct` of today's tracked AI chips (other owners held fixed), built as university AI sites
    the size of Firmus (Australia's only tracked site) and costed at Firmus's estimated cost per site."""
    chips = target_pct / (100 - target_pct) * f["h100_total"]
    sites = chips / f["firmus_h100"]
    cost = sites * f["firmus_cost_bn"]
    gdp_pct = cost / f["gdp_bn"] * 100
    return {"chips": chips, "sites": sites, "cost_bn": cost, "gdp_pct": gdp_pct, "fed_pct": gdp_pct / f["fed_pct_gdp"] * 100}


def conclusion(f: dict) -> str:
    return (
        f"- Universities went from **{f['t_uni_first']:.0f}%** to **{f['t_uni_last']:.1f}%** of notable AI systems "
        f"({f['t_first']}–{f['t_last']}).\n"
        f"- Five companies own **{f['big5_h100']:.1f}%** of the tracked AI chips; no named owner is a university or public lab.\n"
        f"- Australia: **{f['au_top500']:.1f}%** of TOP500 compute, **{f['au_h100']:.1f}%** of the tracked AI chips."
    )


def recommendation(f: dict) -> str:
    one, five = calculator(f, 1.0), calculator(f, 5.0)
    return (
        "### Fund shared GPU capacity for Australian universities, built on public research facilities such as Setonix "
        "(Pawsey).\n"
        f"Even 1% of today's tracked AI chips means about **{one['sites']:.0f}** Firmus-sized sites, roughly "
        f"**${one['cost_bn']:.1f}B**, or **{one['fed_pct']:.1f}%** of one year's federal spending; 5% would take "
        f"**{five['sites']:.0f}** sites and **{five['fed_pct']:.1f}%**. A national investment spread over several budgets, "
        "not a university one. Alternatives we weighed: cloud credits (capacity stays private) and a larger AI share of "
        "existing machines (competes with current users). *This is our recommendation, not a finding of the data.*"
    )


def limits(ai_systems, owners, f: dict) -> str:
    years = ai_systems[ai_systems["year"] >= 2010].groupby("year")["total_year"].first()
    unknown = owners.loc[owners["owner"] == "Unknown"]
    n_sites, n_est = f["n_sites"], f["n_estimated"]
    return (
        "**What each dataset measures**\n\n"
        "- **TOP500 measures Linpack speed, not AI training,** and lists only machines whose owners submit a result. It "
        f"is the one dataset where the public sector leads ({f['public_rmax']:.1f}% of compute), so our Yes rests on the "
        "AI-specific data, not on TOP500.\n"
        f"- **Notable AI systems are counted, not weighted:** {years.min()}–{years.max()} a year, so a few systems move a "
        "share; the sector is that of the researchers' organisations, and recent years may be revised.\n"
        f"- **Epoch tracks only very large AI data centres.** The 0 universities among the owners is about scale: no "
        "university or public lab runs a site that large, which does not mean universities have no AI computing. "
        f"{n_sites - n_est} of {n_sites} sites have no current estimate; {int(unknown['n_datacenters'].sum())} sites "
        f"({unknown['capex_share_pct'].sum():.1f}% of estimated cost) have no known owner; owner means operator, not the "
        "model developer; and Epoch estimates cost from power, so the two are not independent.\n\n"
        "**What no dataset shows**\n\n"
        "- **Demand and access:** how much compute Australian researchers need, or can already rent or borrow from "
        "overseas and from companies.\n"
        "- **Trends in ownership of AI data centres:** TOP500 and Epoch are snapshots (June and October 2026).\n"
        "- **University budgets:** the sources give no separate federal higher-education figure, so the calculator compares "
        "the cost with GDP and total federal spending only.\n\n"
        "**How far the calculator goes**\n\n"
        "- **An order of magnitude, not a budget:** other owners are held at today's size; new capacity "
        f"is costed at Epoch's capital-cost estimate for Firmus (${f['firmus_cost_bn']:.2f}B per site), without running, "
        "power or staff costs.\n"
        f"- **One-off cost against one year:** GDP is calendar {f['gdp_year']} and federal spending is {f['fed_year']}; "
        "a build spread over several years would take a smaller share each year.\n"
        "- **The recommendation is ours,** not a finding of the data."
    )


def summary(f: dict) -> str:
    one, five = calculator(f, 1.0), calculator(f, 5.0)
    return (
        "### Yes: cutting-edge AI is becoming something only big tech can do.\n"
        f"- **The builders changed.** Universities built **{f['t_uni_first']:.0f}%** of notable AI systems in "
        f"{f['t_first']} and **{f['t_uni_last']:.1f}%** in {f['t_last']}; industry has led since {f['t_cross']}.\n"
        f"- **The infrastructure is owned by companies.** Five of them hold **{f['big5_h100']:.1f}%** of the tracked AI "
        f"chips, and none of the {f['named']} named owners is a university or public lab.\n"
        f"- **Public strength is in the old race.** Public institutions run **{f['public_rmax']:.1f}%** of TOP500 "
        f"supercomputing, but universities hold {f['uni_rmax']:.1f}% of it and Australia {f['au_top500']:.1f}%.\n"
        f"- **Catching up is a national decision, and an affordable one.** A **1%** public share means about "
        f"**{one['sites']:.0f}** Firmus-sized sites, **${one['cost_bn']:.1f}B** or **{one['fed_pct']:.1f}%** of one "
        f"year's federal spending; **5%** means **{five['sites']:.0f}** sites and **{five['fed_pct']:.1f}%**.\n\n"
        "**For the decision:** without public investment, Australian university researchers will depend on capacity that "
        "a handful of companies own. Funding shared GPU capacity, starting from public facilities such as "
        "Setonix (Pawsey), is the lever the government controls. *This is our reading of the data and our recommendation.*"
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
    ["au_gdp.csv", "66 rows, Australia's GDP 1960–2025 (US$ bn); used only for the calculator's share of GDP",
     "worldbank/MKTGDPAUA646NWDB.csv", "World Bank, GDP (current US$) NY.GDP.MKTP.CD, via FRED series MKTGDPAUA646NWDB "
     "(retrieved 26/10/2026)", "CC BY 4.0", "2b4932edc8a10823709181e37b9c95b4"],
    ["au_budget.csv", "1 row, Australian Government total expenses 2025-26 (A$ bn and % of GDP); calculator only",
     "pbo/2025-26_Medium-Term_Budget_Outlook_-_Beyond_the_Budget_-_Data.xlsx", "Parliamentary Budget Office, 2025-26 Medium-term budget outlook, Table B-2 "
     "(retrieved 26/10/2026)", "CC BY 4.0", "16a4006e8a5b43df88610341b0b26ce6"],
    ["ai_systems_by_sector.csv", "305 rows, sector x year, 1950–2025", "owid/affiliation-researchers-building-artificial-intelligence-systems-all.csv",
     "Our World in Data, from Epoch AI notable AI systems (2026)", "CC BY 4.0", "9c5bdd24852b8a3d9b06c17e7f61df98"],
]

REFRESH_SHORT = ("Last data refresh: 11/10/2026 (TOP500 June 2026 list; Epoch AI October 2026 update; Our World in Data "
                 "notable AI systems); 26/10/2026 (World Bank GDP and PBO federal expenses, calculator only).")
SOURCE_NOTE = (
    "The TOP500, Epoch AI and Our World in Data files were downloaded on 11/10/2026, the World Bank GDP file from FRED on "
    "26/10/2026, and the PBO budget-outlook data workbook on 26/10/2026; all five are kept unedited in `data/sources/`. `python data/build_processed.py` "
    "checks their MD5s and regenerates every processed file the app reads. Map shapes: Natural Earth 1:110m via "
    "world-atlas 2.0.2 (ISC licence)."
)
