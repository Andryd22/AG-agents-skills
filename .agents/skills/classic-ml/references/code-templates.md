# Template di codice

Template eseguibili per scikit-learn ≥ 1.5, pandas ≥ 2, imbalanced-learn, mlxtend, scipy e statsmodels. Ogni blocco gira da solo con i dataset inclusi o sintetici; sostituisci il caricamento dei dati con quelli del progetto.

```bash
pip install scikit-learn pandas imbalanced-learn mlxtend scipy statsmodels
```

---

## 1. Split, pipeline, baseline e confronto con la CV

Colonne numeriche e categoriche insieme, ogni passo di preprocessing dentro la pipeline, una baseline dummy, gli stessi fold per ogni modello.

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

# --- dati (sostituisci con pd.read_csv(...)) ---
X_num, y = make_classification(n_samples=600, n_features=6, n_informative=4, random_state=0)
X = pd.DataFrame(X_num, columns=[f"num_{i}" for i in range(6)])
X["city"] = np.random.default_rng(0).choice(["pisa", "lucca", "livorno"], size=len(X))
X.loc[X.sample(frac=0.05, random_state=0).index, "num_0"] = np.nan  # qualche valore mancante

# --- un solo split, prima di guardare qualsiasi altra cosa ---
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
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)  # stessi fold per ogni modello
scoring = ["accuracy", "balanced_accuracy", "f1_macro", "roc_auc"]

rows = []
for name, model in models.items():
    pipe = Pipeline([("prep", preprocess), ("model", model)])
    res = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring)
    rows.append({"modello": name, **{m: f"{res[f'test_{m}'].mean():.3f} ± {res[f'test_{m}'].std():.3f}" for m in scoring}})
print(pd.DataFrame(rows).to_string(index=False))
```

---

## 2. Tuning senza toccare il test set, poi una sola valutazione finale

La nested CV stima quanto generalizza la *procedura di tuning*; il modello finale si ottimizza su tutto il training set e si valuta una volta sola sul test set.

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
print(f"F1 con nested CV: {nested.mean():.3f} ± {nested.std():.3f}")

search.fit(X_train, y_train)            # tuning su tutto il training set
print("parametri migliori:", search.best_params_)
print(classification_report(y_test, search.predict(X_test), digits=3))  # l'unico sguardo al test set
```

---

## 3. Classi sbilanciate: resampling nella pipeline, pesi delle classi, soglia

SMOTE deve agire solo sui fold di training, quindi va in una pipeline di `imblearn`, mai prima dello split. La soglia di decisione si ottimizza con la CV, non sul test set.

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

# soglia scelta con la CV sul training set per massimizzare F1
tuned = TunedThresholdClassifierCV(candidates["plain"], scoring="f1", cv=cv).fit(X_train, y_train)
print(f"soglia: {tuned.best_threshold_:.2f}")
proba = tuned.predict_proba(X_test)[:, 1]
pred = tuned.predict(X_test)
print(f"test: PR-AUC {average_precision_score(y_test, proba):.3f}  F1 {f1_score(y_test, pred):.3f}  "
      f"balanced accuracy {balanced_accuracy_score(y_test, pred):.3f}")
```

---

## 4. Regressione

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

## 5. Clustering: scegliere k, confrontare algoritmi, validare

Prima lo scaling. Gli indici interni giudicano compattezza e separazione; quelli esterni (ARI, NMI) solo quando esistono le label vere, e solo per validare, mai per ottimizzare sulle stesse label che riporti.

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

# k-means: inerzia (gomito) e silhouette per un intervallo di k
for k in range(2, 8):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print(f"k={k}  inerzia={km.inertia_:.0f}  silhouette={silhouette_score(X, km.labels_):.3f}  "
          f"DB={davies_bouldin_score(X, km.labels_):.3f}  CH={calinski_harabasz_score(X, km.labels_):.0f}")

# DBSCAN: eps si legge sulla curva delle k-distanze (k = min_samples), nel "ginocchio".
# Unisce i cluster che si toccano: con gruppi sovrapposti meglio k-means o una Gaussian mixture.
min_samples = 5
dist, _ = NearestNeighbors(n_neighbors=min_samples).fit(X).kneighbors(X)
k_dist = np.sort(dist[:, -1])
print("percentili 90/95/99 delle k-distanze:", np.percentile(k_dist, [90, 95, 99]).round(3))
db = DBSCAN(eps=float(np.percentile(k_dist, 95)), min_samples=min_samples).fit(X)
n_noise = int((db.labels_ == -1).sum())
print(f"DBSCAN cluster={len(set(db.labels_)) - (n_noise > 0)} rumore={n_noise}")

# gerarchico (Ward) e validazione esterna con le label note
for name, labels in {"kmeans": KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(X),
                     "ward": AgglomerativeClustering(n_clusters=4, linkage="ward").fit_predict(X),
                     "dbscan": db.labels_}.items():
    print(f"{name:7s} ARI={adjusted_rand_score(y_true, labels):.3f}  NMI={normalized_mutual_info_score(y_true, labels):.3f}")
```

