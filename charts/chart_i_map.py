"""Section 4 / Chart I - TOP500 compute by country (choropleth; Spatial) with a labelled top-10 bar.

Reads data/processed/top500_systems_clean.csv. Country shapes: static/countries-110m.json
(world-atlas 2.0.2, Natural Earth 1:110m, ISC licence).
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import INK, PUBLIC

FILE = "top500_systems_clean.csv"
GROUPS = ["All systems", "Public sector only", "Private sector only"]
MAP_NAMES = {"United States": "United States of America"}
BINS = [(0, 0.5, "under 0.5%"), (0.5, 1, "0.5–1%"), (1, 2.5, "1–2.5%"), (2.5, 5, "2.5–5%"),
        (5, 10, "5–10%"), (10, 20, "10–20%"), (20, 101, "20% or more")]
BLUES = ["#E3ECF6", "#B7CFE8", "#8AB0D8", "#5B8DC4", "#356BA8", "#1F4E8C", "#0B2A55"]
NO_DATA = "No system on the list"


def by_country(df: pd.DataFrame, group: str) -> pd.DataFrame:
    sel = df if group == GROUPS[0] else df[df["sector_group"] == group.split()[0]]
    out = sel.groupby("country", as_index=False).agg(systems=("rank", "size"), rmax_tflops=("rmax_tflops", "sum"))
    out["share_pct"] = out["rmax_tflops"] / out["rmax_tflops"].sum() * 100
    out["bin"] = out["share_pct"].map(lambda s: next(label for low, high, label in BINS if low <= s < high))
    out["map_name"] = out["country"].replace(MAP_NAMES)
    return out.sort_values("share_pct", ascending=False).reset_index(drop=True)


def build_map(table: pd.DataFrame, shapes: alt.Data) -> alt.Chart:
    domain = [label for _, _, label in BINS] + [NO_DATA]
    return (alt.Chart(shapes).mark_geoshape(stroke="#6B737B", strokeWidth=0.4)
            .transform_lookup(lookup="properties.name", from_=alt.LookupData(table, key="map_name", fields=["bin"]))
            .transform_calculate(bin=f"datum.bin ? datum.bin : '{NO_DATA}'")
            .transform_filter("datum.properties.name != 'Antarctica'")
            .encode(color=alt.Color("bin:N", title="Share of Rmax (%)", sort=domain,
                                    scale=alt.Scale(domain=domain, range=BLUES + ["#FFFFFF"]),
                                    legend=alt.Legend(orient="bottom-left", direction="vertical", fillColor="#FFFFFF", padding=8,
                                                      strokeColor=INK, symbolType="square", symbolStrokeColor="#6B737B",
                                                      symbolStrokeWidth=0.6, labelFontSize=11)))
            .project("equalEarth").properties(height=440))


def build_bar(table: pd.DataFrame) -> alt.LayerChart:
    top = table.head(10).assign(label=lambda f: f["share_pct"].map(lambda v: f"{v:.1f}%"))
    base = alt.Chart(top).encode(y=alt.Y("country:N", sort=list(top["country"]), title="Country"),
                                 x=alt.X("share_pct:Q", title="Share of the selected systems' Rmax (%)", scale=alt.Scale(domain=[0, max(45, top["share_pct"].max() * 1.15)])))
    return (base.mark_bar(height=14, color=PUBLIC) + base.mark_text(align="left", dx=4, fontSize=12, color=INK).encode(text="label:N")
            ).properties(height=280)


def texts(df: pd.DataFrame, group: str) -> dict[str, str]:
    table = by_country(df, group).set_index("country")["share_pct"]
    pub = by_country(df, GROUPS[1]).set_index("country")["share_pct"]
    pri = by_country(df, GROUPS[2]).set_index("country")["share_pct"]
    lead3 = [f"{c} (**{v:.1f}%**)" for c, v in table.head(3).items()]
    top3 = ", ".join(lead3[:-1]) + " and " + lead3[-1]
    return {
        "title": "Where the public compute sits, and where Australia stands",
        "caption": ("Chart I. Share of the combined Rmax of TOP500 systems (June 2026 list) located in each country, for the "
                    "selected systems; the bar lists the ten largest shares. Units: % of the selected systems' Rmax."),
        "lead": (
            "The map shades each country by its share of the TOP500's combined Rmax; white countries have no system on the list. "
            "The bar below it labels the ten largest shares, because small countries such as Singapore are too small to see on a "
            "world map. Switch between all, public and private systems."
        ),
        "read": f"**How to read the map:** darker blue = a larger share of the selected systems' compute. Selection shown: {group.lower()}.",
        "after": (
            f"The largest shares are {top3}"
            + ("." if "China" in table.head(3).index else f"; China holds only **{table.get('China', 0):.1f}%**.") + " "
            f"Among public systems the US share is "
            f"{pub.get('United States', 0):.1f}%; among private systems it is lower, {pri.get('United States', 0):.1f}%, because two "
            f"large Italian energy-company machines (HPC6 and HPC7) give Italy {pri.get('Italy', 0):.1f}% of private compute. "
            f"Australia holds {table.get('Australia', 0):.1f}% of the selected compute.\n\n"
            "**Australia's machines on the list:** "
            + "; ".join(f"{r.name} ({r.segment.lower()}, {r.rmax_tflops / 1000:.1f} PFlop/s)"
                        for r in df[df["country"] == "Australia"].sort_values("rmax_tflops", ascending=False).itertuples())
            + ". The largest, Setonix at the Pawsey Supercomputing Centre, is a GPU system run by a public research centre."
        ),
        "bridge": (
            "So Australia has public supercomputing, but little of it, and it holds 0.3% of the AI chips Epoch tracks."
        ),
    }
