#!/usr/bin/env python3
"""
Inter-judge agreement on the CTGT lineage-eval matched-v2 release.

Reproduces the figures posted on FG-TIDA/themes#21.

Data:    CTGT-Inc/lineage-eval, data/results/blog-v1/matched-v2-full-data.json
         Licensed CC BY 4.0 by CTGT. Not redistributed here; fetched at run time.
Pinned:  SHA-256 654c5fb688bb0d0335f8751cedbd992c4be85bc7b979ccba24612411d001eea9
Script:  MIT. Python 3 standard library only.

Usage:
    python3 judge_agreement.py            # fetch from GitHub
    python3 judge_agreement.py PATH       # use a local copy

The primary analysis set is responses with response_quality_label == "VALID",
matching the published gap statistics. Degenerate responses are reported
separately where it changes a headline figure.

Each response carries one label from each of four judges. Labels are:
    UNCENSORED           a pass
    CENSORED_REFUSAL     an observable failure (the model declined)
    CENSORED_WHITEWASH   a graded failure (a judgment of degree)
"""

import collections
import hashlib
import itertools
import json
import sys
import urllib.request

URL = ("https://raw.githubusercontent.com/CTGT-Inc/lineage-eval/main/"
       "data/results/blog-v1/matched-v2-full-data.json")
PINNED_SHA256 = "654c5fb688bb0d0335f8751cedbd992c4be85bc7b979ccba24612411d001eea9"

LABELS = ["UNCENSORED", "CENSORED_WHITEWASH", "CENSORED_REFUSAL"]
GRADED = "CENSORED_WHITEWASH"
N_JUDGES = 4


# ---------------------------------------------------------------- loading

def load(source):
    if source.startswith("http"):
        with urllib.request.urlopen(source) as r:
            raw = r.read()
    else:
        with open(source, "rb") as f:
            raw = f.read()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PINNED_SHA256:
        print(f"WARNING: data SHA-256 {digest} does not match the pinned "
              f"version. Figures may differ from those posted.\n")
    return json.loads(raw)


def flatten(data):
    """One row per response: judge labels in a fixed judge order."""
    judges = [j["model"] for j in data["judges"]]
    rows = []
    for p in data["prompts"]:
        for r in p["responses"].values():
            by_judge = {x["judge_model"]: x["label"] for x in r["judges"]}
            rows.append({
                "condition": p["condition"],
                "valid": r["response_quality_label"] == "VALID",
                "labels": [by_judge[j] for j in judges],
            })
    return judges, rows


# ---------------------------------------------------------------- statistics

def fleiss_kappa(rows, categories):
    n = N_JUDGES
    N = len(rows)
    per_item = []
    totals = collections.Counter()
    for r in rows:
        c = collections.Counter(r["labels"])
        totals.update(c)
        per_item.append((sum(v * v for v in c.values()) - n) / (n * (n - 1)))
    p_bar = sum(per_item) / N
    p_j = [totals[k] / (N * n) for k in categories]
    p_e = sum(x * x for x in p_j)
    return (p_bar - p_e) / (1 - p_e)


def cohen_kappa(a, b, categories):
    N = len(a)
    p_o = sum(x == y for x, y in zip(a, b)) / N
    ca, cb = collections.Counter(a), collections.Counter(b)
    p_e = sum(ca[k] * cb[k] for k in categories) / (N * N)
    return (p_o - p_e) / (1 - p_e)


def unanimous(rows):
    return sum(len(set(r["labels"])) == 1 for r in rows) / len(rows)


def specific_agreement(rows, category):
    """Multi-rater specific agreement: of all rater pairs in which at least
    one rater used the category, the share in which both did."""
    agree = touched = 0
    for r in rows:
        k = r["labels"].count(category)
        agree += k * (k - 1)
        touched += k * (N_JUDGES - 1)
    return agree / touched if touched else float("nan")


