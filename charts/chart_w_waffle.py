"""Chart C - who owns the AI chips, as 100 squares (waffle / unit chart; Part-to-whole).

Each square is 1% of the current estimated H100 equivalents in Epoch AI's data-centre snapshot
(datacenters_by_owner_country.csv). Squares are allocated by largest remainder so they add up to exactly 100.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from charts.common import OTHER, PRIVATE

BIG_FIVE = ["Google", "Meta", "Amazon", "Microsoft", "SpaceXAI"]
GROUPS = ["Five largest named owners", "Other companies", "Owner not identified"]
COLOURS = [PRIVATE, "#E8B98A", OTHER]


def shares(owners: pd.DataFrame) -> dict[str, float]:
    total = owners["h100_equivalents"].sum()
    big = owners[owners["owner"].isin(BIG_FIVE)]["h100_equivalents"].sum()
    unknown = owners[owners["owner"] == "Unknown"]["h100_equivalents"].sum()
    return {GROUPS[0]: big / total * 100, GROUPS[1]: (total - big - unknown) / total * 100, GROUPS[2]: unknown / total * 100}


def squares(owners: pd.DataFrame) -> pd.DataFrame:
    s = shares(owners)
    n = {k: int(v) for k, v in s.items()}
    for k in sorted(s, key=lambda k: s[k] - n[k], reverse=True)[: 100 - sum(n.values())]:
        n[k] += 1
    cells = [g for g in GROUPS for _ in range(n[g])]
    out = pd.DataFrame({"i": range(100), "group": cells})
    out["col"], out["row"] = out["i"] % 20, out["i"] // 20
    return out


def build(owners: pd.DataFrame) -> alt.Chart:
    return (alt.Chart(squares(owners)).mark_rect(stroke="#FFFFFF", strokeWidth=3).encode(
        x=alt.X("col:O", axis=None), y=alt.Y("row:O", axis=None),
        color=alt.Color("group:N", title="Owner of the AI chips (1 square = 1%)", sort=GROUPS,
                        scale=alt.Scale(domain=GROUPS, range=COLOURS), legend=alt.Legend(orient="top", columns=3, titleLimit=400)))
        .properties(height=210))


def texts(owners: pd.DataFrame) -> dict[str, str]:
    s = shares(owners)
    total = owners["h100_equivalents"].sum()
    au = owners[owners["country"].str.split("|").map(lambda c: "Australia" in c)]["h100_equivalents"].sum() / total * 100
    n = squares(owners)["group"].value_counts()
    return {
        "caption": ("Chart C. Who owns the AI chips in the large AI data centres Epoch AI tracks (October 2026 update). "
                    "Each square is 1% of the current estimated H100 equivalents. Units: % of all estimated chips."),
        "read": (f"**How to read it:** {n[GROUPS[0]]} squares belong to the five largest named owners "
                 f"({s[GROUPS[0]]:.1f}%), {n[GROUPS[1]]} to other companies ({s[GROUPS[1]]:.1f}%) and {n[GROUPS[2]]} to sites "
                 f"whose owner Epoch does not identify ({s[GROUPS[2]]:.1f}%). **No square belongs to a university or public "
                 f"research body.** Australia's only listed site would fill {au:.1f}% — a third of one square."),
        "au": au,
    }
