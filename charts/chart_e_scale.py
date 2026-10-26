"""Chart E — AI data-centre scale versus investment (relational scatterplot).

Reads the existing owner-level processed Epoch AI table. The chart deliberately
compares measures rather than re-ranking owners, which is Chart D's purpose.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import INK, OTHER, PRIVATE

BIG_FIVE = ["Google", "Meta", "Amazon", "Microsoft", "SpaceXAI"]

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
    """Estimated capital cost against estimated AI chips (both log scale), one labelled bubble per owner."""
    shown = plottable(df)
    shown["owner_group"] = shown["owner"].map(lambda o: "Five largest named owners" if o in BIG_FIVE else
                                              ("Owner not identified" if o == "Unknown" else "Other companies"))
    groups = ["Five largest named owners", "Other companies", "Owner not identified"]
    base = alt.Chart(shown).encode(
        x=alt.X("capital_cost_2025usd_bn:Q", title="Estimated capital cost (billions of 2025 US dollars, log scale)",
                scale=alt.Scale(type="log", domain=[1, 200]), axis=alt.Axis(values=[1, 2, 5, 10, 20, 50, 100, 200], format="$,.0f")),
        y=alt.Y("h100_equivalents:Q", title="Estimated AI chips (H100 equivalents, log scale)",
                scale=alt.Scale(type="log", domain=[20_000, 5_000_000]), axis=alt.Axis(format="~s")),
    )
    points = base.mark_circle(opacity=0.8, stroke=INK, strokeWidth=0.7).encode(
        size=alt.Size("n_datacenters:Q", title="Data centres (count)", scale=alt.Scale(range=[60, 900])),
        color=alt.Color("owner_group:N", title="Owner group", sort=groups, scale=alt.Scale(domain=groups, range=[PRIVATE, "#E8B98A", OTHER])),
    )
    # Label nudges as fixed dy per layer (a yOffset channel is ignored on a continuous y axis).
    def label(names: list[str], dy: int, align: str, dx: int, keep: bool = True) -> alt.Chart:
        test = f"indexof({names}, datum.owner) {'>=' if keep else '<'} 0"
        return base.transform_filter(test).mark_text(align=align, baseline="middle", dx=dx, dy=dy, fontSize=11,
                                                     color=INK).encode(text="owner:N")
    special = ["SpaceXAI", "Unknown", "Microsoft", "Amazon"]
    labels = (label(special, 0, "left", 9, keep=False) + label(["Microsoft"], -2, "right", -12)
              + label(["Amazon"], 9, "left", 9) + label(["Unknown"], -17, "center", 0) + label(["SpaceXAI"], 13, "right", -8))
    return (points + labels).properties(height=440)


def texts() -> dict[str, str]:
    return {
        "title": "Bigger budgets go with more chips, and every named owner here is a company (one bubble is sites with no known owner)",
        "caption": ("Chart E. Each bubble is an AI data-centre owner in Epoch AI's October 2026 update: estimated capital cost "
                    "against estimated AI chips (both log scales); bubble size is its number of data centres."),
        "lead": "",
        "read": ("**How to read it:** further right = more estimated capital cost; higher = more estimated AI chips; bigger "
                 "bubble = more data centres. Both axes use a log scale, so each step is a multiple. Owners with no estimate "
                 "(Cipher Mining, G42, Mistral AI, Softbank) cannot be placed and appear only in the table."),
        "limits": "**What this cannot show:** utilisation, energy efficiency, or who may use the chips.",
    }
