"""Section 2 / Chart D - TOP500 compute by country (choropleth; Spatial) with a labelled top-10 bar,
a compared country that is always labelled, and a full country table.

Reads data/processed/top500_systems_clean.csv. Country shapes: static/countries-110m.json
(world-atlas 2.0.2, Natural Earth 1:110m, ISC licence). Singapore has no shape at 1:110m, so the table is the
only place its value appears.
"""

from __future__ import annotations

import json

import altair as alt
import pandas as pd

from charts.common import INK, PUBLIC, TEAL

FILE = "top500_systems_clean.csv"
GROUPS = ["All systems", "Public sector only", "Private sector only"]
DEFAULT_FOCUS = "Australia"
MAP_NAMES = {"United States": "United States of America"}
BINS = [(0, 0.5, "under 0.5%"), (0.5, 1, "0.5–1%"), (1, 2.5, "1–2.5%"), (2.5, 5, "2.5–5%"),
        (5, 10, "5–10%"), (10, 20, "10–20%"), (20, 101, "20% or more")]
BLUES = ["#DCE8F5", "#B7CFE8", "#8AB0D8", "#5B8DC4", "#356BA8", "#1F4E8C", "#0B2A55"]
NO_DATA = "No system on the list"


def by_country(df: pd.DataFrame, group: str) -> pd.DataFrame:
    sel = df if group == GROUPS[0] else df[df["sector_group"] == group.split()[0]]
    out = sel.groupby("country", as_index=False).agg(systems=("rank", "size"), rmax_tflops=("rmax_tflops", "sum"))
    out["share_pct"] = out["rmax_tflops"] / out["rmax_tflops"].sum() * 100
    out["bin"] = out["share_pct"].map(lambda s: next(label for low, high, label in BINS if low <= s < high))
    out["map_name"] = out["country"].replace(MAP_NAMES)
    out = out.sort_values("share_pct", ascending=False).reset_index(drop=True)
    out["rank"] = out.index + 1
    return out


def countries(df: pd.DataFrame) -> list[str]:
    return sorted(df["country"].unique())


def share_label(value: float) -> str:
    """One decimal, but never round a non-zero share down to 0.0%."""
    return f"{value:.2f}%" if value < 0.1 else f"{value:.1f}%"


def build_map(table: pd.DataFrame, shapes: alt.Data, focus: str) -> alt.LayerChart:
    domain = [label for _, _, label in BINS] + [NO_DATA]
    land = (alt.Chart(shapes).mark_geoshape(stroke="#6B737B", strokeWidth=0.4)
            .transform_lookup(lookup="properties.name", from_=alt.LookupData(table, key="map_name", fields=["bin"]))
            .transform_calculate(bin=f"datum.bin ? datum.bin : '{NO_DATA}'")
            .transform_filter("datum.properties.name != 'Antarctica'")
            .encode(color=alt.Color("bin:N", title="Share of Rmax (%)", sort=domain,
                                    scale=alt.Scale(domain=domain, range=BLUES + ["#FFFFFF"]),
                                    legend=alt.Legend(orient="bottom-left", direction="vertical", fillColor="#FFFFFF", padding=8,
                                                      strokeColor=INK, symbolType="square", symbolStrokeColor="#6B737B",
                                                      symbolStrokeWidth=0.6, labelFontSize=11))))
    outline = (alt.Chart(shapes).mark_geoshape(fillOpacity=0, stroke=TEAL, strokeWidth=2.5)
               .transform_filter(f"datum.properties.name == {json.dumps(MAP_NAMES.get(focus, focus))}"))
    return (land + outline).project("equalEarth").properties(height=440)


def bar_rows(table: pd.DataFrame, focus: str) -> pd.DataFrame:
    """The ten largest shares, plus the compared country when it ranks lower."""
    rows = pd.concat([table.head(10), table[(table["country"] == focus) & (table["rank"] > 10)]])
    return rows.assign(
        label=rows["share_pct"].map(share_label),
        bar_label="#" + rows["rank"].astype(str) + " " + rows["country"],
        group=rows["country"].map(lambda c: "Compared country" if c == focus else "Ten largest shares"),
    )


