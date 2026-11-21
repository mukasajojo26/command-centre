#!/usr/bin/env python3
"""Validate Agent Skill folders and optionally package them as ZIPs.

Usage:
  validate_skill.py PATH [PATH ...] [--zip OUTDIR]
PATH can be a skill folder (contains SKILL.md) or any parent folder; all
SKILL.md files below it are checked. Exit code 1 if any ERROR is found.
Standard library only.
"""
import argparse
import os
import re
import sys
import zipfile

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED = ("claude", "anthropic")
LINK_RE = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, "SKILL.md must start with '---' YAML frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "frontmatter is not closed with '---'"
    fm = {}
    key = None
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip().strip('"').strip("'")
        elif key and line.startswith((" ", "\t")):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm, None


def check_skill(skill_dir):
    errors, warns = [], []
    path = os.path.join(skill_dir, "SKILL.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm, err = parse_frontmatter(text)
    if err:
        return [err], warns
    name = fm.get("name", "")
    desc = fm.get("description", "")
    folder = os.path.basename(os.path.normpath(skill_dir))
    if not name:
        errors.append("missing 'name'")
    else:
        if len(name) > 64:
            errors.append(f"name longer than 64 chars ({len(name)})")
        if not NAME_RE.match(name):
            errors.append("name must be lowercase letters, digits and single hyphens")
        if any(r in name for r in RESERVED):
            errors.append("name contains a reserved word (claude/anthropic)")
        if name != folder:
            warns.append(f"name '{name}' differs from folder '{folder}'")
    if not desc:
        errors.append("missing 'description'")
    else:
        if len(desc) > 1024:
            errors.append(f"description longer than 1024 chars ({len(desc)})")
        if re.search(r"<[^>]+>", desc):
            errors.append("description contains XML/HTML tags")
        if len(desc) < 80:
            warns.append("description is short; add when-to-use trigger phrases")
        if not re.search(r"\b(use when|use for|use if|when the user)\b", desc, re.I):
            warns.append("description lacks an explicit 'Use when ...' clause")
    lines = text.count("\n") + 1
    if lines > 500:
        warns.append(f"SKILL.md has {lines} lines; move detail to references/")
    for target in LINK_RE.findall(text):
        target = target.split("#")[0]
        if target and not os.path.exists(os.path.join(skill_dir, target)):
            errors.append(f"broken relative link: {target}")
    sdir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(sdir):
        for fn in os.listdir(sdir):
            fp = os.path.join(sdir, fn)
            if fn.endswith((".sh", ".py", ".js", ".mjs")) and not os.access(fp, os.X_OK):
                warns.append(f"script not executable: scripts/{fn}")
    for root, _, files in os.walk(skill_dir):
        for fn in files:
            if fn in (".env", "id_rsa", "credentials.json") or fn.endswith((".pem", ".key")):
                errors.append(f"possible secret file included: {os.path.relpath(os.path.join(root, fn), skill_dir)}")
    return errors, warns


def find_skills(paths):
    found = []
    for p in paths:
        if os.path.isfile(os.path.join(p, "SKILL.md")):
            found.append(p)
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
            if "SKILL.md" in files:
                found.append(root)
    return sorted(set(found))


def zip_skill(skill_dir, outdir):
    os.makedirs(outdir, exist_ok=True)
    name = os.path.basename(os.path.normpath(skill_dir))
    out = os.path.join(outdir, f"{name}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(skill_dir):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "node_modules", ".venv")]
            for fn in sorted(files):
                if fn.endswith(".pyc") or fn == ".DS_Store":
                    continue
                full = os.path.join(root, fn)
                arc = os.path.join(name, os.path.relpath(full, skill_dir))
                z.write(full, arc)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--zip", metavar="OUTDIR", help="package each valid skill as OUTDIR/<name>.zip")
    a = ap.parse_args()
    skills = find_skills(a.paths)
    if not skills:
        print("No SKILL.md found.")
        return 1
    total_err = 0
    for s in skills:
        errs, warns = check_skill(s)
        status = "FAIL" if errs else ("WARN" if warns else "OK")
        print(f"[{status}] {s}")
        for e in errs:
            print(f"   ERROR: {e}")
        for w in warns:
            print(f"   WARN:  {w}")
        total_err += len(errs)
        if a.zip and not errs:
            print(f"   zipped -> {zip_skill(s, a.zip)}")
    print(f"\n{len(skills)} skill(s) checked, {total_err} error(s).")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
