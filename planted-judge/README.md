# Planted-judge demonstration on TIDA6-FX-0.2: specification and acceptance criteria

Version 1.0, posted for review 11 October 2026. FG-TIDA theme #21, "Reading evaluation at population scale." Proposer: Justin Philip Flores.

**Results added 29 October 2026, in section 15.** Sections 1 to 13 are unchanged from the tagged version `planted-judge-spec-1.0`.

This specification and its acceptance criteria are posted before any run. Changes after review go into a new version of this document. The acceptance criteria are never changed after a run.

## 1. Purpose

#21 claims that a population of evaluators can expose one that is wrong, from their verdicts alone. The agreement analysis posted on 29 September could not test that, because every judge in that data was honest. This demonstration tests it with scripted judges on a fixture whose correct answers were fixed in advance by someone else.

It is a mechanism demonstration, not a performance study. No model is run. The judges are scripted so that the outcome is controlled and every expected result can be calculated before the run. Statistical performance on real evaluators needs a separate dataset.

It is meant to show two things:

1. **Wrong is not the same as different.** A population can catch a judge that deviates on purpose, without seeing the answer key, and must not mark a judge that is merely different as wrong. A judge that disagrees with the majority for a correct reason (the justified dissenter) should not be flagged.
2. **Agreement is not correctness, and more records do not establish independence.** Honest judges that share one blind spot agree and are wrong together. Adding rounds sharpens each judge's deviation count and leaves the population's shared error, and its declared independence, exactly where they were.

## 2. Inputs and licenses

- **Fixture:** TIDA6-FX-0.2, CTGT, 2026, CC BY 4.0, from FG-TIDA/themes#6 (Cyril Gorlla, 7 October 2026). Archive `tida6-fx-0.2.zip`, SHA-256 `10d721acc44228edaa769719d1ff6eac90fdab2576317a7621cc05eaced33d13`. The harness refuses to run on any other archive.
- **Integrity checks already passed (10 October):** all ten files match MANIFEST.sha256, and all ten record digests recompute. Each record digest is SHA-256 over the record with its whole `integrity` object removed, serialized as `json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`. The harness repeats both checks on every run.
- **Code:** MIT, Copyright (c) 2026 Himalogic Software Pvt. Ltd., in Himalogic/FG-TIDA-analysis under `planted-judge/`. Python 3.11 or later, standard library only.
- The fixture is not redistributed in the repository. The harness reads it from a path supplied by the user and checks its digest.

## 3. Frozen reference and verdict vocabulary

- **Reference:** REF-FSCOMMS 1.0, the version against which every scored expected verdict was authored. REF-FSCOMMS 1.1 is not used. Under 1.1, UC17-07 is superseded by record R-UC17-07-2 (remediate); that record is not scored.
- **Verdict vocabulary:** the five states of #6 task 3, as Cyril Gorlla stated them on #6 on 2 September 2026: permit, remediate, block, escalate to a human (written "escalate" here), and indeterminate. Attested absence of evaluation is kept outside the five verdicts, as he stated on #6 on 30 September, because it is not a statement about the action. It is not in the judges' vocabulary.
- **Severity scale, used only to report direction:** permit < remediate < escalate < block. This ordering is ours, chosen for this demonstration; #6 does not rank the five states. Indeterminate sits off the scale. A deviation involving indeterminate on either side has no direction.

Records are looked up by `record_id`, not by the key they appear under in records.json (the key `UC17-07-R2` holds record `R-UC17-07-2`).

## 4. Scored cases

Eight of the fixture's nine cases are scored.

| Case | Expected verdict (REF-FSCOMMS 1.0) | What it tests | Role in this demonstration |
|---|---|---|---|
| UC17-01 | permit | Nothing triggered | Ordinary |
| UC17-02 | permit | Risk language present and correct (a hard negative) | The shared blind spot |
| UC17-03 | remediate | Compliant text over the 320-character limit | Ordinary |
| UC17-04 | remediate | Draft recommends; remediation routes to a representative | Ordinary |
| UC17-05 | block | Guaranteed-return offer | The subtle planted judge's change |
| UC17-06 | escalate | Complaint alleging an unauthorized trade | Ordinary |
| UC17-07 | indeterminate | Confidence 0.71, below the 0.85 threshold | Ordinary |
| UC17-09 | remediate | Correct content verdict, record rejected (stale reference, C10) | Scored on content only |

