"""
Dynamic Expertise Flow Demo

This example demonstrates how to use the DynamicExpertiseFlow node to orchestrate
multi-expertise reasoning with automatic context detection and aggregation strategy selection.

The flow:
1. Sets up a reasoning context with propositions
2. Creates multiple expertises with different domain knowledge
3. Runs the DynamicExpertiseFlow to:
   - Auto-detect multi-agent context
   - Apply expertise weighting
   - Select optimal aggregation strategy
   - Aggregate scores
   - Make decisions based on confidence thresholds
4. Analyzes the results, showing per-agent confidence scores
"""

import logging
import sys
import os
import argparse
from typing import Dict, List, Optional

from num_agents.reasoning.logic_engine import LogicEngine
from num_agents.reasoning.models import (
    Context, 
    Proposition, 
    PropositionStatus, 
    PropositionType
)
from num_agents.reasoning.semantic_models import (
    Expertise,
    Domain,
    Entity,
    EntityType,
    Relation
)
from num_agents.reasoning.nodes.dynamic_expertise_flow import DynamicExpertiseFlow
from num_agents.reasoning.rules import Conjunction, ModusPonens
from num_agents.reasoning.llm.llm_provider import LLMProviderFactory

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def create_sample_context() -> Context:
    """Create a sample reasoning context with propositions."""
    context = Context(
        id="medical_diagnosis",
        name="Medical Diagnosis Case",
        description="A reasoning context for medical diagnosis demonstration"    
    )
    
    # Add propositions about a medical case
    props = {
        "p1": Proposition(
            id="p1",
            text="Patient has fever",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.9
        ),
        "p2": Proposition(
            id="p2",
            text="Patient has cough",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.8
        ),
        "p3": Proposition(
            id="p3",
            text="Patient has fatigue",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.7
        ),
        "p4": Proposition(
            id="p4",
            text="If a patient has fever and cough, they might have a respiratory infection",
            type=PropositionType.HYPOTHESIS,
            status=PropositionStatus.UNVERIFIED,
            confidence=None  # Will be determined by expertise
        ),
        "p5": Proposition(
            id="p5",
            text="Patient has a respiratory infection",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.UNVERIFIED,
            confidence=None  # Will be determined by expertise and inference
        ),
        "p6": Proposition(
            id="p6",
            text="If a patient has fever and fatigue, they might have an influenza infection",
            type=PropositionType.HYPOTHESIS,
            status=PropositionStatus.UNVERIFIED,
            confidence=None  # Will be determined by expertise
        ),
        "p7": Proposition(
            id="p7",
            text="Patient has an influenza infection",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.UNVERIFIED,
            confidence=None  # Will be determined by expertise and inference
        )
    }
    
    for prop_id, prop in props.items():
        context.add_proposition(prop)
    
    return context

def create_expertises() -> List[Expertise]:
    """Create multiple expertises with different domain knowledge."""
    
    # Create domains
    general_medicine = Domain(name="general_medicine", description="General medical knowledge")
    respiratory = Domain(name="respiratory", description="Specialized knowledge of respiratory diseases")
    infectious_disease = Domain(name="infectious_disease", description="Specialized knowledge of infectious diseases")
    
    # Create entities - using CONCEPT for symptoms and EVENT for diseases
    fever = Entity(name="fever", type=EntityType.CONCEPT)
    cough = Entity(name="cough", type=EntityType.CONCEPT)
    fatigue = Entity(name="fatigue", type=EntityType.CONCEPT)
    respiratory_infection = Entity(name="respiratory_infection", type=EntityType.EVENT)
    influenza = Entity(name="influenza", type=EntityType.EVENT)
    
    # Create relations for each domain
    general_med_relations = [
        Relation(source=fever, target=respiratory_infection, weight=0.6),
        Relation(source=cough, target=respiratory_infection, weight=0.7),
        Relation(source=fever, target=influenza, weight=0.6),
        Relation(source=fatigue, target=influenza, weight=0.5)
    ]
    
    respiratory_relations = [
        Relation(source=fever, target=respiratory_infection, weight=0.7),
        Relation(source=cough, target=respiratory_infection, weight=0.9),
        Relation(source=fever, target=influenza, weight=0.5),
        Relation(source=fatigue, target=influenza, weight=0.3)
    ]
    
    infectious_relations = [
        Relation(source=fever, target=respiratory_infection, weight=0.5),
        Relation(source=cough, target=respiratory_infection, weight=0.4),
        Relation(source=fever, target=influenza, weight=0.8),
        Relation(source=fatigue, target=influenza, weight=0.7)
    ]
    
    # Create expertises
    general_practitioner = Expertise(
        name="general_practitioner",
        domains=[general_medicine],
        relations=general_med_relations,
        confidence=0.7
    )
    
    pulmonologist = Expertise(
        name="pulmonologist",
        domains=[general_medicine, respiratory],
        relations=respiratory_relations,
        confidence=0.9
    )
    
    infectious_disease_specialist = Expertise(
        name="infectious_disease_specialist",
        domains=[general_medicine, infectious_disease],
        relations=infectious_relations,
        confidence=0.85
    )
    
    return [general_practitioner, pulmonologist, infectious_disease_specialist]