---

## 6. Regole di associazione

Una riga per transazione, una colonna booleana per articolo. `min_support` dipende dai dati: parti alto e abbassalo finché il numero di itemset è gestibile. Filtra le regole sul lift (> 1 vuol dire associazione positiva) oltre che sulla confidence.

```python
import pandas as pd
from mlxtend.frequent_patterns import association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder

transactions = [
    ["pane", "latte"], ["pane", "pannolini", "birra", "uova"], ["latte", "pannolini", "birra", "cola"],
    ["pane", "latte", "pannolini", "birra"], ["pane", "latte", "pannolini", "cola"],
]
te = TransactionEncoder()
basket = pd.DataFrame(te.fit(transactions).transform(transactions), columns=te.columns_)

itemsets = fpgrowth(basket, min_support=0.4, use_colnames=True)   # apriori() dà lo stesso risultato, più lentamente
rules = association_rules(itemsets, num_itemsets=len(basket), metric="confidence", min_threshold=0.6)
rules = rules[rules["lift"] > 1].sort_values(["lift", "confidence"], ascending=False)
print(rules[["antecedents", "consequents", "support", "confidence", "lift", "leverage", "conviction"]]
      .to_string(index=False))
```

---

## 7. Selezione delle feature dentro la pipeline

Selezionare le feature su tutto il dataset e poi fare la cross-validation è data leakage: il selettore deve essere un passo della pipeline.

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
    "tutte le feature": Pipeline([("scale", StandardScaler()), ("clf", logreg)]),
    "kbest mutual info (10)": Pipeline([("scale", StandardScaler()),
                                        ("select", SelectKBest(mutual_info_classif, k=10)), ("clf", logreg)]),
    "importanza della forest": Pipeline([("select", SelectFromModel(RandomForestClassifier(n_estimators=200, random_state=0))),
                                         ("scale", StandardScaler()), ("clf", logreg)]),
    "RFECV": Pipeline([("scale", StandardScaler()),
                       ("select", RFECV(LogisticRegression(max_iter=2000), cv=3, scoring="f1")), ("clf", logreg)]),
}
for name, pipe in pipes.items():
    scores = cross_val_score(pipe, X, y, cv=cv, scoring="f1")
    print(f"{name:24s} F1 {scores.mean():.3f} ± {scores.std():.3f}")
```

---

## 8. Confronto statistico tra due modelli

I fold si sovrappongono, quindi un t-test appaiato semplice sui punteggi della CV è troppo ottimista. Usa il t-test corretto per il resampling (Nadeau & Bengio) sui punteggi di un k-fold ripetuto calcolati sugli **stessi** split; usa McNemar quando entrambi i modelli sono valutati una volta sullo stesso test set.

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
cv = RepeatedStratifiedKFold(n_splits=k, n_repeats=r, random_state=0)   # stessi split per entrambi i modelli
sa = cross_val_score(a, X_train, y_train, cv=cv, scoring="accuracy")
sb = cross_val_score(b, X_train, y_train, cv=cv, scoring="accuracy")

def corrected_resampled_ttest(diff, n_train, n_test):
    """Nadeau & Bengio (2003): varianza gonfiata di n_test/n_train perché i training set si sovrappongono."""
    n = len(diff)
    t = diff.mean() / np.sqrt((1 / n + n_test / n_train) * diff.var(ddof=1))
    return t, 2 * stats.t.sf(abs(t), df=n - 1)

n_test = len(y_train) // k
t, p = corrected_resampled_ttest(sa - sb, len(y_train) - n_test, n_test)
print(f"A {sa.mean():.3f}  B {sb.mean():.3f}  t corretto={t:.2f}  p={p:.3f}")

# McNemar su un solo test set in comune: contano solo le discordanze
ca = a.fit(X_train, y_train).predict(X_test) == y_test
cb = b.fit(X_train, y_train).predict(X_test) == y_test
table = [[np.sum(ca & cb), np.sum(ca & ~cb)], [np.sum(~ca & cb), np.sum(~ca & ~cb)]]
print("McNemar p =", round(mcnemar(table, exact=True).pvalue, 3))
```

Più modelli su più dataset: test di Friedman sui punteggi per dataset, poi un test post-hoc (Nemenyi) se rifiuta.

```python
from scipy.stats import friedmanchisquare

# righe = dataset, colonne = modelli (es. accuratezza media in CV di 3 modelli su 6 dataset)
scores = [[0.91, 0.93, 0.90], [0.85, 0.88, 0.84], [0.78, 0.80, 0.79],
          [0.95, 0.96, 0.94], [0.70, 0.74, 0.71], [0.88, 0.90, 0.87]]
stat, p = friedmanchisquare(*zip(*scores))
print(f"Friedman chi2={stat:.2f}  p={p:.4f}")
```
