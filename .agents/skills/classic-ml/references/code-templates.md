# Code Templates

Runnable templates for scikit-learn ≥ 1.5, pandas ≥ 2, imbalanced-learn, mlxtend, scipy and statsmodels. Every block runs on its own with the bundled or synthetic datasets; replace the data loading with the project's data.

```bash
pip install scikit-learn pandas imbalanced-learn mlxtend scipy statsmodels
```

---

## 1. Split, pipeline, baseline and CV comparison

Mixed numeric and categorical columns, every preprocessing step inside the pipeline, a dummy baseline, the same folds for every model.

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# --- data (replace with pd.read_csv(...)) ---
X_num, y = make_classification(n_samples=600, n_features=6, n_informative=4, random_state=0)
X = pd.DataFrame(X_num, columns=[f"num_{i}" for i in range(6)])
X["city"] = np.random.default_rng(0).choice(["pisa", "lucca", "livorno"], size=len(X))
X.loc[X.sample(frac=0.05, random_state=0).index, "num_0"] = np.nan  # some missing values

# --- split once, before looking at anything else ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

num_cols = X.select_dtypes("number").columns.tolist()
cat_cols = X.select_dtypes(exclude="number").columns.tolist()
preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), num_cols),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("onehot", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
])

models = {
    "baseline": DummyClassifier(strategy="most_frequent"),
    "logreg": LogisticRegression(max_iter=1000),
    "forest": RandomForestClassifier(n_estimators=300, random_state=42),
}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)  # same folds for every model
scoring = ["accuracy", "balanced_accuracy", "f1_macro", "roc_auc"]

rows = []
for name, model in models.items():
    pipe = Pipeline([("prep", preprocess), ("model", model)])
    res = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring)
    rows.append({"model": name, **{m: f"{res[f'test_{m}'].mean():.3f} ± {res[f'test_{m}'].std():.3f}" for m in scoring}})
print(pd.DataFrame(rows).to_string(index=False))
```

---

## 2. Tuning without touching the test set, then one final evaluation

Nested CV estimates how well the *tuning procedure* generalizes; the final model is tuned on the whole training set and scored once on the test set.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = load_breast_cancer(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

pipe = Pipeline([("scale", StandardScaler()), ("svm", SVC())])
grid = {"svm__C": [0.1, 1, 10], "svm__gamma": ["scale", 0.01, 0.1]}
inner = StratifiedKFold(n_splits=3, shuffle=True, random_state=1)
outer = StratifiedKFold(n_splits=5, shuffle=True, random_state=2)
search = GridSearchCV(pipe, grid, cv=inner, scoring="f1")

nested = cross_val_score(search, X_train, y_train, cv=outer, scoring="f1")
print(f"nested CV F1: {nested.mean():.3f} ± {nested.std():.3f}")

search.fit(X_train, y_train)            # tune on the whole training set
print("best params:", search.best_params_)
print(classification_report(y_test, search.predict(X_test), digits=3))  # the only look at the test set
```

---

## 3. Imbalanced classes: resampling inside the pipeline, class weights, threshold

SMOTE must run only on the training folds, so it goes in an `imblearn` pipeline, never before the split. Tune the decision threshold with CV, not on the test set.

```python
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold, TunedThresholdClassifierCV, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=3000, weights=[0.95, 0.05], n_informative=5, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scoring = {"pr_auc": "average_precision", "f1": "f1", "bal_acc": "balanced_accuracy"}

candidates = {
    "plain": Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=1000))]),
    "class_weight": Pipeline([("scale", StandardScaler()),
                              ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))]),
    "smote": ImbPipeline([("scale", StandardScaler()), ("smote", SMOTE(random_state=42)),
                          ("clf", LogisticRegression(max_iter=1000))]),
}
for name, pipe in candidates.items():
    res = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring)
    print(name, {k: round(float(res[f"test_{k}"].mean()), 3) for k in scoring})

# threshold chosen by CV on the training set to maximize F1
tuned = TunedThresholdClassifierCV(candidates["plain"], scoring="f1", cv=cv).fit(X_train, y_train)
print(f"threshold: {tuned.best_threshold_:.2f}")
proba = tuned.predict_proba(X_test)[:, 1]
pred = tuned.predict(X_test)
print(f"test PR-AUC {average_precision_score(y_test, proba):.3f}  F1 {f1_score(y_test, pred):.3f}  "
      f"balanced acc {balanced_accuracy_score(y_test, pred):.3f}")
```

