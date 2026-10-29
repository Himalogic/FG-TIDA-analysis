#!/usr/bin/env python3
"""Unblind one run of the planted-judge demonstration, specification 1.0.

Runs only after detect.py has written flags.json. Checks that flags.json was
computed from this verdicts.json, checks sealed.json against the digest
generate.py printed, then opens sealed.json and the answer key and writes
report.json and report.md: expected versus observed per item, per judge,
with the flags exactly as detect.py recorded them before unblinding.

Usage:
    python3 unblind.py RUNDIR ARCHIVE SEALED_SHA256 EXPECTED_JSON

EXPECTED_JSON is the file written by `expected.py ARCHIVE --json FILE`.

Python 3.11 or later, standard library only.
MIT License, Copyright (c) 2026 Himalogic Software Pvt. Ltd.
Fixture: TIDA6-FX-0.2, CTGT, 2026, CC BY 4.0 (FG-TIDA/themes#6).
"""

import hashlib
import json
import os
import sys
import zipfile
from collections import Counter

ARCHIVE_SHA256 = "10d721acc44228edaa769719d1ff6eac90fdab2576317a7621cc05eaced33d13"
FIXTURE_ROOT = "tida6-fx-0.2/"
CONTENT_VERDICT = {"UC17-09": "remediate"}
ROLE_ORDER = {"honest": 0, "justified dissenter": 1, "planted": 2}
# Section 5, used only to check AC-7 after unblinding.
PLANTED = {
    "subtle": {"UC17-05": "remediate"},
    "gross": {"UC17-03": "permit", "UC17-04": "permit", "UC17-05": "permit",
              "UC17-06": "permit", "UC17-09": "permit"},
}


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def read(path):
    with open(path, "rb") as fh:
        return fh.read()


def answer_key(archive):
    raw = read(archive)
    if sha256_bytes(raw) != ARCHIVE_SHA256:
        sys.exit("Archive digest does not match. Refusing to unblind.")
    with zipfile.ZipFile(archive) as zf:
        key = json.loads(zf.read(FIXTURE_ROOT + "slice-uc17/expected.json"))
    return {c["case"]: CONTENT_VERDICT.get(c["case"], c["expected_state"]) for c in key["cases"]}


