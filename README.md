# Grant Builds With AI — website

A static site built from `site.json` plus the podcast RSS feed.

- `site.json`: show text, listen links, guides. Leave a `url` blank to hide a listen link or show "Coming soon" on a guide. To attach a guide to episode pages, list the episode numbers in its `episodes`.
- `static/style.css`: the look. Cover art comes from the feed at build time.
- `build.py`: fetches the feed and cover, and writes the site into `_site/`.
- `.github/workflows/deploy.yml`: GitHub rebuilds and publishes the site on every push and every 6 hours, so new episodes appear on their own.

Build it with `python build.py` (needs Pillow). Preview it with `python -m http.server 8080 --directory _site`.
