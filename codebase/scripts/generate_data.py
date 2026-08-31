#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data.generator import generate_ticket_dataset
from src.utils.helpers import load_config, ensure_dirs

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n-samples", type=int, default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--output", default=None)
    p.add_argument("--config", default="config/config.yaml")
    args = p.parse_args()
    cfg = load_config(args.config)
    n = args.n_samples or cfg["data"]["n_samples"]
    seed = args.seed or cfg["data"]["random_seed"]
    out = args.output or cfg["paths"]["raw_data"]
    ensure_dirs(Path(out).parent)
    print(f"Generating {n} tickets...")
    df = generate_ticket_dataset(n_samples=n, seed=seed)
    df.to_csv(out, index=False)
    print(f"Saved → {out}")
    print(df["category"].value_counts().to_string())

if __name__ == "__main__":
    main()
