"""Is cutting-edge AI becoming something only big tech can do?

36104 A3 data narrative for an Australian Government research-infrastructure funding officer.
Run:  streamlit run app.py.  Reads only the seven files in data/processed/ (rebuilt from data/sources/ by data/build_processed.py).

Order: question and answer first, then five numbered sections (chart cards with controls, an expandable
"How to read this chart" and a one-line finding), the calculator and recommendation, limits, summary and sources.
"""

from __future__ import annotations

import altair as alt
import pandas as pd
import os

import streamlit as st

from charts import chart_a_segments as A
from charts import chart_b_capex as B
from charts import chart_c_sizes as C
from charts import chart_d_map as D
from charts import chart_e_scale as E
from charts import chart_f_two_worlds as F
from charts import chart_p_pictogram as P
from charts import chart_t_time as T
from charts import chart_w_waffle as W
from charts import hero_visuals as HV
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
    """'How to read' notes stay on screen but folded, so the chart leads."""
    with st.expander("How to read this chart"):
        md(text)


def source_caption(text: str) -> None:
    """A concise, consistent source/date caption for a chart card."""
    st.caption(text)


segments, owners, systems = load(A.FILE), load(B.FILE), load(C.FILE)
ai_systems = load(T.FILE)
fig = page.figures(segments, systems, owners, ai_systems)
SRC_TOP500 = "Source: TOP500 List, June 2026"
SRC_EPOCH = "Source: Epoch AI, Data on AI data centers, October 2026 update"


def finding(text: str) -> None:
    st.markdown(f'<p class="finding">{text}</p>', unsafe_allow_html=True)


st.markdown("""<style>
.finding {font-size: 20px; line-height: 1.4; font-weight: 600; margin: 4px 0 26px;}
.finding b {color: #D9822B;}
</style>""", unsafe_allow_html=True)

# ---------------------------------------------------------------- question and answer, first
st.markdown('<p class="eyebrow">36104 · A3 · data narrative</p>', unsafe_allow_html=True)
st.title(page.TITLE, anchor="question")
st.markdown(f'<p class="bridge">{page.QUESTION_FOR_READER}</p>', unsafe_allow_html=True)
with st.container(border=True, key="answer"):
    md(page.answer(fig))
    left, right = st.columns([1.15, 2.3], gap="large")
    with left:
        st.html(HV.uni_drop(fig))
    with right:
        st.html(HV.chip_owners(owners, fig["n_estimated"]))
    st.html(HV.zero_owners(owners, segments, systems, fig["n_estimated"]))
tp = P.texts(ai_systems, (fig["t_first"], fig["t_last"]))


def draw_p() -> None:
    st.altair_chart(style(P.build(ai_systems, (fig["t_first"], fig["t_last"]))), theme=None)
    read_box(tp["read"])
    source_caption("Source: Our World in Data, from Epoch AI's notable AI systems; processed file `ai_systems_by_sector.csv`. "
                   "Last data refresh: 11/10/2026.")


chart_card("P", "Part-to-whole · pictogram (1 square = 1 system)", tp["caption"], draw_p)
md(page.QUESTION_EXPLAINED + "  \n" + page.AUDIENCE)
st.caption("Last data refresh: 11/10/2026 · sources at the end of the page · " +
           " · ".join(f"[{name}](#{anchor})" for anchor, name in page.CONTENTS[1:]))

# ---------------------------------------------------------------- 1 · time (T)
tt = T.texts(ai_systems)
st.header("1 · Universities' share of notable AI systems has collapsed", anchor="section-1")


