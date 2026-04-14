from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.config import CUSTOMER_SEGMENTS_FILE


SEGMENT_NAME_MAP = {
    0: "Loyal Customers",
    1: "At Risk Customers",
    2: "High Value Customers",
    3: "Occasional Buyers",
}


def _score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    scored = rfm.copy()
    scored["r_score"] = pd.qcut(
        scored["recency"].rank(method="first"),
        q=4,
        labels=[4, 3, 2, 1],
    ).astype(int)
    scored["f_score"] = pd.qcut(
        scored["frequency"].rank(method="first"),
        q=4,
        labels=[1, 2, 3, 4],
    ).astype(int)
    scored["m_score"] = pd.qcut(
        scored["monetary"].rank(method="first"),
        q=4,
        labels=[1, 2, 3, 4],
    ).astype(int)
    scored["rfm_score"] = (
        scored["r_score"].astype(str)
        + scored["f_score"].astype(str)
        + scored["m_score"].astype(str)
    )
    return scored


def _assign_readable_segment(cluster_profile: pd.DataFrame) -> dict[int, str]:
    profile = cluster_profile.copy()
    profile["value_index"] = (
        profile["frequency_rank"]
        + profile["monetary_rank"]
        + profile["recency_rank"]
    )
    ordered_clusters = profile.sort_values("value_index", ascending=False)["cluster"].tolist()

    labels = [
        "High Value Customers",
        "Loyal Customers",
        "Occasional Buyers",
        "At Risk Customers",
    ]
    return {
        cluster: labels[position] if position < len(labels) else f"Segment {position + 1}"
        for position, cluster in enumerate(ordered_clusters)
    }


def segment_customers(rfm: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    scored = _score_rfm(rfm)
    model_data = scored[["recency", "frequency", "monetary"]].copy()
    model_data["recency"] = np.log1p(model_data["recency"])
    model_data["frequency"] = np.log1p(model_data["frequency"])
    model_data["monetary"] = np.log1p(model_data["monetary"])

    scaler = StandardScaler()
    scaled = scaler.fit_transform(model_data)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    scored["cluster"] = kmeans.fit_predict(scaled)

    cluster_profile = (
        scored.groupby("cluster", as_index=False)
        .agg(
            recency=("recency", "median"),
            frequency=("frequency", "median"),
            monetary=("monetary", "median"),
            customers=("customer_id", "count"),
        )
    )
    cluster_profile["recency_rank"] = cluster_profile["recency"].rank(ascending=False, method="dense")
    cluster_profile["frequency_rank"] = cluster_profile["frequency"].rank(ascending=True, method="dense")
    cluster_profile["monetary_rank"] = cluster_profile["monetary"].rank(ascending=True, method="dense")

    label_map = _assign_readable_segment(cluster_profile)
    scored["segment"] = scored["cluster"].map(label_map).fillna("Customer Segment")

    scored = scored.sort_values(["segment", "monetary"], ascending=[True, False])
    scored.to_csv(CUSTOMER_SEGMENTS_FILE, index=False)
    return scored
