"""Presentation layer for the R01 dashboard: design tokens, CSS, HTML components and Plotly styling.

Nothing here reads data; app.py owns every file access (through its allowlist).
"""
from __future__ import annotations

import html

import plotly.graph_objects as go
import streamlit as st

# Design tokens (validated categorical palette, recessive chrome).
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE, PLANE = "#e1e0d9", "#c3c2b7", "#fcfcfb", "#f6f5f1"
NAVY, NAVY2 = "#0d2240", "#163a6b"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
MAGENTA, GREEN, VIOLET, RED = "#e87ba4", "#008300", "#6250d6", "#e34948"
GREY, LIGHT = "#9a9893", "#d9d8d2"
BLUE_TINT, ORANGE_TINT = "rgba(42,120,214,0.16)", "rgba(235,104,52,0.16)"
STATUS = {"good": "#0ca30c", "warning": "#c98500", "serious": "#ec835a", "critical": "#d03b3b",
          "neutral": "#6f6d68"}
FONT = "'Source Sans 3', 'Source Sans Pro', 'Source Sans', system-ui, -apple-system, 'Segoe UI', sans-serif"

CSS = f"""
<style>
header[data-testid="stHeader"] {{ background: transparent; }}
.stApp {{ background: {PLANE}; }}
.block-container {{ padding-top: 1.6rem; padding-bottom: 4rem; max-width: 1240px; }}
h1, h2, h3, h4 {{ font-family: {FONT}; letter-spacing: -0.015em; color: {INK}; }}
h2 {{ font-weight: 750 !important; font-size: 1.9rem !important; padding-top: 0.2rem !important; }}
h3 {{ font-weight: 650 !important; font-size: 1.22rem !important; margin-top: 1.6rem !important; }}
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {{
  font-size: 0.98rem; line-height: 1.62; color: #23221f;
}}
[data-testid="stCaptionContainer"] {{ color: {INK2}; line-height: 1.5; }}
code {{ font-size: 0.84em; }}

/* Sidebar navigation: radio styled as a nav list */
section[data-testid="stSidebar"] {{ background: {NAVY}; }}
section[data-testid="stSidebar"] * {{ color: #dfe7f3; }}
section[data-testid="stSidebar"] a {{ color: #9ec5f4 !important; }}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{ color: #9fb0c8; }}
section[data-testid="stSidebar"] div[role="radiogroup"] {{ gap: 2px; width: 100%; }}
section[data-testid="stSidebar"] div[role="radiogroup"] > div {{ width: 100%; }}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"] {{
  padding: 0.42rem 0.7rem; border-radius: 8px; margin: 0; width: 100%;
  transition: background 120ms ease;
}}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"]:hover {{ background: rgba(255,255,255,0.07); }}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"] > div > div:first-child {{ display: none; }}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"][data-selected="true"] {{
  background: rgba(57,135,229,0.24); box-shadow: inset 3px 0 0 #6da7ec;
}}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"][data-selected="true"] p {{ color: #fff; font-weight: 600; }}
section[data-testid="stSidebar"] div[role="radiogroup"] p {{ font-size: 0.92rem; }}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
  text-transform: uppercase; letter-spacing: 0.09em; font-size: 0.72rem; color: #8aa0bf; font-weight: 600;
}}

/* Hero */
.hero {{
  background: radial-gradient(1200px 400px at 85% -20%, rgba(57,135,229,0.45), transparent 60%),
              linear-gradient(135deg, {NAVY} 0%, {NAVY2} 100%);
  border-radius: 18px; padding: 2.2rem 2.4rem 2rem; color: #fff; margin-bottom: 1.1rem;
  box-shadow: 0 10px 30px rgba(13,34,64,0.18);
}}
.hero .eyebrow {{ text-transform: uppercase; letter-spacing: 0.14em; font-size: 0.74rem; color: #9ec5f4;
  font-weight: 700; }}
.hero h1 {{ color: #fff; font-size: 2.35rem; line-height: 1.15; margin: 0.45rem 0 0.7rem; font-weight: 800;
  padding: 0; }}
.hero p.lead {{ color: #d5e1f1; font-size: 1.06rem; line-height: 1.6; max-width: 860px; margin: 0; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 1.2rem; }}
.chip {{ display: inline-flex; align-items: center; gap: 6px; border-radius: 999px; padding: 0.26rem 0.72rem;
  font-size: 0.78rem; font-weight: 600; background: rgba(255,255,255,0.1); color: #eaf1fb;
  border: 1px solid rgba(255,255,255,0.18); }}
.chip .dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; }}

/* Page heading */
.eyebrow-label {{ text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.74rem; font-weight: 700;
  color: {BLUE}; margin-bottom: -0.6rem; }}
.lead-text {{ font-size: 1.05rem; color: {INK2}; line-height: 1.6; max-width: 900px; margin: 0.1rem 0 1.0rem; }}

/* Context ribbon */
.ribbon {{ display: flex; flex-wrap: wrap; gap: 6px 18px; background: #fff; border: 1px solid rgba(11,11,11,0.08);
  border-radius: 12px; padding: 0.7rem 1rem; font-size: 0.84rem; color: {INK2}; margin-bottom: 0.4rem; }}
.ribbon b {{ color: {INK}; font-weight: 650; }}
.ribbon code {{ background: {PLANE}; }}

/* Stat cards */
.stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px;
  margin: 0.4rem 0 1.2rem; }}
.stat {{ background: #fff; border: 1px solid rgba(11,11,11,0.08); border-radius: 14px; padding: 1.05rem 1.15rem;
  box-shadow: 0 1px 2px rgba(11,11,11,0.04); position: relative; overflow: hidden; }}
.stat::before {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--accent); }}
.stat .label {{ font-size: 0.8rem; color: {INK2}; font-weight: 600; }}
.stat .value {{ font-size: 2.0rem; font-weight: 750; color: {INK}; letter-spacing: -0.02em; margin: 0.15rem 0; }}
.stat .note {{ font-size: 0.8rem; color: {MUTED}; line-height: 1.4; }}

/* Cards */
.card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px;
  margin: 0.5rem 0 1.2rem; }}
.card {{ background: #fff; border: 1px solid rgba(11,11,11,0.08); border-radius: 14px; padding: 1.1rem 1.2rem; }}
.card h4 {{ margin: 0 0 0.35rem; font-size: 1.0rem; font-weight: 700; color: {INK}; padding: 0; }}
.card .kicker {{ font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--accent, {BLUE}); margin-bottom: 0.25rem; }}
.card p, .card li {{ font-size: 0.9rem; line-height: 1.55; color: #33322e; margin: 0.15rem 0; }}
.card ul {{ padding-left: 1.1rem; margin: 0.2rem 0 0; }}

/* Callouts */
.callout {{ border-radius: 12px; padding: 0.85rem 1.05rem; margin: 0.6rem 0 1rem; font-size: 0.92rem;
  line-height: 1.55; border: 1px solid; }}
.callout b {{ font-weight: 650; }}
.callout.note {{ background: #eef5fd; border-color: #cde2fb; color: #123a6b; }}
.callout.caution {{ background: #fff6e8; border-color: #f6dcae; color: #5c3b00; }}
.callout.critical {{ background: #fdeeee; border-color: #f4c9c9; color: #6b1717; }}
.callout.good {{ background: #ecf8f1; border-color: #c4ead4; color: #0f4d2c; }}

/* Status pills and gate grid */
.pill {{ display: inline-block; border-radius: 999px; padding: 0.12rem 0.6rem; font-size: 0.72rem; font-weight: 700;
  letter-spacing: 0.02em; color: #fff; white-space: nowrap; }}
.gate-row {{ display: grid; grid-template-columns: 54px 1fr auto; gap: 12px; align-items: start; background: #fff;
  border: 1px solid rgba(11,11,11,0.08); border-radius: 12px; padding: 0.7rem 0.9rem; margin-bottom: 8px; }}
.gate-row .gid {{ font-weight: 800; color: {INK2}; font-size: 0.95rem; }}
.gate-row .req {{ font-weight: 650; color: {INK}; font-size: 0.93rem; }}
.gate-row .why {{ font-size: 0.84rem; color: {INK2}; line-height: 1.45; margin-top: 2px; }}

/* Flow steps */
.steps {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; margin: 0.6rem 0 1.2rem; }}
.step {{ background: #fff; border: 1px solid rgba(11,11,11,0.08); border-radius: 12px; padding: 0.8rem 0.9rem; }}
.step .n {{ font-size: 0.72rem; font-weight: 800; color: {BLUE}; letter-spacing: 0.08em; }}
.step .t {{ font-weight: 650; font-size: 0.92rem; margin: 2px 0; color: {INK}; }}
.step .d {{ font-size: 0.82rem; color: {INK2}; line-height: 1.45; }}

/* Streamlit element polish */
[data-testid="stExpander"] details {{ border-radius: 12px; background: #fff; border: 1px solid rgba(11,11,11,0.08); }}
[data-testid="stExpander"] summary p {{ font-weight: 600; font-size: 0.9rem; }}
[data-testid="stPlotlyChart"] {{ background: #fff; border: 1px solid rgba(11,11,11,0.08); border-radius: 14px;
  padding: 0.5rem 0.4rem 0.2rem; }}
[data-testid="stDownloadButton"] button {{ border-radius: 8px; font-size: 0.82rem; }}
div[data-testid="stAlert"] {{ border-radius: 12px; }}
.footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid {GRID}; font-size: 0.8rem; color: {MUTED}; }}
@media (max-width: 640px) {{
  .hero {{ padding: 1.5rem 1.2rem; }}
  .hero h1 {{ font-size: 1.7rem; }}
  .gate-row {{ grid-template-columns: 40px 1fr; }}
}}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def esc(text) -> str:
    return html.escape(str(text))


def hero(eyebrow: str, title: str, lead: str, chips: list[tuple[str, str]]) -> None:
    chip_html = "".join(f'<span class="chip"><span class="dot" style="background:{c}"></span>{esc(t)}</span>'
                        for t, c in chips)
    st.markdown(f'<div class="hero"><div class="eyebrow">{esc(eyebrow)}</div><h1>{esc(title)}</h1>'
                f'<p class="lead">{lead}</p><div class="chips">{chip_html}</div></div>', unsafe_allow_html=True)


def page_head(eyebrow: str, title: str, lead: str | None = None) -> None:
    """Eyebrow label, st.header (kept as a real header for navigation/tests) and a lead paragraph."""
    st.markdown(f'<div class="eyebrow-label">{esc(eyebrow)}</div>', unsafe_allow_html=True)
    st.header(title, anchor=False)
    if lead:
        st.markdown(f'<p class="lead-text">{lead}</p>', unsafe_allow_html=True)


def stats(items: list[tuple[str, str, str, str]]) -> None:
    """items: (label, value, note, accent colour)."""
    body = "".join(f'<div class="stat" style="--accent:{a}"><div class="label">{esc(l)}</div>'
                   f'<div class="value">{esc(v)}</div><div class="note">{n}</div></div>' for l, v, n, a in items)
    st.markdown(f'<div class="stat-grid">{body}</div>', unsafe_allow_html=True)


def cards(items: list[tuple[str, str, str]], accent: str = BLUE) -> None:
    """items: (kicker, title, html body)."""
    body = "".join(f'<div class="card" style="--accent:{accent}"><div class="kicker">{esc(k)}</div>'
                   f'<h4>{esc(t)}</h4>{b}</div>' for k, t, b in items)
    st.markdown(f'<div class="card-grid">{body}</div>', unsafe_allow_html=True)


def steps(items: list[tuple[str, str]]) -> None:
    body = "".join(f'<div class="step"><div class="n">STEP {i}</div><div class="t">{esc(t)}</div>'
                   f'<div class="d">{d}</div></div>' for i, (t, d) in enumerate(items, 1))
    st.markdown(f'<div class="steps">{body}</div>', unsafe_allow_html=True)


def callout(text: str, kind: str = "note") -> None:
    st.markdown(f'<div class="callout {kind}">{text}</div>', unsafe_allow_html=True)


def status_colour(status: str) -> str:
    s = status.upper()
    if s.startswith(("PASS", "EXECUTED")):
        return STATUS["good"]
    if s.startswith(("FAIL", "NOT_ESTABLISHED", "NOT_JUSTIFIED")):
        return STATUS["critical"]
    if s.startswith(("UNRESOLVED", "PENDING")):
        return STATUS["warning"]
    return STATUS["neutral"]


def pill(status: str) -> str:
    return f'<span class="pill" style="background:{status_colour(status)}">{esc(status.replace("_", " "))}</span>'


def gate_rows(rows) -> None:
    body = "".join(f'<div class="gate-row"><div class="gid">{esc(r.gate)}</div><div><div class="req">'
                   f'{esc(r.requirement)}</div><div class="why">{esc(r.reason)}</div></div>'
                   f'<div>{pill(r.status)}</div></div>' for r in rows.itertuples())
    st.markdown(body, unsafe_allow_html=True)


def style(fig: go.Figure, height: int = 400, legend: bool = True, title: str | None = None) -> go.Figure:
    fig.update_layout(
        height=height, template="simple_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=13, color=INK2), margin=dict(l=8, r=16, t=56 if title else 30, b=52),
        hoverlabel=dict(font=dict(family=FONT, size=12), bgcolor="#fff", bordercolor=GRID),
        title=dict(text=title, x=0.01, xanchor="left", font=dict(size=15, color=INK)) if title else None,
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, title_text="", font=dict(size=12),
                    bgcolor="rgba(0,0,0,0)"))
    axis = dict(showgrid=True, gridcolor=GRID, gridwidth=1, zeroline=False, linecolor=AXIS, ticks="",
                tickfont=dict(size=12, color=INK2), title_font=dict(size=12.5, color=INK2))
    fig.update_xaxes(**axis)
    fig.update_yaxes(**axis)
    return fig


def plot(fig: go.Figure, key: str | None = None) -> None:
    st.plotly_chart(fig, width="stretch", theme=None, key=key,
                    config={"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"],
                            "toImageButtonOptions": {"format": "png", "scale": 2}})


def footer(text: str) -> None:
    st.markdown(f'<div class="footer">{text}</div>', unsafe_allow_html=True)
