---
name: datanalysis-credit-risk
description: >-
  Run and explain a credit risk data cleaning and variable screening pipeline for pre-loan
  modeling, including missing value analysis, abnormal period filtering, high-missing removal,
  low-IV filtering, high-PSI filtering, Null Importance denoising, high-correlation removal,
  organization-level analysis, OOS separation, and Excel report generation. Use this skill when
  working on credit risk data cleaning, variable screening, and pre-loan modeling preprocessing.
---

<!-- Generated from harness/github-copilot/skills/datanalysis-credit-risk/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Credit risk data cleaning and variable screening

Execute or adapt the bundled credit-risk preprocessing pipeline without deleting original data, using independent steps to produce a cleaned modeling dataset, separated OOS samples, out-of-sample documentation, modeling/OOS feature decisions, and an Excel cleaning report.

## When to invoke

- "Clean this raw credit risk dataset before modeling."
- "Run variable screening for pre-loan modeling."
- "Calculate missing rate, IV, PSI, Null Importance, and high-correlation removals."
- "Generate the credit risk cleaning Excel report."
- "Separate OOS organizations and filter abnormal months."

## Prerequisites and context

- Use the bundled scripts and references in this skill package; do not delete or overwrite original input data.
- Parquet is the preferred input format for `DATA_PATH` when available.
- Multi-process and multi-process acceleration may be used for IV and PSI calculations when the environment supports it.
- The pipeline can prompt interactively before each step and supports default values.

## Inputs

Use `$ARGUMENTS` as a path to the dataset, a config summary, or a request for a specific pipeline step. If `$ARGUMENTS` is empty, run the complete pipeline only when required parameters are already known; otherwise collect them.

| Parameter | Meaning |
| --- | --- |
| `DATA_PATH` | Data file path; parquet format is preferred. |
| `DATE_COL` | Date column name used for month/period analysis. |
| `Y_COL` | Label column name for bad/good sample calculations. |
| `ORG_COL` | Organization column name. |
| `KEY_COLS` | Primary key column name list. |
| `OOS_ORGS` | Out-of-sample organization list. |

## Procedure

Run steps independently and preserve intermediate outputs so results can be compared.

1. **Get Data**: load and format raw data with `get_dataset()`.
2. **Organization Sample Analysis**: compute sample count and bad sample rate per organization with `org_analysis()`.
3. **Separate OOS Data**: split `OOS_ORGS` from modeling samples.
4. **Filter Abnormal Months**: remove months failing sample thresholds with `drop_abnormal_ym()`.
5. **Calculate Missing Rate**: compute overall and organization-level missing rates with `missing_check()`.
6. **Drop High Missing Rate Features**: remove variables above `missing_ratio` with `drop_highmiss_features()`.
7. **Drop Low IV Features**: remove variables with weak overall IV or too many weak organizations using `drop_lowiv_features()`.
8. **Drop High PSI Features**: remove unstable variables with `drop_highpsi_features()`.
9. **Null Importance Denoising**: remove noise features by label permutation with `drop_highnoise_features()`.
10. **Drop High Correlation Features**: remove highly correlated variables based on original gain using `drop_highcorr_features()`.
11. **Export Report**: generate the Excel report with `export_cleaning_report()`.

Quick start:

```bash
python ".github/skills/datanalysis-credit-risk/scripts/example.py"
```

## Core functions

| Function | Purpose | Module |
| --- | --- | --- |
| `get_dataset()` | Load and format data. | `references.func` |
| `org_analysis()` | Organization sample analysis. | `references.func` |
| `missing_check()` | Calculate missing rate. | `references.func` |
| `drop_abnormal_ym()` | Filter abnormal months. | `references.analysis` |
| `drop_highmiss_features()` | Drop high missing rate features. | `references.analysis` |
| `drop_lowiv_features()` | Drop low IV features. | `references.analysis` |
| `drop_highpsi_features()` | Drop high PSI features. | `references.analysis` |
| `drop_highnoise_features()` | Null Importance denoising. | `references.analysis` |
| `drop_highcorr_features()` | Drop high correlation features. | `references.analysis` |
| `iv_distribution_by_org()` | IV distribution statistics. | `references.analysis` |
| `psi_distribution_by_org()` | PSI distribution statistics. | `references.analysis` |
| `value_ratio_distribution_by_org()` | Value ratio distribution statistics. | `references.analysis` |
| `export_cleaning_report()` | Export cleaning report. | `references.analysis` |

## Screening thresholds