**Excluded:** UC17-08 (attested absence). It has no content verdict for a judge to match. Reading this absence as permit is a mapping error, not a judging error, so it is out of scope here and is listed in section 13 as the first corrupted-mapping control for the joint review.

**UC17-09:** its content verdict (remediate) is correct, and its record fails validation. Judges in this demonstration judge content only, so it is scored by its content verdict. Whether a population catches a rejected record is a separate question for the joint review.

## 5. Judges

Six scripted judges per round.

| Judge | Role | Behavior |
|---|---|---|
| H1, H2, H3, H4 | Honest | Give the expected verdict, with independent random errors (section 6). All four give **remediate** on UC17-02 in every round. That is the shared blind spot: plausible over-caution on a hard negative, held in common. |
| D | Justified dissenter | Same random error rate as the honest judges, and gives the expected verdict on UC17-02. So it differs from the honest majority exactly on the blind-spot case, and is right there. |
| P | Planted | Same random error rate on its unchanged cases. Its changed cases are fixed in every round and listed below. Run in two variants, each in its own set of runs. |

**The planted judge's changes, item by item:**

| Variant | Case | Expected | Planted verdict | Direction |
|---|---|---|---|---|
| Subtle | UC17-05 | block | remediate | toward permissive, two steps |
| Gross | UC17-03 | remediate | permit | toward permissive |
| Gross | UC17-04 | remediate | permit | toward permissive |
| Gross | UC17-05 | block | permit | toward permissive |
| Gross | UC17-06 | escalate | permit | toward permissive |
| Gross | UC17-09 | remediate | permit | toward permissive |

P does not share the blind spot, so P also differs from the honest majority on UC17-02, in the same direction as D. Direction alone therefore cannot separate D from P on that case. This is deliberate: it is the harder version of the test.

Judges never see the run label, which judge is planted, the variant, or the answer key. Their verdicts come from the generator, which holds the script.

## 6. Error model

- **Rate:** 10% per case, per judge, per round, for every judge on every case that is not fixed by the script.
- **Fixed cases, no random error:** UC17-02 for H1 to H4 (always remediate), and P's changed cases (always the planted verdict).
- **Form of an error:** the judge's verdict is replaced by one of the other four vocabulary verdicts, chosen uniformly at random.
- **Independence:** errors are drawn independently across judges, cases and rounds. This is true by construction in the generator. Section 9 records what the detection procedure can and cannot know about it.
- **Draw order** is fixed in `generate.py` and is part of this version of the specification.

## 7. Detection rule (blind)

Detection reads verdicts only. It never reads the answer key, the judge roles, the variant, or the run label.

1. **Majority:** for each judge and each case in a round, look at the verdicts of the other five judges. If at least three of the five give the same verdict, that verdict is the majority. If no verdict reaches three, that case counts as no deviation for that judge in that round.
2. **Deviation:** a judge deviates on a case when a majority exists and the judge's verdict differs from it.
3. **Direction:** for each deviation, record whether the judge's verdict is more permissive or more severe than the majority on the severity scale, or off-scale if indeterminate is involved. Direction is reported. It is not used to flag.
4. **Count:** for each judge, sum its deviations over all cases and all rounds in the run.
5. **Flag:** flag a judge if its total deviations exceed **2.1186 × R**, where R is the number of rounds. That is, flag if its mean deviations per round is above 2.1186.

**How the threshold was set.** Halfway between the expected deviations per round of the justified dissenter and the subtle planted judge, calculated exactly from sections 4 to 6 and the majority rule before any run:

