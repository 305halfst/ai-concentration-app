"""Opening hero graphics (HTML + inline SVG, no external assets).

1. chip_owners(): a drawn, generic AI-chip icon beside the share of tracked H100 equivalents held by each of the
   five largest owners, then the other companies and unknown owners.
2. zero_owners(): one tile per named owner of the tracked AI data centres, all companies, plus an empty highlighted
   slot for universities and public labs, which is 0.

Companies are shown by name in plain text, not by logo: logos are trademarks and the names carry the same
information. All numbers come from datacenters_by_owner_country.csv.
"""

from __future__ import annotations

import base64
import html

import pandas as pd

from charts.common import OTHER, PRIVATE, PUBLIC

BIG_FIVE = ["Google", "Meta", "Amazon", "Microsoft", "SpaceXAI"]
LIGHT = "#E8B98A"

CSS = f"""<style>
.hv {{font-family: 'Source Sans Pro', 'IBM Plex Sans', Helvetica, Arial, sans-serif; color: #15181C;}}
.hv-label {{font-size: 14px; color: #3A4047; margin: 0 0 6px;}}
.hv-chip {{display: grid; grid-template-columns: 190px 1fr; gap: 22px; align-items: center;}}
.hv-big {{font-size: 52px; font-weight: 700; line-height: 1; margin: 6px 0 2px; color: {PRIVATE};}}
.hv-row {{display: grid; grid-template-columns: 112px 1fr 58px; gap: 8px; align-items: center; margin: 3px 0;}}
.hv-name {{font-weight: 700; font-size: 15px; letter-spacing: .01em;}}
.hv-name.dim {{font-weight: 500; color: #555D65; font-size: 13px;}}
.hv-track {{background: #EEF0F2; height: 18px; border-radius: 3px; overflow: hidden;}}
.hv-track i {{display: block; height: 100%;}}
.hv-pct {{font-weight: 700; font-size: 14px; text-align: right;}}
.hv-sum {{border-top: 2px solid #15181C; margin-top: 6px; padding-top: 4px; font-size: 14px;}}
.hv-tiles {{display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px;}}
.hv-tile {{background: {PRIVATE}; color: #fff; border-radius: 4px; padding: 6px 8px; font-size: 12px; font-weight: 600;
          min-width: 74px; text-align: center;}}
.hv-zero {{border: 3px dashed {PUBLIC}; background: #FFFFFF; color: {PUBLIC}; border-radius: 6px; padding: 2px 14px;
          display: flex; align-items: center; gap: 10px;}}
.hv-zero b {{font-size: 52px; line-height: 1;}}
.hv-zero span {{font-size: 13px; font-weight: 600; max-width: 150px; line-height: 1.25;}}
.hv-zerorow {{display: flex; gap: 14px; align-items: stretch; flex-wrap: wrap;}}
.hv-note {{font-size: 12px; color: #555D65; margin-top: 6px;}}
@media (max-width: 700px) {{.hv-chip {{grid-template-columns: 1fr;}} .hv-row {{grid-template-columns: 90px 1fr 52px;}}}}
</style>"""


def _chip_svg() -> str:
    """A generic accelerator: package, die and memory stacks, with pins. Not any vendor's artwork."""
    pins = "".join(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#8C96A0"/>'
        for i in range(9)
        for x, y, w, h in [(30 + i * 15, 6, 6, 12), (30 + i * 15, 162, 6, 12), (6, 30 + i * 15, 12, 6), (162, 30 + i * 15, 12, 6)]
    )
    hbm = "".join(f'<rect x="{x}" y="{y}" width="22" height="30" rx="2" fill="#5B6570"/>'
                  for x in (40, 118) for y in (48, 102))
    return (
        '<svg viewBox="0 0 180 180" width="170" height="170" role="img" aria-label="Generic AI accelerator chip">'
        f"{pins}"
        '<rect x="18" y="18" width="144" height="144" rx="10" fill="#2B3138"/>'
        f"{hbm}"
        '<rect x="68" y="48" width="44" height="84" rx="3" fill="#C9A227"/>'
        '<text x="90" y="86" font-family="Helvetica,Arial,sans-serif" text-anchor="middle" font-size="13" font-weight="700" fill="#2B3138">H100</text>'
        '<text x="90" y="101" font-family="Helvetica,Arial,sans-serif" text-anchor="middle" font-size="9" fill="#2B3138">equivalent</text>'
        "</svg>"
    )


