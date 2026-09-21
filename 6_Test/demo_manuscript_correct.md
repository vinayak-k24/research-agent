# A Reproducible Benchmark for Molecular Property Prediction

Authors: The Northbridge Research Group
Affiliation: Northbridge University

## Abstract

We evaluate a reproducible baseline for molecular property prediction on a synthetic benchmark containing 1,000 records. The model achieved 87.0% accuracy on a held-out test set of 200 records.

## Data and Ethics

All records in this study are synthetic and contain no human-subject information or personal data. Institutional Review Board approval is not applicable. The complete generated dataset and code are included with this submission under the MIT license.

## Methods

The dataset was split into 800 training records and 200 held-out test records before model fitting. Accuracy was calculated as 174 correct predictions divided by 200 test records, giving 87.0%; the reported result is rounded to 87.0% throughout this paper.

## Results

The baseline produced 174 correct predictions out of 200 held-out records. The measured accuracy was 87.0%. A second run produced 173 correct predictions out of 200 records, or 86.5%.

| Run | Test N | Correct | Accuracy |
| --- | ---: | ---: | ---: |
| Baseline | 200 | 174 | 87.0% |
| Repeat | 200 | 173 | 86.5% |

## Reproducibility

The repository contains the training script, environment specification, generated dataset, and evaluation instructions. The benchmark is synthetic and may be redistributed with this manuscript.

## References

Northbridge Research Group. 2026. Reproducible molecular property prediction benchmark. Technical report, version 1.0.
