try:
    from keywordsai_tracing.integrations.openai_agents_integration import (
        OpenAIAgentIntegration
    )
    AGENTS_AVAILABLE = True
except ImportError:
    raise ImportError(
        "OpenAI agents integration requires additional dependencies. "
        "Please install them with: pip install 'keywordsai-tracing[openai-agents]'"
    )