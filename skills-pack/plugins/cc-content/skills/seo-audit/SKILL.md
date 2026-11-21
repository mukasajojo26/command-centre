---
name: seo-audit
description: Audit a web page or site for technical and on-page SEO, plus visibility in AI answer engines (AEO/GEO), and produce a prioritised fix list. Includes a script that checks title, meta, canonical, robots, headings, alt text, Open Graph, JSON-LD schema, hreflang, robots.txt and sitemap. Use when the user asks for an SEO audit, why a page is not ranking, schema markup, meta tags, keyword or content optimisation, or how to appear in ChatGPT, Perplexity or Google AI Overviews.
---

# SEO Audit

> Paths: `$SKILL_DIR` means the folder that contains this SKILL.md (Claude Code shows it as the skill base directory). Set it first, e.g. `SKILL_DIR=~/.claude/skills/<skill-name>`.

## Inputs
- URL(s) or local HTML file(s). Ask for the target keyword(s) and country/language if not given (default for UAE: English and Arabic, google.ae).

## Step 1: Automated on-page check

```bash
python3 "$SKILL_DIR/scripts/seo_audit.py" https://example.com/page
python3 "$SKILL_DIR/scripts/seo_audit.py" ./index.html --json
```

If the environment cannot reach the URL, ask the user to save the page (Ctrl+S, "HTML only") and audit the file, or paste the `<head>`.

## Step 2: Manual checks the script cannot do

Technical
- Core Web Vitals: LCP < 2.5 s, INP < 200 ms, CLS < 0.1. Ask for PageSpeed Insights or Search Console data. Do not estimate.
- Indexing: Search Console > Pages report. Look for "Crawled, currently not indexed" and "Duplicate without canonical".
- JavaScript rendering: is the main content in the initial HTML? If it only appears after JS, flag it.
- Internal linking: is the page reachable within 3 clicks from home? Does it have descriptive anchor text pointing to it?

Content (E-E-A-T)
- Does the page answer the search intent in the first 100 words?
- Named author with credentials, date updated, sources cited.
- Original data, photos, or examples that competitors lack.
- One topic per page. Check keyword cannibalisation across the site.

AI answer engines (AEO / GEO)
- Clear question-style H2s with a 40 to 60 word direct answer under each.
- FAQ, HowTo, Organization, Article or LocalBusiness schema where it fits.
- Factual, citable statements with numbers and named sources.
- `llms.txt` at the site root is optional; low cost, unproven benefit. Say so.
- Check robots.txt does not block AI crawlers the user wants (GPTBot, PerplexityBot, Google-Extended, ClaudeBot) or allows ones they want blocked.

Local (if a physical business)
- Google Business Profile complete, NAP (name, address, phone) identical across site and directories, LocalBusiness schema with geo coordinates.

## Step 3: Report

```
SEO Audit: <page>   Date: <date>   Script score: <n>/100

Top 5 fixes (by impact / effort)
| # | Issue | Impact | Effort | Fix |
...

Full findings
- Technical: ...
- On-page: ...
- Content: ...
- AI visibility: ...

Not checked (needs access): Core Web Vitals field data, Search Console, backlinks
```

Impact: High = blocks indexing or ranking, Medium = reduces CTR or relevance, Low = polish.

## Snippets

Title pattern: `<Primary keyword> | <Differentiator> | <Brand>` within 60 characters.

Organization schema:
```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Example Security LLC",
 "url":"https://example.com","logo":"https://example.com/logo.png",
 "address":{"@type":"PostalAddress","addressLocality":"Abu Dhabi","addressCountry":"AE"}}
</script>
```

## Guardrails
- Never promise rankings or traffic numbers.
- Never recommend hidden text, link schemes, or doorway pages.
- Report what was measured versus what was inferred.
