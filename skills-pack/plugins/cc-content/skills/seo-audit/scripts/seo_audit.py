#!/usr/bin/env python3
"""On-page SEO audit for one URL or local HTML file.

Usage:
  seo_audit.py https://example.com/page [--json]
  seo_audit.py ./index.html [--json]
Checks title, meta description, canonical, robots, viewport, lang, headings,
image alt text, links, Open Graph, Twitter card, JSON-LD schema, hreflang,
page weight, and (for URLs) HTTP status, HTTPS, robots.txt and sitemap.xml.
Standard library only. Read-only: one GET per URL, plus robots.txt and sitemap.
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; seo-audit-skill/1.0)"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self._in_title = "", False
        self.meta, self.links, self.imgs, self.anchors = [], [], [], []
        self.headings, self._h, self.html_lang = [], None, None
        self.jsonld, self._in_ld, self._ld = [], False, ""
        self.text_len = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.meta.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "a":
            self.anchors.append(a)
        elif re.fullmatch(r"h[1-6]", tag):
            self._h = [tag, ""]
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_ld, self._ld = True, ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif self._h and tag == self._h[0]:
            self.headings.append((self._h[0], self._h[1].strip()))
            self._h = None
        elif tag == "script" and self._in_ld:
            self._in_ld = False
            try:
                self.jsonld.append(json.loads(self._ld))
            except ValueError:
                self.jsonld.append({"_error": "invalid JSON-LD"})

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._h:
            self._h[1] += data
        if self._in_ld:
            self._ld += data
        self.text_len += len(data.strip())


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.geturl(), dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, url, dict(e.headers or {}), b""
    except Exception as e:  # noqa: BLE001
        return None, url, {}, str(e).encode()


def meta_val(p, key, attr="name"):
    for m in p.meta:
        if m.get(attr, "").lower() == key:
            return m.get("content", "")
    return None


def audit(target):
    res = {"target": target, "checks": []}

    def add(sev, check, detail):
        res["checks"].append({"severity": sev, "check": check, "detail": detail})

    is_url = target.startswith(("http://", "https://"))
    if is_url:
        status, final, headers, body = fetch(target)
        res["status"], res["final_url"] = status, final
        if status is None:
            add("ERROR", "fetch", body[:200].decode(errors="ignore"))
            res["score"] = 0
            return res
        if status != 200:
            add("ERROR", "HTTP status", str(status))
            if not body:
                res["score"] = 0
                return res
        if not final.startswith("https://"):
            add("ERROR", "HTTPS", "page not served over HTTPS")
        xr = headers.get("X-Robots-Tag", "")
        if "noindex" in xr.lower():
            add("ERROR", "X-Robots-Tag", xr)
        base = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(final))
        rs, _, _, rb = fetch(base + "/robots.txt")
        if rs == 200:
            rtxt = rb.decode(errors="ignore")
            add("OK", "robots.txt", "found" + ("; declares Sitemap" if "sitemap:" in rtxt.lower() else "; no Sitemap line"))
            if re.search(r"(?im)^user-agent:\s*\*\s*$[\s\S]*?^disallow:\s*/\s*$", rtxt):
                add("WARN", "robots.txt", "contains 'Disallow: /' for all agents; check it is intended")
        else:
            add("WARN", "robots.txt", f"not found ({rs})")
        ss, _, _, _ = fetch(base + "/sitemap.xml")
        add("OK" if ss == 200 else "WARN", "sitemap.xml", "found" if ss == 200 else f"not at /sitemap.xml ({ss})")
    else:
        with open(target, "rb") as f:
            body = f.read()
    html = body.decode("utf-8", errors="ignore")
    p = Page()
    p.feed(html)
    kb = len(body) / 1024
    add("WARN" if kb > 500 else "OK", "HTML size", f"{kb:.0f} KB" + (" (large: inline assets? split or compress)" if kb > 500 else ""))

    t = re.sub(r"\s+", " ", p.title).strip()
    if not t:
        add("ERROR", "title", "missing")
    else:
        add("WARN" if not 30 <= len(t) <= 60 else "OK", "title", f"{len(t)} chars: {t!r} (target 30-60)")
    d = meta_val(p, "description")
    if not d:
        add("ERROR", "meta description", "missing")
    else:
        add("WARN" if not 70 <= len(d) <= 160 else "OK", "meta description", f"{len(d)} chars (target 70-160)")
    robots = meta_val(p, "robots") or ""
    if "noindex" in robots.lower():
        add("ERROR", "meta robots", f"noindex set: {robots}")
    canon = [l.get("href") for l in p.links if "canonical" in l.get("rel", "").lower()]
    add("OK" if len(canon) == 1 else ("WARN" if not canon else "ERROR"), "canonical",
        canon[0] if len(canon) == 1 else ("missing" if not canon else f"{len(canon)} canonical tags"))
    add("OK" if meta_val(p, "viewport") else "ERROR", "viewport", meta_val(p, "viewport") or "missing (mobile-unfriendly)")
    add("OK" if p.html_lang else "WARN", "html lang", p.html_lang or "missing lang attribute")

    h1 = [h for h in p.headings if h[0] == "h1"]
    add("OK" if len(h1) == 1 else ("ERROR" if not h1 else "WARN"), "H1",
        f"{len(h1)} found" + (f": {h1[0][1][:80]!r}" if h1 else ""))
    levels = [int(h[0][1]) for h in p.headings]
    skips = [f"h{a}->h{b}" for a, b in zip(levels, levels[1:]) if b > a + 1]
    if skips:
        add("WARN", "heading order", "skipped levels: " + ", ".join(sorted(set(skips))))

    no_alt = [i.get("src", "")[:60] for i in p.imgs if "alt" not in i]
    add("WARN" if no_alt else "OK", "image alt", f"{len(no_alt)}/{len(p.imgs)} images missing alt" + (f", e.g. {no_alt[:3]}" if no_alt else ""))
    lazy = sum(1 for i in p.imgs if i.get("loading") == "lazy")
    if len(p.imgs) > 3 and lazy == 0:
        add("WARN", "image loading", "no images use loading=lazy")

    hrefs = [a.get("href", "") for a in p.anchors]
    empty = sum(1 for a in p.anchors if not a.get("href") or a.get("href") in ("#", "javascript:void(0)"))
    nofollow = sum(1 for a in p.anchors if "nofollow" in a.get("rel", ""))
    add("OK", "links", f"{len(hrefs)} anchors, {empty} empty/placeholder, {nofollow} nofollow")

    og = {k: meta_val(p, k, "property") for k in ("og:title", "og:description", "og:image", "og:url")}
    miss = [k for k, v in og.items() if not v]
    add("WARN" if miss else "OK", "Open Graph", "missing: " + ", ".join(miss) if miss else "complete")
    add("OK" if meta_val(p, "twitter:card") else "WARN", "Twitter card", meta_val(p, "twitter:card") or "missing")

    types = []
    for j in p.jsonld:
        for node in (j if isinstance(j, list) else j.get("@graph", [j]) if isinstance(j, dict) else []):
            if isinstance(node, dict):
                types.append(node.get("@type", node.get("_error", "?")))
    add("OK" if types and "invalid JSON-LD" not in types else "WARN", "structured data",
        ", ".join(map(str, types)) if types else "no JSON-LD found")
    hl = [l.get("hreflang") for l in p.links if l.get("hreflang")]
    if hl:
        add("OK" if "x-default" in hl else "WARN", "hreflang", ", ".join(hl) + ("" if "x-default" in hl else " (no x-default)"))
    if p.text_len < 1500:
        add("WARN", "content length", f"~{p.text_len} visible chars; thin content risk")

    sev = [c["severity"] for c in res["checks"]]
    res["score"] = max(0, 100 - 15 * sev.count("ERROR") - 5 * sev.count("WARN"))
    return res


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    r = audit(args[0])
    if "--json" in sys.argv:
        print(json.dumps(r, indent=2))
        return 0
    print(f"SEO audit: {r['target']}")
    if "status" in r:
        print(f"HTTP {r['status']} -> {r.get('final_url')}")
    for sev in ("ERROR", "WARN", "OK"):
        for c in r["checks"]:
            if c["severity"] == sev:
                print(f"[{sev:5}] {c['check']}: {c['detail']}")
    print(f"\nScore: {r.get('score', 0)}/100 (ERROR -15, WARN -5)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
