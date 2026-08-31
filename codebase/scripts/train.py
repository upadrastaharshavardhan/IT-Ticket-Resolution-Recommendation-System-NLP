#!/usr/bin/env python
"""Build embedding index over resolved tickets."""

from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from src.data.generator import generate_ticket_dataset
from src.data.preprocessing import TicketPreprocessor
from src.models.embeddings import EmbeddingModel
from src.models.similarity import SimilarityIndex
from src.utils.helpers import load_config, ensure_dirs, set_seed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--data", default=None)
    args = parser.parse_args()
    cfg = load_config(args.config)
    set_seed(cfg["data"]["random_seed"])
    ensure_dirs(cfg["paths"]["data_dir"], cfg["paths"]["artifacts_dir"])

    data_path = Path(args.data or cfg["paths"]["raw_data"])
    if data_path.exists():
        df = pd.read_csv(data_path)
    else:
        df = generate_ticket_dataset(cfg["data"]["n_samples"], cfg["data"]["random_seed"])
        df.to_csv(data_path, index=False)

    pre = TicketPreprocessor(max_text_length=cfg["preprocessing"]["max_text_length"])
    df = pre.transform_df(df)

    # Hold out 15% as query set for retrieval eval
    train_df, query_df = train_test_split(df, test_size=0.15, random_state=cfg["data"]["random_seed"],
                                          stratify=df["category"])
    print(f"Index: {len(train_df)} | Query eval: {len(query_df)}")

    emb_cfg = cfg["embedding"]
    embedder = EmbeddingModel(model_name=emb_cfg["model_name"], device=emb_cfg.get("device"),
                              normalize=emb_cfg.get("normalize", True))
    print("Encoding...")
    X_train = embedder.encode(train_df["cleaned_text"].tolist(), batch_size=emb_cfg.get("batch_size", 64))
    X_query = embedder.encode(query_df["cleaned_text"].tolist(), batch_size=emb_cfg.get("batch_size", 64))
    embedder.save_embeddings(X_train, cfg["paths"]["embeddings"])

    sim = SimilarityIndex(metric=cfg["similarity"]["metric"], top_k=cfg["similarity"]["top_k"])
    meta_cols = ["ticket_id", "title", "category", "resolution"]
    sim.build(X_train, train_df[meta_cols])
    sim.save(Path(cfg["paths"]["artifacts_dir"]) / "faiss.index",
             Path(cfg["paths"]["artifacts_dir"]) / "metadata.csv")

    # Retrieval metrics: category match as relevance proxy
    results = sim.search(X_query, top_k=5)
    true_cats = query_df["category"].tolist()
    hits_at_1 = 0
    hits_at_5 = 0
    mrr = 0.0
    for i, row in enumerate(results):
        true_c = true_cats[i]
        ranks = [j for j, r in enumerate(row) if r["category"] == true_c]
        if ranks:
            hits_at_5 += 1
            if ranks[0] == 0:
                hits_at_1 += 1
            mrr += 1.0 / (ranks[0] + 1)
    n = len(results)
    print(f"Recall@1 (category): {hits_at_1/n:.3f}")
    print(f"Recall@5 (category): {hits_at_5/n:.3f}")
    print(f"MRR@5: {mrr/n:.3f}")

    print("✅ Index saved to", cfg["paths"]["artifacts_dir"])

if __name__ == "__main__":
    main()
