#!/usr/bin/env python3
"""Builds the GitHub Pages site in docs/ from the standard.

The standard is the single source (P9: one fact, one place). This script
turns it into docs/index.html, docs/sitemap.xml and docs/robots.txt.
Run it from the repository root after changing the standard:

    python3 scripts/build-site.py

Requires pandoc.
"""
import datetime
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STANDARD = ROOT / "plugins/doc-first-engineering/skills/doc-first-engineering/references/standard.md"
OUT = ROOT / "docs"
SITE_URL = "https://oliesta.github.io/doc-first-engineering/"
REPO_URL = "https://github.com/Oliesta/doc-first-engineering"
AUTHOR = "Olwethu Nguza"
AUTHOR_ROLE = "Technical Lead (ex-FAANG)"
PUBLISHED = "2026-10-21"
DESCRIPTION = (
    "The Doc-First Engineering Standard: when LLMs write the code, documentation "
    "becomes the source of truth. Principles, roles, ADRs, runbooks, traceability "
    "and templates, plus a Claude skill that applies them. By Olwethu Nguza."
)

src = STANDARD.read_text(encoding="utf-8")

version = re.search(r"\*\*Version ([\d.]+)\*\*", src).group(1)
issued = re.search(r"\*\*Version [\d.]+\*\* · \*\*([^*]+)\*\*", src).group(1)
tagline = re.search(r"^\*([^*].*)\*$", src, re.M).group(1)
pdf_name = f"Doc_First_Engineering_Standard_v{version}.pdf"

# Body: everything after the title block, minus the hand-written Contents
# list (the page builds its own from the headings).
body_md = src.split("\n---\n", 1)[1]
body_md = re.sub(r"## Contents\n.*?\n---\n", "", body_md, count=1, flags=re.S)

body = subprocess.run(
    ["pandoc", "-f", "gfm", "-t", "html5", "--no-highlight", "--wrap=none"],
    input=body_md, capture_output=True, text=True, check=True,
).stdout

body = body.replace("<hr />", "")
body = re.sub(r"<table>", '<div class="table-wrap"><table>', body)
body = body.replace("</table>", "</table></div>")
body = re.sub(
    r"<blockquote>\s*<p><strong>We cannot see the future, but we can prepare for it\.</strong></p>\s*</blockquote>",
    '<blockquote class="motto"><p>We cannot see the future,<br>but we can prepare for it.</p></blockquote>',
    body,
)
body = body.replace("<blockquote>\n<p><strong>Limit.", '<blockquote class="warn">\n<p><strong>Limit.')
body = body.replace("what to run. <strong>Proactive", "what to run.<br><strong>Proactive")
body = body.replace(" <em>In practice:</em>", "<br><em>In practice:</em>")

# Section kickers and table of contents from the h2 headings.
toc = []


def h2(m):
    hid, text = m.group(1), m.group(2)
    sec = re.match(r"(Section (\d+)|Appendix (\w)): (.*)", text)
    if sec:
        kicker = f"Section {sec.group(2)}" if sec.group(2) else f"Appendix {sec.group(3)}"
        title = sec.group(4)
        toc.append((hid, kicker.replace("Section ", "").replace("Appendix ", ""), title))
        return f'<h2 id="{hid}"><span class="kicker">{kicker}</span>{title}</h2>'
    toc.append((hid, "", text))
    return m.group(0)


body = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', h2, body)

toc_html = "\n".join(
    f'<li><a href="#{hid}"><span class="num">{num}</span>{title}</a></li>' for hid, num, title in toc
)

