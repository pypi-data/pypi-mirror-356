#!/usr/bin/env python3
"""
Script simple pour tester le ModelRouterNode avec un modèle forcé.
"""

import os
import sys
import logging
from num_agents.core import SharedStore
from num_agents.reasoning.nodes.model_router_node import (
    ModelRouterNode,
    InputType,
    OutputType,
    TaskType,
    OptimizationPriority
)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Fonction principale pour tester le ModelRouterNode."""
    # Paramètres
    forced_model = "gemini-2.0-flash"
    providers = ["openai", "gemini"]
    api_keys = {
        "openai": os.environ.get("OPENAI_API_KEY"),
        "gemini": os.environ.get("GOOGLE_API_KEY")
    }
    
    # Afficher les informations
    print("\n" + "="*50)
    print("TEST DU ROUTEUR DE MODÈLE LLM")
    print("="*50)
    print(f"Modèle forcé: {forced_model}")
    print(f"Fournisseurs disponibles: {', '.join(providers)}")
    print("="*50 + "\n")
    
    # Créer le nœud ModelRouterNode
    router_node = ModelRouterNode(
        name="model_router",
        providers=providers,
        optimization_priority=OptimizationPriority.BALANCED,
        api_keys=api_keys,
        forced_model=forced_model
    )
    
    # Créer un store partagé avec les données nécessaires
    shared = SharedStore()
    shared.set("input_data", {"text": "Explique-moi comment fonctionne un modèle de langage en 3 points simples."})
    shared.set("task_type", TaskType.GENERAL)
    shared.set("output_type", OutputType.TEXT)
    shared.set("input_types", [InputType.TEXT])
    
    # Exécuter le nœud
    try:
        result = router_node.exec(shared)
        print("\nRésultat de l'exécution du ModelRouterNode:")
        print(f"Status: {result.get('status')}")
        print(f"Provider sélectionné: {result.get('provider')}")
        print(f"Modèle sélectionné: {result.get('model')}")
        
        print("\nValeurs dans le store partagé:")
        print(f"selected_llm_provider: {shared.get('selected_llm_provider')}")
        print(f"selected_llm_model: {shared.get('selected_llm_model')}")
        print(f"llm_api_key: {'[MASQUÉ]' if shared.get('llm_api_key') else 'Non défini'}")
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du ModelRouterNode: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
