# IT Ticket Resolution Recommendation System

**Project 9** – Find similar historical IT incidents and recommend proven solutions using NLP.

## What it does

Given a new IT ticket (title + description), the system:

1. Embeds the ticket into a semantic vector space
2. Retrieves the most similar **resolved** historical tickets
3. Recommends their resolution steps / solution text
4. Returns similarity scores for transparency

## Key Features

- Synthetic ITSM ticket corpus with resolution text
- Sentence-transformer embeddings + FAISS retrieval
- Ranked solution recommendations
- Metrics: MRR@k, Recall@k (category/match based)
- Gradio demo
- Colab-ready modular structure

## Quick Start

```bash
!pip install -r requirements.txt
!python scripts/generate_data.py --n-samples 3000
!python scripts/train.py
!python -m src.api.gradio_app
```

## Example

```python
from src.pipeline.recommender import ResolutionRecommender
rec = ResolutionRecommender.load("artifacts")
result = rec.recommend(
    title="Cannot connect to VPN from home",
    description="VPN times out after entering credentials. Affects remote users."
)
print(result["recommendations"])
# [{ticket_id, similarity, resolution, category}, ...]
```

## License

MIT
