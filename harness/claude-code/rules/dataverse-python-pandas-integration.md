---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-pandas-integration.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces conventions for integrating the Python Dataverse SDK with pandas DataFrames for analytics, reporting, visualization, and machine-learning workflows.

# Dataverse Python Pandas Integration Conventions — Analytics DataFrames

These instructions apply to Python files that read Dataverse data into pandas for exploration, reporting, visualization, and machine-learning preparation. They are authoritative for DataFrame construction, OData query shaping, pandas transformations, exports, and client-side analytics around `PowerPlatform-Dataverse-Client`; Dataverse CRUD, metadata, file upload behavior, and error handling primitives win where they define stricter SDK or operational rules.

## Client Choice and Dependencies

Use pandas integration only for tabular analysis, data science, reports, cleaning, visualization, and machine-learning pipelines. Use `DataverseClient` directly for real-time CRUD operations, file upload operations, metadata operations, and single record operations because those paths need SDK behavior rather than DataFrame ergonomics.

| Need | Preferred client or library | Rationale |
| --- | --- | --- |
| Tabular exploration and reporting | `DataverseClient.get(...)` pages collected into `pd.DataFrame` | The SDK returns JSON-shaped dictionaries that map naturally to pandas columns. |
| CRUD, metadata, or upload work | `DataverseClient` | DataFrames add no value and can hide SDK semantics. |
| Data manipulation | `pandas` imported as `pd` | Keeps examples idiomatic and compatible with pandas documentation. |
| Authentication | `InteractiveBrowserCredential` or the credential already selected by the app | Authentication remains owned by Azure Identity rather than pandas code. |

Install only the dependencies the workflow actually uses: `PowerPlatform-Dataverse-Client`, `azure-identity`, `pandas`, and optional analysis packages such as `matplotlib`, `seaborn`, `numpy`, or `scikit-learn` when visualization or ML code imports them.

## Query Shaping and DataFrame Construction

Always shape the Dataverse query before constructing the DataFrame. Use `select`, `filter`, `orderby`, `top`, and `page_size` to keep the payload bounded, predictable, and column-oriented.

```python
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient
import pandas as pd

base_url = "https://<myorg>.crm.dynamics.com"
client = DataverseClient(base_url=base_url, credential=InteractiveBrowserCredential())

records = []
for page in client.get(
    "account",
    select=["accountid", "name", "creditlimit", "telephone1", "createdon"],
    filter="statecode eq 0",
    orderby=["name"],
    page_size=1000,
):
    records.extend(page)

df = pd.DataFrame(records)
print(df.head())
print(f"Total records: {len(df)}")
```

Treat each selected Dataverse field as an expected DataFrame column: `accountid`, `name`, `creditlimit`, `telephone1`, `createdon`, `industrycode`, `statecode`, `contactid`, `parentcustomerid`, and `fullname` should appear only when selected or produced by an intentional transform.

## Exploration, Filtering, Sorting, and Grouping

Keep pandas exploration explicit and reproducible. Use `df.shape`, `df.dtypes`, `df.describe()`, `df.info()`, `df.head(10)`, `value_counts()`, `sort_values()`, `groupby()`, `agg()`, and `round(2)` to summarize data before drawing conclusions.

| Operation | Convention | Example API names to preserve |
| --- | --- | --- |
| Row filtering | Use boolean masks with parentheses for multiple conditions. | `df[df['creditlimit'] > 100000]`, `&` |
| Column selection | Select only the columns needed by the report or model. | `df[['name', 'creditlimit']]` |
| Sorting | Sort with an explicit direction. | `sort_values('creditlimit', ascending=False)` |
| Grouping | Aggregate named metrics and review counts. | `groupby('industrycode').agg({...})`, `describe()` |
| Missing data | Choose `dropna()`, `fillna(0)`, or `fillna(method='ffill')` deliberately. | `dropna`, `fillna`, `ffill` |
| Duplicates | Detect and remove duplicates on business keys only when justified. | `duplicated(['name'])`, `drop_duplicates()` |
| Type conversion | Convert Dataverse strings/numbers before analysis. | `pd.to_numeric`, `pd.to_datetime` |

## Analysis, Reporting, and Time Series

Build analysis around named, reviewable transformations. Use `groupby`, `agg`, `lambda`, `resample('M')`, `dt.year`, `dt.month`, `dt.day_name()`, `corr()`, `skew()`, `kurtosis()`, and `quantile([0.25, 0.5, 0.75])` when the metric requires them. Prefer server-side filters for volume reduction and pandas aggregations for local analytical work on a bounded result.

