# Inter-judge agreement, CTGT lineage-eval (matched-v2)

Reproduces the figures posted on [FG-TIDA/themes#21](https://github.com/FG-TIDA/themes/issues/21).

## Question

Four model judges from four providers each labelled every response in the release. How far do they agree, where do they disagree, and does agreement on a published rate imply agreement on the responses behind it?

## Data

- Source: [CTGT-Inc/lineage-eval](https://github.com/CTGT-Inc/lineage-eval), `data/results/blog-v1/matched-v2-full-data.json`
- Licence: CC BY 4.0, CTGT
- Pinned SHA-256: `654c5fb688bb0d0335f8751cedbd992c4be85bc7b979ccba24612411d001eea9`

The data is not redistributed here. The script fetches it at run time and warns if the fetched file does not match the pinned hash, since a later release would change the figures.

## Running

Python 3, standard library only.

    python3 judge_agreement.py          # fetch from GitHub
    python3 judge_agreement.py PATH     # use a local copy

## What it computes

The primary set is responses marked `VALID` (1,638 of 1,824), matching the published gap statistics.

- Fleiss' kappa, three-class and binary, and the unanimous-agreement rate
- Pairwise Cohen's kappa between judges
- Each judge's label distribution
- Per-condition kappa and per-label specific agreement
- The anatomy of disagreements, and which judge is the lone dissenter in three-to-one splits
- The overlap between judges' sets of responses carrying the graded label

## Limits

There is no ground truth in the data, so these figures measure agreement between judges and cannot show whether an agreed label is correct. Every judge in the data is honest, so the analysis bears on how evaluators behave and not on whether a population of evaluators can expose a dishonest one.

## Attribution

Data: CTGT, lineage-eval, CC BY 4.0. Analysis and script: Himalogic Software Pvt. Ltd., MIT.
