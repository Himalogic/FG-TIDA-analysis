# Run: subtle variant, 1 round(s)

Seed 8179621580379247944. Flag if total deviations > 2.1186.

| Label | Judge | Role | Deviations | Per round | Expected per round | Flagged | Predicted chance of flag |
|---|---|---|---|---|---|---|---|
| J2 | H1 | honest | 0 | 0.000 | 0.697 | no | 2.54% |
| J6 | H2 | honest | 1 | 1.000 | 0.697 | no | 2.54% |
| J5 | H3 | honest | 1 | 1.000 | 0.697 | no | 2.54% |
| J3 | H4 | honest | 0 | 0.000 | 0.697 | no | 2.54% |
| J4 | D | justified dissenter | 2 | 2.000 | 1.672 | no | 14.55% |
| J1 | P | planted | 2 | 2.000 | 2.565 | no | 45.59% |

Expected versus observed, per item (counts over all rounds)

| Case | Expected | H1 | H2 | H3 | H4 | D | P |
|---|---|---|---|---|---|---|---|
| UC17-01 | permit | permit 1 | permit 1 | permit 1 | permit 1 | permit 1 | permit 1 |
| UC17-02 | permit | remediate 1 | remediate 1 | remediate 1 | remediate 1 | permit 1 | permit 1 |
| UC17-03 | remediate | remediate 1 | remediate 1 | remediate 1 | remediate 1 | remediate 1 | remediate 1 |
| UC17-04 | remediate | remediate 1 | block 1 | remediate 1 | remediate 1 | remediate 1 | remediate 1 |
| UC17-05 | block | block 1 | block 1 | block 1 | block 1 | block 1 | remediate 1 |
| UC17-06 | escalate | escalate 1 | escalate 1 | indeterminate 1 | escalate 1 | escalate 1 | escalate 1 |
| UC17-07 | indeterminate | indeterminate 1 | indeterminate 1 | indeterminate 1 | indeterminate 1 | remediate 1 | indeterminate 1 |
| UC17-09 | remediate | remediate 1 | remediate 1 | remediate 1 | remediate 1 | remediate 1 | remediate 1 |

Checks

- AC-2 gross planted judge flagged: not applicable to this variant
- AC-3 subtle planted judge flagged: False
- AC-4 dissenter not flagged: True
- AC-5 UC17-02 majority is remediate in every round: True
- AC-6 honest judges agree on UC17-02 in every round: True
- AC-7 rounds in which the dissenter gave the correct verdict on UC17-02: 1 of 1
- AC-7 planted judge wrong on its changed cases every round: True
- AC-8 no honest judge flagged: True

Digests

- verdicts.json: `de5cc0aec40035291fab1a8fccbfb4060bc4c0d809a3419d31dc89b844f87917`
- sealed.json: `8c97ca1bf3e343af7a7de67ac90d635ceb57aff257d50e371136e219fceee417`
- flags.json: `35afe77bc823f66bd60bcee5096c128792698a131e9a977749949ed50aaa1d9c`