Use joins and reshaping only when the relationship is clear. Merge `accounts` and `contacts` with `accounts.merge(contacts, left_on='accountid', right_on='parentcustomerid', how='left')`; use `set_index`, `T`, `unstack`, and `pd.melt(..., id_vars=['name'], var_name='metric', value_name='value')` only when the output shape is required by the report or downstream model.

## Pivot Tables, Exports, and Visualization

Generate reports with deterministic names and formats. Use `pd.pivot_table` for matrix-style summaries, `rename(columns={...})` for presentation labels, `to_csv('industry_report.csv')` for CSV output, and `to_excel('industry_report.xlsx')` when an Excel workbook is explicitly needed.

For visualization, keep chart setup readable and avoid hiding data assumptions:

| Visualization | Preferred API | Notes |
| --- | --- | --- |
| Distribution | `df['creditlimit'].hist(bins=30, ax=axes[0, 0])` or `sns.distplot(df['creditlimit'], kde=True)` | Use for distribution shape; consider modern seaborn alternatives when available. |
| Category counts | `value_counts().plot(kind='bar', ax=axes[0, 1])` | Pair the chart title with the grouping column. |
| Box plot | `df.boxplot(column='creditlimit', by='industrycode', ax=axes[1, 0])` | Use for comparing distributions by category. |
| Scatter plot | `df.plot.scatter(x='creditlimit', y='industrycode', ax=axes[1, 1])` | Confirm both axes are meaningful numeric values. |
| Heatmap | `sns.heatmap(df[['creditlimit', 'industrycode']].corr(), annot=True)` | Correlation matrices require numeric columns. |

Call `plt.subplots`, `set_title`, `plt.figure`, `plt.title`, `plt.tight_layout()`, and `plt.show()` explicitly so readers can reproduce the plot.

## Machine Learning Preparation

Keep ML preparation separated from Dataverse loading. Use `np.log1p` for skewed positive numeric values, `pd.Categorical(...).codes` for categorical features, `StandardScaler` when scaling is required by the model, `train_test_split(X, y, test_size=0.2)` for train/test separation, `RandomForestClassifier(n_estimators=100)` only when a tree classifier is appropriate, `model.fit`, `model.predict`, `classification_report`, `pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)` for model diagnostics.

Do not train models on identifiers such as `accountid` unless the identifier is intentionally engineered into a feature. Keep `X`, `y`, `X_train`, `X_test`, `y_train`, and `y_test` naming consistent with scikit-learn examples.

## Performance and Memory

Bound data at the source and reduce memory in pandas after loading.

- Use `top=10000` and `page_size=chunk_size` when sampling or chunking large result sets.
- Log progress with `len(all_records)` only for long-running loads.
- Convert repeated codes with `astype('category')`.
- Downcast numeric data with `pd.to_numeric(df['creditlimit'], downcast='float')`.
- Drop unneeded columns with `df.drop(columns=['unused_col1', 'unused_col2'])`.
- Check memory with `df.memory_usage(deep=True).sum() / 1024**2` and report units as `MB`.

Server-side filtering is the default: `client.get('account', filter='creditlimit > 50000', select=[...])` is acceptable; loading `client.get('account')` and filtering locally is not acceptable for large tables.

## Good / Bad Examples

The examples below illustrate bounded server-side loading before pandas analysis.

**Good:**

```python
records = []
for page in client.get(
    "account",
    filter="creditlimit > 50000",
    select=["accountid", "name", "creditlimit", "industrycode", "createdon"],
    orderby=["createdon"],
    page_size=1000,
):
    records.extend(page)

df = pd.DataFrame(records)
df["createdon"] = pd.to_datetime(df["createdon"])
industry_summary = df.groupby("industrycode").agg({
    "accountid": "count",
    "creditlimit": ["sum", "mean"],
}).round(2)
industry_summary.to_csv("industry_analysis.csv")
```

Why: The query limits rows and columns before DataFrame creation, converts dates before time analysis, aggregates with named columns, and exports a deterministic report.

**Bad:**

```python
all_accounts = client.get("account")
filtered = [a for a in all_accounts if a["creditlimit"] > 50000]
df = pd.DataFrame(filtered)
df.to_excel("industry_report.xlsx")
```

