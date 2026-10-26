"""Page-level text: title, navigation, limitations and documented sources."""

TITLE = "Is cutting-edge AI becoming something only big tech can do?"

CONTENTS = [
    ("section-1", "1 · Who our audience could be, and how they relate"),
    ("section-2", "2 · Where the compute sits"),
    ("section-3", "3 · Who is paying for frontier AI data centres"),
    ("section-4", "4 · AI data-centre scale versus investment"),
    ("section-5", "5 · What the data cannot show"),
    ("sources", "Sources"),
]


def answer(segments, systems, owners) -> str:
    """On-screen answer; all displayed values are calculated from processed CSVs."""
    from charts.chart_d_map import by_country

    segment_table = segments.set_index("segment")
    public = segments[segments["sector_group"] == "Public"]["rmax_share_pct"].sum()
    public_systems = systems[systems["sector_group"] == "Public"]
    giant_public = public_systems[public_systems["rmax_tflops"] >= 1_000_000]
    giant_share = giant_public["rmax_tflops"].sum() / public_systems["rmax_tflops"].sum() * 100
    country_shares = by_country(systems, "All systems").set_index("country")["share_pct"]
    total = owners["capital_cost_2025usd_bn"].sum()
    big_five = owners[owners["owner"].isin(["Google", "Meta", "Amazon", "Microsoft", "SpaceXAI"])]["capital_cost_2025usd_bn"].sum()
    australia = owners[owners["country"].str.split("|").map(lambda places: "Australia" in places)]

    return (
        "**Short answer: for frontier AI, largely yes; for computing power in general, not yet.**\n\n"
        f"- **Frontier AI is being built by big tech.** Five companies (Google, Meta, Amazon, Microsoft and SpaceXAI) account "
        f"for **{big_five / total * 100:.1f}%** of the ${total:.1f}B spent on the {int(owners['n_datacenters'].sum())} largest AI data "
        "centres, and no university or public research body appears among the named owners (section 3).\n"
        f"- **Measured supercomputing is still mostly public.** Universities, research labs and government hold **{public:.1f}%** "
        f"of TOP500 compute, but {giant_share:.0f}% of that sits in just {len(giant_public)} giant national-lab machines. Universities run "
        f"{segment_table.loc['Academic', 'system_share_pct']:.1f}% of the machines yet hold only **{segment_table.loc['Academic', 'rmax_share_pct']:.1f}%** "
        "of the compute (section 1).\n"
        f"- **Both kinds of capacity lean towards the United States.** It holds {country_shares.get('United States', 0):.1f}% of TOP500 "
        f"compute. Australia holds {country_shares.get('Australia', 0):.1f}% and has {int(australia['n_datacenters'].sum())} listed AI data centre "
        f"({', '.join(australia['owner'])}, ${australia['capital_cost_2025usd_bn'].sum():.1f}B) (sections 2 and 3).\n\n"
        "**For the funder:** academics are not shut out of large-scale computing, because public labs hold most of it, but they own little "
        "of it themselves and none of the listed AI data centres. The TOP500 measures Linpack speed, not AI training, and neither dataset "
        "shows how much compute academics need or can access."
    )


LIMITS = (
    "- **TOP500 measures Linpack (HPL) performance, not AI-training capacity.** A high TOP500 position does not mean a facility can train frontier models.\n"
    "- **China has under-reported to TOP500 since 2023**, so non-Western public compute is undercounted.\n"
    "- **Epoch covers only 93 data centres.** Owner means the operator of a site, not the developer whose models are trained there, and 9 sites (11.8% of capex) have no known owner.\n"
    "- **Neither dataset measures how much compute any group needs or can access.** They show what each group holds (TOP500) or has spent (Epoch), not demand or who may use the machines.\n"
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