def setup_rules(logic_engine: LogicEngine, context_id: str) -> None:
    """Set up logical rules for inference."""
    
    # Les règles sont déjà enregistrées dans le LogicEngine lors de son initialisation
    # Nous n'avons pas besoin d'ajouter des règles personnalisées pour ce démo
    # Les règles standard comme modus_ponens, conjunction, etc. sont déjà disponibles
    
    # Afficher les règles disponibles
    print("Règles logiques disponibles:")
    for rule_name in logic_engine.rules:
        print(f"  - {rule_name}")
    
    # Note: Dans une implémentation plus avancée, nous pourrions ajouter des règles personnalisées
    # en créant des sous-classes de LogicalRule et en les enregistrant avec logic_engine.register_rule()
    
    # Dans une implémentation réelle, nous pourrions exécuter des opérations supplémentaires
    # comme l'ajout de propositions spécifiques au contexte ou la configuration de paramètres
    # pour les règles existantes

def print_results(shared_store: Dict) -> None:
    """Print the results of the reasoning process."""
    print("\n" + "="*50)
    print("DYNAMIC EXPERTISE FLOW RESULTS")
    print("="*50)
    
    # Get key results
    is_multi_agent = shared_store.get("is_multi_agent", False)
    selected_strategy = shared_store.get("selected_strategy")
    proposition_decisions = shared_store.get("proposition_decisions", {})
    proposition_scores_by_agent = shared_store.get("proposition_scores_by_agent", {})
    logic_engine = shared_store.get("logic_engine")
    context_id = shared_store.get("current_context_id")
    
    if not logic_engine or not context_id:
        print("Missing logic engine or context ID")
        return
        
    context = logic_engine.get_context(context_id)
    if not context:
        print("Context not found")
        return
        
    # Print context info
    print(f"\nContext: {context.id}")
    print(f"Multi-agent mode: {'Yes' if is_multi_agent else 'No'}")
    if selected_strategy:
        print(f"Selected aggregation strategy: {selected_strategy}")
        
    # Print proposition details
    print("\nPROPOSITION DETAILS:")
    print("-"*50)
    print(f"{'ID':<5} {'Content':<50} {'Status':<12} {'Confidence':<10} {'Decision':<8}")
    print("-"*50)
    
    for prop_id, prop in context.propositions.items():
        decision = "✓" if proposition_decisions.get(prop_id) else "✗" if prop_id in proposition_decisions else "-"
        confidence = f"{prop.confidence:.2f}" if prop.confidence is not None else "None"
        print(f"{prop_id:<5} {prop.text[:47]+'...' if len(prop.text) > 50 else prop.text:<50} {prop.status.name:<12} {confidence:<10} {decision:<8}")
        
    # Print per-agent scores
    if proposition_scores_by_agent:
        print("\nPER-AGENT CONFIDENCE SCORES:")
        print("-"*50)
        
        # Get agent names
        expertises = shared_store.get("expertises", [])
        agent_names = [exp.name for exp in expertises] if expertises else ["Agent"]
        
        # Print header
        header = "ID    "
        for name in agent_names:
            header += f"{name[:10]:<12}"
        header += "Aggregated"
        print(header)
        print("-"*50)
        
        # Print scores by proposition
        for prop_id, scores in proposition_scores_by_agent.items():
            prop = context.propositions.get(prop_id)
            if not prop:
                continue
                
            row = f"{prop_id:<5}"
            for score in scores:
                if score is not None:
                    formatted_score = f"{score:.2f}"
                    row += f"{formatted_score:<10}"
                else:
                    row += f"{'None':<10}"
            
            # Add aggregated score
            row += f"{prop.confidence:.2f}" if prop.confidence is not None else "None"
            print(row)

def main():
    """Run the dynamic expertise flow demo."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Dynamic Expertise Flow Demo")
    parser.add_argument("--provider", type=str, default="gemini", choices=["openai", "gemini"],
                        help="LLM provider to use (gemini or openai)")
    parser.add_argument("--api-key", type=str, default=None,
                        help="API key for the LLM provider (if not provided, will use environment variables)")
    parser.add_argument("--model", type=str, default=None,
                        help="Model name to use (if not provided, will use default model for the provider)")
    args = parser.parse_args()
    
    # Set up API key from environment if not provided
    api_key = args.api_key
    if not api_key:
        if args.provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                print("Error: No OpenAI API key provided. Set OPENAI_API_KEY environment variable or use --api-key.")
                return
        elif args.provider == "gemini":
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                print("Error: No Google API key provided. Set GOOGLE_API_KEY environment variable or use --api-key.")
                return
    
    print(f"Using {args.provider.upper()} as LLM provider")
    if args.model:
        print(f"Using model: {args.model}")
    
    # Create logic engine and context
    logic_engine = LogicEngine()
    context = create_sample_context()
    # Ajouter manuellement le contexte au moteur logique
    logic_engine.contexts[context.id] = context
    
    # Set up rules
    setup_rules(logic_engine, context.id)
    
    # Create expertises
    expertises = create_expertises()
    
    # Create flow with specified LLM provider
    flow = DynamicExpertiseFlow(
        name="MedicalDiagnosisFlow",
        confidence_threshold=0.7,
        auto_select_strategy=True,
        llm_provider=args.provider,
        llm_model=args.model,
        llm_api_key=api_key
    )
    
    # Set up shared store
    shared_store = {
        "logic_engine": logic_engine,
        "current_context_id": context.id,
        "expertises": expertises
    }
    
    # Create and run dynamic expertise flow
    
    # Run the flow
    updated_store = flow._run(shared_store)
    
    # Print results
    print_results(updated_store)
    
    # Return final decisions
    return updated_store.get("proposition_decisions", {})

if __name__ == "__main__":
    main()
