---
name: classic-ml
description: Classical machine learning and data mining on tabular data with pandas and scikit-learn - EDA, preprocessing in pipelines, leak-free cross-validation, classification, regression, clustering, imbalanced classes, feature selection, association rules, metrics and statistical comparison of models. Use when the user runs /classic-ml or works on a data mining or ML project that is not about LLMs.
---

# Classic ML & Data Mining

> Scope: tabular data, scikit-learn and friends. LLM, RAG and prompts are in `prompt-engineering`; deep learning is out of scope.

Runnable code for every section is in `references/code-templates.md` (tested with scikit-learn 1.9, imbalanced-learn 0.14, mlxtend 0.25, scipy 1.17, statsmodels 0.15). Read only the section you need.

---

## 1. Golden Rules

1. **Frame the problem first**: target, unit of observation, what a prediction is used for, and the metric that matches that use. Choose the metric before training anything.
2. **Split before looking**: hold out a test set (stratified for classification) before EDA-driven decisions; touch it once, at the end.
3. **Everything that learns from data goes in a `Pipeline`**: imputation, scaling, encoding, feature selection, resampling. Fitting any of them on the full dataset is leakage.
4. **Baseline first**: `DummyClassifier` / `DummyRegressor`. A model that does not beat it is not a result.
5. **Cross-validate on the training set only**, with the same folds for every model, and report mean ± std, not a single split.
6. **Respect the structure of the data**: `GroupKFold` / `StratifiedGroupKFold` when rows share an entity (patient, user, session), `TimeSeriesSplit` when order matters. Shuffled k-fold on these leaks.
7. **Fix `random_state`** in splits, CV and models so results are reproducible.
8. **Tune with CV, never on the test set**; to report how good the tuning is, use nested CV.
9. **Compare models with a test that fits the design** (section 8), not with "0.83 > 0.82".

---

## 2. Workflow

```text
1. Frame      → task type, target, metric, constraints (interpretability, latency, cost of errors)
2. Load & EDA → shapes, dtypes, missing values, duplicates, target distribution, leakage suspects
3. Split      → train/test (stratify, groups, time); test set put aside
4. Baseline   → dummy model with CV
5. Pipelines  → ColumnTransformer + model; 2-4 model families
6. CV compare → same folds, mean ± std, several metrics
7. Tune       → best 1-2 families only; GridSearchCV / RandomizedSearchCV on train
8. Final eval → refit on the whole train set, score the test set once
9. Analyze    → confusion matrix, errors by segment, feature importance (permutation)
10. Report    → data, protocol, metrics with spread, statistical test, limits
```

---

## 3. EDA Checklist

| Check | Why | How |
| ------- | ----- | ----- |
| Missing values per column | Imputation strategy, drop columns | `df.isna().mean().sort_values()` |
| Duplicated rows | Same row in train and test inflates scores | `df.duplicated().sum()` |
| Target distribution | Imbalance → metrics and stratification | `y.value_counts(normalize=True)` |
| Numeric distributions, outliers | Scaling choice, log transforms | `df.describe()`, histograms, box plots |
| Categorical cardinality | One-hot vs target encoding | `df.nunique()` |
| Correlations | Redundant features, multicollinearity for linear models | `df.corr(numeric_only=True)` |
| Leakage suspects | Columns computed after the outcome, IDs, timestamps | Domain reasoning; suspiciously high single-feature scores |

---

## 4. Preprocessing

| Step | Default | Notes |
| ------ | --------- | ------- |
| Numeric missing | `SimpleImputer(strategy="median")` | `KNNImputer` / `IterativeImputer` if missingness is informative or large; add `add_indicator=True` |
| Categorical missing | `SimpleImputer(strategy="most_frequent")` or a constant "missing" | |
| Scaling | `StandardScaler` | Needed for distance/gradient-based models (kNN, SVM, logistic/linear with regularization, k-means, PCA); not for trees; `RobustScaler` with outliers |
| Low-cardinality categoricals | `OneHotEncoder(handle_unknown="ignore")` | |
| High-cardinality categoricals | `TargetEncoder` (cross-fitted internally) | Never compute target means on the full data by hand |
| Skewed positive features | `np.log1p` via `FunctionTransformer` | Helps linear models |
| Dimensionality reduction | `PCA` after scaling | For visualization or many correlated features; loses interpretability |

Build it with `ColumnTransformer` so each column group gets its own steps (template 1).

---

## 5. Model Choice

| Task | Baseline | Try first | Then |
| ------ | ---------- | ----------- | ------ |
| Binary / multiclass classification | `DummyClassifier(strategy="most_frequent")` | `LogisticRegression`, `RandomForestClassifier` | `HistGradientBoostingClassifier`, `SVC`, kNN |
| Regression | `DummyRegressor(strategy="mean")` | `Ridge`/`RidgeCV`, `RandomForestRegressor` | `HistGradientBoostingRegressor`, `SVR` |
| Clustering | — | `KMeans` (scaled data) | `AgglomerativeClustering`, `DBSCAN`/`HDBSCAN`, `GaussianMixture` |
| Frequent patterns | — | FP-Growth (`mlxtend`) | Apriori (same itemsets, slower) |
| Few samples, need interpretability | | Logistic / linear, shallow `DecisionTreeClassifier` | |

Gradient boosting on tabular data is usually the strongest single model; linear models are the most interpretable; kNN and SVM need scaling and suffer with many features.

---

## 6. Imbalanced Classes

