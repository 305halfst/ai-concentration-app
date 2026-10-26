"""Section 2 / Chart D - who pays for frontier AI data centres (sorted horizontal bars; Ranking).

Reads data/processed/datacenters_by_owner_country.csv.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import INK, OTHER, PRIVATE, TEAL

FILE = "datacenters_by_owner_country.csv"
BIG_FIVE = ["Google", "Meta", "Amazon", "Microsoft", "SpaceXAI"]


def ranked(df: pd.DataFrame) -> pd.DataFrame:
    priced = df[df["capital_cost_2025usd_bn"] > 0].sort_values("capital_cost_2025usd_bn", ascending=False).reset_index(drop=True)
    priced["rank"] = priced.index + 1
    return priced


def countries(df: pd.DataFrame) -> list[str]:
    return sorted({c for cell in df["country"] for c in cell.split("|")})


def build(df: pd.DataFrame, top_n: int, focus: str) -> alt.LayerChart:
    priced = ranked(df)
    in_focus = priced["country"].str.split("|").map(lambda cs: focus in cs)
    shown = priced[(priced["rank"] <= top_n) | in_focus].copy()

    def group(row) -> str:
        if focus in row["country"].split("|"):
            return f"Has a site in {focus}"
        if row["owner"] in BIG_FIVE:
            return "Five largest named owners"
        return "Owner not identified" if row["owner"] == "Unknown" else "Other owners"

    shown["group"] = shown.apply(group, axis=1)
    shown["label"] = shown["capital_cost_2025usd_bn"].map(lambda v: f"US${v:.1f}B")
    shown["owner_label"] = ("#" + shown["rank"].astype(str) + " " + shown["owner"].replace({"Unknown": "Unknown owner"})
                            + " · " + shown["country"].str.replace("|", ", ", regex=False))
    groups = [f"Has a site in {focus}", "Five largest named owners", "Other owners", "Owner not identified"]
    base = alt.Chart(shown).encode(
        y=alt.Y("owner_label:N", sort=list(shown["owner_label"]), title="Owner (#rank · countries)",
                axis=alt.Axis(labelLimit=320, titleAngle=0, titleAlign="right", titleBaseline="bottom", titleX=-6, titleY=-6)),
        x=alt.X("capital_cost_2025usd_bn:Q", title="Capital cost (billions of 2025 US dollars)", scale=alt.Scale(domain=[0, 135])))
    bars = base.mark_bar(height=16).encode(
        color=alt.Color("group:N", title="Owner group", scale=alt.Scale(domain=groups, range=[TEAL, PRIVATE, "#E8B98A", OTHER])))
    labels = base.mark_text(align="left", dx=4, fontSize=12, color=INK).encode(text="label:N")
    return (bars + labels).properties(height=max(160, 26 * len(shown)))


def texts(df: pd.DataFrame, top_n: int, focus: str) -> dict[str, str]:
    priced = ranked(df)
    total = df["capital_cost_2025usd_bn"].sum()
    big_five = df[df["owner"].isin(BIG_FIVE)]["capital_cost_2025usd_bn"].sum()
    google = df.set_index("owner").loc["Google", "capital_cost_2025usd_bn"]
    rows = priced[priced["country"].str.split("|").map(lambda cs: focus in cs)]
    extra = rows[rows["rank"] > top_n]
    zero = ", ".join(df[df["capital_cost_2025usd_bn"] == 0]["owner"])
    focus_line = (f"Owners with a site in {focus} ({', '.join(rows['owner'])}) account for "
                  f"**US${rows['capital_cost_2025usd_bn'].sum():.1f}B, {rows['capital_cost_2025usd_bn'].sum() / total * 100:.1f}%** of the total"
                  + (f"; {', '.join(f'{r.owner} ranks {r.rank} of {len(priced)}' for r in rows.itertuples())}." if len(rows) else ".")
                  if len(rows) else f"No owner with a listed cost has a site in {focus}.")
    return {
        "title": "Owners ranked by estimated capital cost",
        "caption": ("Chart D. Estimated capital cost of the AI data centres in Epoch AI's October 2026 update, summed by owner. "
                    "Units: billions of 2025 US dollars."),
        "lead": (
            f"Epoch AI tracks large data centres built for AI, with each site's owner, location and estimated capital cost. "
            f"Its October 2026 update covers {int(df['n_datacenters'].sum())} sites with a combined cost of **US${total:.1f}B** "
            f"(2025 US dollars), held by {int((df['owner'] != 'Unknown').sum())} named owners plus sites with no known owner. The bars rank owners by estimated capital cost. Use the slider to show more "
            "owners, and pick a country to highlight; owners with a site there are always shown, in green."
        ),
        "read": (
            f"**How to read the bars:** #n is the owner's rank by capital cost; the countries are where its listed sites are. "
            + (f"Shown in addition to the top {top_n} because they have a site in {focus}: "
               + ", ".join(f"{r.owner} (rank {r.rank})" for r in extra.itertuples()) + ". " if len(extra) else "")
            + f"Not ranked because Epoch lists no cost: {zero}."
        ),
        "after": (
            f"Google tops the ranking at **US${google:.1f}B**. The five largest named owners (Google, Meta, Amazon, Microsoft and "
            f"SpaceXAI) account for **{big_five / total * 100:.1f}%** of the total estimated cost. All five list sites in the United States; only "
            f"Google also lists one other country (the United Kingdom). "
            f"None of the {int((df['owner'] != 'Unknown').sum())} named owners is a university or public research body. {focus_line}\n\n"
            "**So what for the decision:** the infrastructure frontier AI runs on is being built and owned by companies; "
            "no public owner appears in this dataset."
        ),
        "bridge": (
            "Chart D ranks owners by cost. Chart E looks at the same owners by size: power capacity and estimated AI chips."
        ),
    }