def draw_t() -> None:
    libs = "cdn"
    if os.environ.get("A3_INLINE_JS"):  # offline testing only; the deployed app loads the libraries from cdnjs
        libs = os.environ["A3_INLINE_JS"]
        libs = "\n".join(open(path).read() for path in libs.split(os.pathsep))
    st.iframe(T.html(ai_systems, libs), height=545)
    source_caption("Source: Our World in Data, from Epoch AI's notable AI systems; processed file `ai_systems_by_sector.csv`. "
                   "Last data refresh: 11/10/2026.")
    st.download_button("Download chart T data (CSV)", T.yearly(ai_systems).to_csv(index=False), "chart_t_ai_systems_by_sector.csv",
                       key="t_download")


chart_card("T", "Change over time · animated 100% stacked area", tt["caption"], draw_t)
finding(f"Universities built <b>{fig['t_uni_first']:.0f}%</b> of notable AI systems in {fig['t_first']} "
        f"({fig['t_n_first']} systems). In {fig['t_last']}: <b>{fig['t_uni_last']:.1f}%</b> ({fig['t_n_last']} systems). "
        f"Industry took over in {fig['t_cross']}.")

# ---------------------------------------------------------------- 2 · ownership (W, B, E)
st.header("2 · Five companies own most of the tracked AI infrastructure", anchor="section-2")
tw = W.texts(owners)


def draw_w() -> None:
    st.altair_chart(style(W.build(owners)), theme=None, width="stretch")
    read_box(tw["read"])
    source_caption(SRC_EPOCH + "; processed file `datacenters_by_owner_country.csv`. Last data refresh: 11/10/2026.")


chart_card("W", "Part-to-whole · unit chart (1 square = 1%)", tw["caption"], draw_w)
finding(f"<b>{fig['big5_h100']:.1f}%</b> of the AI chips Epoch tracks (October 2026) belong to five companies. "
        "Universities and public labs own <b>none</b> of the squares.")

countries = B.countries(owners)
priced = B.ranked(owners)
tb = B.texts(owners, st.session_state.get("b_top_n", 10), st.session_state.get("b_country", "Australia"))


def draw_b() -> None:
    left, right = st.columns([3, 2])
    n = left.slider("Owners shown (top N by capital cost)", 3, len(priced), 10, key="b_top_n")
    where = right.selectbox("Highlight a country", countries, index=countries.index("Australia"), key="b_country")
    st.altair_chart(style(B.build(owners, n, where)), theme=None, width="stretch")
    read_box(B.texts(owners, n, where)["read"])
    source_caption("Source: Epoch AI, Data on AI data centers, October 2026 update; processed file `datacenters_by_owner_country.csv`. Last documented refresh: 11 October 2026.")
    st.download_button("Download chart B data (CSV)", owners.to_csv(index=False), "chart_b_datacenters_by_owner.csv", key="b_download")


chart_card("B", "Ranking · sorted horizontal bars", tb["caption"], draw_b)
google = owners.set_index("owner").loc["Google", "capital_cost_2025usd_bn"]
finding(f"Google alone: <b>${google:.1f}B</b> of estimated capital cost. Australia's only site: "
        f"<b>${owners.set_index('owner').loc['Firmus', 'capital_cost_2025usd_bn']:.1f}B</b>.")

te = E.texts()


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
    investment.metric("Estimated investment", f"${totals['investment']:.1f}B")
    power.metric("Listed power capacity", f"{totals['power']:,.0f} MW")
    sites.metric("Data centres", f"{totals['datacenters']}")
    h100.metric("Estimated H100 equivalents", f"{totals['h100']:,.0f}")

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
finding(te["title"] + ".")

# ---------------------------------------------------------------- 3 · the turn (F)
st.header("3 · Public institutions won the last race, not this one", anchor="section-3")
tf = F.texts(segments, owners)


def draw_f() -> None:
    st.altair_chart(style(F.build(segments, owners)), theme=None, width="stretch")
    read_box(tf["read"])
    source_caption("Sources: TOP500 List, June 2026 (`fig4_top500_by_segment.csv`); Epoch AI, Data on AI data centers, "
                   "October 2026 update (`datacenters_by_owner_country.csv`). Last documented refresh: 11 October 2026.")


