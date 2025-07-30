#!/usr/bin/env python3
"""
Démonstration du ModelRouterNode qui sélectionne automatiquement le modèle LLM optimal
en fonction des types d'entrée, du type de tâche et des priorités d'optimisation.
"""

import os
import argparse
import logging
from typing import Dict, Any, List

# Essayer d'importer dotenv de deux façons possibles
try:
    from python_dotenv import load_dotenv
except ImportError:
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("AVERTISSEMENT: Module dotenv non trouvé. Les variables d'environnement ne seront pas chargées depuis .env")
        
        def load_dotenv():
            print("Chargement des variables d'environnement ignoré.")
            pass

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

from num_agents.core import Flow, Node
from num_agents.reasoning.nodes.model_router_node import (
    ModelRouterNode,
    InputType,
    OutputType,
    TaskType,
    OptimizationPriority
)
from num_agents.reasoning.llm.llm_provider import LLMProviderFactory


class InputNode(Node):
    """Nœud d'entrée pour préparer les données."""
    
    def __init__(self, name: str, input_data: Dict[str, Any]):
        super().__init__(name=name)
        self.input_data = input_data
        self.logger = logging.getLogger(__name__)
        
    def exec(self, shared):
        """Exécuter le nœud d'entrée.
        
        Args:
            shared: Le store partagé pour accéder et stocker des données
            
        Returns:
            Un dictionnaire contenant les résultats de l'exécution du nœud
        """
        self.logger.info(f"Exécution du nœud {self.name}")
        
        # Stocker les données d'entrée dans le store partagé
        for key, value in self.input_data.items():
            shared.set(key, value)
            
        return {"status": "success", "message": "Données d'entrée préparées"}
        
    def _run(self, shared_store: Dict) -> Dict:
        """Ajoute les données d'entrée au shared_store."""
        shared_store["input_data"] = self.input_data
        shared_store["task_type"] = self.task_type
        shared_store["expected_output_type"] = self.output_type
        return shared_store


