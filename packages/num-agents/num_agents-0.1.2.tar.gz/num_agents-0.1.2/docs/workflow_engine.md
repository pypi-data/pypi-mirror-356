# Workflow Engine

Le moteur de workflow du SDK Nüm Agents fournit un système puissant pour définir et exécuter des chaînes de tâches avec des dépendances, des personas spécialisés et des vérifications internes.

## Table des matières

- [Introduction](#introduction)
- [Concepts clés](#concepts-clés)
- [Format YAML des chaînes de tâches](#format-yaml-des-chaînes-de-tâches)
- [Personas](#personas)
- [Utilisation du CLI](#utilisation-du-cli)
- [Intégration avec d'autres composants](#intégration-avec-dautres-composants)
- [Exemples](#exemples)

## Introduction

Le moteur de workflow permet de définir des chaînes de tâches complexes qui peuvent être exécutées par différents personas spécialisés. Chaque étape de la chaîne peut dépendre des résultats d'étapes précédentes, et le moteur s'assure que les étapes sont exécutées dans le bon ordre.

Ce système est particulièrement utile pour orchestrer des processus de raisonnement complexes, où différentes étapes nécessitent différentes compétences ou perspectives.

## Concepts clés

### TaskPrompt

Un `TaskPrompt` définit ce qu'une étape requiert, ce qu'elle produit, et quelles vérifications internes doivent être effectuées.

```python
class TaskPrompt(BaseModel):
    text: str
    requires: List[str] = []
    produces: List[str] = []
    internal_checks: List[str] = []
```

### TaskStep

Un `TaskStep` représente une unité de travail dans une chaîne de tâches, avec un persona spécifique, des dépendances et des sorties attendues.

```python
class TaskStep(BaseModel):
    index: int
    persona: str
    depends_on: List[int] = []
    description: str
    prompt: TaskPrompt
    outputs: List[str] = []
```

### TaskChain

Un `TaskChain` représente une séquence d'étapes avec des dépendances, des réflexions, des erreurs, des notes et des avertissements.

```python
class TaskChain(BaseModel):
    steps: List[TaskStep]
    reflect: Optional[str] = None
    err: List[str] = []
    note: List[str] = []
    warn: List[str] = []
```

### WorkflowEngine

Le `WorkflowEngine` est responsable du chargement des chaînes de tâches, de l'enregistrement des personas et de l'exécution des chaînes de tâches dans le bon ordre.

```python
class WorkflowEngine:
    def __init__(self, event_bus=None, shared_store=None): ...
    def register_persona(self, name, handler): ...
    def load_chain(self, chain_file): ...
    def save_chain(self, chain, output_file): ...
    def execute_chain(self, chain): ...
```

## Format YAML des chaînes de tâches

Les chaînes de tâches sont définies dans des fichiers YAML avec la structure suivante :

```yaml
steps:
  - index: 0
    persona: "Persona1"
    depends_on: []
    description: "Description de l'étape"
    prompt:
      text: "Texte du prompt"
      requires: []
      produces: ["output1.md"]
      internal_checks: ["Vérification 1", "Vérification 2"]
    outputs: ["output1.md"]

  - index: 1
    persona: "Persona2"
    depends_on: [0]
    description: "Description de l'étape"
    prompt:
      text: "Texte du prompt"
      requires: ["output1.md"]
      produces: ["output2.md"]
      internal_checks: []
    outputs: ["output2.md"]

reflect: "Réflexion sur la chaîne"
err: []
note: ["Note 1", "Note 2"]
warn: ["Avertissement 1"]
```

### Règles importantes

1. Chaque étape doit avoir un index unique.
2. Les dépendances (`depends_on`) doivent référencer des étapes avec des indices inférieurs.
3. Les personas référencés dans les étapes doivent être enregistrés dans le moteur de workflow.
4. Les chaînes de tâches ne doivent pas contenir de dépendances circulaires.

## Personas

Les personas sont des rôles spécialisés qui peuvent être assignés à des étapes dans une chaîne de tâches. Chaque persona a une fonction de traitement spécifique qui est appelée lorsqu'une étape est exécutée.

### Personas prédéfinis

Le SDK Nüm Agents fournit plusieurs personas prédéfinis :

- **Architect** : Responsable des décisions de conception de haut niveau, de l'architecture du système et de la direction technique.
- **Planner** : Responsable de la décomposition des tâches, de la définition des modules et de la création de plans d'implémentation.
- **Designer** : Responsable de la conception UI/UX, des flux utilisateur et des éléments visuels.
- **Coder** : Responsable de l'implémentation du code, de l'écriture des tests et de la correction des bugs.

### Création de personas personnalisés

Vous pouvez créer vos propres personas en définissant une fonction qui prend un `PersonaContext` et retourne un résultat :

```python
from num_agents.workflow.personas import registry
from num_agents.workflow.task_chain import PersonaContext

def my_custom_persona(context: PersonaContext) -> dict:
    # Accéder aux informations de l'étape
    step = context.step
    description = step.get("description", "")
    prompt = step.get("prompt", {})
    prompt_text = prompt.get("text", "")
    
    # Accéder aux résultats des dépendances
    dependencies = context.dependencies
    
    # Accéder au shared store
    shared_store = context.shared_store
    
    # Accéder à l'event bus
    event_bus = context.event_bus
    
    # Effectuer le travail du persona
    results = {}
    # ...
    
    return results

# Enregistrer le persona
registry.register("MyCustomPersona", my_custom_persona)
```

## Utilisation du CLI

Le SDK Nüm Agents fournit des commandes CLI pour travailler avec les chaînes de tâches :

### Exécuter une chaîne de tâches

```bash
num-agents workflow run chain.yaml --output-dir output --verbose
```

### Créer une chaîne de tâches exemple

```bash
num-agents workflow create chain.yaml --steps 3
```

### Valider une chaîne de tâches

```bash
num-agents workflow validate chain.yaml
```

## Intégration avec d'autres composants

Le moteur de workflow s'intègre avec d'autres composants du SDK Nüm Agents :

### EventBus

Le moteur de workflow publie des événements sur l'EventBus lorsque des étapes sont terminées ou échouent :

- `workflow.step.completed` : Publié lorsqu'une étape est terminée avec succès.
- `workflow.step.failed` : Publié lorsqu'une étape échoue.

### SharedStore

Le moteur de workflow utilise le SharedStore pour stocker et partager des données entre les étapes :

- Chaque persona peut accéder au SharedStore via le `PersonaContext`.
- Les résultats des étapes peuvent être stockés dans le SharedStore pour être utilisés par d'autres étapes.

## Exemples

### Exemple de chaîne de tâches

Voir le fichier [task_chain_example.yaml](/examples/task_chain_example.yaml) pour un exemple complet de chaîne de tâches.

### Exemple d'utilisation du moteur de workflow

```python
from num_agents.workflow.task_chain import WorkflowEngine
from num_agents.workflow.personas import registry
from num_agents.eventbus.eventbus import EventBus
from num_agents.core import SharedStore

# Créer un event bus et un shared store
event_bus = EventBus()
shared_store = SharedStore()

# Créer un moteur de workflow
engine = WorkflowEngine(event_bus=event_bus, shared_store=shared_store)

# Enregistrer les personas
for name in registry.list_personas():
    handler = registry.get(name)
    if handler:
        engine.register_persona(name, handler)

# Charger une chaîne de tâches
chain = engine.load_chain("chain.yaml")

# Exécuter la chaîne de tâches
results = engine.execute_chain(chain)

# Afficher les résultats
for step_idx, result in results.items():
    print(f"Step {step_idx} result: {result}")
```
