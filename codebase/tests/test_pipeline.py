from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data.generator import generate_ticket_dataset
from src.data.preprocessing import TicketPreprocessor
from src.models.embeddings import EmbeddingModel
from src.models.similarity import SimilarityIndex

def test_gen():
    df = generate_ticket_dataset(50, seed=1)
    assert len(df) == 50
    assert "resolution" in df.columns

def test_tiny():
    df = generate_ticket_dataset(80, seed=2)
    pre = TicketPreprocessor()
    df = pre.transform_df(df)
    emb = EmbeddingModel(device="cpu")
    X = emb.encode(df["cleaned_text"].tolist(), batch_size=16, show_progress=False)
    sim = SimilarityIndex(top_k=3)
    sim.build(X, df[["ticket_id", "title", "category", "resolution"]])
    r = sim.search(X[:1])
    assert len(r[0]) >= 1
    assert "resolution" in r[0][0]

if __name__ == "__main__":
    test_gen()
    test_tiny()
    print("OK")