class LLMProcessingNode(Node):
    """Nœud qui utilise le modèle LLM sélectionné par le ModelRouterNode."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.logger = logging.getLogger(__name__)
    
    def exec(self, shared):
        """Exécuter le nœud de traitement LLM.
        
        Args:
            shared: Le store partagé pour accéder et stocker des données
            
        Returns:
            Un dictionnaire contenant les résultats de l'exécution du nœud
        """
        self.logger.info(f"Exécution du nœud {self.name}")
        
        provider_name = shared.get("selected_llm_provider")
        model_name = shared.get("selected_llm_model")
        api_key = shared.get("llm_api_key")
        
        if not provider_name or not model_name:
            raise ValueError("Aucun modèle LLM n'a été sélectionné")
        
        self.logger.info(f"Utilisation du modèle {provider_name}/{model_name} pour le traitement")
        
        # Créer le fournisseur LLM avec le modèle sélectionné
        factory = LLMProviderFactory()
        provider = factory.create_provider(
            provider_name=provider_name,
            model=model_name,
            api_key=api_key
        )
        
        # Préparer le prompt en fonction des données d'entrée
        input_data = shared.get("input_data", {})
        prompt = input_data.get("text", "")
        
        if not prompt:
            prompt = "Veuillez fournir une réponse."
        
        # Appeler le modèle LLM
        try:
            response = provider.generate(prompt)
            shared.set("llm_response", response)
            self.logger.info(f"Réponse obtenue du modèle {model_name}")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'appel au modèle LLM: {e}")
            shared.set("llm_error", str(e))
        
        return {"status": "success", "message": "Traitement LLM terminé"}
        
    def _run(self, shared_store: Dict) -> Dict:
        """Utilise le modèle LLM sélectionné pour traiter les données."""
        provider_name = shared_store.get("selected_llm_provider")
        model_name = shared_store.get("selected_llm_model")
        api_key = shared_store.get("llm_api_key")
        
        if not provider_name or not model_name:
            raise ValueError("Aucun modèle LLM n'a été sélectionné")
        
        self.logger.info(f"Utilisation du modèle {provider_name}/{model_name} pour le traitement")
        
        # Créer le fournisseur LLM avec le modèle sélectionné
        factory = LLMProviderFactory()
        provider = factory.create_provider(
            provider_name=provider_name,
            model=model_name,
            api_key=api_key
        )
        
        # Préparer le prompt en fonction des données d'entrée
        input_data = shared_store.get("input_data", {})
        prompt = input_data.get("text", "")
        
        if not prompt:
            prompt = "Veuillez fournir une réponse."
        
        # Appeler le modèle LLM
        try:
            response = provider.generate(prompt)
            shared_store["llm_response"] = response
            self.logger.info(f"Réponse obtenue du modèle {model_name}")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'appel au modèle LLM: {e}")
            shared_store["llm_error"] = str(e)
        
        return shared_store


class ResultNode(Node):
    """Nœud final pour afficher les résultats."""
    
    def __init__(self, name: str):
        super().__init__(name)
        
    def exec(self, shared):
        """Exécuter le nœud de résultat.
        
        Args:
            shared: Le store partagé pour accéder et stocker des données
            
        Returns:
            Un dictionnaire contenant les résultats de l'exécution du nœud
        """
        print("\n" + "="*50)
        print("RÉSULTATS DU FLOW DE ROUTAGE DE MODÈLE")
        print("="*50)
        
        print(f"\nFournisseur LLM sélectionné: {shared.get('selected_llm_provider', 'Non sélectionné')}")
        print(f"Modèle LLM sélectionné: {shared.get('selected_llm_model', 'Non sélectionné')}")
        
        if shared.has("llm_response"):
            print("\nRéponse du modèle LLM:")
            print("-"*50)
            print(shared.get("llm_response"))
            print("-"*50)
        elif shared.has("llm_error"):
            print("\nErreur lors de l'appel au modèle LLM:")
            print(shared.get("llm_error"))
        
        return {"status": "success", "message": "Affichage des résultats terminé"}
        
    def _run(self, shared_store: Dict) -> Dict:
        """Affiche les résultats du flow."""
        print("\n" + "="*50)
        print("RÉSULTATS DU FLOW DE ROUTAGE DE MODÈLE")
        print("="*50)
        
        print(f"\nFournisseur LLM sélectionné: {shared_store.get('selected_llm_provider', 'Non sélectionné')}")
        print(f"Modèle LLM sélectionné: {shared_store.get('selected_llm_model', 'Non sélectionné')}")
        
        if "llm_response" in shared_store:
            print("\nRéponse du modèle LLM:")
            print("-"*50)
            print(shared_store["llm_response"])
            print("-"*50)
        elif "llm_error" in shared_store:
            print("\nErreur lors de l'appel au modèle LLM:")
            print(shared_store["llm_error"])
        
        return shared_store


def create_flow(
    input_data: Dict[str, Any],
    task_type: TaskType,
    output_type: OutputType,
    providers: List[str],
    optimization_priority: OptimizationPriority,
    api_keys: Dict[str, str],
    forced_model: str = None
) -> Flow:
    """
    Crée un flow de démonstration avec le ModelRouterNode.
    
    Args:
        input_data: Données d'entrée pour le flow
        task_type: Type de tâche à effectuer
        output_type: Type de sortie attendu
        providers: Liste des fournisseurs LLM disponibles
        optimization_priority: Priorité d'optimisation pour la sélection du modèle
        api_keys: Clés API pour les fournisseurs LLM
        forced_model: Si spécifié, force l'utilisation de ce modèle LLM spécifique
        
    Returns:
        Un objet Flow configuré
    """
    # Créer les nœuds
    # Préparer les données d'entrée avec les informations nécessaires
    complete_input_data = {
        "text": input_data.get("text", ""),
        "task_type": task_type,
        "output_type": output_type
    }
    
    input_node = InputNode(
        name="input",
        input_data=complete_input_data
    )
    
    router_node = ModelRouterNode(
        name="model_router",
        providers=providers,
        optimization_priority=optimization_priority,
        api_keys=api_keys,
        forced_model=forced_model
    )
    
    processing_node = LLMProcessingNode(name="llm_processing")
    result_node = ResultNode(name="result")
    
    # Créer le flow
    flow = Flow()
    
    # Ajouter les nœuds au flow
    flow.add_node(input_node)
    flow.add_node(router_node)
    flow.add_node(processing_node)
    flow.add_node(result_node)
    
    # Définir les connexions entre les nœuds
    flow.add_transition(input_node, router_node)
    flow.add_transition(router_node, processing_node)
    flow.add_transition(processing_node, result_node)
    
    return flow


def main():
    """Fonction principale pour exécuter la démonstration."""
    # Configurer le logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Analyser les arguments de ligne de commande
    parser = argparse.ArgumentParser(description="Démonstration du ModelRouterNode")
    
    parser.add_argument(
        "--providers",
        type=str,
        default="openai,gemini",
        help="Liste des fournisseurs LLM séparés par des virgules (openai, gemini)"
    )
    
    parser.add_argument(
        "--optimization",
        type=str,
        choices=["cost", "speed", "quality", "balanced"],
        default="balanced",
        help="Priorité d'optimisation pour la sélection du modèle"
    )
    
    parser.add_argument(
        "--task",
        type=str,
        choices=["general", "reasoning", "coding", "summarization", "conversation", "multimodal"],
        default="general",
        help="Type de tâche à effectuer"
    )
    
    parser.add_argument(
        "--input-type",
        type=str,
        choices=["text", "image", "audio", "video", "pdf"],
        default="text",
        help="Type d'entrée principal"
    )
    
    parser.add_argument(
        "--output-type",
        type=str,
        choices=["text", "embeddings", "image", "audio", "video"],
        default="text",
        help="Type de sortie attendu"
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        default="Explique-moi comment fonctionne un modèle de langage de manière simple.",
        help="Texte de prompt à envoyer au modèle"
    )
    
    parser.add_argument(
        "--openai-api-key",
        type=str,
        default=None,
        help="Clé API OpenAI (par défaut: utilise la variable d'environnement OPENAI_API_KEY)"
    )
    
    parser.add_argument(
        "--google-api-key",
        type=str,
        default=None,
        help="Clé API Google (par défaut: utilise la variable d'environnement GOOGLE_API_KEY)"
    )
    
    parser.add_argument(
        "--forced-model",
        type=str,
        default=None,
        help="Force l'utilisation d'un modèle spécifique (ex: gemini-2.0-flash)"
    )
    
    args = parser.parse_args()
    
    # Préparer les données d'entrée
    input_data = {"text": args.prompt}
    
    # Convertir les types d'entrée/sortie et la tâche en énumérations
    task_type = TaskType(args.task)
    output_type = OutputType(args.output_type)
    input_types = [InputType(args.input_type)]
    
    # Préparer la liste des fournisseurs
    providers = [p.strip() for p in args.providers.split(",")]
    
    # Convertir la priorité d'optimisation en énumération
    optimization_map = {
        "cost": OptimizationPriority.COST,
        "speed": OptimizationPriority.SPEED,
        "quality": OptimizationPriority.QUALITY,
        "balanced": OptimizationPriority.BALANCED
    }
    optimization_priority = optimization_map[args.optimization]
    
    # Préparer les clés API
    api_keys = {}
    
    # OpenAI API Key
    openai_api_key = args.openai_api_key or os.environ.get("OPENAI_API_KEY")
    if "openai" in providers and not openai_api_key:
        print("Avertissement: Aucune clé API OpenAI fournie. Utilisez --openai-api-key ou définissez OPENAI_API_KEY.")
    elif "openai" in providers:
        api_keys["openai"] = openai_api_key
    
    # Google API Key
    google_api_key = args.google_api_key or os.environ.get("GOOGLE_API_KEY")
    if "gemini" in providers and not google_api_key:
        print("Avertissement: Aucune clé API Google fournie. Utilisez --google-api-key ou définissez GOOGLE_API_KEY.")
    elif "gemini" in providers:
        api_keys["gemini"] = google_api_key
    
    # Afficher les paramètres de la démonstration
    print("\n" + "="*50)
    print("DÉMONSTRATION DU ROUTEUR DE MODÈLE LLM")
    print("="*50)
    print(f"Fournisseurs disponibles: {', '.join(providers)}")
    if args.forced_model:
        print(f"Modèle forcé: {args.forced_model}")
    else:
        print(f"Priorité d'optimisation: {args.optimization}")
    print(f"Type de tâche: {args.task}")
    print(f"Type d'entrée: {args.input_type}")
    print(f"Type de sortie: {args.output_type}")
    print(f"Prompt: \"{args.prompt}\"")
    print("="*50 + "\n")
    
    # Créer et exécuter le flow
    flow = create_flow(
        input_data=input_data,
        task_type=task_type,
        output_type=output_type,
        providers=providers,
        optimization_priority=optimization_priority,
        api_keys=api_keys,
        forced_model=args.forced_model
    )
    
    # Exécuter le flow
    flow.execute()


if __name__ == "__main__":
    main()
