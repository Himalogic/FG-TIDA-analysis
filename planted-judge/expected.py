#!/usr/bin/env python3
"""Exact expected values for the planted-judge demonstration, specification 1.0.

Computes, before any run, every number the specification commits to: each
judge's expected deviations per round, the flag threshold, the chance each
judge is flagged at 1, 5 and 25 rounds, and the six published seeds.

Nothing here is simulated. Probabilities are exact rational arithmetic over
the error model and majority rule in sections 5 to 7 of the specification.

Usage:
    python3 expected.py path/to/tida6-fx-0.2.zip [--json out.json]

The archive is pinned by SHA-256. The script reads the answer key from the
archive only to confirm it matches the cases this specification was written
against; the calculation itself depends only on the specification.

Python 3.11 or later, standard library only.
MIT License, Copyright (c) 2026 Himalogic Software Pvt. Ltd.
Fixture: TIDA6-FX-0.2, CTGT, 2026, CC BY 4.0 (FG-TIDA/themes#6).
"""

import argparse
import hashlib
import json
import sys
import zipfile
from collections import Counter
from fractions import Fraction
from itertools import product

# ---------------------------------------------------------------------------
# Specification 1.0 parameters. Changing any of these is a new specification.
# ---------------------------------------------------------------------------

SPEC_VERSION = "planted-judge-spec-1.0"
ARCHIVE_SHA256 = "10d721acc44228edaa769719d1ff6eac90fdab2576317a7621cc05eaced33d13"
FIXTURE_ROOT = "tida6-fx-0.2/"

# Section 3: the five states of #6 task 3.
VOCABULARY = ("permit", "remediate", "escalate", "block", "indeterminate")

# Section 4: scored cases and their expected verdicts under REF-FSCOMMS 1.0.
# UC17-08 (attested absence) is excluded. UC17-09 is scored on its content
# verdict, remediate; its record is rejected, which judges do not see.
SCORED = {
    "UC17-01": "permit",
    "UC17-02": "permit",
    "UC17-03": "remediate",
    "UC17-04": "remediate",
    "UC17-05": "block",
    "UC17-06": "escalate",
    "UC17-07": "indeterminate",
    "UC17-09": "remediate",
}
# How each scored case appears in the fixture's slice-uc17/expected.json.
FIXTURE_STATE = dict(SCORED, **{"UC17-09": "remediate carried, record rejected"})
EXCLUDED = {"UC17-08": "attested absence"}

# Section 5: the shared blind spot and the planted judge's changes.
BLIND_SPOT = {"UC17-02": "remediate"}
PLANTED = {
    "subtle": {"UC17-05": "remediate"},
    "gross": {
        "UC17-03": "permit",
        "UC17-04": "permit",
        "UC17-05": "permit",
        "UC17-06": "permit",
        "UC17-09": "permit",
    },
}

# Section 6: honest error rate, per case, per judge, per round.
ERROR_RATE = Fraction(1, 10)

# Section 7: a majority is at least this many of the other five judges.
MAJORITY_MIN = 3

# Section 8: round counts.
ROUNDS = (1, 5, 25)

JUDGES = ("H1", "H2", "H3", "H4", "D", "P")
ROLES = {"H1": "honest", "H2": "honest", "H3": "honest", "H4": "honest",
         "D": "justified dissenter", "P": "planted"}


# ---------------------------------------------------------------------------
# Fixture checks
# ---------------------------------------------------------------------------