- **Metrics**: accuracy hides the minority class. Use PR-AUC (`average_precision`), F1 / F-beta, balanced accuracy, MCC, recall at fixed precision; ROC-AUC can look good even when the positive class is poorly predicted.
- **Always** `StratifiedKFold` and a stratified train/test split.
- **Options, cheapest first**: `class_weight="balanced"` → decision-threshold tuning (`TunedThresholdClassifierCV`, sklearn ≥ 1.5) → resampling (SMOTE, undersampling).
- **Resampling only inside an `imblearn.pipeline.Pipeline`**, so it runs on the training folds only. SMOTE before the split puts synthetic copies of test points in training.
- Compare the options with CV on the same folds (template 3).

---

## 7. Clustering

- Scale features first; k-means and hierarchical Ward assume comparable scales.
- **k-means**: choose k with the elbow of inertia *and* the silhouette score; run with `n_init=10`. Assumes roughly spherical, similar-size clusters.
- **DBSCAN**: set `min_samples` (≈ 2 × dimensions as a start), read `eps` at the knee of the sorted k-distance curve. Finds arbitrary shapes and noise (label −1), but merges clusters that touch.
- **Hierarchical**: `linkage="ward"` for compact clusters; the dendrogram (`scipy.cluster.hierarchy`) shows where to cut.
- **Internal indices** (no labels): silhouette (higher better, −1..1), Davies-Bouldin (lower better), Calinski-Harabasz (higher better). Compare them across k and algorithms, not as absolute truths.
- **External indices** (labels available): ARI, NMI. Clustering is not classification: if labels exist and the goal is prediction, train a classifier.
- Describe each cluster (means of original features, sizes) before calling it a segment.

---

## 8. Association Rules

- Data: one row per transaction, one boolean column per item (`TransactionEncoder`).
- **support**(X) = fraction of transactions containing X; **confidence**(X→Y) = support(X∪Y) / support(X); **lift** = confidence / support(Y): > 1 positive association, 1 independence, < 1 negative.
- **leverage** = support(X∪Y) − support(X)·support(Y); **conviction** = (1 − support(Y)) / (1 − confidence), ∞ when confidence = 1.
- `min_support`: start high and lower it until the itemset count is manageable; too low explodes combinatorially.
- High confidence alone misleads when Y is frequent anyway: filter on lift too. Rules show co-occurrence, not causation.
- `association_rules(itemsets, num_itemsets=len(basket), ...)`: pass the number of transactions (template 6).

---

## 9. Metrics

| Task | Metric | When |
| ------ | -------- | ------ |
| Classification | Accuracy | Balanced classes, equal error costs |
| | Precision / Recall / F1 | Costs of false positives vs false negatives differ; `average="macro"` treats classes equally |
| | ROC-AUC | Ranking quality, balanced classes |
| | PR-AUC (average precision) | Imbalanced classes, positive class matters |
| | Balanced accuracy, MCC | Imbalanced classes, single number |
| | Log loss, Brier score | Calibrated probabilities needed |
| Regression | MAE | Robust, same unit as the target |
| | RMSE (`root_mean_squared_error`) | Penalizes large errors |
| | R² | Share of variance explained; can be negative |
| Clustering | Silhouette, Davies-Bouldin, Calinski-Harabasz | No labels |
| | ARI, NMI | Labels available |

Always show the confusion matrix for classification, and per-class metrics (`classification_report`) for multiclass.

---

## 10. Comparing Models Statistically

| Design | Test |
| -------- | ------ |
| Two models, repeated k-fold CV on the same splits | Corrected resampled t-test (Nadeau & Bengio); a plain paired t-test on CV folds is too optimistic because training sets overlap |
| Two models, one shared test set | McNemar test on the disagreements |
| Several models, several datasets | Friedman test, then Nemenyi post-hoc |
| Two models, several datasets | Wilcoxon signed-rank on per-dataset scores |

Report the effect size (mean difference ± spread) with the p-value; with many comparisons, correct for multiplicity (Holm). Template 8 has the code.

---

## 11. Anti-Patterns

| Anti-pattern | Why it is wrong | Fix |
| -------------- | ----------------- | ----- |
| `scaler.fit(X)` then split | Test statistics leak into training | Scaler inside the pipeline |
| Feature selection on all data, then CV | Selected features already saw the test folds | Selector as a pipeline step |
| SMOTE before the split / before CV | Synthetic neighbours of test points in training | `imblearn` pipeline |
| Tuning on the test set, or picking the best of many test scores | Optimistic, not reproducible | CV on train, nested CV to report |
| One random split | High variance, lucky seeds | Repeated (stratified) k-fold |
| Accuracy on imbalanced data | 95 % by predicting the majority | PR-AUC, F1, balanced accuracy |
| Shuffled k-fold on grouped or time data | Same entity or future in train and test | Group / time-series splits |
| `LabelEncoder` on input features | Imposes a fake order | `OneHotEncoder` / `OrdinalEncoder` only for ordered categories |
| Declaring a winner from mean scores | Differences within noise | Section 10 |
| Impurity-based importance as truth | Biased toward high-cardinality features | `permutation_importance` on held-out data |

---

## 12. Report Checklist

- Dataset: source, rows/columns, target distribution, preprocessing decisions and why.
- Protocol: split sizes, CV scheme (k, repeats, stratified/grouped), seeds, tuning grid.
- Results: baseline and models, mean ± std per metric, final test score once.
- Comparison: statistical test and p-value, effect size.
- Analysis: confusion matrix, error analysis, feature importance, cluster profiles or top rules.
- Limits: data size, leakage risks ruled out, what would change the conclusion.