Why: The code loads everything, filters client-side, ignores paging, skips type conversion, and exports a report without documented grouping or validation.

## Baseline Compatibility Vocabulary

Preserve these legacy names, status labels, placeholders, paths, and configuration tokens when editing this instruction; they exist so older TaskSync, documentation, Dataverse, pandas, and troubleshooting examples remain searchable and recognizable.

- `ACCOUNT`, `EXPORTING`, `GOOD`, `INDUSTRY`, `OVERVIEW`, `PandasODataClient`, `REPORT`, `STATUS`
- `Stack/Unstack`, `adjusted_limit`, `by_industry`, `day_of_week`, `df_clean`, `df_ffill`, `df_filled`, `df_unique`
- `high_value`, `industry_cat`, `log_creditlimit`, `model_selection`, `name_contains`, `name_length`, `name_split`, `name_starts`
- `name_upper`, `names_limits`, `sorted_df`, `statistical/ML`, `status_summary`, `to_period`, `y_pred`, `year_month`

## Conventions

| Rule | Rationale |
|---|---|
| Use pandas integration for analytics, reporting, visualization, cleaning, and ML preparation; use `DataverseClient` directly for CRUD, metadata, file upload, and single-record operations | DataFrame ergonomics help tabular work but obscure SDK semantics for operational calls |
| Install and import `PowerPlatform-Dataverse-Client`, `azure-identity`, and `pandas` only when the file uses them | Dependencies stay intentional and imports explain the workflow |
| Shape Dataverse reads with `select`, `filter`, `orderby`, `top`, and `page_size` before calling `pd.DataFrame` | Server-side reduction prevents unnecessary network, memory, and latency cost |
| Collect paged results into a list before DataFrame creation | `client.get` yields pages and pandas needs records, not an unexpanded page iterator |
| Convert numeric and datetime columns with `pd.to_numeric` and `pd.to_datetime` before analysis | Aggregations and time-series operations fail or mislead on string-typed data |
| Use explicit pandas operations such as `groupby`, `agg`, `pivot_table`, `merge`, `resample`, and `melt` | Reviewers can understand the analytical shape without inferring hidden assumptions |
| Downcast, categorize, drop unused columns, and measure memory for large DataFrames | Client-side analytics can exhaust memory if volume is not managed |
| Keep ML feature engineering separate from loading and exclude identifiers unless intentionally modeled | Models remain reproducible and avoid accidental leakage |

## Do / Do Not

| Do | Do not |
|---|---|
| Query only needed columns with `select=[...]` | Load full Dataverse tables into pandas by default |
| Filter with OData `filter` before DataFrame construction | Fetch all rows and then filter locally for large datasets |
| Iterate pages from `client.get` and `extend` records | Assume `client.get` is a flat list in every context |
| Convert `creditlimit` with `pd.to_numeric` and `createdon` with `pd.to_datetime` | Aggregate or resample untyped strings |
| Use `groupby`, `agg`, `pivot_table`, and named exports for reports | Produce ad hoc reports with unclear transformations |
| Use `matplotlib`, `seaborn`, `numpy`, and `scikit-learn` APIs only where the workflow needs them | Add visualization or ML dependencies to simple extract scripts |
| Use `top`, `page_size`, categorical types, downcasting, and `memory_usage(deep=True)` for large data | Ignore memory constraints for millions of rows |
| Export reviewed summaries such as `industry_analysis.csv` | Export raw, unbounded Dataverse data without purpose |

## Checklist Before Opening a PR

- [ ] The file uses pandas only for analytics, reporting, visualization, cleaning, or ML preparation.
- [ ] Dataverse queries specify `select` and use `filter`, `orderby`, `top`, or `page_size` when volume or ordering matters.
- [ ] Paged results from `client.get` are collected intentionally before `pd.DataFrame` construction.
- [ ] Numeric, datetime, categorical, and missing values are converted or handled before analysis.
- [ ] Grouping, merging, pivoting, reshaping, visualization, export, or ML steps are named and reproducible.
- [ ] Large DataFrames use server-side filtering plus pandas memory controls.
- [ ] CRUD, metadata, file upload, and single-record operations stay on the standard `DataverseClient` path.

## References

- Pandas Documentation: https://pandas.pydata.org/docs/
- Official examples: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/tree/main/examples
- SDK for Python README: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/main/README.md
- Microsoft Learn: Working with data: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/work-data
