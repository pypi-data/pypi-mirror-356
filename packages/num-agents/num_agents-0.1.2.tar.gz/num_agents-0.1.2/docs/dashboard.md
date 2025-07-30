# Tableau de bord Nüm Agents

Le tableau de bord Nüm Agents est une interface web interactive pour visualiser, analyser et gérer vos agents. Il offre des visualisations avancées, des fonctionnalités d'exportation et un contrôle en temps réel de vos agents.

## Démarrage du tableau de bord

Pour lancer le tableau de bord, utilisez la commande CLI suivante :

```bash
num-agents dashboard --agent-dir /chemin/vers/agent
```

Ou pour un système multi-agents :

```bash
num-agents dashboard --system-dir /chemin/vers/systeme
```

## Structure du tableau de bord

Le tableau de bord est organisé en plusieurs vues principales :

### 1. Vue d'ensemble

La vue d'ensemble présente un résumé de l'état de l'agent ou du système multi-agents, avec des indicateurs clés de performance et des liens rapides vers les autres vues.

### 2. Vue des agents

Cette vue affiche les détails de configuration et l'état des agents. Pour un système multi-agents, elle permet de naviguer entre les différents agents.

Fonctionnalités :

- Affichage des métadonnées de l'agent (nom, description, univers utilisés)
- Visualisation de la configuration de l'agent
- Contrôle d'exécution (démarrer/arrêter l'agent)
- Édition de la configuration

### 3. Vue des graphes logiques

Cette vue permet de visualiser les graphes logiques générés par l'agent, avec les propositions, les règles et les inférences.

Fonctionnalités :

- Visualisation interactive des graphes logiques
- Filtrage par contexte, domaine ou type de proposition
- Analyse des chaînes d'inférence
- Exportation des graphes au format image ou JSON

### 4. Vue de la mémoire

Cette vue permet d'explorer la mémoire de l'agent, avec les faits, les croyances et les connaissances stockées.

Fonctionnalités :

- Exploration des différents types de mémoire (court terme, long terme)
- Recherche et filtrage des entrées de mémoire
- Visualisation des relations entre les entrées de mémoire
- Exportation des données de mémoire

### 5. Vue des métriques

Cette vue présente des métriques détaillées sur les performances de l'agent.

Fonctionnalités :

- Performance des nœuds (temps d'exécution, taux d'erreur)
- Utilisation des modèles LLM (nombre d'appels, coûts, tokens)
- Temps de réponse (latence, distribution)
- Visualisations avancées (graphiques à barres, courbes, cartes de chaleur)
- Exportation des métriques au format CSV, JSON ou Excel

### 6. Vue des traces

Cette vue permet d'explorer les traces d'exécution de l'agent, avec les journaux, les événements et les erreurs.

Fonctionnalités :

- Journaux d'exécution avec filtrage par niveau, source et période
- Visualisation des événements avec chronologie interactive
- Analyse des erreurs avec détails et statistiques
- Exportation des traces au format CSV, JSON ou Excel

## Architecture du tableau de bord

Le tableau de bord est construit avec une architecture modulaire :

### Composants

Les composants sont responsables de l'affichage des différentes vues et sont situés dans `num_agents/dashboard/components/`. Chaque composant est un module Python avec une fonction principale qui gère l'affichage de la vue.

### Fournisseurs de données

Les fournisseurs de données sont responsables de la récupération et du traitement des données pour les composants. Ils sont situés dans `num_agents/dashboard/data_providers/`.

- `agent_data_provider.py` : Fournit les données générales de l'agent
- `log_provider.py` : Fournit les journaux d'exécution
- `metrics_provider.py` : Fournit les métriques de performance

### Utilitaires

Les utilitaires fournissent des fonctions communes utilisées par les composants, comme la création de visualisations ou l'exportation de données. Ils sont situés dans `num_agents/dashboard/utils/`.

- `visualizations.py` : Fonctions pour créer des visualisations avancées
- `export.py` : Fonctions pour exporter des données
- `config.py` : Fonctions pour gérer la configuration du tableau de bord

## Personnalisation du tableau de bord

Le tableau de bord peut être personnalisé en modifiant les fichiers de configuration ou en étendant les composants existants.

### Ajout de nouveaux composants

Pour ajouter un nouveau composant, créez un nouveau module dans `num_agents/dashboard/components/` et ajoutez-le à la liste des composants dans `num_agents/dashboard/app.py`.

### Ajout de nouvelles visualisations

Pour ajouter une nouvelle visualisation, ajoutez une fonction dans `num_agents/dashboard/utils/visualizations.py` et utilisez-la dans vos composants.

### Modification du thème

Le thème du tableau de bord peut être modifié en ajustant les paramètres dans `num_agents/dashboard/utils/config.py`.

## Exemples d'utilisation

### Visualisation d'un système multi-agents

```bash
# Générer un système multi-agents
num-agents generate-system --spec multi_agent_system.yaml --catalog univers_catalog.yaml

# Lancer le tableau de bord sur le système
num-agents dashboard --system-dir ./MultiAgentSystem --port 8080
```

### Visualisation des performances d'un agent

```python
from pathlib import Path
from num_agents.dashboard.components.metrics_view import render_metrics_view

# Chemin vers le répertoire de l'agent
agent_dir = Path("/chemin/vers/agent")

# Afficher la vue des métriques
render_metrics_view(agent_dir)
```

### Exportation des journaux d'exécution

```python
from pathlib import Path
from num_agents.dashboard.data_providers.log_provider import LogProvider

# Chemin vers le répertoire de l'agent
agent_dir = Path("/chemin/vers/agent")

# Créer un fournisseur de journaux
log_provider = LogProvider(agent_dir)

# Exporter les journaux au format CSV
output_path = log_provider.export_logs(
    output_format="csv",
    level_filter=["ERROR", "WARNING"],
    start_time="2025-06-01T00:00:00"
)

print(f"Journaux exportés vers {output_path}")
```

### Analyse des erreurs d'un agent

```python
from pathlib import Path
import streamlit as st
from num_agents.dashboard.components.render_errors import render_errors

# Chemin vers le répertoire de l'agent
agent_dir = Path("/chemin/vers/agent")

# Afficher la vue des erreurs
render_errors(agent_dir)
```

## Bonnes pratiques

1. **Utiliser les fournisseurs de données** : Utilisez les fournisseurs de données pour récupérer les informations plutôt que d'accéder directement aux fichiers.

2. **Séparer la logique et l'affichage** : Gardez la logique de traitement des données dans les fournisseurs de données et l'affichage dans les composants.

3. **Gérer les erreurs** : Assurez-vous que vos composants gèrent correctement les cas où les données ne sont pas disponibles.

4. **Optimiser les performances** : Utilisez le cache pour éviter de recharger les mêmes données plusieurs fois.

5. **Documenter les composants** : Ajoutez des docstrings à vos fonctions et classes pour faciliter leur utilisation par d'autres développeurs.
