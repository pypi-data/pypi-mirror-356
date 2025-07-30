# Guide de création de plugins pour Nüm Agents SDK

Ce guide explique comment créer et intégrer des plugins pour le SDK Nüm Agents, permettant d'étendre les fonctionnalités du SDK sans modifier son code source.

## Introduction

Le système de plugins de Nüm Agents SDK permet aux développeurs d'étendre les fonctionnalités du SDK en ajoutant :
- De nouveaux univers et modules
- De nouveaux types de nœuds
- Des fonctionnalités personnalisées

Les plugins sont découverts automatiquement par le SDK, soit via les points d'entrée setuptools, soit en les plaçant dans un répertoire spécifique.

## Structure d'un plugin

Un plugin Nüm Agents doit suivre une structure spécifique :

```
mon-plugin/
├── pyproject.toml (ou setup.py)
├── README.md
└── mon_plugin/
    ├── __init__.py
    ├── plugin.py
    ├── univers/
    │   └── mon_univers.py
    └── nodes/
        └── mon_node.py
```

### Fichier de configuration du plugin

Chaque plugin doit définir une classe qui hérite de `PluginBase` et implémente les méthodes requises. Cette classe est généralement définie dans un fichier `plugin.py` :

```python
from num_agents.plugins.plugin_base import PluginBase, PluginManifest
from num_agents.univers.univers_catalog_loader import UniversCatalogEntry
from num_agents.core import Node

class MonPlugin(PluginBase):
    """Implémentation de mon plugin pour Nüm Agents SDK."""
    
    def get_manifest(self) -> PluginManifest:
        """Retourne le manifeste du plugin."""
        return PluginManifest(
            name="mon-plugin",
            version="0.1.0",
            description="Mon plugin pour Nüm Agents SDK",
            author="Votre Nom",
            website="https://github.com/votre-nom/mon-plugin"
        )
    
    def initialize(self) -> None:
        """Initialise le plugin."""
        # Code d'initialisation si nécessaire
        pass
    
    def get_universes(self) -> dict[str, UniversCatalogEntry]:
        """Retourne les univers fournis par ce plugin."""
        return {
            "MonUnivers": UniversCatalogEntry(
                name="MonUnivers",
                description="Mon univers personnalisé",
                modules=["MonNode", "AutreNode"],
                version="0.1.0",
                author="Votre Nom",
                tags=["personnalisé", "exemple"]
            )
        }
    
    def get_node_types(self) -> dict[str, type[Node]]:
        """Retourne les types de nœuds fournis par ce plugin."""
        from mon_plugin.nodes.mon_node import MonNode
        return {
            "MonNode": MonNode
        }
```

## Enregistrement du plugin

Il existe deux façons d'enregistrer votre plugin pour qu'il soit découvert par le SDK :

### 1. Via les points d'entrée setuptools

Dans votre fichier `pyproject.toml` (si vous utilisez Poetry) :

```toml
[tool.poetry]
name = "mon-plugin"
version = "0.1.0"
description = "Mon plugin pour Nüm Agents SDK"
authors = ["Votre Nom <votre.email@exemple.com>"]

[tool.poetry.dependencies]
python = "^3.9"
num-agents = "^0.1.0"

[tool.poetry.dev-dependencies]
pytest = "^7.0.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.plugins."num_agents.plugins"]
mon_plugin = "mon_plugin.plugin:MonPlugin"
```

Ou dans votre fichier `setup.py` (si vous utilisez setuptools) :

```python
from setuptools import setup, find_packages

setup(
    name="mon-plugin",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "num_agents.plugins": [
            "mon_plugin = mon_plugin.plugin:MonPlugin",
        ],
    },
)
```

### 2. Via un répertoire de plugins

Placez votre plugin dans un répertoire spécifique et configurez le SDK pour qu'il recherche les plugins dans ce répertoire :

```python
from num_agents.plugins.plugin_manager import PluginManager

# Initialiser le gestionnaire de plugins avec un répertoire personnalisé
plugin_manager = PluginManager(plugin_dirs=["/chemin/vers/plugins"])
```

## Création d'un nouvel univers

Pour créer un nouvel univers, définissez une classe qui représente cet univers et ses modules :

```python
# mon_plugin/univers/mon_univers.py
from typing import List

class MonUnivers:
    """Définition de mon univers personnalisé."""
    
    @staticmethod
    def get_modules() -> List[str]:
        """Retourne la liste des modules de cet univers."""
        return ["MonNode", "AutreNode"]
```

## Création d'un nouveau type de nœud

Pour créer un nouveau type de nœud, créez une classe qui hérite de `Node` :

```python
# mon_plugin/nodes/mon_node.py
from typing import Any, Dict
from num_agents.core import Node, SharedStore

class MonNode(Node):
    """Implémentation de mon nœud personnalisé."""
    
    def __init__(self) -> None:
        """Initialise le nœud."""
        super().__init__("MonNode")
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Exécute la logique de traitement du nœud.
        
        Args:
            shared: Le magasin partagé pour accéder et stocker des données
            
        Returns:
            Un dictionnaire contenant les résultats de l'exécution du nœud
        """
        # Implémentez la logique du nœud ici
        return {"status": "success", "message": "Mon nœud personnalisé a été exécuté avec succès !"}
```

## Utilisation de votre plugin

Une fois votre plugin installé ou placé dans le répertoire des plugins, il sera automatiquement découvert par le SDK. Vous pouvez ensuite utiliser les univers et les nœuds fournis par votre plugin dans vos spécifications d'agent :

```yaml
# agent.yaml
name: "Mon Agent"
description: "Un agent utilisant mon plugin personnalisé"
universes:
  - "MonUnivers"  # Univers fourni par votre plugin
protocol: "LLM"
llm:
  provider: "openai"
  model: "gpt-4"
```

## Bonnes pratiques

1. **Documentation** : Documentez clairement votre plugin, ses univers et ses nœuds.
2. **Tests** : Écrivez des tests pour votre plugin pour garantir son bon fonctionnement.
3. **Versionnement** : Utilisez le versionnement sémantique pour votre plugin.
4. **Dépendances** : Spécifiez clairement les dépendances de votre plugin.
5. **Compatibilité** : Indiquez avec quelles versions du SDK votre plugin est compatible.

## Exemple complet

Un exemple complet de plugin est disponible dans le répertoire `examples/plugins/example-plugin/` du SDK.

## Dépannage

Si votre plugin n'est pas découvert automatiquement :

1. Vérifiez que votre plugin est correctement installé ou placé dans le bon répertoire.
2. Assurez-vous que votre plugin implémente correctement l'interface `PluginBase`.
3. Vérifiez que les points d'entrée sont correctement configurés dans votre fichier `pyproject.toml` ou `setup.py`.
4. Activez la journalisation de débogage pour voir les messages de découverte des plugins :
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

## Conclusion

Le système de plugins de Nüm Agents SDK offre une grande flexibilité pour étendre les fonctionnalités du SDK sans modifier son code source. En suivant ce guide, vous pouvez créer et intégrer vos propres plugins pour répondre à vos besoins spécifiques.
