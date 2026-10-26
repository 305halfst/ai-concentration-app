"""Opening / Chart F - two kinds of computing, two kinds of owner (two 100% stacked bars; Part-to-whole).

Each bar is a share of its own dataset's total, so the two units are never mixed:
- TOP500 supercomputing: share of combined Rmax (Linpack), by sector group (fig4_top500_by_segment.csv).
- Epoch AI data centres: share of current estimated H100 equivalents, by owner group
  (datacenters_by_owner_country.csv; 73 of the 93 tracked sites carry a current estimate).
Owner groups are the group's own classification by owner name: the five largest named owners by estimated
capital cost; the other named owners (all companies, none a university or public research body); and sites
whose owner Epoch does not identify ("Unknown").
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import INK, OTHER, PRIVATE, PUBLIC

BIG_FIVE = ["Google", "Meta", "Amazon", "Microsoft", "SpaceXAI"]
GROUPS = ["Public sector", "Five largest named owners", "Companies (industry, vendors, other named owners)", "Other or unknown owner"]
COLOURS = [PUBLIC, PRIVATE, "#E8B98A", OTHER]
BARS = ["Supercomputing (TOP500, Rmax)", "AI data centres (Epoch, est. H100 equivalents)"]


def shares(segments: pd.DataFrame, owners: pd.DataFrame) -> pd.DataFrame:
    sector = segments.groupby("sector_group")["rmax_share_pct"].sum()
    h100 = owners["h100_equivalents"]
    total = h100.sum()
    big = owners[owners["owner"].isin(BIG_FIVE)]["h100_equivalents"].sum()
    unknown = owners[owners["owner"] == "Unknown"]["h100_equivalents"].sum()
    rows = [
        (BARS[0], GROUPS[0], sector.get("Public", 0)),
        (BARS[0], GROUPS[2], sector.get("Private", 0)),
        (BARS[0], GROUPS[3], sector.get("Other", 0)),
        (BARS[1], GROUPS[0], 0.0),
        (BARS[1], GROUPS[1], big / total * 100),
        (BARS[1], GROUPS[2], (total - big - unknown) / total * 100),
        (BARS[1], GROUPS[3], unknown / total * 100),
    ]
    out = pd.DataFrame(rows, columns=["bar", "group", "share"])
    out["rank"] = out["group"].map(GROUPS.index)
    public = out[out["group"] == GROUPS[0]].set_index("bar")["share"]
    out["row"] = out["bar"].map(lambda b: f"{b} · public {public[b]:.1f}%")
    out["label"] = out["share"].map(lambda v: f"{v:.1f}%" if v >= 5 else "")
    return out


def build(segments: pd.DataFrame, owners: pd.DataFrame) -> alt.LayerChart:
    data = shares(segments, owners)
    drawn = data[data["share"] > 0]
    y = alt.Y("row:N", sort=list(dict.fromkeys(data["row"])), title=None, axis=alt.Axis(labelLimit=380, labelFontSize=13))
    bars = alt.Chart(drawn).mark_bar(height=56, stroke="#FFFFFF", strokeWidth=1.5).encode(
        y=y,
        x=alt.X("share:Q", stack="zero", title="% of each dataset's own total (units differ between the two bars)",
                scale=alt.Scale(domain=[0, 100])),
        order=alt.Order("rank:Q"),
        color=alt.Color("group:N", title="Who owns it", sort=GROUPS, scale=alt.Scale(domain=GROUPS, range=COLOURS),
                        legend=alt.Legend(columns=2, labelLimit=320)))
    text = (alt.Chart(drawn)
            .transform_stack(stack="share", groupby=["row"], sort=[alt.SortField("rank")], as_=["x0", "x1"])
            .transform_calculate(mid="(datum.x0 + datum.x1) / 2", tc="datum.rank == 2 ? '#15181C' : 'white'")
            .mark_text(fontSize=13, fontWeight=700)
            .encode(y=y, x="mid:Q", text="label:N", color=alt.Color("tc:N", scale=None)))
    return (bars + text).properties(height=230)


def texts(segments: pd.DataFrame, owners: pd.DataFrame) -> dict[str, str]:
    data = shares(segments, owners).set_index(["bar", "group"])["share"]
    named = int((owners["owner"] != "Unknown").sum())
    sites = int(owners["n_datacenters"].sum())
    from charts.common import read
    estimated = int(read("datacenters_by_country.csv")["n_estimated"].sum())
    return {
        "caption": ("Chart F. Who owns each kind of computing. Top bar: share of the combined Rmax of the TOP500 list "
                    "(June 2026). Bottom bar: share of current estimated H100 equivalents in the AI data centres Epoch AI "
                    "tracks (October 2026 update). Each bar is 100% of its own dataset; the units are not compared."),
        "read": (f"**How to read it:** blue is the public sector. In supercomputing it holds "
                 f"**{data[(BARS[0], GROUPS[0])]:.1f}%**. In AI data centres it holds **0%** of the chips with a named owner: "
                 f"none of the {named} named owners is a university or public research body (our classification by owner name). Grey in the bottom "
                 f"bar is sites whose owner Epoch does not identify; grey in the top bar is TOP500's 'Others' group "
                 f"({data[(BARS[0], GROUPS[3])]:.1f}%, too thin to label). Of the {sites} sites Epoch tracks, {sites - estimated} have no current "
                 f"estimate yet (counted in the raw file; see the data dictionary), so the bottom bar covers the "
                 f"{estimated} that do."),
    }
