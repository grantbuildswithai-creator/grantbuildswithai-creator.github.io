# Grant Builds With AI — website

A static site built from `site.json` plus the podcast RSS feed.

- `site.json`: show text, listen links, guide list. Leave a listen `url` blank to hide it. A guide whose `slug` has a matching `guides/<slug>.md` gets its own page; otherwise it shows "Coming soon". A guide appears on the episode pages listed in its `episodes`.
- `guides/*.md`: guide text in Markdown. `- [ ]` lines become checkboxes that remember ticks in the reader's browser.
- `static/style.css`: the look. Cover art comes from the feed at build time.
- `build.py`: fetches the feed and cover, and writes the site into `_site/`.
- `.github/workflows/deploy.yml`: GitHub rebuilds and publishes the site on every push and every 6 hours, so new episodes appear on their own. If the repo goes 45 days without a commit, its keepalive job makes a small bot commit so GitHub doesn't pause the schedule (it does that after 60 idle days).

Build it with `python build.py` (needs Pillow and Markdown). Preview it with `python -m http.server 8080 --directory _site`.
