"""Chart P - one square per notable AI system: who built them in the first and last year (pictogram; Part-to-whole).

Reads data/processed/ai_systems_by_sector.csv. Each square is one system, so the change is shown in counts, not only
shares: the 2010 row and the 2025 row use the same square size.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import OTHER, PRIVATE

ORDER = ["Universities", "University–industry collaboration", "Industry", "Other / not specified"]
COLOURS = ["#0B2A55", "#8AB0D8", PRIVATE, OTHER]
GROUPS = {"Academia": ORDER[0], "Academia and industry collaboration": ORDER[1], "Industry": ORDER[2],
          "Not specified": ORDER[3], "Other": ORDER[3]}
PER_ROW = 27


def squares(df: pd.DataFrame, years: tuple[int, int]) -> pd.DataFrame:
    rows = []
    for y in years:
        d = df[df["year"] == y].assign(group=lambda f: f["sector"].map(GROUPS)).groupby("group")["n_systems"].sum()
        cells = [g for g in ORDER for _ in range(int(d.get(g, 0)))]
        n = len(cells)
        uni = int(d.get(ORDER[0], 0))
        label = f"{y}: {uni} of {n} built by universities"
        rows += [{"year": label, "group": g, "col": i % PER_ROW, "row": i // PER_ROW} for i, g in enumerate(cells)]
    return pd.DataFrame(rows)


def build(df: pd.DataFrame, years: tuple[int, int]) -> alt.VConcatChart:
    data = squares(df, years)
    charts = []
    for label in dict.fromkeys(data["year"]):
        part = data[data["year"] == label]
        n_rows = int(part["row"].max()) + 1
        charts.append(alt.Chart(part, title=alt.Title(label, anchor="start", fontSize=16, fontWeight="bold")).mark_square(
            size=300, opacity=1).encode(
            x=alt.X("col:O", axis=None, scale=alt.Scale(domain=list(range(PER_ROW)))),
            y=alt.Y("row:O", axis=None),
            color=alt.Color("group:N", title="Built by (1 square = 1 notable AI system)", sort=ORDER,
                            scale=alt.Scale(domain=ORDER, range=COLOURS), legend=alt.Legend(orient="top", columns=4, titleLimit=400)),
        ).properties(width=PER_ROW * 24, height=n_rows * 24))
    return alt.vconcat(*charts, spacing=14)


def texts(df: pd.DataFrame, years: tuple[int, int]) -> dict[str, str]:
    return {
        "caption": (f"Chart P. Every notable AI system released in {years[0]} and in {years[1]}, one square each, coloured by "
                    "the sector of the researchers who built it. Source: Epoch AI via Our World in Data."),
        "read": ("**How to read it:** count the dark-blue squares. The rows are not scaled to the same total: far more notable "
                 "systems appear each year now, and almost all of the new ones come from industry (orange)."),
    }