today = datetime.date.today().isoformat()
jsonld = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "Doc-First Engineering Standard",
    "alternativeHeadline": tagline,
    "description": DESCRIPTION,
    "version": version,
    "datePublished": PUBLISHED,
    "dateModified": today,
    "inLanguage": "en",
    "url": SITE_URL,
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "author": {
        "@type": "Person",
        "name": AUTHOR,
        "jobTitle": "Technical Lead",
        "url": "https://github.com/Oliesta",
    },
    "isBasedOn": REPO_URL,
    "keywords": "doc-first engineering, documentation as source of truth, LLM software development, "
    "AI-assisted development, architecture decision records, ADR, runbooks, docs as code, "
    "spec-driven development, Claude skill, Claude Code plugin",
}

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Doc-First Engineering Standard | {AUTHOR}</title>
<meta name="description" content="{html.escape(DESCRIPTION)}">
<meta name="author" content="{AUTHOR}">
<link rel="canonical" href="{SITE_URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Doc-First Engineering Standard">
<meta property="og:description" content="{html.escape(DESCRIPTION)}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:site_name" content="Doc-First Engineering">
<meta property="article:author" content="{AUTHOR}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Doc-First Engineering Standard">
<meta name="twitter:description" content="{html.escape(DESCRIPTION)}">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%232F5BEA'/%3E%3Crect x='7' y='8' width='18' height='3' rx='1.5' fill='white'/%3E%3Crect x='7' y='14.5' width='14' height='3' rx='1.5' fill='white' opacity='.8'/%3E%3Crect x='7' y='21' width='10' height='3' rx='1.5' fill='white' opacity='.6'/%3E%3C/svg%3E">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<style>
:root {{
  --bg: #ffffff; --bg-soft: #f5f7fb; --ink: #1b1f2a; --muted: #5b6475; --line: #dde2ec;
  --accent: #2f5bea; --accent-soft: #eef2fd; --code-bg: #f4f5f8; --warn-bg: #fff6e5; --warn-line: #e8a33d;
  --hero: #1b1f2a; --hero-ink: #ffffff; --hero-muted: #c9d0de;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #12151c; --bg-soft: #181c25; --ink: #e6e9f0; --muted: #9aa3b5; --line: #2a303d;
    --accent: #7b9bff; --accent-soft: #1c2440; --code-bg: #1a1e28; --warn-bg: #2a2214; --warn-line: #c8872a;
    --hero: #0c0f15; --hero-ink: #ffffff; --hero-muted: #aab3c5;
  }}
}}
* {{ box-sizing: border-box; }}
html {{ scroll-padding-top: 16px; }}
@media (prefers-reduced-motion: no-preference) {{ html {{ scroll-behavior: smooth; }} }}
body {{ margin: 0; background: var(--bg); color: var(--ink);
  font: 17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }}
a {{ color: var(--accent); }}
code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}

