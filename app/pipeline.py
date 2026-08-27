import time

from app.config import Settings
from app.ingestion import load_documents
from app.llm import LocalAnswerGenerator, OpenAIAnswerGenerator
from app.models import AskResponse, Citation
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.dense import DenseRetriever
from app.retrieval.filtering import filter_by_department
from app.retrieval.fusion import reciprocal_rank_fusion
from app.retrieval.reranker import Reranker
from app.security import detect_prompt_injection
from app.trace import Trace


class RAGPipeline:
    def __init__(self, settings: Settings, data_dir: str = "data/sample_docs"):
        self.settings = settings
        self.chunks = load_documents(
            data_dir,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
        )

        if not self.chunks:
            raise RuntimeError(f"No documents found under {data_dir}")

        self.bm25 = BM25Retriever(self.chunks)
        self.dense = DenseRetriever(self.chunks, settings.dense_model)
        self.reranker = Reranker(settings.rerank_model)
        self.answer_generator = self._create_answer_generator()

    def _create_answer_generator(self):
        if self.settings.llm_provider.lower() == "openai":
            if not self.settings.openai_api_key:
                raise RuntimeError("OPENAI_API_KEY is required for OpenAI mode")

            return OpenAIAnswerGenerator(
                api_key=self.settings.openai_api_key,
                model=self.settings.openai_model,
            )

        return LocalAnswerGenerator()

    def _rewrite_query(self, question: str) -> str:
        return " ".join(question.strip().split())

    def ask(self, question: str, department: str | None = None) -> AskResponse:
        request_started = time.perf_counter()
        trace = Trace()

        if detect_prompt_injection(question):
            return AskResponse(
                answer="The request was blocked because it looks like an attempt to override system instructions.",
                citations=[],
                retrieved_chunks=0,
                latency_ms=round((time.perf_counter() - request_started) * 1000, 2),
                trace_id=trace.trace_id,
            )

        started = time.perf_counter()
        query = self._rewrite_query(question)
        trace.record("query_rewrite", started)

        started = time.perf_counter()
        dense_results = self.dense.search(
            query,
            top_k=self.settings.top_k_dense,
        )
        lexical_results = self.bm25.search(
            query,
            top_k=self.settings.top_k_bm25,
        )
        trace.record(
            "first_stage_retrieval",
            started,
            dense=len(dense_results),
            lexical=len(lexical_results),
        )

        started = time.perf_counter()
        dense_results = filter_by_department(dense_results, department)
        lexical_results = filter_by_department(lexical_results, department)
        trace.record("metadata_filter", started, department=department)

        started = time.perf_counter()
        fused = reciprocal_rank_fusion([dense_results, lexical_results])
        trace.record("rrf", started, candidates=len(fused))

        started = time.perf_counter()
        reranked = self.reranker.rerank(
            query=query,
            candidates=fused[:15],
            top_k=self.settings.top_k_rerank,
        )
        trace.record("rerank", started, selected=len(reranked))

        started = time.perf_counter()
        answer = self.answer_generator.generate(question, reranked)
        trace.record("generation", started)

        citations = [
            Citation(
                source=item.chunk.source,
                chunk_id=item.chunk.id,
            )
            for item in reranked
        ]

        elapsed_ms = (time.perf_counter() - request_started) * 1000

        return AskResponse(
            answer=answer,
            citations=citations,
            retrieved_chunks=len(reranked),
            latency_ms=round(elapsed_ms, 2),
            trace_id=trace.trace_id,
        )
