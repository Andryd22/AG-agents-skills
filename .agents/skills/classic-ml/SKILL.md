---
name: classic-ml
description: Machine learning classico e data mining su dati tabellari con pandas e scikit-learn - EDA, preprocessing nelle pipeline, cross-validation senza data leakage, classificazione, regressione, clustering, classi sbilanciate, selezione delle feature, regole di associazione, metriche e confronto statistico tra modelli. Usala quando l'utente lancia /classic-ml o lavora a un progetto di data mining o ML che non riguarda gli LLM.
---

# ML classico e data mining

> Ambito: dati tabellari, scikit-learn e librerie collegate. LLM, RAG e prompt stanno in `prompt-engineering`; il deep learning è fuori ambito.

Il codice eseguibile per ogni sezione è in `references/code-templates.md` (provato con scikit-learn 1.9, imbalanced-learn 0.14, mlxtend 0.25, scipy 1.17, statsmodels 0.15). Leggi solo la sezione che ti serve.

---

## 1. Regole d'oro

1. **Prima inquadra il problema**: target, unità di osservazione, a cosa serve una predizione e la metrica adatta a quell'uso. Scegli la metrica prima di addestrare qualsiasi cosa.
2. **Dividi prima di guardare**: metti da parte un test set (stratificato per la classificazione) prima delle decisioni guidate dall'EDA; lo tocchi una volta sola, alla fine.
3. **Tutto quello che impara dai dati va in una `Pipeline`**: imputazione, scaling, encoding, selezione delle feature, resampling. Fare il fit di uno di questi sull'intero dataset è data leakage.
4. **Prima la baseline**: `DummyClassifier` / `DummyRegressor`. Un modello che non la batte non è un risultato.
5. **Cross-validation solo sul training set**, con gli stessi fold per ogni modello, riportando media ± deviazione standard, non un singolo split.
6. **Rispetta la struttura dei dati**: `GroupKFold` / `StratifiedGroupKFold` quando più righe appartengono alla stessa entità (paziente, utente, sessione), `TimeSeriesSplit` quando conta l'ordine. Un k-fold mescolato su questi dati ha data leakage.
7. **Fissa `random_state`** negli split, nella CV e nei modelli, così i risultati sono riproducibili.
8. **Fai il tuning con la CV, mai sul test set**; per riportare quanto è buono il tuning usa la nested CV.
9. **Confronta i modelli con un test adatto al disegno sperimentale** (sezione 10), non con "0,83 > 0,82".

---

## 2. Procedura

```text
1. Inquadra      → tipo di compito, target, metrica, vincoli (interpretabilità, latenza, costo degli errori)
2. Carica ed EDA → dimensioni, tipi, valori mancanti, duplicati, distribuzione del target, sospetti di leakage
3. Dividi        → train/test (stratificato, per gruppi, temporale); test set messo da parte
4. Baseline      → modello dummy con CV
5. Pipeline      → ColumnTransformer + modello; 2-4 famiglie di modelli
6. Confronto CV  → stessi fold, media ± dev. std, più metriche
7. Tuning        → solo le 1-2 famiglie migliori; GridSearchCV / RandomizedSearchCV sul train
8. Valutazione   → refit su tutto il train, punteggio sul test set una volta sola
9. Analisi       → matrice di confusione, errori per segmento, importanza delle feature (permutation)
10. Resoconto    → dati, protocollo, metriche con dispersione, test statistico, limiti
```

---

## 3. Checklist dell'EDA

| Controllo | Perché | Come |
| --- | --- | --- |
| Valori mancanti per colonna | Strategia di imputazione, colonne da togliere | `df.isna().mean().sort_values()` |
| Righe duplicate | La stessa riga in train e test gonfia i punteggi | `df.duplicated().sum()` |
| Distribuzione del target | Sbilanciamento → metriche e stratificazione | `y.value_counts(normalize=True)` |
| Distribuzioni numeriche, outlier | Scelta dello scaling, trasformazioni logaritmiche | `df.describe()`, istogrammi, box plot |
| Cardinalità delle categoriche | One-hot o target encoding | `df.nunique()` |
| Correlazioni | Feature ridondanti, multicollinearità per i modelli lineari | `df.corr(numeric_only=True)` |
| Sospetti di leakage | Colonne calcolate dopo l'esito, ID, timestamp | Ragionamento sul dominio; punteggi sospettosamente alti con una sola feature |

---

## 4. Preprocessing

