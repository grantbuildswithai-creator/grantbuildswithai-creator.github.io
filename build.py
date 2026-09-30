"""Build the Grant Builds With AI website.

Reads site.json and the podcast RSS feed, then writes a static site to _site/.
Episodes and cover art come from the feed, so publishing an episode on
Spotify for Creators is all it takes. The next build picks it up.

    python build.py            # fetch the live feed, build _site/
    python build.py --offline  # reuse the cached feed.xml and cover.jpg
"""

import html
import io
import json
import re
import shutil
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

import markdown
from PIL import Image

HERE = Path(__file__).parent
OUT = HERE / "_site"
FEED_CACHE = HERE / "feed.xml"
COVER_CACHE = HERE / "cover.jpg"
GUIDES = HERE / "guides"
TRANSCRIPTS = HERE / "transcripts"
ITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"

esc = html.escape


# ---------- data ----------

def _get(url, headers):
    req = urllib.request.Request(url, headers={"User-Agent": "gbwai-site-builder", **headers})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def _build_date(data):
    m = re.search(rb"<lastBuildDate>(.*?)</lastBuildDate>", data)
    try:
        return parsedate_to_datetime(m.group(1).decode()) if m else None
    except (TypeError, ValueError):
        return None


def fetch(url, cache, offline, bust=False):
    if not offline:
        try:
            if not bust:
                data = _get(url, {})
            else:
                # The feed's CDN edges don't all update at once, and some serve an old
                # copy for a while after publishing. Ask several times, keep the newest.
                copies = []
                for i in range(5):
                    fresh = url + ("&" if "?" in url else "?") + f"nocache={int(time.time())}{i}"
                    copies.append(_get(fresh, {"Cache-Control": "no-cache"}))
                    time.sleep(2)
                data = max(copies, key=lambda d: _build_date(d).timestamp() if _build_date(d) else 0)
                print(f"Feed copies' build dates: {[str(_build_date(d)) for d in copies]}")
            cache.write_bytes(data)
            return data
        except Exception as e:
            print(f"Couldn't fetch {url} ({e}); using cached {cache.name}")
    return cache.read_bytes()


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fmt_duration(d):
    secs = 0
    for p in d.split(":") if d else []:
        secs = secs * 60 + int(p)
    return f"{max(round(secs / 60), 1)} min"


def fmt_date(d, long=False):
    return f"{d.strftime('%B' if long else '%b')} {d.day}, {d.year}"


def parse_feed(xml_bytes):
    channel = ET.fromstring(xml_bytes).find("channel")
    image = channel.find(f"{ITUNES}image")
    episodes = []
    for item in channel.findall("item"):
        title = item.findtext("title", "").strip()
        enclosure = item.find("enclosure")
        number = item.findtext(f"{ITUNES}episode")
        episodes.append({
            "title": title,
            "slug": slugify(title),
            "date": parsedate_to_datetime(item.findtext("pubDate")),
            "notes": item.findtext("description", "").strip(),
            "audio": enclosure.get("url") if enclosure is not None else "",
            "duration": fmt_duration(item.findtext(f"{ITUNES}duration", "")),
            "type": item.findtext(f"{ITUNES}episodeType", "full"),
            "number": int(number) if number else None,
        })
    episodes.sort(key=lambda e: e["date"], reverse=True)
    return image.get("href"), episodes


def ep_label(ep):
    if ep["type"] == "trailer":
        return "Trailer"
    if ep["type"] == "bonus":
        return "Bonus"
    return f"Episode {ep['number']}" if ep["number"] else "Episode"


def clean_notes(notes_html):
    # Spotify for Creators pads notes with empty paragraphs.
    return re.sub(r"<p>\s*(<br\s*/?>)?\s*</p>", "", notes_html).strip()


def summary(notes_html, limit=180):
    text = html.unescape(re.sub(r"<[^>]+>", " ", notes_html))
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "…"


# ---------- templates ----------

WORDMARK = '<span class="neon">GB<span class="cbar">c</span>AI</span>'