def build_bar(table: pd.DataFrame, focus: str) -> alt.LayerChart:
    rows = bar_rows(table, focus)
    base = alt.Chart(rows).encode(
        y=alt.Y("bar_label:N", sort=list(rows["bar_label"]), title="Country (#rank)"),
        x=alt.X("share_pct:Q", title="Share of the selected systems' Rmax (%)",
                scale=alt.Scale(domain=[0, max(45, rows["share_pct"].max() * 1.15)])))
    bars = base.mark_bar(height=14).encode(
        color=alt.Color("group:N", title="Bar colour", scale=alt.Scale(domain=["Ten largest shares", "Compared country"], range=[PUBLIC, TEAL])))
    return (bars + base.mark_text(align="left", dx=4, fontSize=12, color=INK).encode(text="label:N")
            ).properties(height=26 * len(rows) + 20)


def focus_line(table: pd.DataFrame, focus: str, group: str) -> str | None:
    """One sentence on the compared country, or None when it has no system in the selection."""
    row = table[table["country"] == focus]
    if row.empty:
        return None
    r = row.iloc[0]
    return (f"**{focus}** ranks **#{r['rank']} of {len(table)}** countries for {group.lower()}: "
            f"{r['systems']} system{'s' if r['systems'] != 1 else ''} with a combined Rmax of {r['rmax_tflops']:,.0f} TFlop/s, "
            f"**{share_label(r['share_pct'])}** of the selected systems' Rmax.")


def country_table(table: pd.DataFrame) -> pd.DataFrame:
    return (table[["rank", "country", "systems", "rmax_tflops", "share_pct"]]
            .assign(rmax_tflops=lambda f: f["rmax_tflops"].round(0).astype(int), share_pct=lambda f: f["share_pct"].round(2))
            .rename(columns={"rank": "Rank", "country": "Country", "systems": "Systems",
                             "rmax_tflops": "Combined Rmax (TFlop/s)", "share_pct": "Share of Rmax (%)"}))


def texts(df: pd.DataFrame, group: str) -> dict[str, str]:
    table = by_country(df, group).set_index("country")["share_pct"]
    pub = by_country(df, GROUPS[1]).set_index("country")["share_pct"]
    pri = by_country(df, GROUPS[2]).set_index("country")["share_pct"]
    lead3 = [f"{c} (**{v:.1f}%**)" for c, v in table.head(3).items()]
    top3 = ", ".join(lead3[:-1]) + " and " + lead3[-1]
    return {
        "title": "2 · Where the compute sits",
        "caption": ("Chart D. Share of the combined Rmax of TOP500 systems (June 2026 list) located in each country, for the "
                    "selected systems; the bar lists the ten largest shares plus the compared country, and the table lists every "
                    "country. Units: % of the selected systems' Rmax; Rmax in TFlop/s."),
        "lead": (
            "The map shades each country by its share of the TOP500's combined Rmax; white countries have no system on the list. "
            "The bar below it labels the ten largest shares, because small countries such as Singapore are too small to see on a "
            "world map. Switch between all, public and private systems, and pick a country to compare: it is outlined in green "
            "on the map and always added to the bar, even when it ranks below the top ten. The table below lists every country."
        ),
        "read": (f"**How to read the map:** darker blue = a larger share of the selected systems' compute; the green outline marks "
                 f"the compared country. #n on the bar is the country's rank. Selection shown: {group.lower()}."),
        "after": (
            f"The largest shares are {top3}"
            + ("." if "China" in table.head(3).index else f"; China holds only **{table.get('China', 0):.1f}%**.") + " "
            f"Among public systems the US share is "
            f"{pub.get('United States', 0):.1f}%; among private systems it is lower, {pri.get('United States', 0):.1f}%, because two "
            f"large Italian energy-company machines (HPC6 and HPC7) give Italy {pri.get('Italy', 0):.1f}% of private compute. "
            f"Australia holds {table.get('Australia', 0):.1f}% of the selected compute."
        ),
        "bridge": (
            "Everything so far comes from the TOP500, which only counts machines whose owners submit a Linpack result, and many of "
            "the largest AI training clusters do not. To see where frontier AI compute is being built, and by whom, we need a "
            "second dataset."
        ),
    }