| Passo | Predefinito | Note |
| --- | --- | --- |
| Mancanti numerici | `SimpleImputer(strategy="median")` | `KNNImputer` / `IterativeImputer` se i mancanti sono informativi o tanti; aggiungi `add_indicator=True` |
| Mancanti categorici | `SimpleImputer(strategy="most_frequent")` o una costante "missing" | |
| Scaling | `StandardScaler` | Serve ai modelli basati su distanze o gradienti (kNN, SVM, logistica/lineare con regolarizzazione, k-means, PCA); non agli alberi; `RobustScaler` con gli outlier |
| Categoriche a bassa cardinalità | `OneHotEncoder(handle_unknown="ignore")` | |
| Categoriche ad alta cardinalità | `TargetEncoder` (fa il cross-fitting da solo) | Mai calcolare a mano le medie del target su tutti i dati |
| Feature positive asimmetriche | `np.log1p` con `FunctionTransformer` | Aiuta i modelli lineari |
| Riduzione della dimensionalità | `PCA` dopo lo scaling | Per visualizzare o con molte feature correlate; si perde interpretabilità |

Costruiscilo con `ColumnTransformer`, così ogni gruppo di colonne ha i suoi passi (template 1).

---

## 5. Scelta del modello

| Compito | Baseline | Prova prima | Poi |
| --- | --- | --- | --- |
| Classificazione binaria / multiclasse | `DummyClassifier(strategy="most_frequent")` | `LogisticRegression`, `RandomForestClassifier` | `HistGradientBoostingClassifier`, `SVC`, kNN |
| Regressione | `DummyRegressor(strategy="mean")` | `Ridge`/`RidgeCV`, `RandomForestRegressor` | `HistGradientBoostingRegressor`, `SVR` |
| Clustering | — | `KMeans` (dati scalati) | `AgglomerativeClustering`, `DBSCAN`/`HDBSCAN`, `GaussianMixture` |
| Pattern frequenti | — | FP-Growth (`mlxtend`) | Apriori (stessi itemset, più lento) |
| Pochi campioni, serve interpretabilità | | Logistica / lineare, `DecisionTreeClassifier` poco profondo | |

Sui dati tabellari il gradient boosting è di solito il modello singolo più forte; i modelli lineari sono i più interpretabili; kNN e SVM richiedono lo scaling e soffrono con molte feature.

---

## 6. Classi sbilanciate

- **Metriche**: l'accuratezza nasconde la classe minoritaria. Usa PR-AUC (`average_precision`), F1 / F-beta, balanced accuracy, MCC, recall a precisione fissata; la ROC-AUC può sembrare buona anche quando la classe positiva è predetta male.
- **Sempre** `StratifiedKFold` e uno split train/test stratificato.
- **Opzioni, dalla più economica**: `class_weight="balanced"` → tuning della soglia di decisione (`TunedThresholdClassifierCV`, sklearn ≥ 1.5) → resampling (SMOTE, undersampling).
- **Resampling solo dentro una `imblearn.pipeline.Pipeline`**, così agisce solo sui fold di training. SMOTE prima dello split mette nel training copie sintetiche dei punti di test.
- Confronta le opzioni con la CV sugli stessi fold (template 3).

---

## 7. Clustering

- Prima fai lo scaling delle feature; k-means e il gerarchico di Ward presuppongono scale confrontabili.
- **k-means**: scegli k con il gomito dell'inerzia *e* con il silhouette score; esegui con `n_init=10`. Presuppone cluster più o meno sferici e di dimensioni simili.
- **DBSCAN**: fissa `min_samples` (≈ 2 × numero di dimensioni per iniziare), leggi `eps` sul ginocchio della curva ordinata delle k-distanze. Trova forme arbitrarie e rumore (label −1), ma unisce i cluster che si toccano.
- **Gerarchico**: `linkage="ward"` per cluster compatti; il dendrogramma (`scipy.cluster.hierarchy`) mostra dove tagliare.
- **Indici interni** (senza label): silhouette (più alto è meglio, −1..1), Davies-Bouldin (più basso è meglio), Calinski-Harabasz (più alto è meglio). Confrontali tra valori di k e algoritmi, non come verità assolute.
- **Indici esterni** (label disponibili): ARI, NMI. Il clustering non è classificazione: se le label ci sono e lo scopo è predire, addestra un classificatore.
- Descrivi ogni cluster (medie delle feature originali, dimensioni) prima di chiamarlo segmento.

---

## 8. Regole di associazione

