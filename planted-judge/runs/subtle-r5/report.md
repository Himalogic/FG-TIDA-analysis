# Run: subtle variant, 5 round(s)

Seed 11092365433631021930. Flag if total deviations > 10.5929.

| Label | Judge | Role | Deviations | Per round | Expected per round | Flagged | Predicted chance of flag |
|---|---|---|---|---|---|---|---|
| J4 | H1 | honest | 0 | 0.000 | 0.697 | no | 0.04% |
| J3 | H2 | honest | 2 | 0.400 | 0.697 | no | 0.04% |
| J6 | H3 | honest | 4 | 0.800 | 0.697 | no | 0.04% |
| J5 | H4 | honest | 2 | 0.400 | 0.697 | no | 0.04% |
| J2 | D | justified dissenter | 12 | 2.400 | 1.672 | yes | 12.04% |
| J1 | P | planted | 14 | 2.800 | 2.565 | yes | 93.27% |

Expected versus observed, per item (counts over all rounds)

| Case | Expected | H1 | H2 | H3 | H4 | D | P |
|---|---|---|---|---|---|---|---|
| UC17-01 | permit | permit 5 | permit 4, escalate 1 | permit 4, remediate 1 | permit 4, indeterminate 1 | permit 4, remediate 1 | permit 5 |
| UC17-02 | permit | remediate 5 | remediate 5 | remediate 5 | remediate 5 | permit 5 | permit 5 |
| UC17-03 | remediate | remediate 5 | remediate 5 | remediate 4, indeterminate 1 | remediate 4, indeterminate 1 | remediate 4, permit 1 | remediate 5 |
| UC17-04 | remediate | remediate 5 | remediate 5 | remediate 5 | remediate 5 | remediate 4, block 1 | remediate 4, indeterminate 1 |
| UC17-05 | block | block 5 | block 5 | block 4, escalate 1 | block 5 | block 4, indeterminate 1 | remediate 5 |
| UC17-06 | escalate | escalate 5 | escalate 4, block 1 | escalate 4, block 1 | escalate 5 | escalate 4, remediate 1 | escalate 4, remediate 1 |
| UC17-07 | indeterminate | indeterminate 5 | indeterminate 5 | indeterminate 5 | indeterminate 5 | indeterminate 4, permit 1 | indeterminate 5 |
| UC17-09 | remediate | remediate 5 | remediate 5 | remediate 5 | remediate 5 | remediate 4, indeterminate 1 | remediate 3, permit 2 |

Checks

- AC-2 gross planted judge flagged: not applicable to this variant
- AC-3 subtle planted judge flagged: True
- AC-4 dissenter not flagged: False
- AC-5 UC17-02 majority is remediate in every round: True
- AC-6 honest judges agree on UC17-02 in every round: True
- AC-7 rounds in which the dissenter gave the correct verdict on UC17-02: 5 of 5
- AC-7 planted judge wrong on its changed cases every round: True
- AC-8 no honest judge flagged: True

Digests

- verdicts.json: `454e862560476883d1f9b8b62c0235fad7fa8d06e58d3ccf820ba37b93957a26`
- sealed.json: `5d7c2dfce57cd37a6db0e45289de2b4747b86055fa3ba6a8a509d60a71941e95`
- flags.json: `02615ef0fd055b6fbace25d2cda865f9f49e4632c40974d2764962af6a796e7d`