def page(site, root, title, body, description=None, active=""):
    full_title = site["title"] if title == site["title"] else f"{title} · {site['title']}"
    desc = esc(description or site["tagline"])
    nav = "".join(
        f'<a href="{root}{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>'
        for key, href, label in [
            ("episodes", "episodes/", "Episodes"),
            ("guides", "guides/", "Guides"),
            ("about", "about/", "About"),
        ]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{root}static/cover-600.jpg">
<link rel="icon" href="{root}static/cover-180.jpg">
<link rel="apple-touch-icon" href="{root}static/cover-180.jpg">
<link rel="alternate" type="application/rss+xml" title="{esc(site['title'])}" href="{esc(site['rss'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}static/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{root}">{WORDMARK}<span class="brand-name">{esc(site['title'])}</span></a>
    <nav>{nav}</nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>{WORDMARK}</p>
    <p>Questions, ideas, or a project you want to hear about? <a href="mailto:{esc(site['email'])}">{esc(site['email'])}</a></p>
    <p class="muted">© {datetime.now().year} Grant Builds With AI</p>
  </div>
</footer>
</body>
</html>
"""


def listen_links(site):
    return "".join(
        f'<a class="pill" href="{esc(l["url"])}" rel="noopener">{esc(l["name"])}</a>'
        for l in site["listen"] if l["url"]
    )


def ep_meta(ep, long=False):
    return (f'<div class="ep-meta"><span class="ep-label">{ep_label(ep)}</span> · '
            f'{fmt_date(ep["date"], long)} · {ep["duration"]}</div>')


def episode_card(ep, root):
    return f"""<li class="ep-card">
  <a href="{root}episodes/{ep['slug']}/">
    {ep_meta(ep)}
    <h3>{esc(ep['title'])}</h3>
    <p>{esc(summary(ep['notes']))}</p>
  </a>
</li>"""


def guide_href(g, root):
    if (GUIDES / f"{g['slug']}.md").exists():
        return f"{root}guides/{g['slug']}/"
    return g.get("url", "")


def guide_card(g, root):
    href = guide_href(g, root)
    if href:
        action = f'<a class="button" href="{esc(href)}">Read the guide</a>'
    else:
        action = '<span class="soon">Coming soon</span>'
    return f"""<li class="guide-card">
  <h3>{esc(g['title'])}</h3>
  <p>{esc(g['summary'])}</p>
  {action}
</li>"""


def render_home(site, episodes):
    latest_html = more_html = ""
    if episodes:
        latest = episodes[0]
        latest_html = f"""<section class="wrap">
  <h2 class="section-title">Latest</h2>
  <article class="latest-card">
    {ep_meta(latest)}
    <h3><a href="episodes/{latest['slug']}/">{esc(latest['title'])}</a></h3>
    <p>{esc(summary(latest['notes'], 320))}</p>
    <audio controls preload="none" src="{esc(latest['audio'])}"></audio>
  </article>
</section>"""
    if len(episodes) > 1:
        more_html = f"""<section class="wrap">
  <h2 class="section-title">More episodes</h2>
  <ul class="ep-list">{"".join(episode_card(e, "") for e in episodes[1:6])}</ul>
  <p><a href="episodes/">All episodes →</a></p>
</section>"""
    body = f"""<section class="hero">
  <div class="wrap hero-inner">
    <img class="hero-cover" src="static/cover-600.jpg" width="600" height="600" alt="Grant Builds With AI cover art: GB c-bar Ai in neon">
    <div>
      <p class="eyebrow">A podcast</p>
      <h1>{esc(site['title'])}</h1>
      <p class="lede">{esc(site['tagline'])}</p>
      <p class="sub">Short episodes, one real project each: what I tried to build, what went wrong, and how it turned out.</p>
      <div class="pills">{listen_links(site)}</div>
    </div>
  </div>
</section>
{latest_html}
{more_html}"""
    return page(site, "", site["title"], body)


def render_episode_index(site, episodes):
    body = f"""<section class="wrap page">
  <h1>Episodes</h1>
  <ul class="ep-list">{"".join(episode_card(e, "../") for e in episodes)}</ul>
</section>"""
    return page(site, "../", "Episodes", body, active="episodes")


def transcript_html(ep):
    # Transcripts are matched by the episode's slug: transcripts/<slug>.md
    path = TRANSCRIPTS / f"{ep['slug']}.md"
    if not path.exists():
        return ""
    return f"""<details class="transcript">
  <summary>Read the transcript</summary>
  <div class="transcript-body">{markdown.markdown(path.read_text(encoding="utf-8"))}</div>
</details>"""


def report_card(r, root):
    return f"""<li class="guide-card">
  <h3>{esc(r['title'])}</h3>
  <p>{esc(r['summary'])}</p>
  <a class="button" href="{root}static/reports/{esc(r['file'])}">Download (Word)</a>
</li>"""


def render_episode(site, ep, guides, reports):
    root = "../../"
    guide_html = ""
    if guides:
        guide_html = f"""<aside class="ep-guides">
  <h2>Build it yourself</h2>
  <ul class="guide-list">{"".join(guide_card(g, root) for g in guides)}</ul>
</aside>"""
    if reports:
        # A report can override the section heading and note; otherwise the site-wide ones apply.
        heading = reports[0].get("heading", "Read the reports")
        note = reports[0].get("note", site.get("reports_note", ""))
        guide_html += f"""<aside class="ep-guides">
  <h2>{esc(heading)}</h2>
  <p>{esc(note)}</p>
  <ul class="guide-list">{"".join(report_card(r, root) for r in reports)}</ul>
</aside>"""
    body = f"""<article class="wrap page episode">
  <p><a href="{root}episodes/">← All episodes</a></p>
  {ep_meta(ep, long=True)}
  <h1>{esc(ep['title'])}</h1>
  <audio controls preload="none" src="{esc(ep['audio'])}"></audio>
  <div class="notes">{clean_notes(ep['notes'])}</div>
  {guide_html}
  {transcript_html(ep)}
  <div class="pills">{listen_links(site)}</div>
</article>"""
    return page(site, root, ep["title"], body, description=summary(ep["notes"]), active="episodes")


def render_guides(site):
    body = f"""<section class="wrap page">
  <h1>Guides</h1>
  <p class="lede">Want to build it yourself? Each guide is a roadmap, not a pile of code. It covers the accounts and setup you'll do by hand, and the parts you can hand to an AI helper.</p>
  <ul class="guide-list">{"".join(guide_card(g, "../") for g in site['guides'])}</ul>
</section>"""
    return page(site, "../", "Guides", body, active="guides")


CHECKLIST_JS = """<script>
(() => {
  const boxes = [...document.querySelectorAll('.guide-body input[type=checkbox]')];
  const key = 'guide-checks:' + location.pathname;
  let saved = [];
  try { saved = JSON.parse(localStorage.getItem(key)) || []; } catch (e) {}
  boxes.forEach((box, i) => {
    box.checked = saved.includes(i);
    box.addEventListener('change', () => {
      const checked = boxes.flatMap((b, j) => b.checked ? [j] : []);
      try { localStorage.setItem(key, JSON.stringify(checked)); } catch (e) {}
    });
  });
})();
</script>"""


def render_guide(site, g, episodes):
    root = "../../"
    md = markdown.Markdown(extensions=["toc", "sane_lists"])
    content = md.convert((GUIDES / f"{g['slug']}.md").read_text(encoding="utf-8"))
    content = re.sub(r"<li>\[ \] (.*?)</li>",
                     r'<li class="task"><label><input type="checkbox"><span>\1</span></label></li>', content)
    toc = "".join(f'<li><a href="#{t["id"]}">{esc(t["name"])}</a></li>' for t in md.toc_tokens)

    related = [e for e in episodes if e["type"] != "bonus" and e["number"] in g.get("episodes", [])]
    related.sort(key=lambda e: e["number"])
    if related:
        story = f'<ul class="ep-list">{"".join(episode_card(e, root) for e in related)}</ul>'
    else:
        nums = " and ".join(str(n) for n in g.get("episodes", []))
        word, them = ("Episodes", "them") if len(g.get("episodes", [])) > 1 else ("Episode", "it")
        story = f"<p>This project is the story of {word} {nums}, coming soon. Follow the show so you don't miss {them}.</p>"

    body = f"""<article class="wrap page guide">
  <p><a href="{root}guides/">← All guides</a></p>
  <p class="eyebrow">Guide</p>
  <h1>{esc(g['title'])}</h1>
  <p class="lede">{esc(g['summary'])}</p>
  <nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>{toc}</ol></nav>
  <div class="guide-body">{content}</div>
  <section class="hear">
    <h2>Hear the story</h2>
    {story}
    <div class="pills">{listen_links(site)}</div>
  </section>
</article>
{CHECKLIST_JS}"""
    return page(site, root, g["title"], body, description=g["summary"], active="guides")


def render_about(site):
    paras = "".join(f"<p>{esc(p)}</p>" for p in site["about"])
    body = f"""<section class="wrap page prose">
  <h1>About the show</h1>
  {paras}
  <h2>Get in touch</h2>
  <p>Got a question, or a project you want to hear me try? Email <a href="mailto:{esc(site['email'])}">{esc(site['email'])}</a>.</p>
  <h2>Listen</h2>
  <div class="pills">{listen_links(site)}</div>
</section>"""
    return page(site, "../", "About", body, active="about")


# ---------- build ----------

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_covers(cover_bytes):
    # Re-encoding also drops any metadata embedded in the original image.
    with Image.open(io.BytesIO(cover_bytes)) as im:
        im = im.convert("RGB")
        for size in (600, 180):
            im.resize((size, size), Image.LANCZOS).save(OUT / "static" / f"cover-{size}.jpg", quality=85)


def main():
    offline = "--offline" in sys.argv
    site = json.loads((HERE / "site.json").read_text(encoding="utf-8"))
    cover_url, episodes = parse_feed(fetch(site["rss"], FEED_CACHE, offline, bust=True))

    # ignore_errors: OneDrive sometimes locks empty folders on Windows.
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.copytree(HERE / "static", OUT / "static", dirs_exist_ok=True)
    write_covers(fetch(cover_url, COVER_CACHE, offline))

    write(OUT / "index.html", render_home(site, episodes))
    write(OUT / "episodes" / "index.html", render_episode_index(site, episodes))
    for ep in episodes:
        guides = [g for g in site["guides"] if ep["type"] != "bonus" and ep["number"] in g.get("episodes", [])]
        reports = [r for r in site.get("reports", []) if ep["type"] != "bonus" and ep["number"] in r.get("episodes", [])]
        write(OUT / "episodes" / ep["slug"] / "index.html", render_episode(site, ep, guides, reports))
    write(OUT / "guides" / "index.html", render_guides(site))
    for g in site["guides"]:
        if (GUIDES / f"{g['slug']}.md").exists():
            write(OUT / "guides" / g["slug"] / "index.html", render_guide(site, g, episodes))
    write(OUT / "about" / "index.html", render_about(site))
    write(OUT / ".nojekyll", "")

    print(f"Built {len(episodes)} episode(s) into {OUT}")


if __name__ == "__main__":
    main()