- Dati: una riga per transazione, una colonna booleana per articolo (`TransactionEncoder`).
- **support**(X) = frazione di transazioni che contengono X; **confidence**(X→Y) = support(X∪Y) / support(X); **lift** = confidence / support(Y): > 1 associazione positiva, 1 indipendenza, < 1 associazione negativa.
- **leverage** = support(X∪Y) − support(X)·support(Y); **conviction** = (1 − support(Y)) / (1 − confidence), ∞ quando confidence = 1.
- `min_support`: parti alto e abbassalo finché il numero di itemset è gestibile; troppo basso esplode in modo combinatorio.
- Una confidence alta da sola inganna quando Y è comunque frequente: filtra anche sul lift. Le regole mostrano co-occorrenza, non causalità.
- `association_rules(itemsets, num_itemsets=len(basket), ...)`: passa il numero di transazioni (template 6).

---

## 9. Metriche

| Compito | Metrica | Quando |
| --- | --- | --- |
| Classificazione | Accuratezza | Classi bilanciate, errori con lo stesso costo |
| | Precision / Recall / F1 | Falsi positivi e falsi negativi costano in modo diverso; `average="macro"` tratta le classi allo stesso modo |
| | ROC-AUC | Qualità dell'ordinamento, classi bilanciate |
| | PR-AUC (average precision) | Classi sbilanciate, conta la classe positiva |
| | Balanced accuracy, MCC | Classi sbilanciate, un solo numero |
| | Log loss, Brier score | Servono probabilità calibrate |
| Regressione | MAE | Robusta, stessa unità del target |
| | RMSE (`root_mean_squared_error`) | Penalizza gli errori grandi |
| | R² | Quota di varianza spiegata; può essere negativo |
| Clustering | Silhouette, Davies-Bouldin, Calinski-Harabasz | Senza label |
| | ARI, NMI | Con label |

Per la classificazione mostra sempre la matrice di confusione, e per il multiclasse le metriche per classe (`classification_report`).

---

## 10. Confronto statistico tra modelli

| Disegno | Test |
| --- | --- |
| Due modelli, k-fold CV ripetuta sugli stessi split | t-test corretto per il resampling (Nadeau & Bengio); un t-test appaiato semplice sui fold è troppo ottimista perché i training set si sovrappongono |
| Due modelli, un solo test set in comune | Test di McNemar sulle discordanze |
| Più modelli, più dataset | Test di Friedman, poi post-hoc di Nemenyi |
| Due modelli, più dataset | Wilcoxon signed-rank sui punteggi per dataset |

Riporta la dimensione dell'effetto (differenza media ± dispersione) insieme al p-value; con molti confronti, correggi per la molteplicità (Holm). Il codice è nel template 8.

---

## 11. Anti-pattern

| Anti-pattern | Perché è sbagliato | Correzione |
| --- | --- | --- |
| `scaler.fit(X)` e poi lo split | Le statistiche del test finiscono nel training | Scaler dentro la pipeline |
| Selezione delle feature su tutti i dati, poi CV | Le feature scelte hanno già visto i fold di test | Selettore come passo della pipeline |
| SMOTE prima dello split / prima della CV | Vicini sintetici dei punti di test nel training | Pipeline di `imblearn` |
| Tuning sul test set, o scegliere il migliore tra tanti punteggi di test | Ottimista, non riproducibile | CV sul train, nested CV per riportare |
| Un solo split casuale | Alta varianza, seed fortunati | k-fold ripetuto (stratificato) |
| Accuratezza su dati sbilanciati | 95 % predicendo sempre la maggioranza | PR-AUC, F1, balanced accuracy |
| k-fold mescolato su dati a gruppi o temporali | La stessa entità o il futuro in train e test | Split per gruppi / per serie temporali |
| `LabelEncoder` sulle feature di input | Impone un ordine finto | `OneHotEncoder` / `OrdinalEncoder` solo per categorie ordinate |
| Dichiarare un vincitore dai punteggi medi | Differenze dentro il rumore | Sezione 10 |
| Importanza basata sull'impurità presa per vera | Favorisce le feature ad alta cardinalità | `permutation_importance` su dati tenuti da parte |

---

## 12. Checklist del resoconto

- Dataset: fonte, righe/colonne, distribuzione del target, decisioni di preprocessing e perché.
- Protocollo: dimensioni degli split, schema di CV (k, ripetizioni, stratificato/per gruppi), seed, griglia di tuning.
- Risultati: baseline e modelli, media ± dev. std per metrica, punteggio finale sul test una volta sola.
- Confronto: test statistico e p-value, dimensione dell'effetto.
- Analisi: matrice di confusione, analisi degli errori, importanza delle feature, profili dei cluster o regole principali.
- Limiti: dimensione dei dati, rischi di leakage esclusi, cosa cambierebbe la conclusione.
