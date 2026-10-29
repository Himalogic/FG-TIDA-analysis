#!/usr/bin/env python3
"""Generate scripted verdicts for the planted-judge demonstration, spec 1.0.

Reads the pinned fixture, checks it, and produces one run's verdicts from the
script in sections 4 to 6 of the specification. Writes two files into the
output directory:

    verdicts.json  verdicts only, judges relabeled J1 to J6
    sealed.json    the relabeling, roles, variant, rounds and seed

and prints the SHA-256 of both. Detection (detect.py) reads verdicts.json
only. The answer key and roles are opened afterward by unblind.py.

Usage:
    python3 generate.py path/to/tida6-fx-0.2.zip VARIANT ROUNDS OUTDIR
    VARIANT is subtle or gross; ROUNDS is 1, 5 or 25.

Draw order (part of specification 1.0, section 6). One random.Random(seed)
per run, used in exactly this order:

  1. Relabeling: the list ["H1", "H2", "H3", "H4", "D", "P"] is shuffled
     once with rng.shuffle. The judge at position i becomes J(i+1).
  2. Verdicts: for each round 1..R, for each scored case in the order
     UC17-01, -02, -03, -04, -05, -06, -07, -09, for each judge in the order
     H1, H2, H3, H4, D, P:
       - if the script fixes this judge's verdict on this case (the blind
         spot for H1 to H4, the planted changes for P), use it and draw
         nothing;
       - otherwise draw u = rng.random(). If u < 0.1, the verdict is
         rng.choice(others), where others is the vocabulary without the
         expected verdict, in the order permit, remediate, escalate, block,
         indeterminate. Otherwise the verdict is the expected verdict.

Python 3.11 or later, standard library only.
MIT License, Copyright (c) 2026 Himalogic Software Pvt. Ltd.
Fixture: TIDA6-FX-0.2, CTGT, 2026, CC BY 4.0 (FG-TIDA/themes#6).
"""

import hashlib
import json
import os
import random
import sys
import zipfile

SPEC_VERSION = "planted-judge-spec-1.0"
ARCHIVE_SHA256 = "10d721acc44228edaa769719d1ff6eac90fdab2576317a7621cc05eaced33d13"
FIXTURE_ROOT = "tida6-fx-0.2/"

VOCABULARY = ("permit", "remediate", "escalate", "block", "indeterminate")
CASES = ("UC17-01", "UC17-02", "UC17-03", "UC17-04",
         "UC17-05", "UC17-06", "UC17-07", "UC17-09")
EXPECTED_IN_KEY = {
    "UC17-01": "permit",
    "UC17-02": "permit",
    "UC17-03": "remediate",
    "UC17-04": "remediate",
    "UC17-05": "block",
    "UC17-06": "escalate",
    "UC17-07": "indeterminate",
    "UC17-08": "attested absence",
    "UC17-09": "remediate carried, record rejected",
}
# Content verdict used for scoring (section 4).
CONTENT_VERDICT = {"UC17-09": "remediate"}

JUDGES = ("H1", "H2", "H3", "H4", "D", "P")
ROLES = {"H1": "honest", "H2": "honest", "H3": "honest", "H4": "honest",
         "D": "justified dissenter", "P": "planted"}
