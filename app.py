"""Is cutting-edge AI becoming something only big tech can do?

36104 A3 data narrative for a university research funding body. Run:  streamlit run app.py
Reads only the three available files in data/processed/. The documented build script is not present in this checkout.

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
from charts import chart_e_scale as E
from charts import page
from charts.common import SEGMENT_NAME, SEGMENT_ORDER, WORLD_URL, read, style

st.set_page_config(page_title="Is frontier AI big tech only?", page_icon=":bar_chart:", layout="wide")
st.markdown(
    """<style>
    .block-container {max-width: 1180px; padding-top: 3rem;}
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
        st.markdown(f'<p class="eyebrow">Chart {letter} · {family}</p>', unsafe_allow_html=True)
        md(f"**{caption}**")
        draw()


def md(text: str) -> None:
    """Markdown without LaTeX: Streamlit treats paired $ signs as maths, so escape them."""
    st.markdown(text.replace("$", "\\$"))


def read_box(text: str) -> None:
    md(text)


def bridge(text: str) -> None:
    st.markdown(f'<p class="bridge">{text}</p>', unsafe_allow_html=True)


def source_caption(text: str) -> None:
    """A concise, consistent source/date caption for a chart card."""
    st.caption(text)


segments, owners, systems = load(A.FILE), load(B.FILE), load(C.FILE)

# ---------------------------------------------------------------- opening
st.markdown('<p class="eyebrow">36104 · A3 · data narrative</p>', unsafe_allow_html=True)
st.title(page.TITLE)
with st.container(border=True):
    st.markdown("**On this page**  \n" + "  \n".join(f"[{name}](#{anchor})" for anchor, name in page.CONTENTS))
with st.container(border=True, key="answer"):
    md(page.answer(segments, systems, owners))

# ---------------------------------------------------------------- section 1: A then C
ta = A.texts(segments, systems)
st.header(ta["title"], anchor="section-1")
md(ta["lead"])


def draw_a() -> None:
    view = st.radio("Measure", A.VIEWS, horizontal=True, key="a_measure")
    chart = A.build_stacked(segments) if view == A.VIEWS[0] else A.build_paired(segments)
    st.altair_chart(style(chart), theme=None, width="stretch")
    read_box(ta["read"])
    source_caption("Source: TOP500 List, June 2026; processed file `fig4_top500_by_segment.csv`. Last documented refresh: 11 October 2026.")
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
    source_caption("Source: TOP500 List, June 2026; processed file `top500_systems_clean.csv`. Last documented refresh: 11 October 2026.")
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
    st.markdown("**All country values**")
    country_table = table.rename(columns={
        "country": "Country", "systems": "TOP500 systems", "rmax_tflops": "Combined Rmax (TFlop/s)",
        "share_pct": "Share of selected Rmax (%)",
    })[["Country", "TOP500 systems", "Combined Rmax (TFlop/s)", "Share of selected Rmax (%)"]]
    st.dataframe(
        country_table.style.format({
            "Combined Rmax (TFlop/s)": "{:,.0f}",
            "Share of selected Rmax (%)": "{:.1f}",
        }),
        hide_index=True,
        width="stretch",
    )
    read_box(D.texts(systems, chosen)["read"])
    source_caption("Source: TOP500 List, June 2026; processed file `top500_systems_clean.csv`. Last documented refresh: 11 October 2026.")
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
    source_caption("Source: Epoch AI, Data on AI data centers, October 2026 update; processed file `datacenters_by_owner_country.csv`. Last documented refresh: 11 October 2026.")
    st.download_button("Download chart B data (CSV)", owners.to_csv(index=False), "chart_b_datacenters_by_owner.csv", key="b_download")


chart_card("B", "Ranking · sorted horizontal bars", tb["caption"], draw_b)
md(B.texts(owners, st.session_state.get("b_top_n", 10), st.session_state.get("b_country", "Australia"))["after"])
bridge(tb["bridge"])

# ---------------------------------------------------------------- section 4: E
te = E.texts()
st.header(te["title"], anchor="section-4")
md(te["lead"])


def draw_e() -> None:
    left, right = st.columns([2, 3])
    country_options = E.countries(owners)
    country = left.selectbox("Filter owners by listed site country", country_options, key="e_country")
    selected_owners = right.multiselect(
        "Owners included", E.owner_options(owners), default=E.owner_options(owners), key="e_owners"
    )
    rows = E.filtered(owners, country, selected_owners)
    if rows.empty:
        st.info("No owners match these filters. Choose at least one owner or a different country.")
        return

    totals = E.summary(rows)
    investment, power, sites, h100 = st.columns(4)
    investment.metric("Estimated investment", f"${totals['investment']:.1f}B", help="Sum of estimated capital cost in 2025 US dollars.")
    power.metric("Listed power capacity", f"{totals['power']:,.0f} MW", help="Sum of listed power capacity for selected owner records.")
    sites.metric("Data centres", f"{totals['datacenters']}", help="Sum of listed data-centre counts for selected owner records.")
    h100.metric("Estimated H100 equivalents", f"{totals['h100']:,.0f}", help="Sum of the dataset's estimated H100 equivalents.")

    visible = E.plottable(rows)
    if visible.empty:
        st.info("The selected owners have no positive capital-cost, power and H100-equivalent values to plot. Their records are shown below.")
    else:
        st.altair_chart(style(E.build(rows)), theme=None, width="stretch")
    read_box(te["read"])
    md(te["limits"])
    source_caption("Source: Epoch AI, Data on AI data centers, October 2026 update; processed file `datacenters_by_owner_country.csv`. Last documented refresh: 11 October 2026.")

    st.markdown("**Filtered owner records**")
    table = rows.rename(columns={
        "owner": "Owner", "country": "Listed site countries", "n_countries": "Countries", "n_datacenters": "Data centres",
        "capital_cost_2025usd_bn": "Capital cost (2025 USD bn)", "power_mw": "Power (MW)",
        "h100_equivalents": "Estimated H100 equivalents", "capex_share_pct": "Capex share (%)",
    })
    st.dataframe(table, hide_index=True, width="stretch")
    st.download_button("Download filtered chart E data (CSV)", rows.to_csv(index=False), "chart_e_datacentre_scale.csv", key="e_download")


chart_card("E", "Relationship · bubble scatterplot", te["caption"], draw_e)

# ---------------------------------------------------------------- section 5 and sources
st.header("5 · What the data cannot show", anchor="section-5")
md(page.LIMITS)

st.header("Sources", anchor="sources")
for app_file, holds, raw, publisher, licence, md5 in page.SOURCES:
    md(f"- **{app_file}** ({holds}). Documented raw-file reference: `data/sources/{raw}` · {publisher} · Licence: {licence} · MD5 `{md5}`")
st.caption(page.SOURCE_NOTE)
st.markdown(f"**{page.REFRESH_SHORT}**")
