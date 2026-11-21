#!/usr/bin/env python3
"""Flag common AI-writing patterns in a text file (or stdin).

Usage: ai_lint.py FILE   |   cat draft.txt | ai_lint.py -
Prints findings as: line:col  SEVERITY  category  "match"  -> suggestion
Exit code 1 if any HIGH finding. Standard library only.
"""
import re
import sys

HIGH, MED, LOW = "HIGH", "MED", "LOW"

BUZZ = {
    "leverage": "use", "leveraging": "using", "seamless": "smooth (or cut)", "seamlessly": "(cut)",
    "robust": "strong / reliable", "holistic": "full / complete", "empower": "let / help",
    "empowers": "lets / helps", "elevate": "raise / improve", "unlock": "open / enable",
    "unlocking": "enabling", "delve": "look at", "delves": "looks at", "landscape": "field / market",
    "game-changer": "(say the actual effect)", "game changer": "(say the actual effect)",
    "cutting-edge": "new / current", "synergy": "(say what combines)", "streamline": "simplify",
    "paradigm": "model", "transformative": "(say the actual change)", "revolutionize": "change",
    "utilize": "use", "facilitate": "help / run", "tapestry": "(cut)", "testament": "(say what it shows)",
    "pivotal": "key", "underscores": "shows", "multifaceted": "(be specific)", "realm": "area",
    "bustling": "busy", "embark": "start", "foster": "build", "navigate": "handle",
}
PHRASES = [
    (r"\bgreat question\b", HIGH, "stock opener", "delete"),
    (r"\bin today'?s (fast[- ]paced|rapidly evolving|digital)\b", HIGH, "stock opener", "delete"),
    (r"\blet'?s dive in\b", HIGH, "stock opener", "delete"),
    (r"\bhere'?s the thing\b", HIGH, "stock opener", "delete"),
    (r"\bi'?d be happy to help\b", HIGH, "stock opener", "delete"),
    (r"\bin conclusion\b", HIGH, "stock closer", "delete"),
    (r"\bat the end of the day\b", HIGH, "stock closer", "delete"),
    (r"\bi hope this helps\b", MED, "stock closer", "delete or give next step"),
    (r"\bfeel free to (reach out|ask)\b", MED, "stock closer", "delete"),
    (r"\bit'?s (important|worth|crucial) to (note|mention|remember) that\b", HIGH, "signposting", "delete frame"),
    (r"\bwhen it comes to\b", HIGH, "signposting", "rephrase: 'for X' / 'in X'"),
    (r"\bnot (just|only|merely) [^.,;]{1,40}?,? (it'?s|but( also)?)\b", HIGH, "contrast formula", "state the second half"),
    (r"\bplays? an? (vital|crucial|key|pivotal) role\b", MED, "significance inflation", "say what it does"),
    (r"\b(experts|studies|research) (say|show|suggest)s?\b", MED, "vague attribution", "name the source"),
    (r"\b(may|might|could) potentially\b", MED, "stacked hedge", "one hedge max"),
    (r"\bin order to\b", LOW, "wordy", "to"),
    (r"\ba (wide|broad) (range|variety|array) of\b", LOW, "wordy", "many / list them"),
    (r"^\s*(ever wondered|have you ever|what if)\b[^?]*\?", MED, "rhetorical opener", "state the answer"),
]
FILLER = r"\b(very|really|truly|extremely|highly|significantly|incredibly|absolutely|literally|basically|actually)\b"
DASH = r"(—|–| - | -- )"
EMOJI = r"[\U0001F300-\U0001FAFF☀-➿]"
TRIPLE = r"\b(\w+), (\w+),? and (\w+)\b"


def lint(text):
    out = []
    for ln, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(">"):
            continue  # skip quoted material
        low = line.lower()
        for w, sug in BUZZ.items():
            for m in re.finditer(r"\b" + re.escape(w) + r"\b", low):
                out.append((ln, m.start() + 1, HIGH, "buzzword", line[m.start():m.end()], sug))
        for pat, sev, cat, sug in PHRASES:
            for m in re.finditer(pat, low):
                out.append((ln, m.start() + 1, sev, cat, line[m.start():m.end()], sug))
        for m in re.finditer(FILLER, low):
            out.append((ln, m.start() + 1, MED, "filler adverb", line[m.start():m.end()], "delete or use a number"))
        for m in re.finditer(DASH, line):
            out.append((ln, m.start() + 1, HIGH, "dash as pause", m.group(0).strip() or "-", "comma, period, colon or ()"))
        if ";" in line and not line.strip().startswith(("`", "    ")):
            out.append((ln, line.index(";") + 1, LOW, "semicolon", ";", "split into two sentences"))
        for m in re.finditer("[“”‘’]", line):
            out.append((ln, m.start() + 1, LOW, "curly quote", m.group(0), "straight quote"))
        for m in re.finditer(EMOJI, line):
            out.append((ln, m.start() + 1, LOW, "emoji", m.group(0), "remove unless intended"))
        for m in re.finditer(TRIPLE, line):
            out.append((ln, m.start() + 1, LOW, "rule of three?", m.group(0), "keep only what is true"))
    return out


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    src = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    findings = lint(src)
    order = {HIGH: 0, MED: 1, LOW: 2}
    for f in sorted(findings, key=lambda f: (order[f[2]], f[0], f[1])):
        print(f'{f[0]}:{f[1]}\t{f[2]}\t{f[3]}\t"{f[4]}"\t-> {f[5]}')
    counts = {s: sum(1 for f in findings if f[2] == s) for s in (HIGH, MED, LOW)}
    words = len(src.split())
    print(f"\nSummary: {words} words | HIGH {counts[HIGH]} | MED {counts[MED]} | LOW {counts[LOW]}")
    return 1 if counts[HIGH] else 0


if __name__ == "__main__":
    sys.exit(main())
