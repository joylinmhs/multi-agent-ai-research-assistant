from app.schemas.chat import ChatRequest, ChatResponse, SourceReference
from app.agents.research_agent import ResearchAgent
from app.agents.summarization_agent import SummarizationAgent
from app.agents.fact_checking_agent import FactCheckingAgent
from app.agents.citation_agent import CitationAgent
from app.agents.memory_agent import MemoryAgent

class ChatService:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.summarization_agent = SummarizationAgent()
        self.fact_checking_agent = FactCheckingAgent()
        self.citation_agent = CitationAgent()
        self.memory_agent = MemoryAgent()

    async def handle_query(self, request: ChatRequest) -> ChatResponse:
        conversation_context = await self.memory_agent.load_context(request.session_id)
        retrieved_chunks = await self.research_agent.retrieve(request.query, conversation_context)
        summary = await self.summarization_agent.summarize(retrieved_chunks, request.query)
        fact_check = await self.fact_checking_agent.verify(summary, retrieved_chunks)
        sources = await self.citation_agent.generate_sources(retrieved_chunks)
        await self.memory_agent.save_context(request.session_id, request.query, summary)

        return ChatResponse(
            answer=summary,
            summary=summary,
            sources=sources,
            confidence=fact_check.get("confidence", 0.0),
            session_id=request.session_id or "default-session",
        )
