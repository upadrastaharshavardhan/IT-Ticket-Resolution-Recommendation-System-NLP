from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import yaml
from src.data.preprocessing import TicketPreprocessor
from src.models.embeddings import EmbeddingModel
from src.models.similarity import SimilarityIndex

class ResolutionRecommender:
    def __init__(self, embedder, similarity, preprocessor):
        self.embedder = embedder
        self.similarity = similarity
        self.preprocessor = preprocessor

    def recommend(self, title: str = "", description: str = "",
                  full_text: Optional[str] = None, top_k: int = 5) -> Dict[str, Any]:
        if full_text is None:
            full_text = f"Title: {title}\nDescription: {description}"
        cleaned = self.preprocessor.clean(full_text)
        emb = self.embedder.encode([cleaned], show_progress=False)
        similar = self.similarity.search(emb, top_k=top_k)[0]
        return {
            "recommendations": similar,
            "top_resolution": similar[0]["resolution"] if similar else "",
            "top_similarity": similar[0]["similarity"] if similar else 0.0,
            "cleaned_input": cleaned[:300],
        }

    def recommend_batch(self, texts: List[str], top_k: int = 3) -> List[Dict]:
        cleaned = self.preprocessor.transform(texts)
        embs = self.embedder.encode(cleaned, show_progress=True)
        all_sim = self.similarity.search(embs, top_k=top_k)
        return [{"recommendations": s, "top_resolution": s[0]["resolution"] if s else ""} for s in all_sim]

    @classmethod
    def load(cls, artifacts_dir: Union[str, Path], config_path: Optional[Union[str, Path]] = None):
        artifacts_dir = Path(artifacts_dir)
        if config_path is None:
            config_path = Path("config/config.yaml")
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        emb_cfg = cfg.get("embedding", {})
        sim_cfg = cfg.get("similarity", {})
        embedder = EmbeddingModel(
            model_name=emb_cfg.get("model_name", "sentence-transformers/all-MiniLM-L6-v2"),
            device=emb_cfg.get("device"), normalize=emb_cfg.get("normalize", True),
        )
        similarity = SimilarityIndex(metric=sim_cfg.get("metric", "cosine"), top_k=sim_cfg.get("top_k", 5))
        similarity.load(artifacts_dir / "faiss.index", artifacts_dir / "metadata.csv")
        preprocessor = TicketPreprocessor(max_text_length=cfg.get("preprocessing", {}).get("max_text_length", 1200))
        return cls(embedder, similarity, preprocessor)