def check_fixture(path):
    """Confirm the archive digest, its manifest, and the answer key."""
    with open(path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    if digest != ARCHIVE_SHA256:
        sys.exit(f"Archive SHA-256 is {digest}, expected {ARCHIVE_SHA256}. Refusing to run.")

    with zipfile.ZipFile(path) as zf:
        manifest = zf.read(FIXTURE_ROOT + "MANIFEST.sha256").decode("utf-8")
        for line in manifest.splitlines():
            if not line.strip():
                continue
            want, name = line.split(None, 1)
            name = name.strip().removeprefix("./")
            got = hashlib.sha256(zf.read(FIXTURE_ROOT + name)).hexdigest()
            if got != want:
                sys.exit(f"MANIFEST mismatch on {name}.")
        key = json.loads(zf.read(FIXTURE_ROOT + "slice-uc17/expected.json"))

    found = {c["case"]: c["expected_state"] for c in key["cases"]}
    for case, state in {**FIXTURE_STATE, **EXCLUDED}.items():
        if found.get(case) != state:
            sys.exit(f"Answer key differs from the specification on {case}: "
                     f"{found.get(case)!r}, expected {state!r}.")
    return digest


# ---------------------------------------------------------------------------
# Exact calculation
# ---------------------------------------------------------------------------

def verdict_distribution(expected, fixed=None):
    """Distribution of one judge's verdict on one case (section 6)."""
    if fixed is not None:
        return {fixed: Fraction(1)}
    others = [v for v in VOCABULARY if v != expected]
    dist = {expected: 1 - ERROR_RATE}
    for v in others:
        dist[v] = ERROR_RATE / len(others)
    return dist


def case_distributions(case, variant):
    expected = SCORED[case]
    dists = {}
    for j in JUDGES:
        if ROLES[j] == "honest":
            dists[j] = verdict_distribution(expected, BLIND_SPOT.get(case))
        elif j == "D":
            dists[j] = verdict_distribution(expected)
        else:
            dists[j] = verdict_distribution(expected, PLANTED[variant].get(case))
    return dists


def deviation_probabilities(case, variant):
    """Exact chance that each judge deviates from the majority on one case."""
    dists = case_distributions(case, variant)
    p_dev = {j: Fraction(0) for j in JUDGES}
    for outcome in product(*(dists[j].items() for j in JUDGES)):
        p = Fraction(1)
        for _, q in outcome:
            p *= q
        verdicts = [v for v, _ in outcome]
        for i, j in enumerate(JUDGES):
            others = verdicts[:i] + verdicts[i + 1:]
            label, count = Counter(others).most_common(1)[0]
            if count >= MAJORITY_MIN and verdicts[i] != label:
                p_dev[j] += p
    return p_dev


def count_distribution(probs):
    """Exact distribution of a sum of independent Bernoulli trials."""
    dist = [Fraction(1)]
    for p in probs:
        nxt = [Fraction(0)] * (len(dist) + 1)
        for k, x in enumerate(dist):
            nxt[k] += x * (1 - p)
            nxt[k + 1] += x * p
        dist = nxt
    return dist


def seed_for(variant, rounds):
    text = f"{SPEC_VERSION}|{ARCHIVE_SHA256}|{variant}|rounds={rounds}"
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def compute():
    per_case = {v: {c: deviation_probabilities(c, v) for c in SCORED} for v in PLANTED}
    expected = {v: {j: sum(per_case[v][c][j] for c in SCORED) for j in JUDGES}
                for v in PLANTED}

    # Section 7: halfway between the dissenter and the subtle planted judge.
    threshold = (expected["subtle"]["D"] + expected["subtle"]["P"]) / 2

    flag_prob = {}
    for v in PLANTED:
        for r in ROUNDS:
            cut = threshold * r
            for j in JUDGES:
                dist = count_distribution([per_case[v][c][j] for c in SCORED] * r)
                flag_prob[(v, r, j)] = sum(x for k, x in enumerate(dist) if k > cut)

    return per_case, expected, threshold, flag_prob


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def pct(x):
    """Format an exact probability without rounding a nonzero value to 0 or 1."""
    if x == 0:
        return "0%"
    if x == 1:
        return "100%"
    if x < Fraction(1, 10000):
        return "<0.01%"
    if x > Fraction(9999, 10000):
        return ">99.99%"
    return f"{float(x) * 100:.2f}%"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("archive", help="path to tida6-fx-0.2.zip")
    ap.add_argument("--json", help="also write all values to this file")
    args = ap.parse_args()

    digest = check_fixture(args.archive)
    per_case, expected, threshold, flag_prob = compute()

    print(f"{SPEC_VERSION}, fixture TIDA6-FX-0.2 sha256 {digest}")
    print("Archive digest, manifest and answer key match the specification.\n")

    print("Expected deviations per round")
    print(f"{'judge':<22}{'subtle variant':>16}{'gross variant':>16}")
    for j in ("H1", "D", "P"):
        name = {"H1": "each honest judge", "D": "justified dissenter", "P": "planted judge"}[j]
        print(f"{name:<22}{float(expected['subtle'][j]):>16.4f}{float(expected['gross'][j]):>16.4f}")

    print(f"\nThreshold: flag if mean deviations per round > {float(threshold):.4f}")
    print(f"  exact value {threshold}\n")

    print("Chance of being flagged")
    print(f"{'variant':<9}{'rounds':>7}{'honest (each)':>15}{'any honest*':>12}{'dissenter':>11}{'planted':>10}")
    for v in PLANTED:
        for r in ROUNDS:
            h = flag_prob[(v, r, "H1")]
            # Approximate: treats the four honest judges' flags as independent.
            # Their errors are independent, but their flags share a majority.
            any_h = 1 - (1 - h) ** 4
            print(f"{v:<9}{r:>7}{pct(h):>15}{pct(any_h):>12}"
                  f"{pct(flag_prob[(v, r, 'D')]):>11}{pct(flag_prob[(v, r, 'P')]):>10}")

    print("* approximate, treating the four honest judges' flags as independent")
    print("\nPer-case chance of deviating in one round, subtle variant")
    print(f"{'case':<10}{'honest':>9}{'dissenter':>11}{'planted':>9}")
    for c in SCORED:
        pc = per_case["subtle"][c]
        print(f"{c:<10}{float(pc['H1']):>9.4f}{float(pc['D']):>11.4f}{float(pc['P']):>9.4f}")

    print("\nSeeds")
    for v in PLANTED:
        for r in ROUNDS:
            print(f"{v:<9}{r:>4}  {seed_for(v, r)}")

    if args.json:
        out = {
            "spec_version": SPEC_VERSION,
            "archive_sha256": digest,
            "threshold_per_round": str(threshold),
            "threshold_per_round_float": float(threshold),
            "expected_deviations_per_round": {
                v: {j: float(expected[v][j]) for j in JUDGES} for v in PLANTED},
            "flag_probability": {
                f"{v}|{r}|{j}": float(flag_prob[(v, r, j)])
                for v in PLANTED for r in ROUNDS for j in JUDGES},
            "seeds": {f"{v}|{r}": seed_for(v, r) for v in PLANTED for r in ROUNDS},
        }
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2, sort_keys=True)
        print(f"\nWrote {args.json}")


if __name__ == "__main__":
    main()
