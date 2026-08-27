import re

from openai import OpenAI

from app.models import RetrievedChunk


class BaseAnswerGenerator:
    def generate(self, question: str, context: list[RetrievedChunk]) -> str:
        raise NotImplementedError


class LocalAnswerGenerator(BaseAnswerGenerator):
    # This fallback keeps local runs and CI independent from an API key.
    # It is intentionally simple and is not meant to behave like an LLM.
    def generate(self, question: str, context: list[RetrievedChunk]) -> str:
        query_terms = set(re.findall(r"\w+", question.lower()))
        scored_sentences = []

        for item in context:
            sentences = re.split(r"(?<=[.!?])\s+", item.chunk.text)
            for sentence in sentences:
                terms = set(re.findall(r"\w+", sentence.lower()))
                score = len(query_terms & terms)
                if score:
                    scored_sentences.append((score, sentence.strip()))

        if not scored_sentences:
            return "I could not find enough information in the retrieved documents."

        scored_sentences.sort(key=lambda item: item[0], reverse=True)

        selected = []
        seen = set()

        for _, sentence in scored_sentences:
            if sentence in seen:
                continue
            selected.append(sentence)
            seen.add(sentence)
            if len(selected) == 3:
                break

        return " ".join(selected)


class OpenAIAnswerGenerator(BaseAnswerGenerator):
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, question: str, context: list[RetrievedChunk]) -> str:
        context_text = "\n\n".join(
            f"[{item.chunk.id}] {item.chunk.text}" for item in context
        )

        prompt = f"""
Answer the question using only the supplied context.

If the context is insufficient, say that clearly.
Do not invent details.
Use chunk ids in square brackets where useful.

Question:
{question}

Context:
{context_text}
""".strip()

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text
