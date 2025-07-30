import os
from typing import List
from yaaaf.components.agents.orchestrator_agent import OrchestratorAgent
from yaaaf.components.agents.reflection_agent import ReflectionAgent
from yaaaf.components.agents.reviewer_agent import ReviewerAgent
from yaaaf.components.agents.sql_agent import SqlAgent
from yaaaf.components.agents.rag_agent import RAGAgent
from yaaaf.components.agents.url_agent import URLAgent
from yaaaf.components.agents.url_reviewer_agent import UrlReviewerAgent
from yaaaf.components.agents.user_input_agent import UserInputAgent
from yaaaf.components.agents.visualization_agent import VisualizationAgent
from yaaaf.components.agents.websearch_agent import DuckDuckGoSearchAgent
from yaaaf.components.agents.brave_search_agent import BraveSearchAgent
from yaaaf.components.agents.bash_agent import BashAgent
from yaaaf.components.client import OllamaClient
from yaaaf.components.sources.sqlite_source import SqliteSource
from yaaaf.components.sources.rag_source import RAGSource
from yaaaf.server.config import Settings, AgentSettings


class OrchestratorBuilder:
    def __init__(self, config: Settings):
        self.config = config
        self._agents_map = {
            "reflection": ReflectionAgent,
            "visualization": VisualizationAgent,
            "sql": SqlAgent,
            "rag": RAGAgent,
            "reviewer": ReviewerAgent,
            "websearch": DuckDuckGoSearchAgent,
            "brave_search": BraveSearchAgent,
            "url": URLAgent,
            "url_reviewer": UrlReviewerAgent,
            "user_input": UserInputAgent,
            "bash": BashAgent,
        }

    def _load_text_from_file(self, file_path: str) -> str:
        """Load text content from a file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()

    def _create_rag_sources(self) -> List[RAGSource]:
        """Create RAG sources from text-type sources in config."""
        rag_sources = []
        for source_config in self.config.sources:
            if source_config.type == "text":
                description = getattr(source_config, "description", source_config.name)
                rag_source = RAGSource(
                    description=description, source_path=source_config.path
                )

                # Load text content from file or directory
                if os.path.isfile(source_config.path):
                    # Single file
                    text_content = self._load_text_from_file(source_config.path)
                    rag_source.add_text(text_content)
                elif os.path.isdir(source_config.path):
                    # Directory of files
                    for filename in os.listdir(source_config.path):
                        file_path = os.path.join(source_config.path, filename)
                        if os.path.isfile(file_path) and filename.lower().endswith(
                            (".txt", ".md", ".html", ".htm")
                        ):
                            text_content = self._load_text_from_file(file_path)
                            rag_source.add_text(text_content)

                rag_sources.append(rag_source)
        return rag_sources

    def _get_sqlite_source(self):
        """Get the first SQLite source from config."""
        for source_config in self.config.sources:
            if source_config.type == "sqlite":
                return SqliteSource(
                    name=source_config.name,
                    db_path=source_config.path,
                )
        return None

    def _create_client_for_agent(self, agent_config) -> OllamaClient:
        """Create a client for an agent, using agent-specific settings if available."""
        if isinstance(agent_config, AgentSettings):
            # Use agent-specific settings, falling back to default client settings
            model = agent_config.model or self.config.client.model
            temperature = (
                agent_config.temperature
                if agent_config.temperature is not None
                else self.config.client.temperature
            )
            max_tokens = (
                agent_config.max_tokens
                if agent_config.max_tokens is not None
                else self.config.client.max_tokens
            )
        else:
            # Use default client settings for string-based agent names
            model = self.config.client.model
            temperature = self.config.client.temperature
            max_tokens = self.config.client.max_tokens

        return OllamaClient(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def _get_agent_name(self, agent_config) -> str:
        """Extract agent name from config (either string or AgentSettings object)."""
        if isinstance(agent_config, AgentSettings):
            return agent_config.name
        return agent_config

    def build(self):
        # Create default client for orchestrator
        orchestrator_client = OllamaClient(
            model=self.config.client.model,
            temperature=self.config.client.temperature,
            max_tokens=self.config.client.max_tokens,
        )

        # Prepare sources
        sqlite_source = self._get_sqlite_source()
        rag_sources = self._create_rag_sources()

        orchestrator = OrchestratorAgent(orchestrator_client)

        for agent_config in self.config.agents:
            agent_name = self._get_agent_name(agent_config)

            if agent_name not in self._agents_map:
                raise ValueError(f"Agent '{agent_name}' is not recognized.")

            # Create agent-specific client
            agent_client = self._create_client_for_agent(agent_config)

            if agent_name == "sql" and sqlite_source is not None:
                orchestrator.subscribe_agent(
                    self._agents_map[agent_name](
                        client=agent_client, source=sqlite_source
                    )
                )
            elif agent_name == "rag" and rag_sources:
                orchestrator.subscribe_agent(
                    self._agents_map[agent_name](
                        client=agent_client, sources=rag_sources
                    )
                )
            elif agent_name not in ["sql", "rag"]:
                orchestrator.subscribe_agent(
                    self._agents_map[agent_name](client=agent_client)
                )

        return orchestrator
