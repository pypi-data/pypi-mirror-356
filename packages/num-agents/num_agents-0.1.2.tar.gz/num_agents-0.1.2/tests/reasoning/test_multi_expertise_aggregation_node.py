import unittest
from unittest.mock import MagicMock
from num_agents.reasoning.nodes.multi_expertise_aggregation_node import MultiExpertiseAggregationNode
from num_agents.reasoning.semantic_models import Expertise, ExpertiseDomain
from num_agents.reasoning.models import Proposition, PropositionType, LogicalContext, PropositionStatus
import math

class TestMultiExpertiseAggregationNode(unittest.TestCase):
    def setUp(self):
        # 3 agents with different profiles
        self.expertises = [
            Expertise(domains=[ExpertiseDomain(name="Physics", proficiency=0.9), ExpertiseDomain(name="Biology", proficiency=0.3)], skills=[], knowledge_bases=[], metadata={}),
            Expertise(domains=[ExpertiseDomain(name="Physics", proficiency=0.5), ExpertiseDomain(name="Biology", proficiency=0.7)], skills=[], knowledge_bases=[], metadata={}),
            Expertise(domains=[ExpertiseDomain(name="Physics", proficiency=0.0), ExpertiseDomain(name="Biology", proficiency=1.0)], skills=[], knowledge_bases=[], metadata={}),
        ]
        self.context = LogicalContext(id="ctx1", name="ctx", description="desc")
        self.prop1 = Proposition(
            id="p1",
            type=PropositionType.STATEMENT,
            text="Prop 1",
            status=PropositionStatus.UNVERIFIED,
            confidence=None,
            source=None,
            metadata={},
            entity_references=[],
            entity_relations=[],
            domain_relevance={"Physics": 0.8, "Biology": 0.4}
        )
        self.prop2 = Proposition(
            id="p2",
            type=PropositionType.STATEMENT,
            text="Prop 2",
            status=PropositionStatus.UNVERIFIED,
            confidence=None,
            source=None,
            metadata={},
            entity_references=[],
            entity_relations=[],
            domain_relevance={"Physics": 0.2, "Biology": 0.9}
        )
        self.context.propositions[self.prop1.id] = self.prop1
        self.context.propositions[self.prop2.id] = self.prop2
        self.logic_engine = MagicMock()
        self.logic_engine.get_context.return_value = self.context
        self.logic_engine.update_proposition_confidence = MagicMock()

    def test_multi_agent_mean(self):
        node = MultiExpertiseAggregationNode()
        shared_store = {
            "expertises": self.expertises,
            "logic_engine": self.logic_engine,
            "current_context_id": self.context.id,
            "aggregation_strategy": "mean"
        }
        node._run(shared_store)
        # Agent 1: (0.8*0.9+0.4*0.3)/(0.9+0.3)=0.7
        # Agent 2: (0.8*0.5+0.4*0.7)/(0.5+0.7)=0.5667
        # Agent 3: (0.8*0+0.4*1)/(0+1)=0.4
        # mean = (0.7+0.5667+0.4)/3 = 0.5556
        calls = self.logic_engine.update_proposition_confidence.call_args_list
        # Map id -> value
        results = {args[0][0]: args[0][1] for args in calls}
        # Agent 1: (0.8*0.9+0.4*0.3)/(0.9+0.3)=0.7
        # Agent 2: (0.8*0.5+0.4*0.7)/(0.5+0.7)=0.5667
        # Agent 3: (0.8*0+0.4*1)/(0+1)=0.4
        expected1 = (0.7+0.5666666667+0.4)/3
        # Agent 1: (0.2*0.9+0.9*0.3)/(0.9+0.3)=0.375
        # Agent 2: (0.2*0.5+0.9*0.7)/(0.5+0.7)=0.608333...
        # Agent 3: (0.2*0+0.9*1)/(0+1)=0.9
        expected2 = (0.375+0.6083333333+0.9)/3
        self.assertIn(self.prop1.id, results)
        self.assertIn(self.prop2.id, results)
        self.assertAlmostEqual(results[self.prop1.id], expected1, places=5)
        self.assertAlmostEqual(results[self.prop2.id], expected2, places=5)

    def test_multi_agent_max(self):
        node = MultiExpertiseAggregationNode()
        shared_store = {
            "expertises": self.expertises,
            "logic_engine": self.logic_engine,
            "current_context_id": self.context.id,
            "aggregation_strategy": "max"
        }
        node._run(shared_store)
        calls = self.logic_engine.update_proposition_confidence.call_args_list
        # prop1: max(0.7,0.5667,0.4)=0.7
        args1, _ = calls[0]
        self.assertAlmostEqual(args1[1], 0.7, places=5)
        # prop2: max(0.375,0.5833,0.9)=0.9
        args2, _ = calls[1]
        self.assertAlmostEqual(args2[1], 0.9, places=5)

    def test_multi_agent_softmax(self):
        node = MultiExpertiseAggregationNode()
        shared_store = {
            "expertises": self.expertises,
            "logic_engine": self.logic_engine,
            "current_context_id": self.context.id,
            "aggregation_strategy": "softmax"
        }
        node._run(shared_store)
        calls = self.logic_engine.update_proposition_confidence.call_args_list
        # prop1 softmax
        s = [0.7,0.5666666667,0.4]
        exp_s = [math.exp(x) for x in s]
        softmax = sum(x*e for x,e in zip(s,exp_s))/sum(exp_s)
        args1, _ = calls[0]
        self.assertAlmostEqual(args1[1], softmax, places=5)

    def test_multi_agent_weights(self):
        node = MultiExpertiseAggregationNode()
        shared_store = {
            "expertises": self.expertises,
            "agent_weights": [2.0, 1.0, 1.0],
            "logic_engine": self.logic_engine,
            "current_context_id": self.context.id,
            "aggregation_strategy": "mean"
        }
        node._run(shared_store)
        calls = self.logic_engine.update_proposition_confidence.call_args_list
        # Weighted mean for prop1: (0.7*2+0.5667*1+0.4*1)/4
        expected = (0.7*2+0.5666666667+0.4)/4
        args1, _ = calls[0]
        self.assertAlmostEqual(args1[1], expected, places=5)

    def test_multi_agent_custom_strategy(self):
        node = MultiExpertiseAggregationNode()
        def custom_agg(scores, weights):
            # Return the sum of squares
            return sum(x**2 for x in scores)
        shared_store = {
            "expertises": self.expertises,
            "logic_engine": self.logic_engine,
            "current_context_id": self.context.id,
            "aggregation_strategy": custom_agg
        }
        node._run(shared_store)
        calls = self.logic_engine.update_proposition_confidence.call_args_list
        s = [0.7,0.5666666667,0.4]
        expected = sum(x**2 for x in s)
        args1, _ = calls[0]
        self.assertAlmostEqual(args1[1], expected, places=5)

    def test_return_agent_details(self):
        node = MultiExpertiseAggregationNode()
        shared_store = {
            "expertises": self.expertises,
            "logic_engine": self.logic_engine,
            "current_context_id": self.context.id,
            "aggregation_strategy": "mean",
            "return_agent_details": True
        }
        node._run(shared_store)
        details = shared_store["agent_confidence_details"]
        self.assertIn(self.prop1.id, details)
        self.assertEqual(len(details[self.prop1.id]), 3)
        self.assertAlmostEqual(details[self.prop1.id][0], 0.7, places=5)
        self.assertAlmostEqual(details[self.prop1.id][1], 0.5666666667, places=5)
        self.assertAlmostEqual(details[self.prop1.id][2], 0.4, places=5)

    def test_backward_compat_single_expertise(self):
        node = MultiExpertiseAggregationNode()
        shared_store = {
            "expertise": self.expertises[0],
            "logic_engine": self.logic_engine,
            "current_context_id": self.context.id
        }
        node._run(shared_store)
        calls = self.logic_engine.update_proposition_confidence.call_args_list
        # Should behave like the legacy single-agent node
        args1, _ = calls[0]
        self.assertAlmostEqual(args1[1], 0.7, places=5)

    def test_aggregation(self):
        self.node = MultiExpertiseAggregationNode()
        self.expertise = Expertise(
            domains=[
                ExpertiseDomain(name="Physics", proficiency=0.9),
                ExpertiseDomain(name="Biology", proficiency=0.3),
            ],
            skills=[], knowledge_bases=[], metadata={}
        )
        self.context = LogicalContext(id="ctx1", name="ctx", description="desc")
        self.prop = Proposition(
            id="p1",
            type=PropositionType.STATEMENT,
            text="Test prop",
            status=PropositionStatus.UNVERIFIED,
            confidence=None,
            source=None,
            metadata={},
            entity_references=[],
            entity_relations=[],
            domain_relevance={"Physics": 0.8, "Biology": 0.4}
        )
        self.context.propositions[self.prop.id] = self.prop
        self.logic_engine = MagicMock()
        self.logic_engine.get_context.return_value = self.context
        self.logic_engine.update_proposition_confidence = MagicMock()
        self.shared_store = {
            "expertise": self.expertise,
            "logic_engine": self.logic_engine,
            "current_context_id": self.context.id
        }
        self.node._run(self.shared_store)
        # (0.8*0.9 + 0.4*0.3) / (0.9+0.3) = (0.72+0.12)/1.2 = 0.7
        args, _ = self.logic_engine.update_proposition_confidence.call_args
        self.assertEqual(args[0], self.prop.id)
        self.assertAlmostEqual(args[1], 0.7, places=6)
        self.assertAlmostEqual(self.prop.confidence, 0.7, places=6)

if __name__ == "__main__":
    unittest.main()
