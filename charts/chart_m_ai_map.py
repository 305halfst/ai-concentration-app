"""Chart M - where the AI chips are (choropleth; Spatial). Companion to Chart D's TOP500 map.

Reads data/processed/datacenters_by_country.csv (Epoch AI sites grouped by country).
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import INK

FILE = "datacenters_by_country.csv"
MAP_NAMES = {"United States": "United States of America"}
BINS = [(0, 0.5, "under 0.5%"), (0.5, 1, "0.5–1%"), (1, 2.5, "1–2.5%"), (2.5, 5, "2.5–5%"),
        (5, 10, "5–10%"), (10, 20, "10–20%"), (20, 101, "20% or more")]
BLUES = ["#DCE8F5", "#B7CFE8", "#8AB0D8", "#5B8DC4", "#356BA8", "#1F4E8C", "#0B2A55"]
NO_DATA = "No tracked site with chips"


def table(df: pd.DataFrame) -> pd.DataFrame:
    out = df[df["h100_equivalents"] > 0].copy()
    out["bin"] = out["h100_share_pct"].map(lambda s: next(label for low, high, label in BINS if low <= s < high))
    out["map_name"] = out["country"].replace(MAP_NAMES)
    return out


def build(df: pd.DataFrame, shapes) -> alt.Chart:
    domain = [label for _, _, label in BINS] + [NO_DATA]
    return (alt.Chart(shapes).mark_geoshape(stroke="#6B737B", strokeWidth=0.4)
            .transform_lookup(lookup="properties.name", from_=alt.LookupData(table(df), key="map_name", fields=["bin"]))
            .transform_calculate(bin=f"datum.bin ? datum.bin : '{NO_DATA}'")
            .transform_filter("datum.properties.name != 'Antarctica'")
            .encode(color=alt.Color("bin:N", title="Share of estimated AI chips (%)", sort=domain,
                                    scale=alt.Scale(domain=domain, range=BLUES + ["#FFFFFF"]),
                                    legend=alt.Legend(orient="bottom-left", direction="vertical", fillColor="#FFFFFF", padding=8,
                                                      strokeColor=INK, symbolType="square", symbolStrokeColor="#6B737B",
                                                      symbolStrokeWidth=0.6, labelFontSize=11)))
            .project("equalEarth").properties(height=400))


def texts(df: pd.DataFrame) -> dict[str, str]:
    t = df.set_index("country")
    rows = "; ".join(f"{c} {v:.2f}%" for c, v in t[t["h100_equivalents"] > 0]["h100_share_pct"].items())
    unestimated = int(df["n_datacenters"].sum() - df["n_estimated"].sum())
    return {
        "caption": ("Chart M. Share of the current estimated H100 equivalents in Epoch AI's tracked AI data centres, by the "
                    "country where each site is (October 2026 update). Units: % of all estimated chips."),
        "read": (f"**Every country with estimated chips:** {rows}. {unestimated} of the {int(df['n_datacenters'].sum())} sites "
                 "have no current estimate and are not counted."),
        "us": t.loc["United States", "h100_share_pct"], "au": t.loc["Australia", "h100_share_pct"],
    }