def _chip_img() -> str:
    """As an <img> data URI: st.html sanitises inline SVG away."""
    svg = _chip_svg().replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    data = base64.b64encode(svg.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{data}" width="170" height="170" alt="Generic AI accelerator chip">'



def chip_shares(owners: pd.DataFrame) -> pd.DataFrame:
    total = owners["h100_equivalents"].sum()
    big = owners[owners["owner"].isin(BIG_FIVE)].sort_values("h100_equivalents", ascending=False)
    rows = [(o, v / total * 100, PRIVATE, True) for o, v in zip(big["owner"], big["h100_equivalents"])]
    unknown = owners.loc[owners["owner"] == "Unknown", "h100_equivalents"].sum()
    rest = total - big["h100_equivalents"].sum() - unknown
    rows += [("Other companies", rest / total * 100, LIGHT, False), ("Owner unknown", unknown / total * 100, OTHER, False)]
    return pd.DataFrame(rows, columns=["name", "share", "colour", "big"])


def chip_owners(owners: pd.DataFrame, n_estimated: int) -> str:
    data = chip_shares(owners)
    top = data["share"].max()
    big = data.loc[data["big"], "share"].sum()
    bars = "".join(
        f'<div class="hv-row"><span class="hv-name{"" if r.big else " dim"}">{html.escape(r.name)}</span>'
        f'<span class="hv-track"><i style="width:{r.share / top * 100:.1f}%;background:{r.colour}"></i></span>'
        f'<span class="hv-pct">{r.share:.1f}%</span></div>'
        for r in data.itertuples()
    )
    return (
        f'{CSS}<div class="hv"><p class="hv-label">Who owns the tracked AI chips (estimated H100 equivalents, '
        f'Epoch AI data centres, October 2026)</p><div class="hv-chip"><div style="text-align:center">{_chip_img()}<div class="hv-big">{big:.1f}%</div><div style="font-size:13px;color:#555D65">owned by five companies</div></div><div>'
        f"{bars}<div class=\"hv-sum\">100% = {owners['h100_equivalents'].sum():,.0f} estimated H100 equivalents "
        f"in the {n_estimated} of {int(owners['n_datacenters'].sum())} tracked sites with an estimate</div></div></div></div>"
    )


def zero_owners(owners: pd.DataFrame) -> str:
    named = owners[owners["owner"] != "Unknown"].sort_values(["h100_equivalents", "owner"], ascending=[False, True])
    tiles = "".join(
        f'<span class="hv-tile">{html.escape(o)}{" (AU)" if o == "Firmus" else ""}</span>' for o in named["owner"]
    )
    return (
        f'{CSS}<div class="hv"><p class="hv-label">The {len(named)} named owners of the tracked AI data centres: '
        f'<b style="color:{PRIVATE}">all {len(named)} are companies</b></p>'
        f'<div class="hv-zerorow"><div class="hv-zero"><b>0</b><span>universities or public research labs</span></div>'
        f'<div class="hv-tiles" style="flex:1">{tiles}</div></div>'
        f'<p class="hv-note">Ordered by estimated H100 equivalents; our classification by owner name. A further '
        f'{int(owners.loc[owners["owner"] == "Unknown", "n_datacenters"].sum())} sites have no known owner.</p></div>'
    )


SCENARIO_CSS = f"""<style>
.sc {{font-family: 'Source Sans Pro', 'IBM Plex Sans', Helvetica, Arial, sans-serif; color: #15181C; background: #FFFFFF;
      border: 1px solid #DCDFE2; border-left: 6px solid {PUBLIC}; border-radius: 8px; padding: 16px 20px; margin: 4px 0 12px;}}
.sc-who {{display: flex; align-items: center; gap: 12px;}}
.sc-who b {{font-size: 20px; color: {PUBLIC};}}
.sc-who small {{display: block; font-size: 12px; color: #555D65;}}
.sc-goal {{font-size: 22px; line-height: 1.35; margin: 12px 0 4px;}}
.sc-goal em {{font-style: normal; font-weight: 700; color: {PUBLIC}; font-size: 30px;}}
.sc-need {{font-size: 13px; text-transform: uppercase; letter-spacing: .05em; color: #555D65; margin: 14px 0 6px;}}
.sc-grid {{display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;}}
.sc-grid div {{background: #F3F5F8; border-radius: 6px; padding: 10px 12px;}}
.sc-grid span {{display: block; font-size: 13px; color: #3A4047;}}
.sc-grid b {{display: block; font-size: 30px; line-height: 1.15; margin-top: 2px;}}
.sc-icons {{margin-top: 10px; line-height: 0;}}
.sc-gdp {{display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; border-top: 1px solid #DCDFE2; margin-top: 12px; padding-top: 10px;}}
.sc-gdp span {{font-size: 15px; font-weight: 600;}}
.sc-gdp b {{font-size: 30px; color: {PUBLIC};}}
.sc-gdp small {{font-size: 12px; color: #555D65;}}
.sc-icons img {{margin: 0 3px 3px 0;}}
@media (max-width: 700px) {{.sc-grid {{grid-template-columns: 1fr;}}}}
</style>"""


def _gov_icon() -> str:
    """Generic public-building icon (pediment and columns). Deliberately not the Commonwealth Coat of Arms."""
    cols = "".join(f'<rect x="{x}" y="22" width="5" height="22" fill="{PUBLIC}"/>' for x in (10, 20, 30, 40))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 56" width="44" height="44">'
           f'<polygon points="28,4 4,18 52,18" fill="{PUBLIC}"/>{cols}<rect x="4" y="46" width="48" height="6" fill="{PUBLIC}"/></svg>')
    return f'<img src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}" width="44" height="44" alt="">'


