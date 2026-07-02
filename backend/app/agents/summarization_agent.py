import re

from typing import List, Optional


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "did",
    "do",
    "does",
    "for",
    "how",
    "in",
    "is",
    "of",
    "on",
    "the",
    "to",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
}

ACTION_WORDS = {
    "asked",
    "built",
    "carried",
    "created",
    "discovered",
    "found",
    "gave",
    "helped",
    "made",
    "moved",
    "opened",
    "picked",
    "planted",
    "ran",
    "saved",
    "shared",
    "spoke",
    "took",
    "tried",
    "walked",
    "watered",
    "went",
    "worked",
    "wrote",
}

class SummarizationAgent:
    """Summarization Agent converts retrieved chunks into concise answers.

    This local implementation selects the sentences that best match the
    question. It avoids returning raw chunks while keeping the app usable
    without an external LLM.
    """

    async def summarize(self, chunks: List[dict], query: Optional[str] = None) -> str:
        if not chunks:
            return "I couldn't find relevant documents to answer that question."

        ranked = sorted(chunks, key=lambda c: (c.get("distance") is None, c.get("distance")))
        text = re.sub(r"\s+", " ", str(ranked[0].get("text", ""))).strip()
        if not text:
            return "I couldn't find relevant documents to answer that question."

        sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
        if not sentences:
            return text[:350].strip()

        query_terms = {
            token
            for token in re.findall(r"[a-z0-9]+", (query or "").lower())
            if len(token) > 1 and token not in STOP_WORDS
        }
        is_action_question = bool(re.search(r"\bwhat\s+(?:did|does|do)\b", (query or "").lower()))
        best_index = max(
            range(len(sentences)),
            key=lambda index: self._sentence_score(
                sentences[index], query_terms, is_action_question, index
            ),
        )

        selected = [sentences[best_index]]
        if is_action_question and best_index + 1 < len(sentences):
            following = sentences[best_index + 1]
            if re.match(r"(?i)^(?:he|she|they|it|instead|then|after|before)\b", following):
                selected.append(following)

        answer = " ".join(selected)
        answer = re.sub(r"^.*?\bonce upon a time,?\s*", "", answer, flags=re.IGNORECASE)
        answer = answer.strip()
        if answer:
            answer = answer[0].upper() + answer[1:]
        return answer[:500]

    @staticmethod
    def _sentence_score(
        sentence: str,
        query_terms: set[str],
        is_action_question: bool,
        index: int,
    ) -> tuple[int, int, int]:
        words = set(re.findall(r"[a-z0-9]+", sentence.lower()))
        overlap = len(words & query_terms)
        action_score = len(words & ACTION_WORDS) if is_action_question else 0
        return overlap, action_score, -index
