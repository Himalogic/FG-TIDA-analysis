# Run: subtle variant, 25 round(s)

Seed 6156945943295693019. Flag if total deviations > 52.9643.

| Label | Judge | Role | Deviations | Per round | Expected per round | Flagged | Predicted chance of flag |
|---|---|---|---|---|---|---|---|
| J3 | H1 | honest | 17 | 0.680 | 0.697 | no | <0.01% |
| J4 | H2 | honest | 21 | 0.840 | 0.697 | no | <0.01% |
| J1 | H3 | honest | 19 | 0.760 | 0.697 | no | <0.01% |
| J5 | H4 | honest | 17 | 0.680 | 0.697 | no | <0.01% |
| J2 | D | justified dissenter | 41 | 1.640 | 1.672 | no | 0.61% |
| J6 | P | planted | 67 | 2.680 | 2.565 | yes | 99.97% |

Expected versus observed, per item (counts over all rounds)

| Case | Expected | H1 | H2 | H3 | H4 | D | P |
|---|---|---|---|---|---|---|---|
| UC17-01 | permit | permit 20, block 2, indeterminate 1, escalate 1, remediate 1 | permit 23, indeterminate 1, block 1 | permit 23, remediate 1, escalate 1 | permit 24, escalate 1 | permit 24, indeterminate 1 | permit 21, block 2, remediate 2 |
| UC17-02 | permit | remediate 25 | remediate 25 | remediate 25 | remediate 25 | permit 21, indeterminate 2, escalate 1, remediate 1 | permit 24, indeterminate 1 |
| UC17-03 | remediate | remediate 24, indeterminate 1 | remediate 21, indeterminate 3, escalate 1 | remediate 24, block 1 | remediate 22, escalate 2, block 1 | remediate 24, permit 1 | remediate 23, block 2 |
| UC17-04 | remediate | remediate 23, indeterminate 1, block 1 | remediate 22, block 2, permit 1 | remediate 23, indeterminate 1, escalate 1 | remediate 23, indeterminate 2 | remediate 24, escalate 1 | remediate 21, permit 2, escalate 1, indeterminate 1 |
| UC17-05 | block | block 22, remediate 3 | block 20, permit 2, remediate 2, escalate 1 | block 20, remediate 2, escalate 2, indeterminate 1 | block 23, permit 1, remediate 1 | block 23, indeterminate 1, escalate 1 | remediate 25 |
| UC17-06 | escalate | escalate 23, block 1, remediate 1 | escalate 24, permit 1 | escalate 22, permit 2, block 1 | escalate 22, block 1, permit 1, remediate 1 | escalate 23, permit 1, indeterminate 1 | escalate 22, block 1, permit 1, remediate 1 |
| UC17-07 | indeterminate | indeterminate 23, escalate 1, block 1 | indeterminate 22, remediate 1, escalate 1, block 1 | indeterminate 23, block 1, permit 1 | indeterminate 23, block 2 | indeterminate 20, escalate 3, permit 1, block 1 | indeterminate 24, escalate 1 |
| UC17-09 | remediate | remediate 23, indeterminate 1, permit 1 | remediate 21, block 2, escalate 1, indeterminate 1 | remediate 23, permit 1, indeterminate 1 | remediate 21, block 3, indeterminate 1 | remediate 21, indeterminate 3, escalate 1 | remediate 22, block 2, permit 1 |

Checks

- AC-2 gross planted judge flagged: not applicable to this variant
- AC-3 subtle planted judge flagged: True
- AC-4 dissenter not flagged: True
- AC-5 UC17-02 majority is remediate in every round: True
- AC-6 honest judges agree on UC17-02 in every round: True
- AC-7 rounds in which the dissenter gave the correct verdict on UC17-02: 21 of 25
- AC-7 planted judge wrong on its changed cases every round: True
- AC-8 no honest judge flagged: True

Digests

- verdicts.json: `ed1b9fb2fcbe4b8882a6750cb450dd594ad23c4eb5b4b5332febfcc6a3bcae8c`
- sealed.json: `ab83e9ed9fb9c7f4313db9589861e343f40f57539d8133b1bab3c17a982dc6f4`
- flags.json: `0be3180af9a886ab8352d9804d41740eab0eab5e1f9df421dba4ab69beb77bc7`
