"""
Expertise Weighting Node for Nüm Agents SDK.

This module provides a Node implementation that uses LLM to analyze propositions
and adjust their confidence based on the agent's expertise in relevant domains.
"""

import json
import logging
from typing import List, Dict, Optional, Any

from num_agents.core import Node, SharedStore
from num_agents.reasoning.llm import LLMProviderFactory
from num_agents.reasoning.models import (
    Proposition, 
    PropositionType, 
    PropositionStatus,
    LogicalContext
)
from num_agents.reasoning.semantic_models import (
    Expertise,
    ExpertiseDomain
)
from num_agents.reasoning.logic_engine import LogicEngine
from .node_base import Node


class ExpertiseWeightingNode(Node):
    """
    A node that uses an LLM to analyze propositions and adjust their confidence based on domain-specific expertise.
    """

    def __init__(
        self,
        name: str,
        llm_provider: str = "openai",
        llm_model: Optional[str] = None,
        llm_api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1000,
    ):
        super().__init__(name)
        self.logger = logging.getLogger(__name__)
        self.llm_provider: LLMProvider = LLMProviderFactory.create_provider(
            provider_name=llm_provider,
            model=llm_model,
            api_key=llm_api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def _get_domain_relevance_prompt(
        self, proposition_text: str, expertise_domains: List[str]
    ) -> str:
        """
        Creates a prompt to ask the LLM for the domain relevance of a proposition.
        """
        return (
            f"Analyze the following proposition: '{proposition_text}'. "
            f"Determine its relevance to each of the following domains: {expertise_domains}. "
            "Provide a score from 0.0 to 1.0 for each domain, where 1.0 is highly relevant. "
            "Return the result as a JSON object with domain names as keys and scores as values. "
            'Example: {{"Physics": 0.9, "Biology": 0.1}}'
        )

    def _get_confidence_adjustment_prompt(
        self, proposition_text: str, relevant_domains: Dict[str, float], expertise: Expertise
    ) -> str:
        """
        Creates a prompt to ask the LLM for a confidence adjustment factor.
        """
        expertise_details = ", ".join(
            [
                f"{domain.name} (Proficiency: {domain.proficiency})"
                for domain in expertise.domains
            ]
        )
        return (
            f"A proposition is given: '{proposition_text}'.\n"
            f"It is relevant to the following domains with given scores: {relevant_domains}.\n"
            f"The agent has the following expertise: {expertise_details}.\n"
            "Based on the agent's expertise in the relevant domains, calculate a confidence adjustment factor "
            "between 0.5 (no expertise) and 1.5 (high expertise). "
            "A factor of 1.0 means neutral confidence. "
            "Return the result as a JSON object with a single key 'confidence_factor'. "
            'Example: {{"confidence_factor": 1.2}}'
        )

    def _process_proposition(
        self, proposition: Proposition, logic_engine: LogicEngine, expertise: Expertise
    ):
        """
        Processes a single proposition to determine domain relevance and adjust confidence.
        """
        # 1. Get domain relevance if not already present
        if not proposition.domain_relevance:
            expertise_domains = [d.name for d in expertise.domains]
            if not expertise_domains:
                self.logger.warning("No expertise domains found to evaluate relevance.")
                return

            prompt = self._get_domain_relevance_prompt(
                proposition.text, expertise_domains
            )
            relevance_response = self.llm_provider.generate_json(prompt)

            if relevance_response:
                try:
                    proposition.domain_relevance = relevance_response
                    logic_engine.update_proposition_domain_relevance(
                        proposition.id, proposition.domain_relevance
                    )
                    self.logger.info(
                        f"Updated domain relevance for proposition {proposition.id}: {proposition.domain_relevance}"
                    )
                except Exception as e:
                    self.logger.error(
                        f"Failed to parse or validate domain relevance response: {relevance_response}. Error: {e}"
                    )
                    return

        # 2. Get confidence adjustment factor
        if proposition.domain_relevance:
            # Filter for relevant domains (score > 0.5)
            relevant_domains = {
                domain: score
                for domain, score in proposition.domain_relevance.items()
                if score > 0.5
            }

            if not relevant_domains:
                self.logger.info(
                    f"No highly relevant domains for proposition {proposition.id}. Skipping confidence adjustment."
                )
                return

            prompt = self._get_confidence_adjustment_prompt(
                proposition.text, relevant_domains, expertise
            )
            adjustment_response = self.llm_provider.generate_json(prompt)

            if adjustment_response and "confidence_factor" in adjustment_response:
                confidence_factor = adjustment_response["confidence_factor"]
                # Appliquer le facteur d'ajustement à la confiance actuelle
                new_confidence = proposition.confidence
                if new_confidence is not None:
                    new_confidence = max(0.0, min(1.0, new_confidence * confidence_factor))
                else:
                    new_confidence = confidence_factor  # Si la confiance initiale est None, on prend le facteur tel quel
                logic_engine.update_proposition_confidence(
                    proposition.id, new_confidence
                )
                self.logger.info(
                    f"Adjusted confidence for proposition {proposition.id} to {new_confidence:.2f} (factor: {confidence_factor:.2f})"
                )
            else:
                self.logger.error(
                    f"Failed to parse or validate confidence adjustment response: {adjustment_response}."
                )

    def _run(self, shared_store: SharedStore) -> SharedStore:
        """
        The main execution method for the node.
        """
        self.logger.info(f"Running node: {self.name}")

        expertise = shared_store.get("expertise")
        logic_engine = shared_store.get("logic_engine")
        current_context_id = shared_store.get("current_context_id")

        if not all([expertise, logic_engine, current_context_id]):
            self.logger.error(
                "Missing one or more required items from shared store: 'expertise', 'logic_engine', 'current_context_id'"
            )
            return shared_store

        if not isinstance(expertise, Expertise):
            self.logger.error("Item 'expertise' in shared store is not a valid Expertise object.")
            return shared_store

        if not isinstance(logic_engine, LogicEngine):
            self.logger.error("Item 'logic_engine' in shared store is not a valid LogicEngine object.")
            return shared_store

        context = logic_engine.get_context(current_context_id)
        if not context:
            self.logger.error(f"Could not find logical context with ID: {current_context_id}")
            return shared_store

        propositions = list(context.propositions.values())
        if not propositions:
            self.logger.info("No propositions in the current context to process.")
            return shared_store

        for proposition in propositions:
            self._process_proposition(proposition, logic_engine, expertise)

        self.logger.info(f"Finished running node: {self.name}")
        return shared_store