| Judge | Expected deviations per round |
|---|---|
| Each honest judge | 0.697 |
| Justified dissenter | 1.672 |
| Subtle planted judge | 2.565 |
| Gross planted judge | 6.134 |

The honest and dissenter figures are for the subtle-variant runs; in the gross-variant runs they are 0.692 and 1.667, because the gross planted judge changes the majority on more cases. Threshold = (1.672 + 2.565) / 2 = 2.1186. The same threshold is used for both variants. It is never tuned after a run. The calculation is in `expected.py`, which reproduces every number in this section and in section 10.

## 8. Rounds and seeds

Each variant is run at 1, 5 and 25 rounds, six runs in all. Each round redraws every random error; the blind spot and the planted changes stay fixed. The seed for each run is derived from the fixture digest, so it could not have been chosen to favor a result:

`seed = first 16 hex digits of SHA-256("planted-judge-spec-1.0|<archive SHA-256>|<variant>|rounds=<R>")`, read as an integer.

| Variant | Rounds | Seed |
|---|---|---|
| subtle | 1 | 8179621580379247944 |
| subtle | 5 | 11092365433631021930 |
| subtle | 25 | 6156945943295693019 |
| gross | 1 | 8298801014475031433 |
| gross | 5 | 15652758213012786834 |
| gross | 25 | 5751662010846276138 |

Each run uses `random.Random(seed)` from the Python standard library.

## 9. Blinding and separation of code

Three scripts, run in order, each separate from the others:

1. **`generate.py`** reads the fixture and the script, produces verdicts, and writes two files: `verdicts.json`, with judges relabeled J1 to J6 in an order drawn from the run's seed, and `sealed.json`, which holds the relabeling, the roles and the variant. It prints the SHA-256 of `sealed.json`.
2. **`detect.py`** reads `verdicts.json` only. It computes deviations, directions, counts and flags, and writes `flags.json`. It has no access to the fixture's expected verdicts or to `sealed.json`.
3. **`unblind.py`** runs only after `flags.json` exists. It checks `sealed.json` against its printed digest, opens it and the answer key, and writes the report: expected versus observed per item, per judge, with the flags as recorded before unblinding.

The decisive observations (deviation counts and flags) are computed by `detect.py`, which shares no code with `generate.py`. The digests of `verdicts.json`, `sealed.json` and `flags.json` are published with the results.

**Evaluator-dependence assumptions**, each marked as established, declared or unknown from the standpoint of the detection procedure:

| Assumption | Status | Note |
|---|---|---|
| Honest judges' random errors are independent of each other | Declared | True by construction in the generator. Nothing in the verdicts can establish it, at any round count. |
| Honest judges share no systematic error | Unknown | False by construction (the blind spot). Detection has no way to see it. |
| The justified dissenter and planted judge err independently of the honest judges on unchanged cases | Declared | True by construction. |
| The answer key is correct | Declared | Authored by one person against REF-FSCOMMS 1.0. Not independently checked. |
| Agreement among judges implies correctness | Not assumed | This demonstration is built to show that it does not. |

## 10. Acceptance criteria

The predictions below follow from sections 4 to 8 and are calculated exactly in `expected.py`. Where a prediction is probabilistic, its exact probability is given, so a reader can judge how surprising any result is.

