# Example Plugin pour Nüm Agents SDK

Ce projet est un exemple de plugin pour le SDK Nüm Agents, démontrant comment étendre les fonctionnalités du SDK sans modifier son code source.

## Fonctionnalités

Ce plugin fournit :

- Un nouvel univers : `ExampleUnivers`
- Deux nouveaux types de nœuds :
  - `ExampleNode` : Un nœud simple qui ajoute un message au magasin partagé
  - `DataProcessingNode` : Un nœud qui effectue des opérations de traitement de données

## Installation

### Installation depuis le code source

```bash
# Cloner le dépôt
git clone https://github.com/Creativityliberty/numagents.git
cd numagents/examples/plugins/example-plugin

# Installer le plugin en mode développement
pip install -e .
```

## Utilisation

Une fois le plugin installé, vous pouvez l'utiliser dans vos spécifications d'agent :

```yaml
# agent.yaml
name: "Mon Agent avec Plugin"
description: "Un agent qui utilise l'exemple de plugin"
universes:
  - "ExampleUnivers"  # Univers fourni par le plugin
protocol: "LLM"
llm:
  provider: "openai"
  model: "gpt-4"
```

Le plugin sera automatiquement découvert par le SDK Nüm Agents, et les univers et nœuds qu'il fournit seront disponibles pour votre agent.

## Structure du plugin

```
example-plugin/
├── pyproject.toml             # Configuration du package et points d'entrée
├── README.md                  # Ce fichier
└── example_plugin/            # Package Python du plugin
    ├── __init__.py            # Initialisation du package
    ├── plugin.py              # Implémentation du plugin (ExamplePlugin)
    ├── nodes/                 # Nœuds fournis par le plugin
    │   ├── example_node.py    # Implémentation de ExampleNode
    │   └── data_processing_node.py  # Implémentation de DataProcessingNode
    └── univers/               # Univers fournis par le plugin
        └── example_univers.py # Implémentation de ExampleUnivers
```

## Développement

Pour développer ce plugin :

1. Modifiez les fichiers dans le répertoire `example_plugin/`
2. Installez le plugin en mode développement avec `pip install -e .`
3. Testez le plugin avec le SDK Nüm Agents

## Licence

Propriétaire. Tous droits réservés à "lionel TAGNE".
