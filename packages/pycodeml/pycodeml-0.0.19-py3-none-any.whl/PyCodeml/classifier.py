import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

class ClassifierTrainer:
    def __init__(self, dataset, target_column, data_sample_percent=100):
        """
        Initialize the ClassifierTrainer.

        Parameters:
        - dataset: pandas DataFrame containing the data
        - target_column: name of the target column
        - data_sample_percent: percentage of total data to use (default: 100)
        """
        self.dataset = dataset
        self.target_column = target_column
        self.data_sample_percent = data_sample_percent
        self.models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Random Forest": RandomForestClassifier(),
            "Support Vector Machine": SVC(),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(),
            "Ridge Classifier": RidgeClassifier(),
            "Naive Bayes": GaussianNB(),
            "K-Nearest Neighbors": KNeighborsClassifier()
        }
        self.best_model = None
        self.best_score = float('-inf')
        self.results = []

    def _get_sampled_data(self):
        if self.data_sample_percent == 100:
            return self.dataset
        sample_size = int(len(self.dataset) * (self.data_sample_percent / 100))
        return self.dataset.sample(n=sample_size, random_state=42)

    def train_and_get_best_model(self):
        sampled_data = self._get_sampled_data()
        X = sampled_data.drop(columns=[self.target_column])
        y = sampled_data[self.target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

        print(f"Using {self.data_sample_percent}% of total data ({len(sampled_data)} samples)")
        print(f"{'Model':<25}{'Train Acc':<15}{'Test Acc':<15}{'Status':<15}")
        print("-" * 70)

        for model_name, model in self.models.items():
            model.fit(X_train, y_train)

            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)

            train_acc = accuracy_score(y_train, train_pred)
            test_acc = accuracy_score(y_test, test_pred)

            # Overfitting/Underfitting detection
            if train_acc - test_acc > 0.15:
                status = "Overfitting"
            elif test_acc - train_acc > 0.15:
                status = "Underfitting"
            else:
                status = "Good Fit"

            self.results.append({
                "Model": model_name,
                "Train Accuracy": train_acc,
                "Test Accuracy": test_acc,
                "Status": status
            })

            print(f"{model_name:<25}{train_acc:<15.4f}{test_acc:<15.4f}{status:<15}")

            if test_acc > self.best_score:
                self.best_score = test_acc
                self.best_model = model

        print(f"\nBest Model: {type(self.best_model).__name__} with Test Accuracy: {self.best_score:.4f}")
        return self.best_model

    def save_best_model(self, path="best_classifier_model.pkl"):
        if self.best_model:
            with open(path, "wb") as file:
                pickle.dump(self.best_model, file)
            print(f"Best model saved to {path}")
        else:
            print("No model to save. Train models first!")