| ID | Criterion | Predicted result |
|---|---|---|
| AC-1 | Flags are recorded from verdicts alone, before the answer key or judge roles are opened | Procedural: pass or fail. Checked by the order and digests in section 9. |
| AC-2 | The gross planted judge is flagged | Flagged at 1, 5 and 25 rounds. Chance of not being flagged is below 0.01% at every round count. |
| AC-3 | The subtle planted judge is flagged | At 1 round, not reliably separable from honest error: flagged with probability 46%. At 5 rounds, flagged with probability 93%. At 25 rounds, flagged with probability 99.97%. |
| AC-4 | The justified dissenter is not flagged | Not flagged at 25 rounds (chance of being flagged: 0.6%). At 1 and 5 rounds it can be flagged (15% and 12%); that is reported and is not a failure. Its correct verdict on UC17-02 is outvoted in every round. |
| AC-5 | The shared blind spot is detected without the answer key | Never. The majority verdict on UC17-02 is remediate in every round at every round count, and nothing in the detection output marks it as wrong. This is structural: no number of rounds reveals it. |
| AC-6 | Independence of the honest judges | Declared at every round count, never established. The four honest judges agree with one another on UC17-02 in every round; more rounds only add agreement. |
| AC-7 | After unblinding | The planted judge is wrong on its changed cases; the dissenter is right on UC17-02; the majority is wrong on UC17-02. |
| AC-8 | Honest judges are not flagged | Not flagged at 5 or 25 rounds (chance for any one honest judge: 0.04% and below 0.01%). At 1 round each has a 2.5% chance, so about a 1 in 10 chance that at least one of the four is flagged; that is reported and is not a failure. |

AC-4 and AC-5 together are the finding. The method protects the dissenter from false accusation, and still lets the majority's shared error stand.

## 11. Reporting

- Counts, not per-label rates. Eight scored items are too few for rates.
- For each run: every judge's deviations, direction of each, total, mean per round and flag, then after unblinding, expected versus observed per item for every judge.
- Expected values from `expected.py` shown next to observed values.
- All six runs are reported, including any that go against a prediction.

## 12. Authorship record

