"""
Clustering Processor
Performs K-Means clustering and PCA on engagement features.
Used for Charts 17, 18, 19, 20.
"""
from typing import Dict, Tuple

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from .base import BaseProcessor


class ClusteringProcessor(BaseProcessor):

    @property
    def name(self) -> str:
        return "clustering_processor"

    def _prepare_features(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Helper to create feature matrix for clustering."""
        # 1. Aggregate totals and frequencies
        demo = data["demographic"].assign(total=lambda x: x["demo_age_5_17"] + x["demo_age_17_"])
        bio = data["biometric"].assign(total=lambda x: x["bio_age_5_17"] + x["bio_age_17_"])
        enroll = data["enrollment"].assign(total=lambda x: x["age_0_5"] + x["age_5_17"] + x["age_18_greater"])

        demo_agg = demo.groupby("pincode")["total"].agg(["sum", "count"]).rename(columns={"sum": "demo_total", "count": "demo_freq"})
        bio_agg = bio.groupby("pincode")["total"].agg(["sum", "count"]).rename(columns={"sum": "bio_total", "count": "bio_freq"})
        enroll_agg = enroll.groupby("pincode")["total"].agg(["sum", "count"]).rename(columns={"sum": "enroll_total", "count": "enroll_freq"})

        # Merge
        features = pd.concat([demo_agg, bio_agg, enroll_agg], axis=1).fillna(0)
        
        # 2. Derive Features
        features["total_inter"] = features["demo_total"] + features["bio_total"] + features["enroll_total"]
        features["total_freq"] = features["demo_freq"] + features["bio_freq"] + features["enroll_freq"]
        
        # Avoid division by zero
        features = features[features["total_freq"] > 0].copy()
        
        # Ratios
        features["demo_ratio"] = features["demo_total"] / features["total_inter"]
        features["bio_ratio"] = features["bio_total"] / features["total_inter"]
        features["enroll_ratio"] = features["enroll_total"] / features["total_inter"]
        
        # Intensity
        features["avg_intensity"] = features["total_inter"] / features["total_freq"]
        
        # Select features for clustering
        # We'll use ratios, frequencies, and intensity
        return features

    def process_elbow(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Calculate inertia for k=2 to 10.
        Returns DataFrame with 'k' and 'inertia'.
        """
        features_df = self._prepare_features(data)
        
        # Select numerical columns for clustering
        cols = ["demo_ratio", "bio_ratio", "enroll_ratio", "avg_intensity", "total_freq"]
        X = features_df[cols].fillna(0)
        
        # Scale
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        inertias = []
        k_values = range(2, 11)
        
        for k in k_values:
            model = KMeans(n_clusters=k, random_state=42, n_init=10)
            model.fit(X_scaled)
            inertias.append(model.inertia_)
            
        return pd.DataFrame({"k": k_values, "inertia": inertias})

    def process_clusters(self, data: Dict[str, pd.DataFrame], k: int = 5) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Fit K-Means with k=5 and PCA.
        Returns:
            - labeled_data: Original data with 'cluster' column
            - pca_data: DataFrame with 'PC1', 'PC2', 'cluster'
        """
        features_df = self._prepare_features(data)
        
        cols = ["demo_ratio", "bio_ratio", "enroll_ratio", "avg_intensity", "total_freq"]
        X = features_df[cols].fillna(0)
        
        # Scale
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Fit K-Means
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)
        
        features_df["cluster"] = clusters
        
        # Fit PCA
        pca = PCA(n_components=2)
        pcs = pca.fit_transform(X_scaled)
        
        pca_df = pd.DataFrame(pcs, columns=["PC1", "PC2"], index=features_df.index)
        pca_df["cluster"] = clusters
        
        return features_df, pca_df

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Default process method (not used directly, but required by abstract base)."""
        return self._prepare_features(data)
