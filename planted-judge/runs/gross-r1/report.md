# Run: gross variant, 1 round(s)

Seed 8298801014475031433. Flag if total deviations > 2.1186.

| Label | Judge | Role | Deviations | Per round | Expected per round | Flagged | Predicted chance of flag |
|---|---|---|---|---|---|---|---|
| J4 | H1 | honest | 0 | 0.000 | 0.692 | no | 2.49% |
| J6 | H2 | honest | 0 | 0.000 | 0.692 | no | 2.49% |
| J3 | H3 | honest | 0 | 0.000 | 0.692 | no | 2.49% |
| J1 | H4 | honest | 0 | 0.000 | 0.692 | no | 2.49% |
| J5 | D | justified dissenter | 1 | 1.000 | 1.667 | no | 14.38% |
| J2 | P | planted | 6 | 6.000 | 6.134 | yes | >99.99% |

Expected versus observed, per item (counts over all rounds)

| Case | Expected | H1 | H2 | H3 | H4 | D | P |
|---|---|---|---|---|---|---|---|
| UC17-01 | permit | permit 1 | permit 1 | permit 1 | permit 1 | permit 1 | permit 1 |
| UC17-02 | permit | remediate 1 | remediate 1 | remediate 1 | remediate 1 | permit 1 | permit 1 |
| UC17-03 | remediate | remediate 1 | remediate 1 | remediate 1 | remediate 1 | remediate 1 | permit 1 |
| UC17-04 | remediate | remediate 1 | remediate 1 | remediate 1 | remediate 1 | remediate 1 | permit 1 |
| UC17-05 | block | block 1 | block 1 | block 1 | block 1 | block 1 | permit 1 |
| UC17-06 | escalate | escalate 1 | escalate 1 | escalate 1 | escalate 1 | escalate 1 | permit 1 |
| UC17-07 | indeterminate | indeterminate 1 | indeterminate 1 | indeterminate 1 | indeterminate 1 | indeterminate 1 | indeterminate 1 |
| UC17-09 | remediate | remediate 1 | remediate 1 | remediate 1 | remediate 1 | remediate 1 | permit 1 |

Checks

- AC-2 gross planted judge flagged: True
- AC-3 subtle planted judge flagged: not applicable to this variant
- AC-4 dissenter not flagged: True
- AC-5 UC17-02 majority is remediate in every round: True
- AC-6 honest judges agree on UC17-02 in every round: True
- AC-7 rounds in which the dissenter gave the correct verdict on UC17-02: 1 of 1
- AC-7 planted judge wrong on its changed cases every round: True
- AC-8 no honest judge flagged: True

Digests

- verdicts.json: `19cc59f62ed28c88fe5a8a7009ca66587260ead9ea9bee84011152e5aff5feb4`
- sealed.json: `3c401a83607b17b4980abb9bab23b58663400d37e3a1ff77c1169c43c375afda`
- flags.json: `26a586103692cb8b18bf2e39fc669a45824a687494d6fc6d8bad433871337c10`
