import re

from typing import Dict, List

class FactCheckingAgent:
    """Fact Checking Agent validates generated outputs and computes confidence."""

    async def verify(self, summary: str, chunks: List[dict]) -> Dict[str, float]:
        if not summary or not chunks:
            return {"confidence": 0.0}

        evidence = " ".join(str(chunk.get("text", "")) for chunk in chunks).lower()
        terms = set(re.findall(r"[a-z0-9]+", summary.lower()))
        meaningful_terms = {term for term in terms if len(term) > 2}
        if not meaningful_terms:
            return {"confidence": 0.0}

        supported = sum(term in evidence for term in meaningful_terms)
        return {"confidence": round(supported / len(meaningful_terms), 2)}
