# Run: gross variant, 5 round(s)

Seed 15652758213012786834. Flag if total deviations > 10.5929.

| Label | Judge | Role | Deviations | Per round | Expected per round | Flagged | Predicted chance of flag |
|---|---|---|---|---|---|---|---|
| J5 | H1 | honest | 7 | 1.400 | 0.692 | no | 0.04% |
| J2 | H2 | honest | 2 | 0.400 | 0.692 | no | 0.04% |
| J3 | H3 | honest | 4 | 0.800 | 0.692 | no | 0.04% |
| J1 | H4 | honest | 2 | 0.400 | 0.692 | no | 0.04% |
| J4 | D | justified dissenter | 9 | 1.800 | 1.667 | no | 11.74% |
| J6 | P | planted | 30 | 6.000 | 6.134 | yes | >99.99% |

Expected versus observed, per item (counts over all rounds)

| Case | Expected | H1 | H2 | H3 | H4 | D | P |
|---|---|---|---|---|---|---|---|
| UC17-01 | permit | permit 4, indeterminate 1 | permit 5 | permit 3, escalate 1, block 1 | permit 5 | permit 4, escalate 1 | permit 5 |
| UC17-02 | permit | remediate 5 | remediate 5 | remediate 5 | remediate 5 | permit 4, remediate 1 | permit 5 |
| UC17-03 | remediate | remediate 4, escalate 1 | remediate 4, block 1 | remediate 3, indeterminate 1, permit 1 | remediate 5 | remediate 4, block 1 | permit 5 |
| UC17-04 | remediate | remediate 3, permit 1, block 1 | remediate 5 | remediate 5 | remediate 5 | remediate 5 | permit 5 |
| UC17-05 | block | block 3, escalate 1, permit 1 | block 5 | block 5 | block 5 | block 4, indeterminate 1 | permit 5 |
| UC17-06 | escalate | escalate 5 | escalate 4, permit 1 | escalate 5 | escalate 4, block 1 | escalate 5 | permit 5 |
| UC17-07 | indeterminate | indeterminate 4, remediate 1 | indeterminate 5 | indeterminate 5 | indeterminate 4, permit 1 | indeterminate 5 | indeterminate 5 |
| UC17-09 | remediate | remediate 5 | remediate 5 | remediate 5 | remediate 5 | remediate 3, escalate 2 | permit 5 |

Checks

- AC-2 gross planted judge flagged: True
- AC-3 subtle planted judge flagged: not applicable to this variant
- AC-4 dissenter not flagged: True
- AC-5 UC17-02 majority is remediate in every round: True
- AC-6 honest judges agree on UC17-02 in every round: True
- AC-7 rounds in which the dissenter gave the correct verdict on UC17-02: 4 of 5
- AC-7 planted judge wrong on its changed cases every round: True
- AC-8 no honest judge flagged: True

Digests

- verdicts.json: `795199fe7b97db0c4d81a755eaffefc5bc6444c862db5481842793052513c1bc`
- sealed.json: `70b7df653983faa04ea26f454f2db089246905405c9582e1ca83af1831202167`
- flags.json: `1225ba58184a52ee4a030818673ace2b07a1a4dc688f98c2010c41f7bd76a92f`
