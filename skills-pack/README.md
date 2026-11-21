# Skills Pack: 16 skills researched, rebuilt and ready to install

Research date: 21 Nov 2026. This pack covers the 16 skills and plugins in the "16 Claude Skills & Plugins to Install" infographic.

The pack has two parts:

1. **Original skills (this repo).** I rewrote all 16 from scratch, modelled on what each community skill does, and tailored them to security, safety and operations work. Every one passes validation. Six include working scripts, and those scripts were tested.
2. **Upstream install guide.** For each original project: the verified repo, the official install command, requirements, and a security note. Install the upstream version when you want the author's full feature set.

I did not copy third-party code. Several upstream projects are large (dozens of skills, Python environments, browser automation), and copying them would mean shipping code I had not audited under someone else's licence.

---

## 1. Install this pack

### Option A: Claude Code plugin marketplace (recommended)

```
/plugin marketplace add mukasajojo26/command-centre
/plugin install cc-dev@command-centre
/plugin install cc-content@command-centre
/plugin install cc-knowledge@command-centre
/plugin install cc-business@command-centre
```

Install only the plugins you need. Each one loads only its own skills.

| Plugin | Skills |
|---|---|
| `cc-dev` | frontend-design, coding-conventions, dev-discipline, eng-team-roles, second-opinion-review, skill-factory |
| `cc-content` | humanizer, seo-audit, marketing-copy, social-media, html-to-video |
| `cc-knowledge` | second-brain, source-grounded-qa, terse-mode |
| `cc-business` | finance-analysis, legal-review |

If the repo is private, the marketplace add needs GitHub access from your machine (`gh auth login` or SSH keys).

### Option B: Copy into your skills folder (Claude Code)

```bash
git clone https://github.com/mukasajojo26/command-centre.git
bash command-centre/skills-pack/scripts/install-local.sh            # ~/.claude/skills
bash command-centre/skills-pack/scripts/install-local.sh --project  # ./.claude/skills
```

If a skill with the same name already exists, the script backs it up first.

### Option C: Claude.ai (web, desktop, mobile)

1. Download the ZIPs from `skills-pack/dist/` (one per skill).
2. Claude.ai > Settings > Capabilities > Skills > Upload skill. Upload each ZIP.
3. Turn on Code execution in the same settings page. The script-based skills need it.

Rebuild the ZIPs after you edit a skill: `bash skills-pack/scripts/build-zips.sh`.

---

## 2. What was built and tested

| # | Infographic item | Built here as | Plugin | Script | Tested |
|---|---|---|---|---|---|
| 01 | frontend-design | `frontend-design` | cc-dev | none | validated |
| 02 | hyperframes | `html-to-video` | cc-content | `render.mjs` (Playwright + ffmpeg) | rendered 4 s 1920x1080 MP4, checked frames |
| 03 | ai-second-brain | `second-brain` | cc-knowledge | none | validated |
| 04 | notebooklm-skill | `source-grounded-qa` | cc-knowledge | none (uses pdftotext) | validated |
| 05 | humanizer | `humanizer` | cc-content | `ai_lint.py` | flagged 11 patterns in a sample, 0 in clean text |
| 06 | claude-seo | `seo-audit` | cc-content | `seo_audit.py` | audited this repo's `index.html` (75/100), handles fetch failure |
| 07 | antfu-skills | `coding-conventions` | cc-dev | none | validated |
| 08 | caveman | `terse-mode` | cc-knowledge | none | validated |
| 09 | gstack | `eng-team-roles` | cc-dev | none | validated |
| 10 | superpowers | `dev-discipline` | cc-dev | none | validated |
| 11 | codex-plugin-cc | `second-opinion-review` | cc-dev | `check-reviewers.sh` | ran, detects codex and git |
| 12 | financial-services | `finance-analysis` | cc-business | `fincalc.py` (DCF, NPV/IRR, payback, variance, ratios) | NPV and payback checked by hand |
| 13 | claude-for-legal | `legal-review` | cc-business | none | validated |
| 14 | claude-skills | `skill-factory` | cc-dev | `validate_skill.py` (validate + zip) | validated all 16, built all ZIPs |
| 15 | marketingskills | `marketing-copy` | cc-content | none | validated |
| 16 | social-media-skills | `social-media` | cc-content | none | validated |

Checks run: `claude plugin validate` passed for the marketplace and all 4 plugins. A marketplace install (`cc-content@command-centre`) and the local installer were tested in a clean home directory.

Skill names avoid "claude" and "anthropic", which are reserved words for skill names. That is why `claude-seo` became `seo-audit`, and so on.

---

## 3. Research: the 16 upstream projects

