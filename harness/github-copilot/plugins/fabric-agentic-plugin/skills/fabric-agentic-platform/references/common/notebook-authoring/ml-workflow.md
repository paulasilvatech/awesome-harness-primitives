# ML Workflow — MLflow, SynapseML & Model Training in Notebooks

How to train, track, register, and score machine learning models inside Fabric Notebooks using MLflow experiment tracking, SynapseML, and the PREDICT function.

> **Public documentation — fetch via Microsoft Learn MCP before generating code.**
> Agent MUST fetch the relevant page(s) below for code examples and API details rather than relying on inline snippets here.

---

## Documentation Index

### MLflow & Experiment Tracking

| Topic | Documentation | When to Fetch |
|---|---|---|
| Data Science overview | [Data Science in Fabric](https://learn.microsoft.com/en-us/fabric/data-science/data-science-overview) | full ML lifecycle overview, capabilities, semantic link |
| Model training overview | [Train ML models](https://learn.microsoft.com/en-us/fabric/data-science/model-training-overview) | SparkML vs SynapseML vs popular libraries, framework comparison |
| MLflow autologging | [Autologging in Fabric](https://learn.microsoft.com/en-us/fabric/data-science/mlflow-autologging) | autolog default config, `exclusive=False` for custom logging, disable per-session or workspace-wide |
| ML experiments | [ML experiments](https://learn.microsoft.com/en-us/fabric/data-science/machine-learning-experiment) | `set_experiment`, `start_run`, `search_runs`, compare runs, tags, inline widget |
| ML models | [ML models](https://learn.microsoft.com/en-us/fabric/data-science/machine-learning-model) | `register_model`, model versioning, compare versions, apply models |
| MLflow upgrade | [Upgrade ML tracking](https://learn.microsoft.com/en-us/fabric/data-science/mlflow-upgrade) | upgrading workspace ML tracking experience |
| Cross-workspace logging | [Cross-workspace MLflow](https://learn.microsoft.com/en-us/fabric/data-science/machine-learning-cross-workspace-logging) | log models/experiments across workspaces |

### Model Training (fetch for complete code examples)

| Topic | Documentation | When to Fetch |
|---|---|---|
| Train with scikit-learn | [sklearn + MLflow](https://learn.microsoft.com/en-us/fabric/data-science/train-models-scikit-learn) | LogisticRegression, `log_model`, `register_model`, inference with `MLFlowTransformer` |
| Train with PyTorch | [PyTorch + MLflow](https://learn.microsoft.com/en-us/fabric/data-science/train-models-pytorch) | CNN training, `mlflow.pytorch.log_model`, load & evaluate |
| Train with SparkML | [SparkML tutorial](https://learn.microsoft.com/en-us/fabric/data-science/fabric-sparkml-tutorial) | SparkML pipeline, VectorAssembler, ML pipeline stages |
| AutoML with FLAML | [AutoML in Fabric](https://learn.microsoft.com/en-us/fabric/data-science/how-to-use-automated-machine-learning-fabric) | `flaml.AutoML`, Spark parallelization, `to_pandas_on_spark`, time budget |
| Low-code AutoML UI | [Low-code AutoML](https://learn.microsoft.com/en-us/fabric/data-science/low-code-automl) | code-free AutoML via UI widget |

### SynapseML (pre-installed in Fabric runtimes)

| Topic | Documentation | When to Fetch |
|---|---|---|
| SynapseML overview | [SynapseML site](https://microsoft.github.io/SynapseML/) | installation, Spark integration, language support |
| LightGBM models | [LightGBM + SynapseML](https://learn.microsoft.com/en-us/fabric/data-science/how-to-use-lightgbm-with-synapseml) | `LightGBMClassifier`, `LightGBMRegressor`, `LightGBMRanker`, feature importance |
| First model with SynapseML | [Build a model](https://learn.microsoft.com/en-us/fabric/data-science/synapseml-first-model) | text featurization pipeline, prebuilt models |
| Foundry Tools + SynapseML | [Foundry Tools BYOK](https://learn.microsoft.com/en-us/fabric/data-science/ai-services/ai-services-in-synapseml-bring-your-own-key) | vision, speech, language, translation, anomaly detection via SynapseML transformers |
| OpenAI + SynapseML | [Azure OpenAI at scale](https://learn.microsoft.com/en-us/fabric/data-science/open-ai) | distributed LLM prompting with `OpenAICompletion` |

### Model Scoring & Deployment

| Topic | Documentation | When to Fetch |
|---|---|---|
| PREDICT function | [PREDICT scoring](https://learn.microsoft.com/en-us/fabric/data-science/model-scoring-predict) | `MLFlowTransformer` (Transformer API), Spark SQL `PREDICT()`, PySpark UDF, supported flavors |
| Model endpoints | [Real-time endpoints](https://learn.microsoft.com/en-us/fabric/data-science/model-endpoints) | activate/deactivate endpoints, auto-sleep, consumption rate, REST API |

### End-to-End Tutorials (fetch for full walkthrough code)

| Topic | Documentation | When to Fetch |
|---|---|---|
| Bank churn prediction | [Churn tutorial](https://learn.microsoft.com/en-us/fabric/data-science/customer-churn) | RandomForest + LightGBM, autolog, PREDICT |
| Fraud detection | [Fraud detection](https://learn.microsoft.com/en-us/fabric/data-science/fraud-detection) | SMOTE, LightGBM, model registration, batch scoring |
| Machine fault detection | [Predictive maintenance](https://learn.microsoft.com/en-us/fabric/data-science/predictive-maintenance) | RF + LogReg + XGBoost, MLflow model comparison |
| Sales forecasting | [Sales forecasting](https://learn.microsoft.com/en-us/fabric/data-science/sales-forecasting) | time-series, Prophet, autolog |
| Text classification | [Text classification](https://learn.microsoft.com/en-us/fabric/data-science/title-genre-classification) | Word2Vec, cross-validation, Spark ML pipeline |

---

## Key Facts (quick reference — no need to fetch docs for these)

### Autologging Defaults

- Fabric notebooks call `mlflow.autolog()` **automatically** on `import mlflow`.
- Default: `exclusive=True` — manual `log_param`/`log_metric` calls are **ignored** unless you set `exclusive=False`.
- Supported frameworks: TensorFlow, PyTorch, Scikit-learn, XGBoost, LightGBM, Spark, Statsmodels, CatBoost, Keras.

### PREDICT Supported Model Flavors

CatBoost, Keras, LightGBM, ONNX, Prophet, PyTorch, Sklearn, Spark, Statsmodels, TensorFlow, XGBoost.

### SynapseML Key Imports

| Component | Import Path |
|---|---|
| LightGBMClassifier | `from synapse.ml.lightgbm import LightGBMClassifier` |
| LightGBMRegressor | `from synapse.ml.lightgbm import LightGBMRegressor` |
| LightGBMRanker | `from synapse.ml.lightgbm import LightGBMRanker` |
| MLFlowTransformer | `from synapse.ml.predict import MLFlowTransformer` |
| ComputeModelStatistics | `from synapse.ml.train import ComputeModelStatistics` |
| VectorAssembler | `from pyspark.ml.feature import VectorAssembler` |

---

## Rules

1. **Never create a new SparkSession** — use the built-in `spark` session. `SparkSession.builder.appName(...)` is for standalone apps, not notebooks.
2. **Use `mlflow.set_experiment()` before training** — always name your experiment explicitly.
3. **Set `exclusive=False` for custom logging** — default autolog uses `exclusive=True`, which ignores manual `log_param`/`log_metric` calls.
4. **Save models in MLflow format with signatures** — required for PREDICT function compatibility. Use `infer_signature()` from `mlflow.models.signature`.
5. **Use `%pip install` for additional ML libraries** — never `!pip install`. Check the [built-in library list](library-mgmt.md) before installing.
6. **Store training/test data in Lakehouse Delta tables** — avoid reading from local files in notebook cells.
7. **Log artifacts to the experiment run** — use `mlflow.log_artifact()` for plots, reports, and data files rather than saving to ad-hoc locations.
8. **Fetch public docs before generating ML code** — always fetch the relevant documentation page from the index above to get current API patterns and complete code examples. If the MCP fetch fails (server unavailable, timeout), proceed using the local guidance in this module and your internal knowledge, and add a disclaimer that the code should be verified against the latest documentation.
