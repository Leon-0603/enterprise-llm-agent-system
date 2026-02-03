# router.py

from enum import Enum
from typing import Dict

class Tool(Enum):
    RAG = "rag_tool"
    LORA = "lora_tool"

def route_with_confidence(query: str) -> Dict:
    q = query.lower()
    score = {
        Tool.RAG: 0,
        Tool.LORA: 0
    }

    rag_keywords = [
        "cite", "reference", "paper", "section", "page",
        "according to", "source"
    ]

    lora_keywords = [
        "why", "how", "explain", "compare",
        "advantage", "disadvantage", "impact", "reason"
    ]

    for k in rag_keywords:
        if k in q:
            score[Tool.RAG] += 2

    for k in lora_keywords:
        if k in q:
            score[Tool.LORA] += 2

    # Keywords
    if q.startswith(("why", "how", "explain")):
        score[Tool.LORA] += 1

    if "according to" in q:
        score[Tool.RAG] += 1

    # Decision
    if score[Tool.RAG] > score[Tool.LORA]:
        decision = Tool.RAG
    elif score[Tool.LORA] > score[Tool.RAG]:
        decision = Tool.LORA
    else:
        decision = Tool.RAG  #  Default : RAG

    confidence = abs(score[Tool.RAG] - score[Tool.LORA])

    return {
        "tool": decision,
        "score": score,
        "confidence": confidence
    }