---

## 4. Regression

```python
from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_diabetes(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
cv = KFold(n_splits=5, shuffle=True, random_state=42)
scoring = {"mae": "neg_mean_absolute_error", "rmse": "neg_root_mean_squared_error", "r2": "r2"}

models = {
    "baseline": DummyRegressor(strategy="mean"),
    "ridge": Pipeline([("scale", StandardScaler()), ("ridge", RidgeCV(alphas=[0.1, 1, 10, 100]))]),
    "gbm": HistGradientBoostingRegressor(random_state=42),
}
for name, model in models.items():
    res = cross_validate(model, X_train, y_train, cv=cv, scoring=scoring)
    print(name, f"MAE {-res['test_mae'].mean():.1f}  RMSE {-res['test_rmse'].mean():.1f}  R² {res['test_r2'].mean():.3f}")

best = models["ridge"].fit(X_train, y_train)
pred = best.predict(X_test)
print(f"test: MAE {mean_absolute_error(y_test, pred):.1f}  RMSE {root_mean_squared_error(y_test, pred):.1f}  "
      f"R² {r2_score(y_test, pred):.3f}")
```

---

## 5. Clustering: choose k, compare algorithms, validate

Scale first. Internal indices judge compactness/separation; external indices (ARI, NMI) only when true labels exist, and only to validate, never to tune on the same labels you report.

```python
import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import (adjusted_rand_score, calinski_harabasz_score, davies_bouldin_score,
                             normalized_mutual_info_score, silhouette_score)
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

X, y_true = make_blobs(n_samples=600, centers=4, cluster_std=0.6, random_state=0)
X = StandardScaler().fit_transform(X)

# k-means: inertia (elbow) and silhouette for a range of k
for k in range(2, 8):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print(f"k={k}  inertia={km.inertia_:.0f}  silhouette={silhouette_score(X, km.labels_):.3f}  "
          f"DB={davies_bouldin_score(X, km.labels_):.3f}  CH={calinski_harabasz_score(X, km.labels_):.0f}")

# DBSCAN: read eps off the k-distance curve (k = min_samples), at the "knee".
# It merges clusters that touch: with overlapping groups prefer k-means or a Gaussian mixture.
min_samples = 5
dist, _ = NearestNeighbors(n_neighbors=min_samples).fit(X).kneighbors(X)
k_dist = np.sort(dist[:, -1])
print("k-distance percentiles 90/95/99:", np.percentile(k_dist, [90, 95, 99]).round(3))
db = DBSCAN(eps=float(np.percentile(k_dist, 95)), min_samples=min_samples).fit(X)
n_noise = int((db.labels_ == -1).sum())
print(f"DBSCAN clusters={len(set(db.labels_)) - (n_noise > 0)} noise={n_noise}")

# hierarchical (Ward) and external validation against known labels
for name, labels in {"kmeans": KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(X),
                     "ward": AgglomerativeClustering(n_clusters=4, linkage="ward").fit_predict(X),
                     "dbscan": db.labels_}.items():
    print(f"{name:7s} ARI={adjusted_rand_score(y_true, labels):.3f}  NMI={normalized_mutual_info_score(y_true, labels):.3f}")
```

---

## 6. Association rules

One row per transaction, one boolean column per item. `min_support` depends on the data: start high, lower it until the number of itemsets is manageable. Filter rules on lift (> 1 means positive association) as well as confidence.

