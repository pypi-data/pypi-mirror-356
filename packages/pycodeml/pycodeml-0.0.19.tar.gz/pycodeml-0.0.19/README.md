Got it! Here's the full `README.md` as **one continuous markdown block**, without unnecessary spacing between sections — just like your screenshot style.

````markdown
# PyCodeML
**PyCodeML** is a Python package designed to automate the training, evaluation, tuning, and selection of the best-performing machine learning models for regression, classification, and clustering tasks. It simplifies the process of model training, comparison, tuning, and deployment.

## ✅ Features
- Supports **Regression**, **Classification**, and **Clustering** tasks  
- Evaluates multiple models and selects the best one  
- **Hyperparameter tuning** support for optimized performance  
- Saves and loads trained models for future use  
- Simple and intuitive API for fast prototyping and deployment  

````
````markdown

## 📦 Installation

pip install PyCodeML
````

## 💻 Usage

### 1️⃣ Train and Save the Best Regression Model

```python
import pandas as pd
from PyCodeML.regressor import RegressorTrainer  # For regression tasks

df = pd.read_csv("data.csv")

trainer = RegressorTrainer(df, "target", data_sample_percent=100)
best_model = trainer.train_and_get_best_model()

trainer.save_best_model("best_regression_model.pkl")
```

### 2️⃣ Train and Save the Best Classification Model

```python
import pandas as pd
from PyCodeML.classifire import ClassifierTrainer  # For classification tasks

df = pd.read_csv("classification_data.csv")

trainer = ClassifierTrainer(df, "label", data_sample_percent=100)
best_model = trainer.train_and_get_best_model()

trainer.save_best_model("best_classifier_model.pkl")
```

### 3️⃣ Tune the Best Regression Model

```python
from PyCodeML.tunner import RegressorTuner

tuner = RegressorTuner(
    dataset=df,
    target_column="target",
    model_name="Random Forest"  # Must match one of the supported models
)

tuned_model, score = tuner.tune()
```

### 4️⃣ Tune the Best Classification Model

```python
from PyCodeML.tunner import ClassifierTuner

tuner = ClassifierTuner(
    dataset=df,
    target_column="label",
    model_name="Random Forest Classifier"
)

tuned_model = tuner.tune()
```

### 5️⃣ Train and Save the Best Clustering Model

```python
import pandas as pd
from PyCodeML.clustering import ClusteringTrainer

df = pd.read_csv("unsupervised_data.csv")

trainer = ClusteringTrainer(df, n_clusters=3, data_sample_percent=100)
best_model = trainer.train_and_get_best_model()

trainer.save_best_model("best_clustering_model.pkl")
```

### 6️⃣ Load and Use the Saved Model

```python
import pandas as pd
from PyCodeML.utils import load_model

model = load_model("best_model.pkl")

new_data = pd.read_csv("new_data.csv")
predictions = model.predict(new_data)

print("Predicted Values:", predictions)
```

### 7️⃣ Label Data Using Clustering

```python
labeled_df = trainer.label_data()
print(labeled_df.head())
```

## 📊 Supported Models

### Regression

* Linear Regression
* Decision Tree Regressor
* Random Forest Regressor
* Support Vector Regressor (SVR)
* Gradient Boosting Regressor
* Ridge Regression
* Lasso Regression
* Elastic Net

### Classification

* Logistic Regression
* Random Forest Classifier
* Support Vector Machine (SVM)
* Decision Tree Classifier
* Gradient Boosting Classifier
* K-Nearest Neighbors (KNN)

### Clustering

* KMeans
* DBSCAN
* Agglomerative Clustering

## 🤝 Contributing

Contributions are welcome!
If you'd like to improve this package, feel free to fork the repository and submit a pull request.

## 🔗 GitHub

[https://github.com/Nachiket858/PyCodeML](https://github.com/Nachiket858/PyCodeML)