def pct(x):
    if x == 0:
        return "0%"
    if x < 1e-4:
        return "<0.01%"
    if x >= 0.9999:
        # Stored as a float; exact values below 1 can round to 1.0.
        return ">99.99%"
    return f"{x * 100:.2f}%"


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    rundir, archive, sealed_digest, expected_json = sys.argv[1:]

    fpath = os.path.join(rundir, "flags.json")
    if not os.path.exists(fpath):
        sys.exit("flags.json not found. Run detect.py first.")
    vraw, sraw, fraw = (read(os.path.join(rundir, n))
                        for n in ("verdicts.json", "sealed.json", "flags.json"))
    flags = json.loads(fraw)
    if flags["verdicts_sha256"] != sha256_bytes(vraw):
        sys.exit("flags.json was not computed from this verdicts.json.")
    if sha256_bytes(sraw) != sealed_digest:
        sys.exit("sealed.json does not match the digest printed by generate.py.")

    verdicts = json.loads(vraw)
    sealed = json.loads(sraw)
    exp = json.loads(read(expected_json))
    key = answer_key(archive)
    variant, rounds, roles = sealed["variant"], sealed["rounds"], sealed["roles"]
    cases = verdicts["cases"]

    labels = sorted(roles, key=lambda lab: (ROLE_ORDER[roles[lab]], sealed["relabel"][lab]))
    name = {lab: sealed["relabel"][lab] for lab in labels}

    # Observed verdicts per judge per case, over all rounds.
    observed = {lab: {c: Counter() for c in cases} for lab in labels}
    for row in verdicts["verdicts"]:
        for lab, v in row["verdicts"].items():
            observed[lab][row["case"]][v] += 1

    judges = []
    for lab in labels:
        s = flags["summary"][lab]
        who = name[lab]
        judges.append({
            "label": lab, "judge": who, "role": roles[lab],
            "total_deviations": s["total_deviations"],
            "mean_per_round": s["mean_per_round"],
            "expected_per_round": exp["expected_deviations_per_round"][variant][who],
            "flagged": s["flagged"],
            "predicted_flag_probability": exp["flag_probability"][f"{variant}|{rounds}|{who}"],
            "by_direction": s["by_direction"],
            "items": {c: dict(observed[lab][c]) for c in cases},
            "wrong_items": sum(n for c in cases for v, n in observed[lab][c].items() if v != key[c]),
        })

    by = {j["judge"]: j for j in judges}
    maj02 = [m for m in flags["case_majorities"] if m["case"] == "UC17-02"]
    honest = [lab for lab in labels if roles[lab] == "honest"]
    honest_agree_02 = all(
        len({row["verdicts"][h] for h in honest}) == 1
        for row in verdicts["verdicts"] if row["case"] == "UC17-02")
    p_lab = next(lab for lab in labels if roles[lab] == "planted")
    planted_wrong = all(observed[p_lab][c] == Counter({v: rounds}) and v != key[c]
                        for c, v in PLANTED[variant].items())
    checks = {
        "AC-2 gross planted judge flagged": by["P"]["flagged"] if variant == "gross" else None,
        "AC-3 subtle planted judge flagged": by["P"]["flagged"] if variant == "subtle" else None,
        "AC-4 dissenter not flagged": not by["D"]["flagged"],
        "AC-5 UC17-02 majority is remediate in every round": all(m["majority_of_six"] == "remediate" for m in maj02),
        "AC-6 honest judges agree on UC17-02 in every round": honest_agree_02,
        # The dissenter keeps the 10% random error on UC17-02 (section 6), so
        # this is reported as a count, not as a pass or fail.
        "AC-7 rounds in which the dissenter gave the correct verdict on UC17-02":
            f'{by["D"]["items"]["UC17-02"].get(key["UC17-02"], 0)} of {rounds}',
        "AC-7 planted judge wrong on its changed cases every round": planted_wrong,
        "AC-8 no honest judge flagged": not any(by[h]["flagged"] for h in ("H1", "H2", "H3", "H4")),
    }

    report = {
        "spec_version": sealed["spec_version"], "variant": variant, "rounds": rounds,
        "seed": sealed["seed"],
        "digests": {"verdicts.json": sha256_bytes(vraw), "sealed.json": sha256_bytes(sraw),
                    "flags.json": sha256_bytes(fraw)},
        "threshold_total": flags["threshold_total"],
        "answer_key": {c: key[c] for c in cases},
        "judges": judges, "checks": checks,
    }
    with open(os.path.join(rundir, "report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")

    md = [f"# Run: {variant} variant, {rounds} round(s)", "",
          f"Seed {sealed['seed']}. Flag if total deviations > {flags['threshold_total']:.4f}.", "",
          "| Label | Judge | Role | Deviations | Per round | Expected per round | Flagged | Predicted chance of flag |",
          "|---|---|---|---|---|---|---|---|"]
    for j in judges:
        md.append(f"| {j['label']} | {j['judge']} | {j['role']} | {j['total_deviations']} | "
                  f"{j['mean_per_round']:.3f} | {j['expected_per_round']:.3f} | "
                  f"{'yes' if j['flagged'] else 'no'} | {pct(j['predicted_flag_probability'])} |")
    md += ["", "Expected versus observed, per item (counts over all rounds)", "",
           "| Case | Expected | " + " | ".join(j["judge"] for j in judges) + " |",
           "|---|---|" + "---|" * len(judges)]
    for c in cases:
        cells = []
        for j in judges:
            items = j["items"][c]
            cells.append(", ".join(f"{v} {n}" for v, n in sorted(items.items(), key=lambda x: -x[1])))
        md.append(f"| {c} | {key[c]} | " + " | ".join(cells) + " |")
    md += ["", "Checks", ""]
    for k, v in checks.items():
        md.append(f"- {k}: {v if v is not None else 'not applicable to this variant'}")
    md += ["", "Digests", ""] + [f"- {k}: `{v}`" for k, v in report["digests"].items()]
    with open(os.path.join(rundir, "report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
