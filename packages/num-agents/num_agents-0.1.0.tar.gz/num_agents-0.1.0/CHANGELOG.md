# Changelog

Toutes les modifications notables apportées au projet Nüm Agents SDK seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-06-19

### Ajouté
- Architecture de base du SDK avec système de nœuds et de flux
- Implémentation du `ModelRouterNode` pour la sélection intelligente de modèles LLM
- Support pour les fournisseurs OpenAI et Google Gemini
- Système de routage dynamique basé sur les types d'entrée/sortie, le type de tâche et les priorités d'optimisation
- Support pour forcer l'utilisation d'un modèle spécifique dans le `ModelRouterNode`
- Moteur de logique (`LogicEngine`) pour le raisonnement et l'inférence
- Nœud de pondération d'expertise (`ExpertiseWeightingNode`) pour la fusion d'opinions d'experts
- Interface CLI de base pour la gestion des workflows
- Système de store partagé pour la communication entre les nœuds
- Exemples de démonstration pour les fonctionnalités principales

### Changé
- Refactorisation de l'architecture des nœuds pour utiliser la méthode `exec` au lieu de `_run`

### Corrigé
- Correction des problèmes d'indentation et de syntaxe dans le `ModelRouterNode`
- Restauration des docstrings originales dans tous les fichiers
- Correction des erreurs de validation dans les tests