```python
import pandas as pd
from mlxtend.frequent_patterns import association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder

transactions = [
    ["bread", "milk"], ["bread", "diapers", "beer", "eggs"], ["milk", "diapers", "beer", "cola"],
    ["bread", "milk", "diapers", "beer"], ["bread", "milk", "diapers", "cola"],
]
te = TransactionEncoder()
basket = pd.DataFrame(te.fit(transactions).transform(transactions), columns=te.columns_)

itemsets = fpgrowth(basket, min_support=0.4, use_colnames=True)   # apriori() gives the same result, slower
rules = association_rules(itemsets, num_itemsets=len(basket), metric="confidence", min_threshold=0.6)
rules = rules[rules["lift"] > 1].sort_values(["lift", "confidence"], ascending=False)
print(rules[["antecedents", "consequents", "support", "confidence", "lift", "leverage", "conviction"]]
      .to_string(index=False))
```

---

## 7. Feature selection inside the pipeline

Selecting features on the whole dataset and then cross-validating is leakage: the selector must be a pipeline step.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV, SelectFromModel, SelectKBest, mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True, as_frame=True)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
logreg = LogisticRegression(max_iter=2000)

pipes = {
    "all features": Pipeline([("scale", StandardScaler()), ("clf", logreg)]),
    "kbest mutual info (10)": Pipeline([("scale", StandardScaler()),
                                        ("select", SelectKBest(mutual_info_classif, k=10)), ("clf", logreg)]),
    "from forest importance": Pipeline([("select", SelectFromModel(RandomForestClassifier(n_estimators=200, random_state=0))),
                                        ("scale", StandardScaler()), ("clf", logreg)]),
    "RFECV": Pipeline([("scale", StandardScaler()),
                       ("select", RFECV(LogisticRegression(max_iter=2000), cv=3, scoring="f1")), ("clf", logreg)]),
}
for name, pipe in pipes.items():
    scores = cross_val_score(pipe, X, y, cv=cv, scoring="f1")
    print(f"{name:24s} F1 {scores.mean():.3f} ± {scores.std():.3f}")
```

---

## 8. Statistical comparison of two models

Folds overlap, so a plain paired t-test on CV scores is too optimistic. Use the corrected resampled t-test (Nadeau & Bengio) on repeated k-fold scores computed on the **same** splits; use McNemar when both models are scored once on the same test set.

```python
import numpy as np
from scipy import stats
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.contingency_tables import mcnemar

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
a = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
b = RandomForestClassifier(n_estimators=300, random_state=0)

k, r = 10, 5
cv = RepeatedStratifiedKFold(n_splits=k, n_repeats=r, random_state=0)   # same splits for both models
sa = cross_val_score(a, X_train, y_train, cv=cv, scoring="accuracy")
sb = cross_val_score(b, X_train, y_train, cv=cv, scoring="accuracy")

def corrected_resampled_ttest(diff, n_train, n_test):
    """Nadeau & Bengio (2003): variance inflated by n_test/n_train for overlapping training sets."""
    n = len(diff)
    t = diff.mean() / np.sqrt((1 / n + n_test / n_train) * diff.var(ddof=1))
    return t, 2 * stats.t.sf(abs(t), df=n - 1)

n_test = len(y_train) // k
t, p = corrected_resampled_ttest(sa - sb, len(y_train) - n_test, n_test)
print(f"A {sa.mean():.3f}  B {sb.mean():.3f}  corrected t={t:.2f}  p={p:.3f}")

# McNemar on one shared test set: only the disagreements matter
ca = a.fit(X_train, y_train).predict(X_test) == y_test
cb = b.fit(X_train, y_train).predict(X_test) == y_test
table = [[np.sum(ca & cb), np.sum(ca & ~cb)], [np.sum(~ca & cb), np.sum(~ca & ~cb)]]
print("McNemar p =", round(mcnemar(table, exact=True).pvalue, 3))
```

Several models on several datasets: Friedman test on the per-dataset scores, then a post-hoc test (Nemenyi) if it rejects.

```python
from scipy.stats import friedmanchisquare

# rows = datasets, columns = models (e.g. mean CV accuracy of 3 models on 6 datasets)
scores = [[0.91, 0.93, 0.90], [0.85, 0.88, 0.84], [0.78, 0.80, 0.79],
          [0.95, 0.96, 0.94], [0.70, 0.74, 0.71], [0.88, 0.90, 0.87]]
stat, p = friedmanchisquare(*zip(*scores))
print(f"Friedman chi2={stat:.2f}  p={p:.4f}")
```
