#!/usr/bin/env python3
"""i18ngap - compare i18n JSON locale files: missing keys, extra keys, placeholder mismatches, untranslated values.
Usage: python3 i18ngap.py locales/en.json locales/es.json [--csv out.csv]
First file is the reference. Exit code 1 if problems found (CI friendly)."""
import json, re, sys, csv

PH = re.compile(r"\{\{?\s*\w+\s*\}?\}|%\d*\$?[sd]|\$\{\w+\}|:\w+")

def flat(d, p=""):
    out = {}
    for k, v in d.items():
        key = f"{p}.{k}" if p else str(k)
        if isinstance(v, dict):
            out.update(flat(v, key))
        else:
            out[key] = str(v)
    return out

def ph(s):
    return sorted(m.replace(" ", "") for m in PH.findall(s))

def compare(ref, tgt):
    rows = []
    for k, v in ref.items():
        if k not in tgt:
            rows.append((k, "missing", v, ""))
        else:
            if ph(v) != ph(tgt[k]):
                rows.append((k, "placeholder_mismatch", v, tgt[k]))
            elif tgt[k].strip() == v.strip() and len(v) > 3 and re.search(r"[A-Za-z]{3}", v):
                rows.append((k, "same_as_reference", v, tgt[k]))
            elif not tgt[k].strip():
                rows.append((k, "empty", v, tgt[k]))
    for k in tgt:
        if k not in ref:
            rows.append((k, "extra", "", tgt[k]))
    return rows

def main(a):
    csvp = None
    if "--csv" in a:
        i = a.index("--csv"); csvp = a[i+1]; del a[i:i+2]
    if len(a) < 2:
        print(__doc__); return 2
    ref = flat(json.load(open(a[0], encoding="utf-8")))
    allrows = []
    for f in a[1:]:
        rows = compare(ref, flat(json.load(open(f, encoding="utf-8"))))
        print(f"== {f}: {len(rows)} issue(s)")
        for k, t, r, v in rows:
            print(f"  [{t}] {k}")
            allrows.append((f, k, t, r, v))
    if csvp:
        with open(csvp, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh); w.writerow(["file", "key", "issue", "reference", "current"]); w.writerows(allrows)
    return 1 if allrows else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