def _mini_chip(fill: str) -> str:
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" width="20" height="20">'
           f'<rect x="3" y="3" width="14" height="14" rx="2" fill="{fill}"/><rect x="7" y="7" width="6" height="6" fill="#C9A227"/></svg>')
    return base64.b64encode(svg.encode()).decode()


MINI_PUBLIC = _mini_chip(PUBLIC)


def scenario(target: float, chips: float, cost_bn: float, times_au: float, au_chips: float, gdp_pct: float, gdp_bn: float, gdp_year: int) -> str:
    """Plain-language card for Calculator K. Element ids let the static HTML export update it with JavaScript."""
    icons = "".join(f'<img src="data:image/svg+xml;base64,{MINI_PUBLIC}" width="20" height="20" alt="">'
                    for _ in range(max(1, round(times_au))))
    return (
        f'{SCENARIO_CSS}<div class="sc"><div class="sc-who">{_gov_icon()}<div><b>Scenario: if the Australian Government set a goal</b>'
        f'<small>the reader sets the goal with the slider; not a government policy, target or figure</small></div></div>'
        f'<p class="sc-goal">Goal: public institutions own <em id="sc-pct">{target:.1f}%</em> of the world\'s tracked AI chips.</p>'
        f'<p class="sc-need">That would take</p><div class="sc-grid">'
        f'<div><span>New AI chips to build (H100 equivalents)</span><b id="sc-chips">{chips:,.0f}</b></div>'
        f'<div><span>Rough cost (2025 US$)</span><b id="sc-cost">${cost_bn:,.1f}B</b></div>'
        f'<div><span>Copies of the only Australian AI site Epoch tracks (Firmus, {au_chips:,.0f} chips)</span>'
        f'<b><span id="sc-times" style="display:inline;font-size:30px;color:#15181C">{times_au:,.0f}</span> ×</b></div></div>'
        f'<div class="sc-icons" id="sc-icons" title="Each icon = one Firmus-sized site">{icons}</div>'
        f'<p style="font-size:12px;color:#555D65;margin:4px 0 0">Each blue chip icon = one site the size of Firmus.</p>'
        f'<div class="sc-gdp"><span>Share of Australia\'s GDP</span><b id="sc-gdp">{gdp_pct:.2f}%</b>'
        f'<small>one-off cost ÷ Australia\'s {gdp_year} GDP of US${gdp_bn:,.0f}B (World Bank, current US$). For scale only: the build '
        f'would be spread over several years.</small></div></div>'
    )


