#!/usr/bin/env python3
"""
Test simple pour vérifier le forçage de modèle dans ModelRouterNode
"""

import os
import logging
import sys

# Ajouter le répertoire parent au chemin Python pour pouvoir importer les modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from num_agents.core import SharedStore
    from num_agents.reasoning.nodes.model_router_node import (
        ModelRouterNode,
        InputType,
        OutputType,
        TaskType,
        OptimizationPriority
    )
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    sys.exit(1)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def main():
    # Modèle à forcer (utilisons gemini-2.0-flash comme demandé)
    forced_model = "gemini-2.0-flash"
    
    # Récupérer les clés API depuis les variables d'environnement
    api_keys = {
        "openai": os.environ.get("OPENAI_API_KEY"),
        "gemini": os.environ.get("GOOGLE_API_KEY")
    }
    
    print("\n" + "="*50)
    print(f"TEST DU ROUTEUR DE MODÈLE LLM AVEC {forced_model} FORCÉ")
    print("="*50)
    
    # Créer un store partagé avec les données nécessaires
    shared = SharedStore()
    shared.set("input_data", {"text": "Exemple de texte d'entrée"})
    shared.set("task_type", TaskType.GENERAL)
    shared.set("output_type", OutputType.TEXT)
    shared.set("input_types", [InputType.TEXT])
    
    # Créer le nœud ModelRouterNode avec le modèle forcé
    router_node = ModelRouterNode(
        name="model_router_test",
        providers=["openai", "gemini"],
        optimization_priority=OptimizationPriority.BALANCED,
        api_keys=api_keys,
        forced_model=forced_model
    )
    
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
        
        if result.get('model') == forced_model:
            print("\n✅ TEST RÉUSSI: Le modèle forcé a été correctement sélectionné!")
        else:
            print(f"\n❌ TEST ÉCHOUÉ: Le modèle sélectionné ({result.get('model')}) ne correspond pas au modèle forcé ({forced_model})!")
    
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
