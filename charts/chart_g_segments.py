"""Section 4 / Chart G - who runs the TOP500, and where our audience sits.

Main view: 100% stacked bars (Part-to-whole). Toggle: paired bars (Magnitude).
Reads data/processed/fig4_top500_by_segment.csv.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import INK, LIGHT_PUBLIC, PUBLIC, SEGMENT_COLOUR, SEGMENT_NAME, SEGMENT_ORDER

FILE = "fig4_top500_by_segment.csv"
MEASURES = {"system_share_pct": "Share of systems", "rmax_share_pct": "Share of compute (Rmax)"}
VIEWS = ["Whole list (100% stacked bars)", "Segment by segment (paired bars)"]


def _long(df: pd.DataFrame) -> pd.DataFrame:
    long = df.melt(id_vars=["segment", "sector_group"], value_vars=list(MEASURES), var_name="column", value_name="share")
    long["measure"] = long["column"].map(MEASURES)
    long["who"] = long["segment"].map(SEGMENT_NAME)
    long["rank"] = long["segment"].map(SEGMENT_ORDER.index)
    return long


def build_stacked(df: pd.DataFrame) -> alt.LayerChart:
    long = _long(df)
    short = {"Academic": "Universities", "Research": "Research labs", "Industry": "Industry"}
    long["show"] = long.apply(lambda r: f"{short.get(r['segment'], r['segment'])} {r['share']:.1f}%" if r["share"] >= 15
                              else (f"{r['share']:.1f}" if r["share"] >= 3.4 else ""), axis=1)
    names = [SEGMENT_NAME[s] for s in SEGMENT_ORDER]
    y = alt.Y("measure:N", sort=list(MEASURES.values()), title="Measure", axis=alt.Axis(labelFontSize=13, labelLimit=220))
    bars = alt.Chart(long).mark_bar(height=50, stroke="#FFFFFF", strokeWidth=1.5).encode(
        y=y, x=alt.X("share:Q", stack="normalize", title="Share of the TOP500 list (100%)", axis=alt.Axis(format="%")),
        order=alt.Order("rank:Q"),
        color=alt.Color("who:N", title="Type of organisation", sort=names, scale=alt.Scale(domain=names, range=[SEGMENT_COLOUR[s] for s in SEGMENT_ORDER]),
                        legend=alt.Legend(columns=3)))
    text = (alt.Chart(long)
            .transform_stack(stack="share", groupby=["measure"], sort=[alt.SortField("rank")], as_=["x0", "x1"], offset="normalize")
            .transform_calculate(mid="(datum.x0 + datum.x1) / 2", tc="datum.rank < 2 ? 'white' : '#15181C'")
            .mark_text(fontSize=12, fontWeight=600).encode(y=y, x="mid:Q", text="show:N", color=alt.Color("tc:N", scale=None)))
    public = df[df["sector_group"] == "Public"][list(MEASURES)].sum()
    edge = pd.DataFrame([{"measure": MEASURES[c], "x": public[c] / 100, "t": f"◀ public sector {public[c]:.1f}%"} for c in MEASURES])
    tick = alt.Chart(edge).mark_tick(color=INK, thickness=3, size=64).encode(y=y, x="x:Q")
    note = alt.Chart(edge).mark_text(align="right", dx=-4, dy=-32, fontSize=11, fontWeight=600, color=INK).encode(y=y, x="x:Q", text="t:N")
    return (bars + text + tick + note).properties(height=270)


def build_paired(df: pd.DataFrame) -> alt.LayerChart:
    long = _long(df)
    long["label"] = long["share"].map(lambda v: f"{v:.1f}%")
    order = [SEGMENT_NAME[s] for s in df.sort_values("rmax_share_pct", ascending=False)["segment"]]
    base = alt.Chart(long).encode(
        y=alt.Y("who:N", sort=order, title="Type of organisation", axis=alt.Axis(labelLimit=240)),
        yOffset=alt.YOffset("measure:N", sort=list(MEASURES.values())),
        x=alt.X("share:Q", title="Share of the TOP500 list (%)", scale=alt.Scale(domain=[0, 70])))
    bars = base.mark_bar(height=13).encode(color=alt.Color("measure:N", title="Measure", sort=list(MEASURES.values()),
                                                           scale=alt.Scale(range=[LIGHT_PUBLIC, PUBLIC])))
    return (bars + base.mark_text(align="left", dx=4, fontSize=12, color=INK).encode(text="label:N")).properties(height=330)


WHY = [
    ("Academic", "Universities (our audience)",
     "academic researchers and PhD students, the people the funder would serve directly."),
    ("Research", "Public research labs",
     "national labs and research-computing centres that already run shared machines, so the likely host or partner for any shared compute."),
    ("Government", "Government",
     "agencies that run systems for their own work and set research-funding policy."),
    ("Industry", "Industry",
     "companies running their own machines; a funder could rent capacity from them instead of building it."),
    ("Vendor", "Vendors",
     "the companies that build supercomputers, and so the suppliers of any machine the funder buys."),
    ("Others", "Others",
     "systems that fit none of these groups, shown for completeness."),
]


def texts(df: pd.DataFrame, systems: pd.DataFrame | None = None) -> dict[str, str]:
    a = df.set_index("segment")
    public = df[df["sector_group"] == "Public"][list(MEASURES)].sum()
    largest = systems.groupby("segment")["rmax_tflops"].max() / 1000 if systems is not None else None

    def holds(seg: str) -> str:
        seg = "Vendor" if seg == "Vendors" else seg
        r = a.loc[seg]
        out = (f"They run {int(r['n_systems'])} machines ({r['system_share_pct']:.1f}% of the list) holding "
               f"{r['rmax_share_pct']:.1f}% of its compute")
        return out + (f"; their largest runs at {largest[seg]:,.0f} PFlop/s." if largest is not None else ".")

    return {
        "title": "What universities and public labs hold",
        "caption": ("Chart G. How the 500 systems on the TOP500 list (June 2026) split by type of organisation: by number of "
                    "machines (top bar) and by combined Rmax (bottom bar). Units: % of the whole list."),
        "read": (
            "**How to read the two bars**\n\n"
            "- **Share of systems:** how many of the 500 machines each type of organisation runs, divided by 500. Every machine counts once, from the smallest (2.7 PFlop/s) to the largest (2,198 PFlop/s).\n"
            "- **Share of compute (Rmax):** each group's combined Rmax, the sustained speed a machine reaches on the Linpack (HPL) benchmark, divided by the list total of 18.7 million TFlop/s. Big machines weigh more.\n\n"
            + "Blocks too thin to label inside the bars: "
            + "; ".join(f"{SEGMENT_NAME[r.segment]} {getattr(r, c):.1f}% of {'systems' if c == 'system_share_pct' else 'compute'}"
                        for c in MEASURES for r in df.itertuples() if getattr(r, c) < 3.4)
            + ". Every value is also printed in the paired-bars view."
        ),
    }