def uni_drop(f: dict) -> str:
    """Universities' share of notable AI systems, first vs last year, as two circles whose AREAS match the shares."""
    first, last = f["t_uni_first"], f["t_uni_last"]
    r1 = 64
    r2 = r1 * (last / first) ** 0.5
    navy = "#0B2A55"
    font = "font-family='Helvetica,Arial,sans-serif'"
    svg = (
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 200' width='360' height='200'>"
        f"<defs><marker id='a' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='7' markerHeight='7' orient='auto'>"
        f"<path d='M0,0 L10,5 L0,10 z' fill='#B4232A'/></marker></defs>"
        f"<circle cx='74' cy='84' r='{r1}' fill='{navy}'/>"
        f"<text x='74' y='96' text-anchor='middle' {font} font-size='34' font-weight='700' fill='white'>{first:.0f}%</text>"
        f"<text x='74' y='172' text-anchor='middle' {font} font-size='15' font-weight='700' fill='#15181C'>{f['t_first']}</text>"
        f"<text x='74' y='190' text-anchor='middle' {font} font-size='12' fill='#555D65'>"
        f"{round(first * f['t_n_first'] / 100)} of {f['t_n_first']} systems</text>"
        f"<line x1='148' y1='84' x2='206' y2='84' stroke='#B4232A' stroke-width='4' marker-end='url(#a)'/>"
        f"<text x='177' y='70' text-anchor='middle' {font} font-size='13' font-weight='700' fill='#B4232A'>"
        f"{last - first:+.1f} pts</text>"
        f"<circle cx='{222 + r2:.1f}' cy='84' r='{r2:.2f}' fill='{navy}'/>"
        f"<text x='{230 + 2 * r2:.1f}' y='100' {font} font-size='44' font-weight='700' fill='{navy}'>{last:.1f}%</text>"
        f"<text x='{222 + r2:.1f}' y='172' text-anchor='middle' {font} font-size='15' font-weight='700' fill='#15181C'>{f['t_last']}</text>"
        f"<text x='{222 + r2:.1f}' y='190' text-anchor='middle' {font} font-size='12' fill='#555D65'>"
        f"{round(last * f['t_n_last'] / 100)} of {f['t_n_last']} systems</text>"
        f"</svg>"
    )
    data = base64.b64encode(svg.encode()).decode()
    return (
        f"{CSS}<div class='hv'><p class='hv-label'>Universities' share of notable AI systems, {f['t_first']} → {f['t_last']}</p>"
        f"<img src='data:image/svg+xml;base64,{data}' style='width:100%;max-width:360px;height:auto' "
        f"alt='Universities built {first:.0f}% of notable AI systems in {f['t_first']} and {last:.1f}% in {f['t_last']}'>"
        f"<p class='hv-note'>Circle area = share. Source: Epoch AI notable AI systems via Our World in Data.</p></div>"
    )
