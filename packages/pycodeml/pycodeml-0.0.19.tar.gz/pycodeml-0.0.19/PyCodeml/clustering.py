import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler


class ClusteringTrainer:
    def __init__(self, dataset, features=None, n_clusters=3, data_sample_percent=100):
        """
        Initialize the ClusteringTrainer.

        Parameters:
        - dataset: pandas DataFrame containing the data
        - features: list of feature columns to use (default: all except object columns)
        - n_clusters: number of clusters (used by algorithms that require it)
        - data_sample_percent: percentage of total data to use (default: 100)
        """
        self.dataset = dataset.copy()
        self.features = features or dataset.select_dtypes(exclude=['object']).columns.tolist()
        self.n_clusters = n_clusters
        self.data_sample_percent = data_sample_percent
        self.models = {
            "KMeans": KMeans(n_clusters=self.n_clusters, random_state=42),
            "DBSCAN": DBSCAN(),
            "Agglomerative Clustering": AgglomerativeClustering(n_clusters=self.n_clusters)
        }
        self.scaler = StandardScaler()
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
        X = sampled_data[self.features]
        X_scaled = self.scaler.fit_transform(X)

        print(f"Using {self.data_sample_percent}% of total data ({len(sampled_data)} samples)")
        print(f"{'Model':<30}{'Silhouette Score':<20}")
        print("-" * 50)

        for model_name, model in self.models.items():
            try:
                clusters = model.fit_predict(X_scaled)

                # Ignore models that return a single cluster (e.g., bad DBSCAN output)
                if len(set(clusters)) < 2:
                    score = -1
                    print(f"{model_name:<30}{'Too few clusters':<20}")
                    continue

                score = silhouette_score(X_scaled, clusters)

                self.results.append({
                    "Model": model_name,
                    "Silhouette Score": score,
                    "Clusters": len(set(clusters))
                })

                print(f"{model_name:<30}{score:<20.4f}")

                if score > self.best_score:
                    self.best_score = score
                    self.best_model = model
                    self.best_clusters = clusters
            except Exception as e:
                print(f"{model_name:<30}Failed: {str(e)}")

        if self.best_model:
            print(f"\nBest Model: {type(self.best_model).__name__} with Silhouette Score: {self.best_score:.4f}")
        else:
            print("\nNo valid clustering model found.")
        return self.best_model

    def save_best_model(self, path="best_clustering_model.pkl"):
        if self.best_model:
            with open(path, "wb") as file:
                pickle.dump(self.best_model, file)
            print(f"Best clustering model saved to {path}")
        else:
            print("No model to save. Train models first!")

    def label_data(self):
        """
        Add cluster labels to the original dataset and return the labeled DataFrame.
        """
        if not self.best_model:
            print("Train the model before labeling.")
            return None

        data = self.dataset[self.features]
        data_scaled = self.scaler.transform(data)
        cluster_labels = self.best_model.fit_predict(data_scaled)
        labeled_df = self.dataset.copy()
        labeled_df['Cluster_Label'] = cluster_labels
        return labeled_df
