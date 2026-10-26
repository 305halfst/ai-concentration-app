"""Chart E — AI data-centre scale versus investment (relational scatterplot).

Reads the existing owner-level processed Epoch AI table. The chart deliberately
compares measures rather than re-ranking owners, which is Chart B's purpose.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import INK, OTHER, PRIVATE

FILE = "datacenters_by_owner_country.csv"
ALL_COUNTRIES = "All countries"


def countries(df: pd.DataFrame) -> list[str]:
    """Return countries in the pipe-separated owner location field."""
    return [ALL_COUNTRIES] + sorted({country for cell in df["country"] for country in cell.split("|")})


def owner_options(df: pd.DataFrame) -> list[str]:
    return sorted(df["owner"].tolist())


def filtered(df: pd.DataFrame, country: str, owners: list[str]) -> pd.DataFrame:
    """Filter owners without changing the source data or its owner-level grain."""
    out = df[df["owner"].isin(owners)].copy()
    if out.empty:
        return out
    if country != ALL_COUNTRIES:
        out = out[out["country"].str.split("|").map(lambda places: country in places)]
    return out.reset_index(drop=True)


def plottable(df: pd.DataFrame) -> pd.DataFrame:
    """Keep rows with positive, numeric values for all three scatterplot encodings."""
    numeric = ["capital_cost_2025usd_bn", "power_mw", "h100_equivalents"]
    out = df.copy()
    for column in numeric:
        out[column] = pd.to_numeric(out[column], errors="coerce")
    return out[(out["capital_cost_2025usd_bn"] > 0) & (out["power_mw"] > 0) & (out["h100_equivalents"] > 0)].copy()


def summary(df: pd.DataFrame) -> dict[str, float | int]:
    return {
        "investment": float(df["capital_cost_2025usd_bn"].sum()),
        "power": float(df["power_mw"].sum()),
        "datacenters": int(df["n_datacenters"].sum()),
        "h100": float(df["h100_equivalents"].sum()),
    }


def build(df: pd.DataFrame) -> alt.LayerChart:
    """Build a labelled bubble chart; labels avoid requiring hover to identify owners."""
    shown = plottable(df)
    shown["owner_group"] = shown["owner"].map(lambda owner: "Owner not identified" if owner == "Unknown" else "Named owner")
    base = alt.Chart(shown).encode(
        x=alt.X("capital_cost_2025usd_bn:Q", title="Capital cost (billions of 2025 US dollars)", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("power_mw:Q", title="Power capacity (MW)", axis=alt.Axis(format=",.0f")),
    )
    points = base.mark_circle(opacity=0.72, stroke=INK, strokeWidth=0.7).encode(
        size=alt.Size("h100_equivalents:Q", title="Estimated H100 equivalents", scale=alt.Scale(range=[120, 2200])),
        color=alt.Color("owner_group:N", title="Owner record", scale=alt.Scale(
            domain=["Named owner", "Owner not identified"], range=[PRIVATE, OTHER]
        )),
    )
    labels = base.mark_text(align="left", baseline="middle", dx=7, fontSize=11, color=INK).encode(text="owner:N")
    return (points + labels).properties(height=460)


def texts() -> dict[str, str]:
    return {
        "title": "How big the AI data-centre owners are",
        "caption": (
            "Chart E. Each bubble is an AI data-centre owner in Epoch AI's October 2026 update. "
            "Position compares estimated capital cost with listed power capacity; bubble area represents estimated H100 equivalents."
        ),
        "lead": (
            "Chart B ranks owners by spending. This dashboard instead asks whether higher reported investment is paired with "
            "larger reported power capacity and estimated H100-equivalent scale. Filter by listed site country or owner."
        ),
        "read": (
            "**How to read this chart:** owners farther right have higher estimated capital cost; owners higher up have more listed "
            "power capacity. Larger bubbles represent more estimated H100 equivalents. Owners with zero or missing values for any "
            "of those three measures remain in the table and KPI totals when selected, but cannot be positioned as bubbles "
            "(4 owners have no estimate: Cipher Mining, G42, Mistral AI and Softbank). Note: Epoch estimates capital cost from "
            "power (about $0.038B per MW for every owner), so the two axes carry largely the same information; bubble size "
            "(estimated AI chips) is the independent measure."
        ),
        "limits": (
            "**What this cannot show:** this is an owner-level summary, not a site-by-site comparison. It cannot show utilisation, "
            "energy efficiency, access for universities, model-training output, or a causal relationship between cost, power and chips."
        ),
    }
