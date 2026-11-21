#!/usr/bin/env python3
"""Small, auditable finance calculators. Standard library only.

Commands:
  dcf      --fcf 100 110 121 --wacc 0.10 --g 0.03 [--net-debt 50] [--shares 10]
  npv      --rate 0.08 --flows -1000 300 400 500 [--irr]
  variance --csv budget_vs_actual.csv [--threshold 0.10] [--abs 5000]
           CSV columns: line,budget,actual  (expense lines: add column type=expense)
  payback  --flows -1000 300 400 500
  ratios   --revenue 1000 --gross 400 --ebitda 200 --net 120 --assets 900 --equity 500 --current-assets 300 --current-liab 150
Every command prints its inputs and formula so the result can be checked.
"""
import argparse
import csv
import sys


def npv(rate, flows):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))


def irr(flows, lo=-0.99, hi=10.0):
    f_lo, f_hi = npv(lo, flows), npv(hi, flows)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = npv(mid, flows)
        if abs(f_mid) < 1e-9:
            break
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def cmd_dcf(a):
    if a.wacc <= a.g:
        sys.exit("ERROR: WACC must exceed terminal growth g")
    pv = [cf / (1 + a.wacc) ** (t + 1) for t, cf in enumerate(a.fcf)]
    n = len(a.fcf)
    tv = a.fcf[-1] * (1 + a.g) / (a.wacc - a.g)
    pv_tv = tv / (1 + a.wacc) ** n
    ev = sum(pv) + pv_tv
    print(f"Inputs: FCF={a.fcf} WACC={a.wacc:.2%} g={a.g:.2%} (end-of-year discounting)")
    for t, (cf, p) in enumerate(zip(a.fcf, pv), 1):
        print(f"  Year {t}: FCF {cf:,.2f}  PV {p:,.2f}")
    print(f"Terminal value (Gordon) = FCF_n x (1+g)/(WACC-g) = {tv:,.2f}; PV = {pv_tv:,.2f}")
    print(f"Enterprise value = {ev:,.2f}  (terminal share {pv_tv / ev:.0%})")
    if pv_tv / ev > 0.75:
        print("WARN: terminal value > 75% of EV; result is highly sensitive to g and WACC")
    if a.net_debt is not None:
        eq = ev - a.net_debt
        print(f"Equity value = EV - net debt = {eq:,.2f}")
        if a.shares:
            print(f"Per share = {eq / a.shares:,.4f}")
    print("\nSensitivity (EV): rows WACC, cols g")
    gs = [a.g - 0.01, a.g, a.g + 0.01]
    print("        " + "".join(f"{g:>12.1%}" for g in gs))
    for w in (a.wacc - 0.01, a.wacc, a.wacc + 0.01):
        row = []
        for g in gs:
            if w <= g:
                row.append(f"{'n/a':>12}")
                continue
            v = sum(cf / (1 + w) ** (t + 1) for t, cf in enumerate(a.fcf)) + a.fcf[-1] * (1 + g) / (w - g) / (1 + w) ** n
            row.append(f"{v:>12,.0f}")
        print(f"{w:>7.1%} " + "".join(row))


def cmd_npv(a):
    v = npv(a.rate, a.flows)
    print(f"Inputs: rate={a.rate:.2%} flows={a.flows} (t=0 first, undiscounted)")
    print(f"NPV = sum(CF_t / (1+r)^t) = {v:,.2f}")
    if a.irr:
        r = irr(a.flows)
        print("IRR = " + (f"{r:.2%}" if r is not None else "not found (no sign change)"))


def cmd_payback(a):
    cum = 0.0
    for t, cf in enumerate(a.flows):
        prev = cum
        cum += cf
        if prev < 0 <= cum and t > 0:
            print(f"Payback = {t - 1 + (-prev / cf):.2f} periods")
            return
    print("No payback within the horizon")


def cmd_variance(a):
    rows = list(csv.DictReader(open(a.csv, newline="", encoding="utf-8-sig")))
    print(f"{'Line':<28}{'Budget':>14}{'Actual':>14}{'Var':>14}{'Var%':>8}  Flag")
    tot = {}
    for r in rows:
        b, act = float(r["budget"]), float(r["actual"])
        exp = r.get("type", "").strip().lower() == "expense"
        var = act - b
        pct = var / b if b else float("inf")
        fav = (var <= 0) if exp else (var >= 0)
        flag = ""
        if abs(pct) >= a.threshold or abs(var) >= a.abs:
            flag = "FAV" if fav else "ADVERSE - explain"
        k = "expense" if exp else "revenue/other"
        tb, ta = tot.get(k, (0.0, 0.0))
        tot[k] = (tb + b, ta + act)
        print(f"{r['line'][:27]:<28}{b:>14,.0f}{act:>14,.0f}{var:>14,.0f}{pct:>8.1%}  {flag}")
    for k, (tb, ta) in tot.items():
        print(f"{('TOTAL ' + k)[:27]:<28}{tb:>14,.0f}{ta:>14,.0f}{ta - tb:>14,.0f}{(ta - tb) / tb if tb else 0:>8.1%}")
    print(f"\nFlag rule: |var%| >= {a.threshold:.0%} or |var| >= {a.abs:,.0f}. Expense lines favourable when under budget.")


def cmd_ratios(a):
    def show(name, num, den, fmt="{:.1%}"):
        if num is None or not den:
            return
        print(f"{name:<22}{fmt.format(num / den)}")
    show("Gross margin", a.gross, a.revenue)
    show("EBITDA margin", a.ebitda, a.revenue)
    show("Net margin", a.net, a.revenue)
    show("ROA", a.net, a.assets)
    show("ROE", a.net, a.equity)
    show("Current ratio", a.current_assets, a.current_liab, "{:.2f}x")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("dcf")
    p.add_argument("--fcf", type=float, nargs="+", required=True)
    p.add_argument("--wacc", type=float, required=True)
    p.add_argument("--g", type=float, required=True)
    p.add_argument("--net-debt", type=float)
    p.add_argument("--shares", type=float)
    p = sp.add_parser("npv")
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--flows", type=float, nargs="+", required=True)
    p.add_argument("--irr", action="store_true")
    p = sp.add_parser("payback")
    p.add_argument("--flows", type=float, nargs="+", required=True)
    p = sp.add_parser("variance")
    p.add_argument("--csv", required=True)
    p.add_argument("--threshold", type=float, default=0.10)
    p.add_argument("--abs", type=float, default=float("inf"))
    p = sp.add_parser("ratios")
    for k in ("revenue", "gross", "ebitda", "net", "assets", "equity", "current-assets", "current-liab"):
        p.add_argument(f"--{k}", type=float)
    a = ap.parse_args()
    {"dcf": cmd_dcf, "npv": cmd_npv, "payback": cmd_payback, "variance": cmd_variance, "ratios": cmd_ratios}[a.cmd](a)


if __name__ == "__main__":
    main()