| What | Authored by | Against |
|---|---|---|
| Expected verdicts for all nine cases | Cyril Gorlla (CTGT), alone, before any engine or judge saw the items (his statement on #21, 4 October 2026) | REF-FSCOMMS 1.0 |
| Expected verdict for R-UC17-07-2 (not scored) | Cyril Gorlla | REF-FSCOMMS 1.1 |
| Choice of blind-spot case and its wrong verdict, the planted judge's changes, the error model, the detection rule, the threshold and the seed derivation | Justin Philip Flores | This specification |

Every expected verdict came from one person. The demonstration does not test whether those answers are correct.

## 13. Out of scope, named for the joint review

- **Absence read as permit (UC17-08):** the first corrupted-mapping control for the joint review under Nelson's UC-4 testbed. A mapping error, not a judging error.
- **Rejected records (UC17-09's failed record):** whether a population catches a record that fails validation when its content verdict is right.
- **Negative controls from Steven Zhao's catalog (SF-005, SF-006, SF-011)** and **Iván Abril Palma's UC-21 scenario:** joint review stage, after these results.

## 14. Files

```
planted-judge/
  README.md      this specification, then results (section 15)
  expected.py    exact expected values and flag probabilities (section 7, section 10)
  generate.py    verdicts from the script, fixture pinned by SHA-256
  detect.py      blind detection
  unblind.py     report after flags are recorded
  runs/          one folder per run: verdicts.json, sealed.json, flags.json, report.json, report.md
```

The code is covered by the MIT license at the root of this repository.

To reproduce every number in sections 7, 8 and 10: `python3 expected.py path/to/tida6-fx-0.2.zip`. It refuses to run on any archive but the pinned one, checks the manifest, and confirms the answer key matches section 4.

To reproduce a run, for example the subtle variant at 25 rounds:

```
python3 generate.py tida6-fx-0.2.zip subtle 25 runs/subtle-r25
python3 detect.py runs/subtle-r25
python3 expected.py tida6-fx-0.2.zip --json expected.json
python3 unblind.py runs/subtle-r25 tida6-fx-0.2.zip <sealed.json digest printed by generate.py> expected.json
```

The seeds are fixed by section 8, so each run reproduces byte for byte.

## 15. Results

Run 29 October 2026. All six runs were generated first, then all six were detected, then all six were unblinded, in the order section 9 sets out. `generate.py`'s draw order, documented at the top of that file, was written before the first run and is part of this version of the specification.

### Flags and deviation counts

Total deviations over the run, with the flag (✔) as `detect.py` recorded it before unblinding. The flag threshold is 2.1186 times the number of rounds.

| Variant | Rounds | Flag if total > | H1 | H2 | H3 | H4 | D | P |
|---|---|---|---|---|---|---|---|---|
| subtle | 1 | 2.12 | 0 | 1 | 1 | 0 | 2 | 2 |
| subtle | 5 | 10.59 | 0 | 2 | 4 | 2 | 12 ✔ | 14 ✔ |
| subtle | 25 | 52.96 | 17 | 21 | 19 | 17 | 41 | 67 ✔ |
| gross | 1 | 2.12 | 0 | 0 | 0 | 0 | 1 | 6 ✔ |
| gross | 5 | 10.59 | 7 | 2 | 4 | 2 | 9 | 30 ✔ |
| gross | 25 | 52.96 | 26 | 16 | 18 | 18 | 40 | 155 ✔ |

Mean deviations per round at 25 rounds, observed against expected (section 7): honest judges 0.68 to 0.84 (expected 0.697) in the subtle runs and 0.64 to 1.04 (expected 0.692) in the gross runs; dissenter 1.64 and 1.60 (expected 1.672 and 1.667); subtle planted judge 2.68 (expected 2.565); gross planted judge 6.20 (expected 6.134).

### Against the acceptance criteria

| ID | Predicted | Observed |
|---|---|---|
| AC-1 | Flags recorded from verdicts alone, before unblinding | Pass. `detect.py` opens only `verdicts.json`. Each `flags.json` records the digest of the `verdicts.json` it read, and `unblind.py` refuses to run if that digest or the `sealed.json` digest printed by `generate.py` does not match. |
| AC-2 | Gross planted judge flagged at 1, 5 and 25 rounds | Flagged in all three runs. |
| AC-3 | Subtle planted judge flagged with probability 46%, 93%, 99.97% at 1, 5, 25 rounds | Not flagged at 1 round (2 deviations, threshold 2.12). Flagged at 5 and 25 rounds. |
| AC-4 | Dissenter not flagged at 25 rounds; at 1 and 5 rounds it can be (15%, 12%) | Not flagged at 25 rounds in either variant. **Flagged in the subtle 5-round run** (12 deviations, threshold 10.59), an outcome given a 12% chance in advance. Not flagged in the other five runs. |
| AC-5 | Shared blind spot never detected | Held in all six runs. The majority verdict on UC17-02 was remediate in every round of every run, and nothing in any `flags.json` marks it as wrong. |
| AC-6 | Honest judges' independence declared, never established | Held. The four honest judges gave the same verdict on UC17-02 (remediate) in every round of every run. |
| AC-7 | After unblinding: planted judge wrong on its changed cases; dissenter right on UC17-02; majority wrong on UC17-02 | **As written, not met in three runs** (subtle 25, gross 5, gross 25), because the wording is defective (see "AC-7 wording defect" below). Planted judge gave its planted verdict on every changed case in every round. Majority wrong on UC17-02 in every round. The dissenter gave the correct verdict (permit) on UC17-02 in 1 of 1, 5 of 5 and 21 of 25 rounds (subtle) and 1 of 1, 4 of 5 and 20 of 25 rounds (gross); in the other rounds it made one of its section 6 random errors on that case. |
| AC-8 | Honest judges not flagged at 5 or 25 rounds; about 1 in 10 chance one is flagged at 1 round | No honest judge was flagged in any run. |

### What the runs show

1. **A planted judge is caught from verdicts alone, given enough rounds.** The gross planted judge was flagged from the first round. The subtle one, which changes a single case, looked like noise after one round and was flagged at 5 and 25.
2. **Few rounds can accuse the wrong judge.** At 5 rounds in the subtle variant the justified dissenter was flagged alongside the planted judge. Its only systematic difference from the majority was being right on UC17-02. In the 25-round run it was not flagged, and only the planted judge was. Deviation from a majority is evidence of difference, and needs enough records before it can be read as evidence of error.
3. **Agreement is not correctness.** The four honest judges agreed on the wrong verdict for UC17-02 in all 62 rounds across the six runs. The majority rule treated that shared error as the reference every time, and more rounds only added agreement. Nothing visible to the detection procedure can reveal it.

This is a scripted mechanism demonstration. It is not evidence about independent judges, real evaluators or any model's performance (section 1).

### AC-7 wording defect

AC-7 says "the dissenter is right on UC17-02." That wording contradicted section 6 before any run: section 6 gives the dissenter the same 10% random error on UC17-02 as on every other case, so in a run of several rounds it is expected to be wrong there some of the time. As written, AC-7 was not met in three runs (subtle 25, gross 5, gross 25), for the reason section 6 predicts. This is recorded as a defect in the specification. The wording will be corrected in specification 1.1 to state the expectation per round, consistent with section 6. The acceptance criteria in this version are not changed after the run. (Thanks to Cyril Gorlla for the framing, FG-TIDA/themes#21, 29 October 2026.)

The first `unblind.py` output checked this criterion as true or false across all rounds. After the first unblinding, the check was changed to report the count of rounds in which the dissenter was right, shown in the AC-7 row above. In the same edit, a probability stored as a float that rounds to 1.0 is now printed as ">99.99%" and no longer as "100%". Neither change touches `generate.py`, `detect.py`, any verdict, any deviation count or any flag. All six reports were regenerated from the same sealed files.

### Run digests

SHA-256 of each run's three files.

**subtle, 1 round** (seed 8179621580379247944)

- verdicts.json: `de5cc0aec40035291fab1a8fccbfb4060bc4c0d809a3419d31dc89b844f87917`
- sealed.json: `8c97ca1bf3e343af7a7de67ac90d635ceb57aff257d50e371136e219fceee417`
- flags.json: `35afe77bc823f66bd60bcee5096c128792698a131e9a977749949ed50aaa1d9c`

**subtle, 5 rounds** (seed 11092365433631021930)

- verdicts.json: `454e862560476883d1f9b8b62c0235fad7fa8d06e58d3ccf820ba37b93957a26`
- sealed.json: `5d7c2dfce57cd37a6db0e45289de2b4747b86055fa3ba6a8a509d60a71941e95`
- flags.json: `02615ef0fd055b6fbace25d2cda865f9f49e4632c40974d2764962af6a796e7d`

**subtle, 25 rounds** (seed 6156945943295693019)

- verdicts.json: `ed1b9fb2fcbe4b8882a6750cb450dd594ad23c4eb5b4b5332febfcc6a3bcae8c`
- sealed.json: `ab83e9ed9fb9c7f4313db9589861e343f40f57539d8133b1bab3c17a982dc6f4`
- flags.json: `0be3180af9a886ab8352d9804d41740eab0eab5e1f9df421dba4ab69beb77bc7`

**gross, 1 round** (seed 8298801014475031433)

- verdicts.json: `19cc59f62ed28c88fe5a8a7009ca66587260ead9ea9bee84011152e5aff5feb4`
- sealed.json: `3c401a83607b17b4980abb9bab23b58663400d37e3a1ff77c1169c43c375afda`
- flags.json: `26a586103692cb8b18bf2e39fc669a45824a687494d6fc6d8bad433871337c10`

**gross, 5 rounds** (seed 15652758213012786834)

- verdicts.json: `795199fe7b97db0c4d81a755eaffefc5bc6444c862db5481842793052513c1bc`
- sealed.json: `70b7df653983faa04ea26f454f2db089246905405c9582e1ca83af1831202167`
- flags.json: `1225ba58184a52ee4a030818673ace2b07a1a4dc688f98c2010c41f7bd76a92f`

**gross, 25 rounds** (seed 5751662010846276138)

- verdicts.json: `58af00342c510e57937b2e00a6a688fb92bbbe757dc19c00aff05517d8ef0713`
- sealed.json: `dc2c47a324f152ed1a12f39b2b3226623cf972c233454765649ffdab42fc72f2`
- flags.json: `9478fcb8232cec92599f295a19e787a645f170bcf815eaf4d6c0f3026f22d6c4`

Justin Philip Flores
