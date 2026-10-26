"""Shared loading, colours and text helpers used by every section.

Each chart module exposes pure `build_*` functions that return an Altair chart (used by the
Streamlit app and by the static HTML preview) and a `section()` function that renders the
section in Streamlit: lead text -> controls -> chart -> how to read it -> bridge to the next section.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import altair as alt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
GEO_FILE = ROOT / "static" / "countries-110m.json"
# In Streamlit the map is fetched from static file serving (.streamlit/config.toml: server.enableStaticServing).
WORLD_URL = "app/static/countries-110m.json"

# One colour meaning across the page: blues = public sector, oranges = private, grey = other.
SEGMENT_ORDER = ["Academic", "Research", "Government", "Industry", "Vendor", "Others"]
SEGMENT_NAME = {"Academic": "Universities (our audience)", "Research": "Public research labs", "Government": "Government",
                "Industry": "Industry", "Vendor": "Vendors", "Others": "Others"}
SEGMENT_COLOUR = {"Academic": "#0B2A55", "Research": "#5B8DC4", "Government": "#A9C1DE",
                  "Industry": "#D9822B", "Vendor": "#EDB27A", "Others": "#8C96A0"}
PUBLIC, PRIVATE, OTHER = "#1F4E8C", "#D9822B", "#8C96A0"
GROUP_COLOURS = {"Public": PUBLIC, "Private": PRIVATE, "Other": OTHER}
LIGHT_PUBLIC, INK, MUTED, TEAL = "#9DB5D6", "#15181C", "#555D65", "#1B7F6B"
FONT = "IBM Plex Sans, Helvetica, Arial, sans-serif"


def read(name: str) -> pd.DataFrame:
    """Read one file from data/processed/ (only empty fields count as missing)."""
    return pd.read_csv(PROCESSED / name, keep_default_na=False, na_values=[""])


def style(chart: alt.TopLevelMixin) -> alt.TopLevelMixin:
    """Consistent fonts and axes. No tooltips are defined anywhere: every value is printed."""
    return (chart.configure(font=FONT)
            .configure_axis(labelFontSize=12, titleFontSize=12, labelColor=INK, titleColor=MUTED,
                            gridColor="#E4E7EA", domainColor="#9AA1A8")
            .configure_legend(labelFontSize=12, titleFontSize=12, orient="top")
            .configure_view(strokeWidth=0))


def md_to_html(text: str) -> str:
    """Tiny converter for the preview: **bold** and paragraphs only."""
    out = []
    for para in text.strip().split("\n\n"):
        para = html.escape(para.strip())
        para = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", para)
        if para.startswith("- "):
            items = "".join(f"<li>{i[2:]}</li>" for i in para.split("\n"))
            out.append(f"<ul>{items}</ul>")
        else:
            out.append(f"<p>{para}</p>")
    return "\n".join(out)
