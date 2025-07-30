from typing import Dict, List, Optional, Callable, Any, Union
from num_agents.reasoning.nodes.node_base import Node
from num_agents.reasoning.semantic_models import Expertise
from num_agents.reasoning.models import Proposition
import math
import statistics
import numpy as np

# Import robust aggregation strategies
try:
    from num_agents.reasoning.nodes.dynamic_expertise_flow import trimmed_mean, winsorized_mean
except ImportError:
    # Define them here as fallback
    def trimmed_mean(scores, weights=None, trim_percent=0.1):
        """Calculate trimmed mean (removes extreme values)."""
        if not scores:
            return 0.0
        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        k = int(n * trim_percent)
        if k >= n // 2:
            return statistics.median(sorted_scores)
        return sum(sorted_scores[k:n-k]) / (n - 2*k)

    def winsorized_mean(scores, weights=None, winsor_percent=0.1):
        """Calculate winsorized mean (caps extreme values instead of removing them)."""
        if not scores:
            return 0.0
        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        k = int(n * winsor_percent)
        if k >= n // 2:
            return statistics.median(sorted_scores)
        winsorized = sorted_scores.copy()
        for i in range(k):
            winsorized[i] = sorted_scores[k]
            winsorized[n-i-1] = sorted_scores[n-k-1]
        return sum(winsorized) / n

class MultiExpertiseAggregationNode(Node):
    """
    Node that aggregates domain relevance and multiple expertises (multi-agents) to compute a global confidence score for a proposition.
    Supports:
      - Multiple expertises (shared_store["expertises"])
      - Optional agent weights (shared_store["agent_weights"])
      - Aggregation strategy: 'mean', 'max', 'min', 'softmax', 'median', or a custom callable
      - Returns agent-level details if shared_store["return_agent_details"] is True
      - Backward compatible: if only 'expertise' is present, acts as before
    """
    def __init__(self, name: str = "MultiExpertiseAggregationNode"):
        super().__init__(name=name)
        import logging
        self.logger = logging.getLogger(__name__)

    def _run(self, shared_store: dict) -> dict:
        # Store shared_store for access in _aggregate
        self.shared_store = shared_store
        
        # Backward compatibility: single expertise
        expertises: Optional[List[Expertise]] = shared_store.get("expertises")
        if expertises is None:
            single = shared_store.get("expertise")
            if single is not None:
                expertises = [single]
        if not expertises:
            self.logger.error("No expertises provided.")
            return shared_store
        logic_engine = shared_store.get("logic_engine")
        current_context_id = shared_store.get("current_context_id")
        if not (logic_engine and current_context_id):
            self.logger.error("Missing required shared_store items.")
            return shared_store
        context = logic_engine.get_context(current_context_id)
        if not context or not context.propositions:
            self.logger.info("No propositions to process.")
            return shared_store
        agent_weights: Optional[List[float]] = shared_store.get("agent_weights")
        if agent_weights is not None and len(agent_weights) != len(expertises):
            raise ValueError("Length of agent_weights must match number of expertises")
        aggregation_strategy: Union[str, Callable[[List[float], Optional[List[float]]], float]] = shared_store.get("aggregation_strategy", "mean")
        return_agent_details: bool = shared_store.get("return_agent_details", False)
        agent_confidence_details = {}
        for prop in context.propositions.values():
            agent_scores = []
            for idx, exp in enumerate(expertises):
                score = self._agent_confidence(prop, exp)
                weight = agent_weights[idx] if agent_weights else 1.0
                agent_scores.append((score, weight))
            # Sépare les scores et poids
            scores = [s for s, w in agent_scores]
            weights = [w for s, w in agent_scores]
            confidence = self._aggregate(scores, weights, aggregation_strategy)
            logic_engine.update_proposition_confidence(prop.id, confidence)
            prop.confidence = confidence
            if return_agent_details:
                agent_confidence_details[prop.id] = scores
            self.logger.info(f"Multi-agent aggregated confidence for proposition {prop.id}: {confidence:.4f}")
        if return_agent_details:
            shared_store["agent_confidence_details"] = agent_confidence_details
        return shared_store

    def _agent_confidence(self, proposition: Proposition, expertise: Expertise) -> float:
        domain_relevance: Dict[str, float] = proposition.domain_relevance or {}
        prof_dict = {d.name: d.proficiency for d in expertise.domains}
        weighted_sum = 0.0
        total_weight = 0.0
        for domain, relevance in domain_relevance.items():
            proficiency = prof_dict.get(domain)
            if proficiency is not None:
                weighted_sum += relevance * proficiency
                total_weight += proficiency
        if total_weight > 0:
            return weighted_sum / total_weight
        return 0.0

    def _aggregate(self, scores: List[float], weights: Optional[List[float]], strategy: Union[str, Callable[[List[float], Optional[List[float]]], float]]) -> float:
        if callable(strategy):
            return float(strategy(scores, weights))
        if not scores:
            return 0.0
        if strategy == "mean":
            if weights:
                return sum(s * w for s, w in zip(scores, weights)) / sum(weights)
            else:
                return sum(scores) / len(scores)
        elif strategy == "max":
            return max(scores)
        elif strategy == "min":
            return min(scores)
        elif strategy == "median":
            return statistics.median(scores)
        elif strategy == "softmax":
            exp_scores = [math.exp(s) for s in scores]
            return sum(s * e for s, e in zip(scores, exp_scores)) / sum(exp_scores)
        elif strategy == "trimmed_mean":
            # Get parameters from shared_store if available
            trim_percent = 0.1  # Default
            if hasattr(self, "shared_store") and self.shared_store.get("robust_aggregation_params"):
                trim_percent = self.shared_store.get("robust_aggregation_params").get("trim_percent", 0.1)
            return trimmed_mean(scores, weights, trim_percent)
        elif strategy == "winsorized_mean":
            # Get parameters from shared_store if available
            winsor_percent = 0.1  # Default
            if hasattr(self, "shared_store") and self.shared_store.get("robust_aggregation_params"):
                winsor_percent = self.shared_store.get("robust_aggregation_params").get("winsor_percent", 0.1)
            return winsorized_mean(scores, weights, winsor_percent)
        else:
            raise ValueError(f"Unknown aggregation strategy: {strategy}")
