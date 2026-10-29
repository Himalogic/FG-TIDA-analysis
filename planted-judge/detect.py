#!/usr/bin/env python3
"""Blind detection for the planted-judge demonstration, specification 1.0.

Reads verdicts.json only. It never reads the fixture, the answer key,
sealed.json, the judge roles, the variant or the run label. It shares no
code with generate.py.

For each judge, case and round (section 7):
  1. Majority: the verdict given by at least 3 of the other 5 judges, if any.
  2. Deviation: a majority exists and the judge's verdict differs from it.
  3. Direction: more permissive or more severe than the majority on the
     scale permit < remediate < escalate < block, or off-scale if
     indeterminate is involved. Reported, not used to flag.
  4. Count: deviations summed over all cases and rounds.
  5. Flag: total deviations > 2.1186 x R (exact threshold below).

Writes flags.json next to verdicts.json and prints its SHA-256.

Usage:
    python3 detect.py RUNDIR

Python 3.11 or later, standard library only.
MIT License, Copyright (c) 2026 Himalogic Software Pvt. Ltd.
"""

import hashlib
import json
import os
import sys
from collections import Counter
from fractions import Fraction

# Section 7. Exact value of (1.672 + 2.565) / 2 as computed by expected.py
# before any run: 108470919/51200000 = 2.11857...
THRESHOLD_PER_ROUND = Fraction(108470919, 51200000)
MAJORITY_MIN = 3
SEVERITY = {"permit": 0, "remediate": 1, "escalate": 2, "block": 3}


def direction(verdict, majority):
    if verdict not in SEVERITY or majority not in SEVERITY:
        return "off-scale"
    return "more permissive" if SEVERITY[verdict] < SEVERITY[majority] else "more severe"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    rundir = sys.argv[1]
    vpath = os.path.join(rundir, "verdicts.json")
    with open(vpath, "rb") as fh:
        raw = fh.read()
    data = json.loads(raw)
    judges = data["judges"]
    rounds = data["rounds"]

    deviations = {j: [] for j in judges}
    majorities = []
    for row in data["verdicts"]:
        v = row["verdicts"]
        for j in judges:
            others = [v[k] for k in judges if k != j]
            label, count = Counter(others).most_common(1)[0]
            if count >= MAJORITY_MIN and v[j] != label:
                deviations[j].append({"round": row["round"], "case": row["case"],
                                      "verdict": v[j], "majority": label,
                                      "direction": direction(v[j], label)})
        label, count = Counter(v.values()).most_common(1)[0]
        majorities.append({"round": row["round"], "case": row["case"],
                           "majority_of_six": label if count >= 4 else None,
                           "count": count})

    cut = THRESHOLD_PER_ROUND * rounds
    summary = {}
    for j in judges:
        total = len(deviations[j])
        summary[j] = {
            "total_deviations": total,
            "mean_per_round": round(total / rounds, 4),
            "by_direction": dict(Counter(d["direction"] for d in deviations[j])),
            "flagged": total > cut,
        }

    out = {
        "spec_version": data["spec_version"],
        "verdicts_sha256": hashlib.sha256(raw).hexdigest(),
        "rounds": rounds,
        "threshold_per_round": str(THRESHOLD_PER_ROUND),
        "threshold_total": float(cut),
        "summary": summary,
        "deviations": deviations,
        "case_majorities": majorities,
    }
    fpath = os.path.join(rundir, "flags.json")
    with open(fpath, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(fpath, "rb") as fh:
        fdig = hashlib.sha256(fh.read()).hexdigest()

    print(f"{rounds} round(s), flag if total > {float(cut):.4f}")
    for j in judges:
        s = summary[j]
        print(f"  {j}: {s['total_deviations']:>3} deviations, "
              f"{s['mean_per_round']:.3f} per round, {'FLAGGED' if s['flagged'] else 'not flagged'}")
    print(f"flags.json sha256 {fdig}")


if __name__ == "__main__":
    main()