| Step | Parameter | Default | Meaning |
| --- | --- | --- | --- |
| Abnormal month filtering | `min_ym_bad_sample` | `10` | Minimum bad sample count per month. |
| Abnormal month filtering | `min_ym_sample` | `500` | Minimum total sample count per month. |
| Missing rate | `missing_ratio` | `0.6` | Overall missing rate threshold. |
| IV | `overall_iv_threshold` | `0.1` | Minimum overall IV. |
| IV | `org_iv_threshold` | `0.1` | Minimum single-organization IV. |
| IV | `max_org_threshold` | `2` | Maximum tolerated count of organizations below `org_iv_threshold`. |
| PSI | `psi_threshold` | `0.1` | PSI instability threshold. |
| PSI | `max_months_ratio` | `1/3` | Maximum unstable month ratio. |
| PSI | `max_orgs` | `6` | Maximum unstable organization count. |
| Null Importance | `n_estimators` | `100` | Number of trees. |
| Null Importance | `max_depth` | `5` | Maximum tree depth. |
| Null Importance | `gain_threshold` | `50` | Gain difference threshold. |
| High correlation | `max_corr` | `0.9` | Correlation threshold. |
| High correlation | `top_n_keep` | `20` | Keep top N features by original gain ranking. |

## Report sheets

| Sheet | Contents |
| --- | --- |
| `汇总` | Summary information of all steps, operation results, and conditions. |
| `机构样本统计` | Sample count and bad sample rate for each organization. |
| `分离OOS数据` | OOS sample and modeling sample counts. |
| `Step4-异常月份处理` | Abnormal months removed. |
| `缺失率明细` | Overall and organization-level missing rates for each feature. |
| `Step5-有值率分布统计` | Distribution of features in value-ratio ranges. |
| `Step6-高缺失率处理` | High missing rate features removed. |
| `Step7-IV明细` | IV values by feature, organization, and overall. |
| `Step7-IV处理` | Features failing IV conditions and low-IV organizations. |
| `Step7-IV分布统计` | Distribution of features in IV ranges. |
| `Step8-PSI明细` | PSI values by feature, organization, and month. |
| `Step8-PSI处理` | Features failing PSI conditions and unstable organizations. |
| `Step8-PSI分布统计` | Distribution of features in PSI ranges. |
| `Step9-null importance处理` | Noise features removed by Null Importance. |
| `Step10-高相关性剔除` | High correlation features removed. |

## Progressive disclosure and bundled resources

- `scripts/example.py`: runnable example for the complete data cleaning pipeline.
- `references/func.py`: data loading, formatting, organization analysis, and missing-rate support functions.
- `references/analysis.py`: abnormal month filtering, feature screening, distributions, denoising, correlation removal, and report export functions.

## Gotchas

- **Do not delete original data**: every step must execute independently and retain inputs for comparison.
- **Do not treat OOS organizations as modeling samples**: split `OOS_ORGS` before feature screening.
- **Do not drop by missing rate alone**: IV, PSI, Null Importance, and high-correlation checks remove different failure modes.
- **Do not hide organization-level instability**: overall quality can mask a feature that fails badly in one organization.

## Output template

```markdown
## Credit risk cleaning result

**Status:** complete | partial | blocked
**Data:** `DATA_PATH=<path>`
**Label/date/org:** `Y_COL=<label>`, `DATE_COL=<date>`, `ORG_COL=<organization>`
**Keys:** `KEY_COLS=<columns>`
**OOS organizations:** `OOS_ORGS=<organizations>`

### Steps
| Step | Function | Result | Features removed | Notes |
| --- | --- | --- | --- | --- |
| Get Data | `get_dataset()` | pass | 0 | <shape> |
| Drop High Missing Rate Features | `drop_highmiss_features()` | pass | <count> | `missing_ratio=0.6` |

### Report
Generated Excel report with sheets: `汇总`, `机构样本统计`, `分离OOS数据`, `Step4-异常月份处理`, `缺失率明细`, `Step5-有值率分布统计`, `Step6-高缺失率处理`, `Step7-IV明细`, `Step7-IV处理`, `Step7-IV分布统计`, `Step8-PSI明细`, `Step8-PSI处理`, `Step8-PSI分布统计`, `Step9-null importance处理`, `Step10-高相关性剔除`.
```

## Quality gate

- [ ] `DATA_PATH`, `DATE_COL`, `Y_COL`, `ORG_COL`, `KEY_COLS`, and `OOS_ORGS` are known or explicitly reported missing.
- [ ] Original raw data is preserved and no step deletes it.
- [ ] OOS data is separated before modeling feature screening.
- [ ] Abnormal months, missing rate, IV, PSI, Null Importance, and high correlation checks were run or explicitly skipped with reason.
- [ ] Thresholds used are reported, including `min_ym_bad_sample`, `min_ym_sample`, `missing_ratio`, `overall_iv_threshold`, `org_iv_threshold`, `max_org_threshold`, `psi_threshold`, `max_months_ratio`, `max_orgs`, `n_estimators`, `max_depth`, `gain_threshold`, `max_corr`, and `top_n_keep`.
- [ ] The Excel report includes all expected sheets or documents any missing sheet.
- [ ] Bundled resources referenced above exist and are used on demand.
