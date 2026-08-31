#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline.recommender import ResolutionRecommender
from src.utils.helpers import load_config

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--artifacts", default="artifacts")
    p.add_argument("--config", default="config/config.yaml")
    args = p.parse_args()
    rec = ResolutionRecommender.load(args.artifacts, args.config)
    r = rec.recommend(
        title="Cannot connect to VPN from home",
        description="VPN times out after entering credentials.",
    )
    print("Top similarity:", r["top_similarity"])
    print("Top resolution:", r["top_resolution"][:200])
    print("Num recommendations:", len(r["recommendations"]))

if __name__ == "__main__":
    main()
