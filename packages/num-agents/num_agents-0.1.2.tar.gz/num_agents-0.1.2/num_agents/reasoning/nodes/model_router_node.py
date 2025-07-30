"""
Model Router Node

Ce module définit un nœud spécialisé pour la sélection intelligente de modèles LLM
en fonction du contexte, des types d'entrée/sortie et des contraintes spécifiées.
"""

import logging
import os
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Union, Tuple

from num_agents.core import Node
from num_agents.reasoning.llm.llm_provider import LLMProviderFactory

class OptimizationPriority(str, Enum):
    """Priorités d'optimisation pour la sélection de modèle."""
    COST = "cost"
    QUALITY = "quality"
    SPEED = "speed"
    BALANCED = "balanced"

class TaskType(str, Enum):
    """Types de tâches pour lesquelles un modèle peut être optimisé."""
    GENERAL = "general"
    REASONING = "reasoning"
    CODING = "coding"
    SUMMARIZATION = "summarization"
    CLASSIFICATION = "classification"
    GENERATION = "generation"
    TRANSLATION = "translation"
    CONVERSATION = "conversation"
    MULTIMODAL = "multimodal"

class InputType(str, Enum):
    """Types d'entrée supportés par les modèles."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    PDF = "pdf"

class OutputType(str, Enum):
    """Types de sortie supportés par les modèles."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    EMBEDDINGS = "embeddings"
    VIDEO = "video"