chart_card("F", "Part-to-whole · two 100% stacked bars", tf["caption"], draw_f)
finding(f"Public institutions run <b>{fig['public_rmax']:.1f}%</b> of TOP500 supercomputing (June 2026), and <b>0%</b> "
        "of the tracked AI chips with a named owner (October 2026).")

# ---------------------------------------------------------------- 4 · universities and Australia (A, C, D)
st.header("4 · Universities and Australia barely register", anchor="section-4")
ta = A.texts(segments, systems)


def draw_a() -> None:
    view = st.radio("Measure", A.VIEWS, horizontal=True, key="a_measure")
    chart = A.build_stacked(segments) if view == A.VIEWS[0] else A.build_paired(segments)
    st.altair_chart(style(chart), theme=None, width="stretch")
    read_box(ta["read"])
    source_caption("Source: TOP500 List, June 2026; processed file `fig4_top500_by_segment.csv`. Last documented refresh: 11 October 2026.")
    st.download_button("Download chart A data (CSV)", segments.to_csv(index=False), "chart_a_top500_by_segment.csv", key="a_download")


chart_card("A", "Part-to-whole · 100% stacked bars", ta["caption"], draw_a)
finding(f"Even in supercomputing, universities run {fig['uni_systems']:.1f}% of the machines but hold "
        f"<b>{fig['uni_rmax']:.1f}%</b> of the compute.")

tc = C.texts(systems, SEGMENT_ORDER)


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
uni_max = systems[systems["segment"] == "Academic"]["rmax_tflops"].max() / 1000
finding(f"Their biggest machine runs at <b>{uni_max:,.0f}</b> PFlop/s; the list's biggest at "
        f"{systems['rmax_tflops'].max() / 1000:,.0f}.")

td = D.texts(systems, st.session_state.get("d_group", D.GROUPS[0]))


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
finding(f"Australia: <b>{fig['au_top500']:.1f}%</b> of TOP500 compute (June 2026) and <b>{fig['au_h100']:.1f}%</b> of the "
        "AI chips Epoch tracks (October 2026).")

# ---------------------------------------------------------------- 5 · what it would take, and the ask
st.header("5 · What it would take, and our ask", anchor="section-5")


def draw_k() -> None:
    target = st.slider("Scenario goal for the Australian Government: public share of the world's tracked AI chips (%)",
                       0.5, 10.0, 1.0, 0.5, key="k_target")
    k = page.calculator(fig, target)
    st.html(HV.scenario(target, k, fig))
    md("*Other owners are held at today's size; new capacity is costed at Epoch's estimate for the Firmus site. "
       "An order of magnitude, not a budget.*")
    source_caption(SRC_EPOCH + "; processed files `datacenters_by_owner_country.csv`, `au_gdp.csv` (World Bank) and `au_budget.csv` (PBO).")


chart_card("K", "Calculator · what it would take", "Calculator K. What a chosen public share of today's tracked AI "
           "chips would take, in Firmus-sized university sites, and its cost against Australia's GDP and federal spending. Units: H100 equivalents; billions "
           "of 2025 US dollars; % of one year.", draw_k)
with st.container(border=True, key="recommendation_box"):
    md(page.recommendation(fig))

# ---------------------------------------------------------------- limits and sources
st.header("What the data cannot show", anchor="limits")
md(page.limits(ai_systems, owners, fig))
st.header("In summary", anchor="summary")
with st.container(border=True, key="summary_box"):
    md(page.summary(fig))
st.header("Sources", anchor="sources")
for app_file, holds, raw, publisher, licence, md5 in page.SOURCES:
    md(f"- **{app_file}** ({holds}). Raw file: `data/sources/{raw}` · {publisher} · Licence: {licence} · MD5 `{md5}`")
st.caption(page.SOURCE_NOTE.replace("$", "\\$"))
st.markdown(f"**{page.REFRESH_SHORT}**")
