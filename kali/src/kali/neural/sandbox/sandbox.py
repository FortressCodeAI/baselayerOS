"""
Kali v1.0.0 — Neural Sandbox

This is where DeepSeek is actually used.

Responsibilities:
- build governance prompt
- sanitize prompt
- call NeuralClient
- validate output schema
- log everything
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.config import KaliConfig
from kali.core.logging import KaliLogger
from kali.neural.sandbox.logger import SandboxLogger
from kali.neural.sandbox.filters import sanitize_prompt, build_governance_prompt
from kali.neural.sandbox.schema import validate_explanation
from kali.neural.sandbox.client import NeuralClient


class NeuralSandbox:
    def __init__(self, config: KaliConfig, logger: KaliLogger):
        self.config = config
        self.logger = logger
        self.sandbox_logger = SandboxLogger()
        self.client = NeuralClient(model_name=config.neural.model_name)

    def explain_governance(self, envelope_state) -> Dict[str, Any]:
        """
        Use the model to explain the governance decision.
        """
        raw_prompt = build_governance_prompt(envelope_state)
        safe_prompt = sanitize_prompt(raw_prompt)

        self.sandbox_logger.log(
            "prompt_built",
            envelope_id=envelope_state.envelope_id,
            raw_prompt=raw_prompt,
            safe_prompt=safe_prompt,
        )

        output_text = self.client.generate(
            prompt=safe_prompt,
            max_tokens=self.config.neural.max_tokens,
            temperature=self.config.neural.temperature,
        )

        self.sandbox_logger.log(
            "output_received",
            envelope_id=envelope_state.envelope_id,
            output_text=output_text,
        )

        explanation = validate_explanation({"text": output_text, "format": "text"})

        self.sandbox_logger.log(
            "explanation_validated",
            envelope_id=envelope_state.envelope_id,
            explanation=explanation,
        )

        self.logger.info(
            "neural_explanation_generated",
            envelope_id=envelope_state.envelope_id,
        )

        return explanation