class ModelRouterNode(Node):
    """
    Un nœud qui sélectionne automatiquement le modèle LLM optimal en fonction du contexte.
    
    Ce nœud agit comme un routeur contextuel qui sélectionne le modèle LLM le plus approprié
    en fonction des types d'entrée, du type de sortie attendue, des caractéristiques de la tâche
    et des contraintes spécifiées (coût, latence, qualité).
    """
    
    def __init__(
        self,
        name: str,
        providers: List[str] = ["openai", "gemini"],
        optimization_priority: Union[str, OptimizationPriority] = OptimizationPriority.BALANCED,
        available_models: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = None,
        api_keys: Optional[Dict[str, str]] = None,
        forced_model: Optional[str] = None,
    ):
        """
        Initialise le nœud de routage de modèles.
        
        Args:
            name: Nom du nœud
            providers: Liste des fournisseurs LLM disponibles
            available_models: Dictionnaire des modèles disponibles avec leurs caractéristiques
            api_keys: Dictionnaire des clés API pour chaque fournisseur
            forced_model: Nom du modèle à utiliser de manière forcée
        """
        super().__init__(name)
        self.providers = providers
        
        if isinstance(optimization_priority, str):
            self.optimization_priority = OptimizationPriority(optimization_priority)
        else:
            self.optimization_priority = optimization_priority
            
        self.model_registry = self._build_model_registry(available_models)
        self.api_keys = api_keys or {}
        self.forced_model = forced_model
        self.logger = logging.getLogger(__name__)
        
    def _build_model_registry(self, available_models: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = None) -> Dict:
        """
        Construit un registre de modèles avec leurs capacités et caractéristiques.
        
        Args:
            available_models: Dictionnaire optionnel de modèles à ajouter ou remplacer
            
        Returns:
            Un dictionnaire contenant le registre complet des modèles
        """
        registry = {
            "gemini": {
                "gemini-2.5-pro": {
                    "input_types": [InputType.TEXT, InputType.IMAGE, InputType.AUDIO, InputType.VIDEO, InputType.PDF],
                    "output_types": [OutputType.TEXT],
                    "strengths": [TaskType.REASONING, TaskType.MULTIMODAL, TaskType.CODING],
                    "cost": "medium",
                    "speed": "medium",
                    "quality": "high"
                },
                "gemini-2.0-flash": {
                    "input_types": [InputType.TEXT],
                    "output_types": [OutputType.TEXT],
                    "strengths": [TaskType.GENERAL],
                    "cost": "low",
                    "speed": "medium",
                    "quality": "medium"
                },
                "gemini-2.5-flash": {
                    "input_types": [InputType.TEXT, InputType.IMAGE, InputType.AUDIO, InputType.VIDEO],
                    "output_types": [OutputType.TEXT],
                    "strengths": [TaskType.GENERAL, TaskType.CONVERSATION],
                    "cost": "low",
                    "speed": "high",
                    "quality": "medium"
                },
                "gemini-2.5-flash-lite-preview": {
                    "input_types": [InputType.TEXT, InputType.IMAGE, InputType.AUDIO, InputType.VIDEO],
                    "output_types": [OutputType.TEXT],
                    "strengths": [TaskType.GENERAL],
                    "cost": "very_low",
                    "speed": "very_high",
                    "quality": "medium_low"
                },
                "gemini-1.5-pro": {
                    "input_types": [InputType.TEXT, InputType.IMAGE, InputType.AUDIO, InputType.VIDEO],
                    "output_types": [OutputType.TEXT],
                    "strengths": [TaskType.REASONING, TaskType.MULTIMODAL],
                    "cost": "medium",
                    "speed": "medium",
                    "quality": "high"
                },
                "gemini-1.5-flash": {
                    "input_types": [InputType.TEXT, InputType.IMAGE, InputType.AUDIO, InputType.VIDEO],
                    "output_types": [OutputType.TEXT],
                    "strengths": [TaskType.GENERAL],
                    "cost": "low",
                    "speed": "high",
                    "quality": "medium"
                },
                "gemini-embedding": {
                    "input_types": [InputType.TEXT],
                    "output_types": [OutputType.EMBEDDINGS],
                    "strengths": [],
                    "cost": "very_low",
                    "speed": "very_high",
                    "quality": "high"
                },
                "imagen-3.0-generate": {
                    "input_types": [InputType.TEXT],
                    "output_types": [OutputType.IMAGE],
                    "strengths": [TaskType.GENERATION],
                    "cost": "high",
                    "speed": "medium",
                    "quality": "high"
                },
                "veo-2.0-generate": {
                    "input_types": [InputType.TEXT, InputType.IMAGE],
                    "output_types": [OutputType.VIDEO],
                    "strengths": [TaskType.GENERATION],
                    "cost": "very_high",
                    "speed": "slow",
                    "quality": "high"
                },
            },
            "openai": {
                "gpt-4o": {
                    "input_types": [InputType.TEXT, InputType.IMAGE],
                    "output_types": [OutputType.TEXT],
                    "strengths": [TaskType.REASONING, TaskType.CODING, TaskType.CONVERSATION],
                    "cost": "high",
                    "speed": "medium",
                    "quality": "high"
                },
                "gpt-4o-mini": {
                    "input_types": [InputType.TEXT, InputType.IMAGE],
                    "output_types": [OutputType.TEXT],
                    "strengths": [TaskType.GENERAL, TaskType.CONVERSATION],
                    "cost": "medium",
                    "speed": "high",
                    "quality": "medium"
                },
                "gpt-3.5-turbo": {
                    "input_types": [InputType.TEXT],
                    "output_types": [OutputType.TEXT],
                    "strengths": [TaskType.GENERAL],
                    "cost": "very_low",
                    "speed": "very_high",
                    "quality": "medium"
                },
                "text-embedding-3-large": {
                    "input_types": [InputType.TEXT],
                    "output_types": [OutputType.EMBEDDINGS],
                    "strengths": [],
                    "cost": "very_low",
                    "speed": "very_high",
                    "quality": "high"
                },
                "text-embedding-3-small": {
                    "input_types": [InputType.TEXT],
                    "output_types": [OutputType.EMBEDDINGS],
                    "strengths": [],
                    "cost": "very_low",
                    "speed": "very_high",
                    "quality": "medium"
                },
                "dall-e-3": {
                    "input_types": [InputType.TEXT],
                    "output_types": [OutputType.IMAGE],
                    "strengths": [TaskType.GENERATION],
                    "cost": "high",
                    "speed": "medium",
                    "quality": "high"
                },
                "tts-1": {
                    "input_types": [InputType.TEXT],
                    "output_types": [OutputType.AUDIO],
                    "strengths": [TaskType.GENERATION],
                    "cost": "low",
                    "speed": "high",
                    "quality": "medium"
                },
                "tts-1-hd": {
                    "input_types": [InputType.TEXT],
                    "output_types": [OutputType.AUDIO],
                    "strengths": [TaskType.GENERATION],
                    "cost": "medium",
                    "speed": "medium",
                    "quality": "high"
                },
            }
        }
        
        # Ajouter ou remplacer par les modèles fournis
        if available_models:
            for provider, models in available_models.items():
                if provider not in registry:
                    registry[provider] = {}
                for model_name, specs in models.items():
                    registry[provider][model_name] = specs
                    
        return registry
        
    def _detect_input_types(self, input_data: Dict) -> List[InputType]:
        """
        Détecte automatiquement les types d'entrée à partir des données.
        
        Args:
            input_data: Données d'entrée à analyser
            
        Returns:
            Liste des types d'entrée détectés
        """
        detected_types = []
        
        # Détection de texte
        if any(key in input_data for key in ["text", "prompt", "query", "content"]):
            detected_types.append(InputType.TEXT)
            
        # Détection d'image
        if any(key in input_data for key in ["image", "images", "image_url", "image_data"]):
            detected_types.append(InputType.IMAGE)
            
        # Détection d'audio
        if any(key in input_data for key in ["audio", "audio_url", "audio_data", "speech"]):
            detected_types.append(InputType.AUDIO)
            
        # Détection de vidéo
        if any(key in input_data for key in ["video", "video_url", "video_data"]):
            detected_types.append(InputType.VIDEO)
            
        # Détection de PDF
        if any(key in input_data for key in ["pdf", "pdf_url", "document"]):
            detected_types.append(InputType.PDF)
            
        # Si aucun type n'est détecté, on suppose que c'est du texte
        if not detected_types:
            detected_types.append(InputType.TEXT)
            
        return detected_types
    
    def _score_model_match(self, model_info: Dict[str, Any], input_types: List[InputType], output_type: OutputType, task_type: TaskType, constraints: Dict[str, str]) -> float:
        """
        Évalue à quel point un modèle correspond aux exigences spécifiées.
        
        Args:
            model_info: Informations sur le modèle
            input_types: Types d'entrée requis
            output_type: Type de sortie attendu
            task_type: Type de tâche à effectuer
            constraints: Contraintes supplémentaires
            
        Returns:
            Score de correspondance (plus élevé = meilleure correspondance)
        """
        score = 0.0
        
        # Vérifier la compatibilité des types d'entrée (critère éliminatoire)
        if not all(input_type in model_info["input_types"] for input_type in input_types):
            return 0.0
            
        # Vérifier la compatibilité du type de sortie (critère éliminatoire)
        if output_type not in model_info["output_types"]:
            return 0.0
            
        # Points pour les forces correspondant au type de tâche
        if task_type in model_info.get("strengths", []):
            score += 30.0
        elif TaskType.GENERAL in model_info.get("strengths", []):
            score += 10.0
            
        # Évaluation basée sur la priorité d'optimisation
        cost_scores = {"very_low": 50, "low": 40, "medium": 30, "high": 20, "very_high": 10}
        speed_scores = {"very_high": 50, "high": 40, "medium": 30, "slow": 20, "very_slow": 10}
        quality_scores = {"high": 50, "medium_high": 40, "medium": 30, "medium_low": 20, "low": 10}
        
        if self.optimization_priority == OptimizationPriority.COST:
            score += cost_scores.get(model_info.get("cost", "medium"), 0) * 3
            score += speed_scores.get(model_info.get("speed", "medium"), 0) * 1
            score += quality_scores.get(model_info.get("quality", "medium"), 0) * 1
        elif self.optimization_priority == OptimizationPriority.SPEED:
            score += cost_scores.get(model_info.get("cost", "medium"), 0) * 1
            score += speed_scores.get(model_info.get("speed", "medium"), 0) * 3
            score += quality_scores.get(model_info.get("quality", "medium"), 0) * 1
        elif self.optimization_priority == OptimizationPriority.QUALITY:
            score += cost_scores.get(model_info.get("cost", "medium"), 0) * 1
            score += speed_scores.get(model_info.get("speed", "medium"), 0) * 1
            score += quality_scores.get(model_info.get("quality", "medium"), 0) * 3
        else:  # BALANCED
            score += cost_scores.get(model_info.get("cost", "medium"), 0) * 1.5
            score += speed_scores.get(model_info.get("speed", "medium"), 0) * 1.5
            score += quality_scores.get(model_info.get("quality", "medium"), 0) * 1.5
            
        # Appliquer les contraintes spécifiques
        if constraints:
            if "min_quality" in constraints:
                quality_level = model_info.get("quality", "medium")
                quality_levels = ["low", "medium_low", "medium", "medium_high", "high"]
                if quality_levels.index(quality_level) < quality_levels.index(constraints["min_quality"]):
                    return 0.0
                    
            if "max_cost" in constraints:
                cost_level = model_info.get("cost", "medium")
                cost_levels = ["very_low", "low", "medium", "high", "very_high"]
                if cost_levels.index(cost_level) > cost_levels.index(constraints["max_cost"]):
                    return 0.0
                    
            if "min_speed" in constraints:
                speed_level = model_info.get("speed", "medium")
                speed_levels = ["very_slow", "slow", "medium", "high", "very_high"]
                if speed_levels.index(speed_level) < speed_levels.index(constraints["min_speed"]):
                    return 0.0
                    
        return score
    
    def select_optimal_model(self, input_types: List[Union[str, InputType]], output_type: Union[str, OutputType] = OutputType.TEXT, task_type: Union[str, TaskType] = TaskType.GENERAL, constraints: Dict[str, str] = None) -> Tuple[str, str]:
        """
        Sélectionne le modèle optimal en fonction des types d'entrée/sortie et des contraintes.
        
        Args:
            input_types: Types d'entrée requis
            output_type: Type de sortie attendu
            task_type: Type de tâche à effectuer
            constraints: Contraintes supplémentaires
            
        Returns:
            Tuple[str, str]: (provider_name, model_name)
        """
        # Convertir les types d'entrée en énumérations si nécessaire
        input_types_enum = []
        for input_type in input_types:
            if isinstance(input_type, str):
                input_types_enum.append(InputType(input_type))
            else:
                input_types_enum.append(input_type)
                
        # Convertir le type de sortie en énumération si nécessaire
        if isinstance(output_type, str):
            output_type_enum = OutputType(output_type)
        else:
            output_type_enum = output_type
            
        # Convertir le type de tâche en énumération si nécessaire
        if isinstance(task_type, str):
            task_type_enum = TaskType(task_type)
        else:
            task_type_enum = task_type
            
        constraints = constraints or {}
        
        best_score = -1
        best_provider = None
        best_model = None
        
        # Évaluer chaque modèle disponible
        for provider_name, provider_models in self.model_registry.items():
            # Ignorer les fournisseurs non spécifiés
            if provider_name not in self.providers:
                continue
                
            for model_name, model_specs in provider_models.items():
                score = self._score_model_match(
                    model_specs=model_specs,
                    input_types=input_types_enum,
                    output_type=output_type_enum,
                    task_type=task_type_enum,
                    constraints=constraints
                )
                
                if score > best_score:
                    best_score = score
                    best_provider = provider_name
                    best_model = model_name
        
        if best_provider is None or best_model is None:
            # Aucun modèle ne correspond aux critères, utiliser un modèle par défaut
            if OutputType.TEXT == output_type_enum:
                if "openai" in self.providers:
                    return "openai", "gpt-3.5-turbo"
                elif "gemini" in self.providers:
                    return "gemini", "gemini-1.5-flash"
            elif OutputType.EMBEDDINGS == output_type_enum:
                if "openai" in self.providers:
                    return "openai", "text-embedding-3-small"
                elif "gemini" in self.providers:
                    return "gemini", "gemini-embedding"
            
            # Si toujours pas de correspondance, lever une exception
            raise ValueError(f"Aucun modèle ne correspond aux critères: {input_types}, {output_type}, {task_type}")
        
        return best_provider, best_model
    
    def exec(self, shared):
        """Exécute la logique de routage et choisit le modèle LLM.

        1. Utilise `self.forced_model` si fourni pour bypasser la sélection automatique.
        2. Sinon, appelle `select_optimal_model` pour déterminer le meilleur couple (provider, model).
        3. Stocke le résultat dans le `shared` store.
        """
        self.logger.info("[ModelRouter] exécution du nœud")

        # -----------------------------------------
        # Lecture du contexte
        # -----------------------------------------
        input_data = shared.get("input_data", {})
        input_types = shared.get("input_types") or self._detect_input_types(input_data)
        output_type = shared.get("output_type", OutputType.TEXT)
        task_type = shared.get("task_type", TaskType.GENERAL)
        constraints = shared.get("model_constraints", {})

        provider: Optional[str] = None
        model: Optional[str] = None

        # -----------------------------------------
        # 1. Modèle forcé ?
        # -----------------------------------------
        if self.forced_model:
            for prov, models in self.model_registry.items():
                if self.forced_model in models:
                    provider = prov
                    model = self.forced_model
                    break
            if provider is None:
                raise ValueError(f"Le modèle forcé '{self.forced_model}' n'existe pas dans le registre.")
        else:
            # -----------------------------------------
            # 2. Sélection automatique
            # -----------------------------------------
            try:
                provider, model = self.select_optimal_model(
                    input_types=input_types,
                    output_type=output_type,
                    task_type=task_type,
                    constraints=constraints,
                )
            except ValueError as e:
                self.logger.error(f"Sélection automatique impossible : {e}. Fallback.")
                if "openai" in self.providers:
                    provider, model = "openai", "gpt-3.5-turbo"
                elif "gemini" in self.providers:
                    provider, model = "gemini", "gemini-1.5-flash"
                else:
                    raise

        # -----------------------------------------
        # 3. Mise à jour du shared store
        # -----------------------------------------
        shared.set("selected_llm_provider", provider)
        shared.set("selected_llm_model", model)
        shared.set("llm_api_key", self.api_keys.get(provider))

        self.logger.info(f"[ModelRouter] modèle sélectionné : {provider}/{model}")
        return {"status": "success", "provider": provider, "model": model}