The infographic has several errors, and some of them would make the install command fail:
- **#07** reads `antru/skills`. The real repo is **`antfu/skills`** (Anthony Fu).
- **#12** reads `anthoopics/skills`. Anthropic's finance plugins live at **`anthropics/financial-services`**.
- **#13** reads `anthropics/skills`. The legal plugins live at **`anthropics/claude-for-legal`**.
- **#16** reads `rampstackco/claude-skills`. That repo is a general web-lifecycle library of about 103 skills, and I found no social media pack in it. The closest real social media collection is `charlie947/social-media-skills`.
- **#03** names "ai-second-brain", but the repo `coleam00/second-brain-starter` is a PRD generator. A separate repo, `coleam00/second-brain-skills`, holds the skills collection.

Risk ratings are mine. They reflect what the upstream code can do on your machine. They do not grade code quality.

| # | Project | Verified repo | What it does | Official install (Claude Code) | Needs | Risk |
|---|---|---|---|---|---|---|
| 01 | frontend-design | `anthropics/claude-plugins-official` | Anthropic's skill for distinctive UI design | `/plugin install frontend-design@claude-plugins-official` | none | Low (instructions only, first-party) |
| 02 | HyperFrames | `heygen-com/hyperframes` (Apache 2.0) | HTML-to-video framework with agent skills and a CLI | `npx skills add heygen-com/hyperframes`, or the plugin marketplace route in its README | Node, Chromium, ffmpeg, Git LFS | Medium (runs a CLI and npm packages) |
| 03 | Second brain starter | `coleam00/second-brain-starter` | Generates a phased PRD for building a personal AI second brain | Copy `.claude/skills/create-second-brain-prd/` into your project | none | Low to Medium (Tessl rates it "Advisory": review first) |
| 04 | NotebookLM skill | `PleasePrompto/notebooklm-skill` (MIT) | Queries Google NotebookLM through browser automation | `git clone https://github.com/PleasePrompto/notebooklm-skill ~/.claude/skills/notebooklm` | Python, Chrome, Google login. Local Claude Code only | **High** (stores a Google session cookie, automates a browser) |
| 05 | Humanizer | `blader/humanizer` (MIT) | Removes AI-writing patterns, based on Wikipedia's "Signs of AI writing" guide | `/plugin marketplace add blader/humanizer`, or clone into `~/.claude/skills/humanizer` | none | Low (instructions only) |
| 06 | Claude SEO | `AgriciDaniel/claude-seo` | About 30 SEO sub-skills, with Python tools | `/plugin marketplace add AgriciDaniel/claude-seo` then `/plugin install claude-seo@agricidaniel-claude-seo` then `/seo setup` | Python 3.x venv | Medium (installs Python packages; read `install.sh` and skip the curl one-liner) |
| 07 | antfu skills | `antfu/skills` | Anthony Fu's JS/TS, Vue and Vite conventions | `npx skills add antfu/skills --skill='*'` | Node | Low |
| 08 | Caveman | `JuliusBrussee/caveman` | Terse output mode, file compression, token statistics | `claude plugin marketplace add JuliusBrussee/caveman && claude plugin install caveman@caveman` | none | Low to Medium (adds hooks that read session logs) |
| 09 | gstack | `garrytan/gstack` | Garry Tan's role-based skills (office hours, review, QA, ship) plus a browser binary | `git clone` into `~/.claude/skills/gstack`, then `./setup` | Bun, Git. Builds a native binary | Medium to High (compiles and runs a browser automation binary) |
| 10 | Superpowers | `obra/superpowers` | Brainstorm, plan, TDD, debugging and verification workflows | `/plugin install superpowers@claude-plugins-official`, or `/plugin marketplace add obra/superpowers-marketplace` | none | Low to Medium (includes hooks) |
| 11 | Codex plugin | `openai/codex-plugin-cc` | Runs OpenAI Codex reviews from inside Claude Code | `/plugin marketplace add openai/codex-plugin-cc`, `/plugin install codex@openai-codex`, `/codex:setup` | Node 18.18+, Codex CLI, ChatGPT account or OpenAI API key | Medium (sends your code to OpenAI) |
| 12 | Financial services | `anthropics/financial-services` | DCF, comps, LBO, equity research and banking plugins | `/plugin marketplace add anthropics/financial-services`, then install the core financial-analysis plugin first | Paid Claude plan. Data connectors are optional | Low (first-party). Connectors need vendor accounts |
| 13 | Claude for Legal | `anthropics/claude-for-legal` | 13 practice-area plugins, each with a playbook interview | `/plugin marketplace add anthropics/claude-for-legal`, then for example `/plugin install commercial-legal@claude-for-legal` | none | Low (first-party). Outputs still need a lawyer |
| 14 | Claude skills library | `alirezarezvani/claude-skills` | A large library (170+ skills) across engineering, product, marketing and compliance | `/plugin marketplace add alirezarezvani/claude-skills`, then install the bundles you need | varies by skill | Medium (large surface: install bundles selectively) |
| 15 | Marketing skills | `coreyhaines31/marketingskills` (MIT) | CRO, copywriting, SEO, email and launch skills built on a product context file | `/plugin marketplace add coreyhaines31/marketingskills`, `/plugin install marketing-skills@marketingskills` | none | Low (instructions only) |
| 16 | Social media skills | `rampstackco/claude-skills` as labelled, which is really a web-lifecycle library | See the note above | `npx skills add rampstackco/claude-skills` | none | Low |

