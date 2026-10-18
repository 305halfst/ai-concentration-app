"""Section 1, part 2 / Chart C - how big each group's machines are (counts by size band; Distribution).

Explains chart A: why universities run many machines but hold little compute.
Reads data/processed/top500_systems_clean.csv.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import SEGMENT_NAME, SEGMENT_ORDER

FILE = "top500_systems_clean.csv"
EMPTY = "No systems match the selected segments. Pick at least one segment to see the size bands."
BANDS = [(0, 5, "Small · under 5"), (5, 20, "Medium · 5–20"), (20, 100, "Large · 20–100"),
         (100, 1000, "Very large · 100–1,000"), (1000, float("inf"), "Giant · over 1,000")]
BAND_NAMES = [b[2] for b in BANDS]


def band_counts(df: pd.DataFrame, segments: list[str]) -> pd.DataFrame:
    """One row per (segment, size band) with the number of machines, including empty cells."""
    sel = df[df["segment"].isin(segments)].assign(pflops=lambda f: f["rmax_tflops"] / 1000)
    sel["band"] = sel["pflops"].map(lambda v: next(name for low, high, name in BANDS if low <= v < high))
    counts = sel.groupby(["segment", "band"]).size().rename("machines").reset_index()
    grid = pd.MultiIndex.from_product([[s for s in SEGMENT_ORDER if s in segments], BAND_NAMES],
                                      names=["segment", "band"]).to_frame(index=False)
    out = grid.merge(counts, how="left").fillna({"machines": 0}).astype({"machines": int})
    totals = out.groupby("segment")["machines"].sum()
    out["row"] = out["segment"].map(lambda s: f"{SEGMENT_NAME[s]} ({totals[s]} machines)")
    out["label"] = out["machines"].map(lambda n: str(n) if n else "–")
    return out


def build(df: pd.DataFrame, segments: list[str]) -> alt.LayerChart:
    counts = band_counts(df, segments)
    rows = list(dict.fromkeys(counts["row"]))
    base = alt.Chart(counts).encode(
        x=alt.X("band:N", sort=BAND_NAMES, title="Machine size (Rmax, PFlop/s)",
                axis=alt.Axis(orient="top", labelAngle=0, labelLimit=170)),
        y=alt.Y("row:N", sort=rows, title=None, axis=alt.Axis(labelLimit=320)))
    cells = base.mark_rect(stroke="#FFFFFF", strokeWidth=2).encode(
        color=alt.Color("machines:Q", scale=alt.Scale(scheme="blues", domainMin=0), legend=None))
    text = base.mark_text(fontSize=14, fontWeight=600).encode(
        text="label:N", color=alt.condition("datum.machines > 40", alt.value("white"), alt.value("#15181C")))
    return (cells + text).properties(height=52 * len(rows) + 10)


def texts(df: pd.DataFrame, segments: list[str]) -> dict[str, str]:
    c = band_counts(df, SEGMENT_ORDER).set_index(["segment", "band"])["machines"]
    uni_small = c[("Academic", BAND_NAMES[0])] + c[("Academic", BAND_NAMES[1])]
    uni_total = c.loc["Academic"].sum()
    return {
        "title": "Why universities hold so little of the compute",
        "lead": (
            "Chart A showed universities running a quarter of the machines but holding a tenth of the compute. The reason is "
            "machine size. The table sorts all 500 systems into five size bands by Rmax and counts how many each kind of "
            "organisation runs in each band. Use the segment filter to compare groups."
        ),
        "read": ("**How to read the table:** each cell is a number of machines; darker blue means more machines. A dash means "
                 "none. Size bands are in PFlop/s (1 PFlop/s = 1,000 TFlop/s); the smallest machine on the list runs at 2.7 and "
                 "the largest at 2,198."),
        "after": (
            f"**{uni_small} of the universities' {uni_total} machines are under 20 PFlop/s**, and none is over 1,000. All "
            f"{c[('Research', BAND_NAMES[4])]} giant machines belong to public research labs, which is why labs hold almost 60% of "
            f"the compute. Industry runs the most small machines ({c[('Industry', BAND_NAMES[0])]}), which is why its share of compute "
            "is smaller than its share of machines."
        ),
        "bridge": "So the public sector's compute sits in a handful of national-lab giants. The next question is where those machines are.",
    }
