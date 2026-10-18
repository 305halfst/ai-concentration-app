"""Is cutting-edge AI becoming something only big tech can do?

36104 A3 data narrative for a university research funding body. Run:  streamlit run app.py
Reads only the three files in data/processed/ (built by data/build_processed.py).

Order follows the course session pages: one-line purpose -> contents -> numbered sections, each with
lead text -> controls -> chart -> how to read it -> what it shows -> bridge to the next section.
"""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from charts import chart_a_segments as A
from charts import chart_b_capex as B
from charts import chart_c_sizes as C
from charts import chart_d_map as D
from charts import page
from charts.common import SEGMENT_NAME, SEGMENT_ORDER, WORLD_URL, read, style

# Fill in the member who owns each chart (shown above the chart).
OWNERS = {"A": "Member A", "B": "Member B", "C": "Member C", "D": "Member D"}

st.set_page_config(page_title="Is frontier AI big tech only?", page_icon=":bar_chart:", layout="centered")
st.markdown(
    """<style>
    .block-container {max-width: 980px; padding-top: 2rem;}
    .eyebrow {font: 500 12px/1.2 'IBM Plex Mono', monospace; letter-spacing: .06em; text-transform: uppercase; color: #1F4E8C; margin: 0;}
    .answer {border-left: 4px solid #1F4E8C; background: #FFFFFF; padding: 12px 18px; border-radius: 6px;}
    .readbox {background: #F3F4F5; border-radius: 8px; padding: 10px 16px; font-size: 14px;}
    .bridge {font-style: italic; color: #3A4047;}
    </style>""",
    unsafe_allow_html=True,
)


@st.cache_data
def load(name: str) -> pd.DataFrame:
    return read(name)


def chart_card(letter: str, family: str, caption: str, draw) -> None:
    """Bordered card holding one member's chart: eyebrow, caption stating what it shows, then controls and chart."""
    with st.container(border=True, key=f"chart_{letter.lower()}"):
        st.markdown(f'<p class="eyebrow">Chart {letter} · {family} · owner: {OWNERS[letter]}</p>', unsafe_allow_html=True)
        md(f"**{caption}**")
        draw()


def md(text: str) -> None:
    """Markdown without LaTeX: Streamlit treats paired $ signs as maths, so escape them."""
    st.markdown(text.replace("$", "\\$"))


def read_box(text: str) -> None:
    md(text)


def bridge(text: str) -> None:
    st.markdown(f'<p class="bridge">{text}</p>', unsafe_allow_html=True)


segments, owners, systems = load(A.FILE), load(B.FILE), load(C.FILE)

# ---------------------------------------------------------------- opening
st.markdown('<p class="eyebrow">36104 · A3 · data narrative</p>', unsafe_allow_html=True)
st.title(page.TITLE)
md(page.INTRO)
for column, (label, value, note) in zip(st.columns(3), page.headline(segments, owners)):
    column.metric(label, value)
    column.caption(note.replace("$", "\\$"))
st.caption(page.REFRESH)
with st.container(border=True):
    st.markdown("**On this page**  \n" + "  \n".join(f"[{name}](#{anchor})" for anchor, name in page.CONTENTS))
st.markdown(f'<div class="answer">{page.ANSWER.replace("**Short answer:**", "<b>Short answer:</b>")}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- section 1: A then C
ta = A.texts(segments)
st.header(ta["title"], anchor="section-1")
md(ta["lead"])


def draw_a() -> None:
    view = st.radio("Measure", A.VIEWS, horizontal=True, key="a_measure")
    chart = A.build_stacked(segments) if view == A.VIEWS[0] else A.build_paired(segments)
    st.altair_chart(style(chart), theme=None, width="stretch")
    read_box(ta["read"])
    st.download_button("Download chart A data (CSV)", segments.to_csv(index=False), "chart_a_top500_by_segment.csv", key="a_download")


chart_card("A", "Part-to-whole · 100% stacked bars", ta["caption"], draw_a)
md(ta["after"])
bridge(ta["bridge"])

tc = C.texts(systems, SEGMENT_ORDER)
st.subheader(tc["title"], anchor="why-universities")
md(tc["lead"])


def draw_c() -> None:
    chosen = st.multiselect("Segments", SEGMENT_ORDER, default=SEGMENT_ORDER, format_func=SEGMENT_NAME.get, key="c_segments")
    if not chosen:
        st.info(C.EMPTY)
        return
    st.altair_chart(style(C.build(systems, chosen)), theme=None, width="stretch")
    read_box(tc["read"])
    rows = systems[systems["segment"].isin(chosen)]
    st.download_button("Download chart C data (CSV)", rows.to_csv(index=False), "chart_c_top500_systems.csv", key="c_download")


chart_card("C", "Distribution · machines by size band", tc["caption"], draw_c)
md(tc["after"])
bridge(tc["bridge"])

# ---------------------------------------------------------------- section 2: D
group = st.session_state.get("d_group", D.GROUPS[0])
td = D.texts(systems, group)
st.header(td["title"], anchor="section-2")
md(td["lead"])


def draw_d() -> None:
    chosen = st.radio("Systems included", D.GROUPS, horizontal=True, key="d_group")
    table = D.by_country(systems, chosen)
    st.altair_chart(style(D.build_map(table, alt.topo_feature(WORLD_URL, "countries"))), theme=None, width="stretch")
    st.markdown("**Top 10 countries by share of Rmax** (labelled, because small countries are hard to see on the map)")
    st.altair_chart(style(D.build_bar(table)), theme=None, width="stretch")
    read_box(D.texts(systems, chosen)["read"])
    st.download_button("Download chart D data (CSV)", table.drop(columns=["map_name"]).to_csv(index=False),
                       "chart_d_rmax_by_country.csv", key="d_download")


chart_card("D", "Spatial · choropleth", td["caption"], draw_d)
md(D.texts(systems, st.session_state.get("d_group", D.GROUPS[0]))["after"])
bridge(td["bridge"])

# ---------------------------------------------------------------- section 3: B
countries = B.countries(owners)
priced = B.ranked(owners)
top_n = st.session_state.get("b_top_n", 10)
focus = st.session_state.get("b_country", "Australia")
tb = B.texts(owners, top_n, focus)
st.header(tb["title"], anchor="section-3")
md(tb["lead"])


def draw_b() -> None:
    left, right = st.columns([3, 2])
    n = left.slider("Owners shown (top N by capital cost)", 3, len(priced), 10, key="b_top_n")
    where = right.selectbox("Highlight a country", countries, index=countries.index("Australia"), key="b_country")
    st.altair_chart(style(B.build(owners, n, where)), theme=None, width="stretch")
    read_box(B.texts(owners, n, where)["read"])
    st.download_button("Download chart B data (CSV)", owners.to_csv(index=False), "chart_b_datacenters_by_owner.csv", key="b_download")


chart_card("B", "Ranking · sorted horizontal bars", tb["caption"], draw_b)
md(B.texts(owners, st.session_state.get("b_top_n", 10), st.session_state.get("b_country", "Australia"))["after"])
bridge(tb["bridge"])

# ---------------------------------------------------------------- section 4 and sources
st.header("4 · What the data cannot show", anchor="section-4")
md(page.LIMITS)

st.header("Sources", anchor="sources")
for app_file, holds, raw, publisher, licence, md5 in page.SOURCES:
    md(f"- **{app_file}** ({holds}). Raw file: `data/sources/{raw}` · {publisher} · Licence: {licence} · MD5 `{md5}`")
st.caption(page.SOURCE_NOTE)
st.markdown(f"**{page.REFRESH_SHORT}**")