### Before you install any upstream skill

Skills and plugins run with your user permissions. Treat them like any other third-party code:

1. Read every script, hook (`hooks/hooks.json`) and install script before you run it. Never pipe `curl | bash` without reading it.
2. Search the code for network calls, credential paths (`~/.ssh`, `~/.aws`, `.env`) and `eval` or `exec`.
3. Pin to a commit you reviewed. Third-party marketplaces have auto-update off by default, so keep it off.
4. Use a dedicated Google or OpenAI account for anything that stores session cookies or sends code outside your machine (#04, #11).
5. On a work laptop, check with IT first. Several of these projects install browsers, binaries or Python environments.

---

## 4. Which to use first (for a security and safety lead)

| Priority | Skill | Why |
|---|---|---|
| 1 | `source-grounded-qa` | Answers questions about ADOSH-SF, FLS Code, SOPs and ISO standards with page citations, and says so when a document does not cover the question |
| 2 | `humanizer` | Reports, emails and LinkedIn posts in your own style. The lint script enforces your writing rules |
| 3 | `legal-review` | Security contractor and vendor contracts, with checks for insurance, licensing, PDPL and liability |
| 4 | `finance-analysis` | Business cases for CCTV, access control and manpower changes, with computed NPV, IRR and payback |
| 5 | `second-brain` | Daily notes, decision log and weekly review across several properties |
| 6 | `social-media` | LinkedIn authority content, with a confidentiality guardrail for security details |

The dev skills (`cc-dev`) matter most if you keep building tools like Command Centre.

---

## Sources

- frontend-design: [skills.sh listing](https://skills.sh/anthropics/claude-plugins-official/frontend-design), [ClaudeLog FAQ](https://claudelog.com/faqs/what-is-frontend-design-skill-in-claude-code/)
- HyperFrames: [GitHub](https://github.com/heygen-com/hyperframes), [skills.sh](https://skills.sh/heygen-com/hyperframes)
- Second brain starter: [README](https://raw.githubusercontent.com/coleam00/second-brain-starter/main/README.md), [Tessl](https://tessl.io/registry/skills/github/coleam00/second-brain-starter)
- NotebookLM skill: [README](https://raw.githubusercontent.com/PleasePrompto/notebooklm-skill/HEAD/README.md)
- Humanizer: [GitHub](https://github.com/blader/humanizer), [README](https://raw.githubusercontent.com/blader/humanizer/main/README.md)
- Claude SEO: [README](https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/README.md)
- antfu skills: [GitHub](https://github.com/antfu/skills), [Vercel skills CLI](https://vercel.com/blog/introducing-skills)
- Caveman: [README](https://raw.githubusercontent.com/juliusbrussee/caveman/HEAD/README.md), [DEV review](https://dev.to/andrew-ooo/caveman-review-the-claude-code-skill-that-cuts-65-of-tokens-2boe)
- gstack: [GitHub](https://github.com/garrytan/gstack)
- Superpowers: [install docs](https://www.mintlify.com/obra/superpowers/installation/claude-code), [guide](https://www.developersdigest.tech/blog/claude-code-superpowers-plugin-guide)
- Codex plugin: [README](https://raw.githubusercontent.com/openai/codex-plugin-cc/HEAD/README.md), [OpenAI community post](https://community.openai.com/t/introducing-codex-plugin-for-claude-code/1378186)
- Financial services: [Claude Help Center](https://support.claude.com/en/articles/13851150-install-financial-services-plugins), [Claude docs](https://claude.com/docs/office-agents/fsi-plugins)
- Claude for Legal: [Tessl](https://tessl.io/registry/skills/github/anthropics/claude-for-legal), [Claude marketplace](https://claude.com/marketplace/plugins/legal-builder-hub)
- alirezarezvani/claude-skills: [Getting started](https://alirezarezvani.github.io/claude-skills/getting-started/), [Wiki](https://github.com/alirezarezvani/claude-skills/wiki/Installing-Skills)
- Marketing skills: [README](https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/README.md)
- RampStack: [README](https://raw.githubusercontent.com/rampstackco/claude-skills/main/README.md), [skills.sh](https://www.skills.sh/rampstackco/claude-skills)

Install commands and skill counts come from the official READMEs where available, and from directory listings otherwise. Projects change often, so confirm the command against the repo README on the day you install.
