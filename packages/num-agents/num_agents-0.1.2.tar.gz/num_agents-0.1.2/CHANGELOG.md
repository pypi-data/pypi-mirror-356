# Changelog

Toutes les modifications notables apportées au projet Nüm Agents SDK seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2025-06-19

### Ajouté

- Commande CLI `dashboard` pour lancer le tableau de bord Streamlit sur un agent ou un système multi-agents
- Commande CLI `generate-system` pour générer automatiquement la structure d’un système multi-agents à partir d’un fichier YAML
- Commande CLI `run` avec l’option `--live-graph` pour exécuter un agent avec visualisation en temps réel du graphe logique
- Génération automatique des dossiers, coordination et ressources partagées pour les systèmes multi-agents

### Amélioré

- Documentation enrichie pour l’utilisation avancée du CLI et la génération de systèmes multi-agents



### Ajouté

- Tableau de bord interactif avec Streamlit pour la visualisation et la gestion des agents
- Visualisations avancées avec Plotly (chronologies, diagrammes de Gantt, cartes de chaleur, graphiques radar)
- Fonctionnalités d'exportation de données en CSV, JSON et Excel
- Édition interactive des configurations d'agents via l'interface web
- Contrôle d'exécution des agents (démarrage/arrêt) depuis le tableau de bord
- Vues détaillées pour les agents, graphes logiques, mémoire, métriques et traces
- Script de démonstration pour générer des données d'exemple pour le tableau de bord
- Fournisseurs de données modulaires pour les agents, journaux et métriques
- Visualisation avancée des événements d'agent avec filtrage et chronologie interactive
- Visualisation avancée des erreurs avec analyse statistique et classification
- Amélioration de la visualisation des performances des nœuds avec vue d'ensemble et analyse détaillée
- Documentation complète du tableau de bord et de son architecture

### Amélioré

- Structure modulaire du tableau de bord pour faciliter les extensions futures
- Styles personnalisés et thèmes pour une meilleure expérience utilisateur
- Architecture de fournisseurs de données pour une séparation claire entre la logique et l'affichage
- Optimisation des performances avec mise en cache des données fréquemment utilisées

## [0.1.0] - 2025-06-18

### Fonctionnalités initiales

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
