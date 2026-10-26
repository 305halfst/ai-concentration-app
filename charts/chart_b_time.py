"""Chart B - who builds notable AI systems, 2010-2025 (animated 100% stacked area; Change over time).

Rendered with React + D3 inside a Streamlit component, because the year-by-year animation is the point of the
chart. All numbers are computed here in Python from data/processed/ai_systems_by_sector.csv and passed to the
page; the browser only draws them. Every value for the selected year is printed, so nothing needs hovering.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

FILE = "ai_systems_by_sector.csv"
FIRST_YEAR = 2010
GROUPS = {"Academia": "Universities", "Academia and industry collaboration": "University–industry collaboration",
          "Industry": "Industry", "Not specified": "Other / not specified", "Other": "Other / not specified"}
TEMPLATE = Path(__file__).resolve().parent / "js" / "chart_b_template.html"
CDN = [  # exact versions, loaded by the deployed app
    "https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.3.1/umd/react-dom.production.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js",
]


def yearly(df: pd.DataFrame) -> pd.DataFrame:
    d = df[df["year"] >= FIRST_YEAR].assign(group=lambda f: f["sector"].map(GROUPS))
    wide = d.pivot_table(index="year", columns="group", values="share_pct", aggfunc="sum").fillna(0)
    wide["total"] = d.groupby("year")["total_year"].first()
    return wide.reset_index()


def facts(df: pd.DataFrame) -> dict:
    w = yearly(df).set_index("year")
    first, last = w.index.min(), w.index.max()
    cross = int(w[w["Industry"] > w["Universities"]].index.min())
    early = df[df["year"] < FIRST_YEAR].groupby("year")["total_year"].first()
    return {"first": first, "last": last, "uni_first": w.loc[first, "Universities"], "uni_last": w.loc[last, "Universities"],
            "ind_first": w.loc[first, "Industry"], "ind_last": w.loc[last, "Industry"], "cross": cross,
            "n_first": int(w.loc[first, "total"]), "n_last": int(w.loc[last, "total"]),
            "collab_last": w.loc[last, "University–industry collaboration"],
            "early_max": int(early[early.index >= 2000].max())}


def html(df: pd.DataFrame, libs: str = "cdn") -> str:
    """libs='cdn' for the deployed app; libs=<inline script text> for offline previews."""
    f = facts(df)
    keys = ["Universities", "University–industry collaboration", "Industry", "Other / not specified"]
    rows = [{"year": int(r["year"]), "total": int(r["total"]), **{k: round(float(r[k]), 1) for k in keys}}
            for _, r in yearly(df).iterrows()]
    text = {
        "title": f"In {f['first']}, universities built {f['uni_first']:.0f}% of notable AI systems. By {f['last']}, {f['uni_last']:.1f}%.",
        "source": (f"Source: Our World in Data, from Epoch AI's notable AI systems (sector of the researchers who built each "
                   f"system; 2026 is incomplete and left out). Years before {f['first']} have {f['early_max']} or fewer "
                   "systems each and are left out."),
        "start": f["last"],
    }
    scripts = "\n".join(f'<script src="{u}"></script>' for u in CDN) if libs == "cdn" else f"<script>{libs}</script>"
    page = TEMPLATE.read_text()
    fallback = (f'<h2>{text["title"]}</h2><p class="read">The animated chart needs JavaScript libraries that did not load. '
                f'In {f["first"]}, universities built {f["uni_first"]:.0f}% of the {f["n_first"]} notable AI systems; in '
                f'{f["last"]}, {f["uni_last"]:.1f}% of {f["n_last"]}, and industry {f["ind_last"]:.1f}%. Industry overtook '
                f'universities in {f["cross"]}.</p><p class="src">{text["source"]}</p>')
    page = page.replace("<!--FALLBACK-->", fallback)
    return (page.replace("<!--LIBS-->", scripts).replace("/*DATA*/", json.dumps(rows))
            .replace("/*TEXT*/", json.dumps(text, ensure_ascii=False)))


def texts(df: pd.DataFrame) -> dict[str, str]:
    f = facts(df)
    return {
        "caption": (f"Chart B. Share of each year's notable AI systems by the sector of the researchers who built them, "
                    f"{f['first']}–{f['last']}. Units: % of that year's notable systems."),
    }
