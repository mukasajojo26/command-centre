---
name: finance-analysis
description: Financial analysis with auditable calculations - budget vs actual variance commentary, departmental budgets, business cases (NPV, IRR, payback), DCF valuation with sensitivity tables, comparable company analysis, and financial ratio review. Includes a calculator script so numbers are computed, not estimated. Use when the user asks for a business case, ROI, budget variance explanation, valuation, DCF, NPV/IRR, cost-benefit of a security or safety investment, or to review financial statements.
---

# Finance Analysis

> Paths: `$SKILL_DIR` means the folder that contains this SKILL.md (Claude Code shows it as the skill base directory). Set it first, e.g. `SKILL_DIR=~/.claude/skills/<skill-name>`.

Numbers are computed by the script or a spreadsheet formula, never by mental arithmetic. Every output states its inputs and assumptions.

## Calculator

```bash
S="$SKILL_DIR/scripts/fincalc.py"
python3 $S npv --rate 0.08 --flows -250000 90000 90000 90000 90000 --irr
python3 $S payback --flows -250000 90000 90000 90000 90000
python3 $S dcf --fcf 100 110 121 --wacc 0.10 --g 0.03 --net-debt 50 --shares 10
python3 $S variance --csv budget_vs_actual.csv --threshold 0.10 --abs 5000
python3 $S ratios --revenue 1000 --gross 400 --ebitda 200 --net 120 --assets 900 --equity 500
```

No shell available (e.g. Claude.ai without code execution)? Build the model in a spreadsheet with visible formulas instead, and say which cells hold assumptions.

## Workflow 1: Business case (e.g. CCTV upgrade, access control, guard-force automation)

1. **Baseline**: current annual cost and risk (incidents/year x average loss, insurance premium, manpower hours).
2. **Option costs**: CAPEX (hardware, install, integration), OPEX (licences, maintenance, connectivity), one-off (training, downtime).
3. **Benefits**: only quantifiable ones go in the cash flows (manpower hours saved x loaded rate, reduced losses, lower premium). Qualitative benefits listed separately.
4. **Cash flows**: Year 0 = investment (negative), Years 1-5 = net benefit. Use the organisation's hurdle rate; if unknown, state the assumption (e.g. 8%).
5. **Run** NPV, IRR, payback. Then a downside case (benefits -30%) and upside case.
6. **Output**:
   ```
   Recommendation: <invest / do not / phase it>
   NPV @ r: | IRR: | Payback: | Downside NPV:
   Key assumptions (ranked by sensitivity):
   Risks and mitigations:
   Non-financial benefits: (life safety, compliance, guest experience)
   ```
   For life-safety items mandated by law or code (fire systems, first aid under ADOSH-SF), say clearly that compliance is not optional and the case is about the cheapest compliant option, not whether to comply.

## Workflow 2: Budget vs actual variance commentary

1. Get a CSV: `line,budget,actual,type` (`type=expense` for cost lines).
2. Run `variance` with the materiality threshold (default 10% or a fixed amount).
3. For each flagged line write: what happened, why (driver: volume, rate, timing, one-off), whether it recurs, and the action.
   Example: "Security contract +AED 11,000 (9.2%) adverse: 3 additional guards for the National Day event (one-off, approved by GM). No change to run-rate."
4. Never invent a driver. If unknown, write `[Driver needed from <owner>]`.

## Workflow 3: Valuation (DCF and comps)

- DCF: project unlevered FCF 5 years, WACC from CAPM (state risk-free rate, ERP, beta source), terminal growth below long-run nominal GDP. Always show the WACC x g sensitivity table the script prints. Warn if terminal value is over 75% of EV.
- Comps: pick 5-10 peers by sector, size and geography. Use EV/EBITDA, EV/Revenue, P/E. Show median and interquartile range, not the mean. State the data date and source.

## Workflow 4: Ratio review

Run `ratios`. Compare to prior period and peers. Flag: margin compression, current ratio below 1.0, ROE driven by leverage rather than margin.

## Guardrails

- Not investment, tax or audit advice. Say so once in formal deliverables.
- Cite the data source and date for every external number. No invented market data.
- Currency explicit on every figure (AED, USD). State VAT treatment (UAE VAT 5%).
- Upstream: Anthropic's official financial services plugins (`anthropics/financial-services` marketplace) add data connectors and banking-grade workflows (comps, LBO, pitch decks). Prefer them for professional finance work.