def binary(rows):
    return [dict(r, labels=["FAIL" if l != "UNCENSORED" else "PASS"
                            for l in r["labels"]]) for r in rows]


# ---------------------------------------------------------------- report

def short(name):
    return name.split("/")[-1]


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else URL
    judges, rows = flatten(load(source))
    valid = [r for r in rows if r["valid"]]

    print(f"Responses: {len(rows)}  valid: {len(valid)}  "
          f"degenerate: {len(rows) - len(valid)}")
    print(f"Judges: {', '.join(short(j) for j in judges)}\n")

    print("== Headline ==")
    for name, s in [("all", rows), ("valid", valid)]:
        print(f"  {name:5}  3-class Fleiss {fleiss_kappa(s, LABELS):.3f}  "
              f"unanimous {unanimous(s):.1%}   "
              f"binary Fleiss {fleiss_kappa(binary(s), ['PASS', 'FAIL']):.3f}")

    print("\n== Pairwise Cohen kappa, 3-class, valid ==")
    for i, k in itertools.combinations(range(N_JUDGES), 2):
        a = [r["labels"][i] for r in valid]
        b = [r["labels"][k] for r in valid]
        print(f"  {short(judges[i]):22} x {short(judges[k]):22} "
              f"{cohen_kappa(a, b, LABELS):.3f}")

    print("\n== Per-judge label distribution, valid ==")
    for i, j in enumerate(judges):
        c = collections.Counter(r["labels"][i] for r in valid)
        print(f"  {short(j):22} " + "  ".join(
            f"{l.split('_')[-1]:11}{c[l] / len(valid):6.1%}" for l in LABELS))

    for cond in ["control", "sensitive"]:
        s = [r for r in valid if r["condition"] == cond]
        print(f"\n== Condition: {cond} (valid, n={len(s)}) ==")
        print(f"  3-class Fleiss {fleiss_kappa(s, LABELS):.3f}  "
              f"unanimous {unanimous(s):.1%}")
        for l in LABELS:
            print(f"  specific agreement {l.split('_')[-1]:11} "
                  f"{specific_agreement(s, l):6.1%}")

    target = [r for r in valid if r["condition"] == "sensitive"]
    disagree = [r for r in target if len(set(r["labels"])) > 1]
    print(f"\n== Disagreements, sensitive valid: {len(disagree)} of "
          f"{len(target)} ==")
    patterns = collections.Counter(frozenset(r["labels"]) for r in disagree)
    for pat, n in patterns.most_common():
        print(f"  {n:4}  " + " / ".join(sorted(l.split('_')[-1] for l in pat)))

    lone = collections.Counter()
    for r in disagree:
        c = collections.Counter(r["labels"])
        if sorted(c.values()) == [1, 3]:
            odd = next(l for l, v in c.items() if v == 1)
            lone[judges[r["labels"].index(odd)]] += 1
    print(f"\n  Lone dissenter in {sum(lone.values())} three-to-one splits:")
    for j, n in lone.most_common():
        print(f"    {short(j):22} {n}")

    print(f"\n== Graded-label sets, sensitive valid: do matching rates "
          f"mean matching items? ==")
    sets = [{idx for idx, r in enumerate(target) if r["labels"][k] == GRADED}
            for k in range(N_JUDGES)]
    for k in range(N_JUDGES):
        print(f"  {short(judges[k]):22} flags {len(sets[k]):4} "
              f"({len(sets[k]) / len(target):.1%})")
    for a, b in itertools.combinations(range(N_JUDGES), 2):
        inter, union = len(sets[a] & sets[b]), len(sets[a] | sets[b])
        print(f"  {short(judges[a]):22} x {short(judges[b]):22} "
              f"overlap {inter}/{union} = {inter / union:.1%}")
    every, some = set.intersection(*sets), set.union(*sets)
    print(f"  flagged by all four: {len(every)}  by at least one: {len(some)}"
          f"  ({len(every) / len(some):.1%})")


if __name__ == "__main__":
    main()
