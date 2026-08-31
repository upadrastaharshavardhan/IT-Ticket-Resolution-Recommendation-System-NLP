# Research Package - Project 9
## IT Ticket Resolution Recommendation System

Complete research paper, documentation, metrics, and full codebase.

**Key metrics:** Recall@1 0.890 | Recall@5 0.970 | MRR@5 0.930

## Contents
- paper/ (PDF + MD)
- docs/
- results/
- codebase/ (full Project 9 source)

## Reproduce
```bash
cd codebase
pip install -r requirements.txt
python scripts/generate_data.py --n-samples 3000 --seed 42
python scripts/train.py
```
