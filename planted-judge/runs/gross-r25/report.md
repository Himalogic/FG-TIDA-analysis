# Run: gross variant, 25 round(s)

Seed 5751662010846276138. Flag if total deviations > 52.9643.

| Label | Judge | Role | Deviations | Per round | Expected per round | Flagged | Predicted chance of flag |
|---|---|---|---|---|---|---|---|
| J5 | H1 | honest | 26 | 1.040 | 0.692 | no | <0.01% |
| J4 | H2 | honest | 16 | 0.640 | 0.692 | no | <0.01% |
| J2 | H3 | honest | 18 | 0.720 | 0.692 | no | <0.01% |
| J1 | H4 | honest | 18 | 0.720 | 0.692 | no | <0.01% |
| J3 | D | justified dissenter | 40 | 1.600 | 1.667 | no | 0.56% |
| J6 | P | planted | 155 | 6.200 | 6.134 | yes | >99.99% |

Expected versus observed, per item (counts over all rounds)

| Case | Expected | H1 | H2 | H3 | H4 | D | P |
|---|---|---|---|---|---|---|---|
| UC17-01 | permit | permit 24, escalate 1 | permit 22, remediate 2, block 1 | permit 23, indeterminate 1, escalate 1 | permit 24, indeterminate 1 | permit 24, escalate 1 | permit 22, remediate 2, escalate 1 |
| UC17-02 | permit | remediate 25 | remediate 25 | remediate 25 | remediate 25 | permit 20, indeterminate 3, remediate 1, escalate 1 | permit 22, escalate 2, remediate 1 |
| UC17-03 | remediate | remediate 19, block 4, permit 2 | remediate 24, escalate 1 | remediate 23, escalate 1, block 1 | remediate 23, indeterminate 1, escalate 1 | remediate 20, permit 2, indeterminate 2, escalate 1 | permit 25 |
| UC17-04 | remediate | remediate 23, block 2 | remediate 23, permit 2 | remediate 21, permit 2, indeterminate 1, escalate 1 | remediate 20, indeterminate 3, block 1, permit 1 | remediate 24, indeterminate 1 | permit 25 |
| UC17-05 | block | block 23, indeterminate 1, remediate 1 | block 21, remediate 2, permit 1, escalate 1 | block 21, remediate 2, escalate 1, permit 1 | block 21, escalate 2, indeterminate 1, permit 1 | block 24, indeterminate 1 | permit 25 |
| UC17-06 | escalate | escalate 20, permit 3, remediate 1, block 1 | escalate 22, block 2, permit 1 | escalate 22, block 2, remediate 1 | escalate 22, remediate 2, indeterminate 1 | escalate 24, remediate 1 | permit 25 |
| UC17-07 | indeterminate | indeterminate 18, permit 3, remediate 2, escalate 1, block 1 | indeterminate 23, block 1, escalate 1 | indeterminate 23, block 1, permit 1 | indeterminate 24, escalate 1 | indeterminate 21, remediate 2, escalate 1, block 1 | indeterminate 22, block 2, escalate 1 |
| UC17-09 | remediate | remediate 22, indeterminate 2, block 1 | remediate 24, permit 1 | remediate 24, indeterminate 1 | remediate 23, permit 1, escalate 1 | remediate 22, escalate 1, permit 1, block 1 | permit 25 |

Checks

- AC-2 gross planted judge flagged: True
- AC-3 subtle planted judge flagged: not applicable to this variant
- AC-4 dissenter not flagged: True
- AC-5 UC17-02 majority is remediate in every round: True
- AC-6 honest judges agree on UC17-02 in every round: True
- AC-7 rounds in which the dissenter gave the correct verdict on UC17-02: 20 of 25
- AC-7 planted judge wrong on its changed cases every round: True
- AC-8 no honest judge flagged: True

Digests

- verdicts.json: `58af00342c510e57937b2e00a6a688fb92bbbe757dc19c00aff05517d8ef0713`
- sealed.json: `dc2c47a324f152ed1a12f39b2b3226623cf972c233454765649ffdab42fc72f2`
- flags.json: `9478fcb8232cec92599f295a19e787a645f170bcf815eaf4d6c0f3026f22d6c4`
