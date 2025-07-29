"""Prototype Guardrail Designer agent with model routing."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional
from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:                      # static-analysis path
    from agents import Agent as AgentBase
else:                                  # runtime – keep the graceful fallback
    try:
        from agents import Agent as AgentBase  # type: ignore
    except Exception:  # pragma: no cover – SDK unavailable

        class AgentBase:               # noqa: D101  (very small stub)
            """Minimal stand-in when the Agents SDK is unavailable."""

            def __init__(
                self, name: str | None = None, tools: list[Any] | None = None
            ) -> None:
                self.name = name or "StubAgent"
                self.tools = tools or []

            async def run(self, *_: Any, **__: Any) -> Dict[str, Any]:
                return {"status": "error", "error": "agents SDK unavailable"}


from meta_agent.services.guardrail_router import GuardrailModelRouter, LLMModelAdapter
from meta_agent.services.llm_service import LLMService

BaseAgent = AgentBase

logger = logging.getLogger(__name__)


class GuardrailDesignerAgent(BaseAgent):
    """Generates guardrail code using configurable model backends."""

    def __init__(
        self,
        model_router: Optional[GuardrailModelRouter] = None,
        *,
        api_key: Optional[str] = None,
        default_model: str = "gpt-4o-mini",
    ) -> None:
        super().__init__(name="GuardrailDesignerAgent", tools=[])

        if model_router is None:
            service = LLMService(api_key=api_key, model=default_model)
            adapter = LLMModelAdapter(service)
            model_router = GuardrailModelRouter({default_model: adapter}, default_model)
            self.default_model = default_model
        else:
            # Use the router's default model to ensure compatibility
            self.default_model = model_router.default_model

        self.model_router = model_router
        logger.info(
            "GuardrailDesignerAgent initialized with model %s", self.default_model
        )

    async def run(self, specification: Dict[str, Any]) -> Dict[str, Any]:
        prompt = specification.get("prompt") or specification.get("description", "")
        model = specification.get("model", self.default_model)
        result = await self.model_router.invoke(prompt, model=model)
        return {"status": "success", "output": result}