.hero {{ background: var(--hero); color: var(--hero-ink); border-top: 6px solid #2f5bea; }}
.hero-inner {{ max-width: 1120px; margin: 0 auto; padding: 56px 20px 48px; display: grid; grid-template-columns: minmax(0, 1fr); gap: 32px; }}
@media (min-width: 880px) {{ .hero-inner {{ grid-template-columns: 1.4fr 1fr; align-items: end; padding: 80px 32px 64px; }} }}
.eyebrow {{ font-size: 13px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: #8fa8ff; margin: 0 0 12px; }}
.hero h1 {{ font-size: clamp(36px, 6vw, 56px); line-height: 1.05; margin: 0 0 16px; letter-spacing: -.02em; }}
.hero .tag {{ font-size: 19px; color: var(--hero-muted); margin: 0 0 24px; max-width: 34em; }}
.byline {{ margin: 0 0 28px; }}
.byline strong {{ display: block; font-size: 17px; }}
.byline span {{ color: var(--hero-muted); font-size: 15px; }}
.actions {{ display: flex; flex-wrap: wrap; gap: 10px; }}
.btn {{ display: inline-block; padding: 10px 16px; border-radius: 8px; font-weight: 600; font-size: 15px;
  text-decoration: none; border: 1px solid #3a4256; color: #fff; }}
.btn.primary {{ background: #2f5bea; border-color: #2f5bea; }}
.btn:hover {{ filter: brightness(1.12); }}
.ladder {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }}
.ladder li {{ background: #2a3142; color: #fff; font-size: 13px; padding: 6px 12px; border-radius: 5px; }}
.ladder li:first-child {{ background: #2f5bea; font-weight: 700; }}
.ladder li:nth-child(2) {{ font-weight: 700; }}
.ladder li:nth-child(1) {{ width: 100%; }} .ladder li:nth-child(2) {{ width: 90%; }}
.ladder li:nth-child(3) {{ width: 80%; }} .ladder li:nth-child(4) {{ width: 70%; }}
.ladder li:nth-child(5) {{ width: 60%; }} .ladder li:nth-child(6) {{ width: 50%; }}
.ladder-cap {{ font-size: 13px; color: var(--hero-muted); margin: 10px 0 0; }}

.glance {{ background: var(--bg-soft); border-bottom: 1px solid var(--line); }}
.glance-inner {{ max-width: 1120px; margin: 0 auto; padding: 32px 20px; display: grid; grid-template-columns: minmax(0, 1fr); gap: 20px; }}
@media (min-width: 880px) {{ .glance-inner {{ grid-template-columns: repeat(3, 1fr); padding: 40px 32px; }} }}
.glance h2 {{ font-size: 13px; text-transform: uppercase; letter-spacing: .06em; color: var(--accent); margin: 0 0 6px; }}
.glance p {{ margin: 0; font-size: 16px; }}
.glance-inner > div {{ min-width: 0; }}
.install pre {{ margin: 8px 0 0; font-size: 12.5px; line-height: 1.5; background: var(--bg); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; white-space: pre-wrap; overflow-wrap: anywhere; }}

.layout {{ max-width: 1120px; margin: 0 auto; padding: 0 20px 80px; }}
@media (min-width: 1000px) {{ .layout {{ display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 56px; padding: 0 32px 96px; }} }}
nav.toc {{ padding: 24px 0 8px; }}
@media (min-width: 1000px) {{ nav.toc {{ position: sticky; top: 0; align-self: start; max-height: 100vh; overflow-y: auto; padding: 40px 0; }} }}
nav.toc details > summary {{ cursor: pointer; font-weight: 700; font-size: 14px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); list-style: none; }}
nav.toc details > summary::-webkit-details-marker {{ display: none; }}
nav.toc ol {{ list-style: none; margin: 12px 0 0; padding: 0; }}
nav.toc a {{ display: flex; gap: 10px; padding: 5px 0; font-size: 14.5px; line-height: 1.35; color: var(--ink); text-decoration: none; }}
nav.toc a:hover {{ color: var(--accent); }}
nav.toc .num {{ flex: 0 0 22px; color: var(--accent); font-weight: 700; font-variant-numeric: tabular-nums; }}

main {{ min-width: 0; max-width: 46rem; padding-top: 8px; }}
main h2 {{ font-size: clamp(26px, 3.4vw, 32px); line-height: 1.2; margin: 72px 0 16px; letter-spacing: -.01em; }}
main h2 .kicker {{ display: block; font-size: 13px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--accent); margin-bottom: 6px; }}
main h3 {{ font-size: 20px; margin: 36px 0 10px; }}
main h2:first-child {{ margin-top: 40px; }}
main p, main li {{ max-width: 42rem; }}
main ul, main ol {{ padding-left: 1.3em; }}
main li {{ margin: 4px 0; }}
main code {{ background: var(--code-bg); padding: 1px 5px; border-radius: 4px; font-size: .88em; overflow-wrap: anywhere; }}
main pre {{ background: var(--code-bg); border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px; overflow-x: auto; font-size: 13.5px; line-height: 1.5; }}
main pre code {{ background: none; padding: 0; font-size: inherit; overflow-wrap: normal; }}
.table-wrap {{ overflow-x: auto; margin: 16px 0 24px; border: 1px solid var(--line); border-radius: 8px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 15px; line-height: 1.45; }}
th, td {{ text-align: left; vertical-align: top; padding: 10px 12px; border-bottom: 1px solid var(--line); }}
th {{ background: var(--accent-soft); font-weight: 700; white-space: nowrap; }}
tr:last-child td {{ border-bottom: 0; }}
td:first-child {{ font-weight: 600; }}
blockquote {{ margin: 20px 0; padding: 14px 18px; background: var(--accent-soft); border-left: 4px solid var(--accent); border-radius: 0 8px 8px 0; }}
blockquote p {{ margin: 0; }}
blockquote p + p {{ margin-top: 8px; }}
blockquote.warn {{ background: var(--warn-bg); border-left-color: var(--warn-line); }}
blockquote.motto {{ background: var(--hero); border-left-color: #2f5bea; color: #fff; padding: 22px 24px; }}
blockquote.motto p {{ font-size: 24px; font-weight: 700; line-height: 1.3; }}

footer {{ border-top: 1px solid var(--line); background: var(--bg-soft); }}
.footer-inner {{ max-width: 1120px; margin: 0 auto; padding: 28px 20px; font-size: 14.5px; color: var(--muted); display: grid; gap: 6px; }}
@media (min-width: 1000px) {{ .footer-inner {{ padding: 32px; }} }}
.footer-inner p {{ margin: 0; }}
</style>
</head>
<body>

<header class="hero">
  <div class="hero-inner">
    <div>
      <p class="eyebrow">Standard · Version {version} · {issued}</p>
      <h1>Doc-First Engineering</h1>
      <p class="tag">Documentation is the source of truth. LLMs write the code. Humans own the decisions.</p>
      <p class="byline"><strong>{AUTHOR}</strong><span>{AUTHOR_ROLE}</span></p>
      <div class="actions">
        <a class="btn primary" href="#section-01-purpose-and-scope">Read the standard</a>
        <a class="btn" href="#install">Install the Claude skill</a>
        <a class="btn" href="{pdf_name}">PDF</a>
        <a class="btn" href="{REPO_URL}">GitHub</a>
      </div>
    </div>
    <div>
      <ol class="ladder" aria-label="The abstraction ladder, from highest to lowest">
        <li>Human</li><li>Documentation</li><li>LLM</li><li>Programming language</li><li>Assembly</li><li>Binary</li>
      </ol>
      <p class="ladder-cap">Every layer below the LLM is deterministic. The LLM is not, so the durable human work moves up into documentation.</p>
    </div>
  </div>
</header>

<section class="glance" aria-label="At a glance">
  <div class="glance-inner">
    <div>
      <h2>The thesis</h2>
      <p>Code becomes a derived artifact. Documentation becomes the source. Engineers define intent, record decisions and judge results.</p>
    </div>
    <div>
      <h2>The motto</h2>
      <p>We cannot see the future, but we can prepare for it. Runbooks are written before the incident, and the LLM turns them into exact commands during it.</p>
    </div>
    <div class="install" id="install">
      <h2>Install the skill</h2>
      <p>In Claude Code:</p>
<pre><code>/plugin marketplace add Oliesta/doc-first-engineering
/plugin install doc-first-engineering@doc-first-engineering</code></pre>
      <p style="margin-top:8px;font-size:14.5px">Claude app: upload <a href="{REPO_URL}/raw/main/dist/doc-first-engineering.zip">the skill zip</a> in your skills settings.</p>
    </div>
  </div>
</section>

<div class="layout">
  <nav class="toc" aria-label="Contents">
    <details open>
      <summary>Contents</summary>
      <ol>
{toc_html}
      </ol>
    </details>
  </nav>
  <main>
{body}
  </main>
</div>

<footer>
  <div class="footer-inner">
    <p>Doc-First Engineering Standard, Version {version}, by {AUTHOR}, {AUTHOR_ROLE}.</p>
    <p>The standard is licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. The Claude skill is <a href="{REPO_URL}/blob/main/LICENSE">MIT</a>. Source on <a href="{REPO_URL}">GitHub</a>.</p>
  </div>
</footer>

<script>
  // Collapse the contents list on small screens so the standard is one tap away.
  if (window.matchMedia("(max-width: 999px)").matches) {{
    var d = document.querySelector("nav.toc details"); if (d) d.removeAttribute("open");
  }}
</script>
</body>
</html>
"""

OUT.mkdir(exist_ok=True)
(OUT / "index.html").write_text(page, encoding="utf-8")
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"  <url><loc>{SITE_URL}</loc><lastmod>{today}</lastmod></url>\n"
    f"  <url><loc>{SITE_URL}{pdf_name}</loc><lastmod>{today}</lastmod></url>\n"
    "</urlset>\n",
    encoding="utf-8",
)
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
print(f"Built docs/index.html for Version {version} ({len(toc)} sections)")