BLIND_SPOT = {"UC17-02": "remediate"}
PLANTED = {
    "subtle": {"UC17-05": "remediate"},
    "gross": {"UC17-03": "permit", "UC17-04": "permit", "UC17-05": "permit",
              "UC17-06": "permit", "UC17-09": "permit"},
}
ERROR_RATE = 0.1
ROUNDS = (1, 5, 25)


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_fixture(path):
    """Check the archive digest, manifest and record digests; return the key."""
    digest = sha256_file(path)
    if digest != ARCHIVE_SHA256:
        sys.exit(f"Archive SHA-256 is {digest}, expected {ARCHIVE_SHA256}. Refusing to run.")
    with zipfile.ZipFile(path) as zf:
        manifest = zf.read(FIXTURE_ROOT + "MANIFEST.sha256").decode("utf-8")
        n = 0
        for line in manifest.splitlines():
            if not line.strip():
                continue
            want, name = line.split(None, 1)
            name = name.strip().removeprefix("./")
            if hashlib.sha256(zf.read(FIXTURE_ROOT + name)).hexdigest() != want:
                sys.exit(f"MANIFEST mismatch on {name}.")
            n += 1
        records = json.loads(zf.read(FIXTURE_ROOT + "slice-uc17/records.json"))["records"]
        key = json.loads(zf.read(FIXTURE_ROOT + "slice-uc17/expected.json"))
    for rec in records.values():
        body = {k: v for k, v in rec.items() if k != "integrity"}
        canon = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        got = "sha256:" + hashlib.sha256(canon.encode("utf-8")).hexdigest()
        if got != rec["integrity"]["digest"]:
            sys.exit(f"Record digest mismatch on {rec['record_id']}.")
    found = {c["case"]: c["expected_state"] for c in key["cases"]}
    for case, state in EXPECTED_IN_KEY.items():
        if found.get(case) != state:
            sys.exit(f"Answer key differs from the specification on {case}.")
    expected = {c: CONTENT_VERDICT.get(c, found[c]) for c in CASES}
    return digest, n, len(records), expected


def seed_for(variant, rounds):
    text = f"{SPEC_VERSION}|{ARCHIVE_SHA256}|{variant}|rounds={rounds}"
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def fixed_verdict(judge, case, variant):
    if ROLES[judge] == "honest":
        return BLIND_SPOT.get(case)
    if judge == "P":
        return PLANTED[variant].get(case)
    return None


def generate(expected, variant, rounds):
    seed = seed_for(variant, rounds)
    rng = random.Random(seed)
    order = list(JUDGES)
    rng.shuffle(order)
    relabel = {f"J{i + 1}": j for i, j in enumerate(order)}
    to_label = {j: lab for lab, j in relabel.items()}

    rows = []
    for r in range(1, rounds + 1):
        for case in CASES:
            exp = expected[case]
            out = {}
            for j in JUDGES:
                v = fixed_verdict(j, case, variant)
                if v is None:
                    if rng.random() < ERROR_RATE:
                        v = rng.choice([x for x in VOCABULARY if x != exp])
                    else:
                        v = exp
                out[to_label[j]] = v
            rows.append({"round": r, "case": case,
                         "verdicts": {lab: out[lab] for lab in sorted(out)}})
    return seed, relabel, rows


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    archive, variant, rounds, outdir = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    if variant not in PLANTED or rounds not in ROUNDS:
        sys.exit("VARIANT must be subtle or gross; ROUNDS must be 1, 5 or 25.")

    digest, n_files, n_records, expected = load_fixture(archive)
    seed, relabel, rows = generate(expected, variant, rounds)

    os.makedirs(outdir, exist_ok=True)
    vpath = os.path.join(outdir, "verdicts.json")
    spath = os.path.join(outdir, "sealed.json")
    write_json(vpath, {
        "spec_version": SPEC_VERSION,
        "vocabulary": list(VOCABULARY),
        "judges": sorted(relabel),
        "cases": list(CASES),
        "rounds": rounds,
        "verdicts": rows,
    })
    write_json(spath, {
        "spec_version": SPEC_VERSION,
        "archive_sha256": digest,
        "variant": variant,
        "rounds": rounds,
        "seed": seed,
        "relabel": relabel,
        "roles": {lab: ROLES[j] for lab, j in relabel.items()},
    })
    print(f"Fixture checks passed: archive digest, {n_files} manifest files, {n_records} record digests, answer key.")
    print(f"{variant}, {rounds} round(s), seed {seed}")
    print(f"verdicts.json sha256 {sha256_file(vpath)}")
    print(f"sealed.json   sha256 {sha256_file(spath)}")


if __name__ == "__main__":
    main()
