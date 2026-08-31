from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import gradio as gr
from src.pipeline.recommender import ResolutionRecommender
from src.utils.helpers import load_config

def build_demo(artifacts_dir="artifacts", config_path="config/config.yaml"):
    cfg = load_config(config_path)
    rec = ResolutionRecommender.load(artifacts_dir, config_path)

    def recommend_fn(title, description, top_k):
        r = rec.recommend(title=title, description=description, top_k=int(top_k))
        lines = [
            f"### Top recommended resolution (sim={r['top_similarity']:.3f})",
            f"{r['top_resolution']}",
            "",
            "### Similar historical tickets",
        ]
        for i, s in enumerate(r.get("recommendations", []), 1):
            lines.append(
                f"**{i}. `{s['ticket_id']}`** | {s['category']} | sim={s['similarity']:.3f}  \n"
                f"   *{s['title']}*  \n"
                f"   Resolution: {s['resolution'][:200]}{'...' if len(s['resolution'])>200 else ''}"
            )
        return "\n".join(lines)

    demo = gr.Interface(
        fn=recommend_fn,
        inputs=[
            gr.Textbox(label="Ticket title", value="Cannot connect to VPN from home"),
            gr.Textbox(lines=4, label="Description",
                       value="VPN times out after entering credentials. Affects remote users."),
            gr.Slider(1, 8, value=5, step=1, label="Number of recommendations"),
        ],
        outputs=gr.Markdown(),
        title=cfg.get("gradio", {}).get("title", "IT Ticket Resolution Recommender"),
        description=cfg.get("gradio", {}).get("description", ""),
        examples=[
            ["Cannot connect to VPN from home", "VPN times out after credentials.", 5],
            ["New employee cannot access email", "AD account missing. Cannot open Outlook.", 3],
            ["Production DB high CPU", "CPU above 90% for 2 hours. App latency high.", 5],
        ],
        allow_flagging="never",
    )
    return demo

if __name__ == "__main__":
    build_demo().launch(share=False, server_name="0.0.0.0")
