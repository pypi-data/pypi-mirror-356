# Moteur de Raisonnement Logique

Le moteur de raisonnement logique (`LogicEngine`) est un composant du SDK Nüm Agents qui permet aux agents d'effectuer des raisonnements structurés, d'évaluer des propositions logiques et de construire des preuves formelles.

## Objectifs du moteur de raisonnement

- Permettre aux agents de manipuler et d'évaluer des propositions logiques
- Faciliter la construction et la vérification de preuves logiques
- Évaluer la cohérence d'un ensemble de propositions
- Fournir une structure pour le raisonnement basé sur des critères
- Intégrer des capacités de raisonnement logique dans les flux d'agents

## Modèles de données

Le moteur de raisonnement utilise plusieurs modèles Pydantic pour représenter les éléments logiques :

### Proposition

Une proposition est une affirmation ou une question qui peut être évaluée logiquement.

```python
class PropositionType(str, Enum):
    STATEMENT = "statement"
    QUESTION = "question"
    HYPOTHESIS = "hypothesis"
    CONCLUSION = "conclusion"
    AXIOM = "axiom"
    LEMMA = "lemma"
    THEOREM = "theorem"

class PropositionStatus(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    REFUTED = "refuted"
    UNDECIDABLE = "undecidable"
    PENDING = "pending"

class Proposition(BaseModel):
    id: str
    type: PropositionType
    text: str
    status: PropositionStatus = PropositionStatus.UNVERIFIED
    confidence: Optional[float] = None
    source: Optional[PropositionSource] = None
    metadata: Dict[str, Any] = {}
```

### Preuve

Une preuve connecte des prémisses à une conclusion à travers une série d'étapes logiques.

```python
class ProofStep(BaseModel):
    id: str
    from_propositions: List[str]
    to_propositions: List[str]
    rule: str
    justification: str
    metadata: Dict[str, Any] = {}

class Proof(BaseModel):
    id: str
    premise_ids: List[str]
    conclusion_ids: List[str]
    steps: List[ProofStep]
    metadata: Dict[str, Any] = {}
```

### Critère

Les critères permettent d'évaluer les propositions, les preuves et autres éléments logiques.

```python
class CriterionType(str, Enum):
    CONSISTENCY = "consistency"
    COMPLETENESS = "completeness"
    SOUNDNESS = "soundness"
    RELEVANCE = "relevance"
    CLARITY = "clarity"
    PARSIMONY = "parsimony"

class Criterion(BaseModel):
    id: str
    type: CriterionType
    description: str
    weight: float = 1.0
    metadata: Dict[str, Any] = {}
```

### Contexte logique

Un contexte logique regroupe tous les éléments logiques liés à un sujet ou un problème particulier.

```python
class LogicalContext(BaseModel):
    id: str
    name: str
    description: str
    propositions: Dict[str, Proposition] = {}
    evidence: Dict[str, Evidence] = {}
    proofs: Dict[str, Proof] = {}
    criteria: Dict[str, Criterion] = {}
    evaluations: List[CriterionEvaluation] = []
    metadata: Dict[str, Any] = {}
```

## Utilisation du moteur de raisonnement

### Initialisation

```python
from num_agents.reasoning.logic_engine import LogicEngine

# Créer une instance du moteur de raisonnement
engine = LogicEngine()
```

### Création d'un contexte logique

```python
# Créer un nouveau contexte logique
context = engine.create_context(
    name="Analyse de projet",
    description="Contexte logique pour l'analyse d'un projet de développement"
)

# Récupérer un contexte existant
context = engine.get_context(context_id)
```

### Manipulation de propositions

```python
# Ajouter une proposition
proposition = engine.add_proposition(
    context_id=context.id,
    text="Le framework React est adapté pour ce projet",
    prop_type=PropositionType.HYPOTHESIS,
    confidence=0.7,
    metadata={"domain": "web_development"}
)

# Ajouter une preuve
proof = engine.create_proof(
    context_id=context.id,
    premise_ids=["prop1", "prop2"],
    conclusion_ids=["prop3"],
    steps=[
        ProofStep(
            id="step1",
            from_propositions=["prop1", "prop2"],
            to_propositions=["prop3"],
            rule="inférence",
            justification="Si les exigences incluent une interface utilisateur dynamique et des composants réutilisables, alors React est adapté."
        )
    ]
)

# Vérifier la cohérence du contexte
is_consistent, inconsistencies = engine.check_consistency(context.id)
if not is_consistent:
    print("Inconsistances détectées:", inconsistencies)
```

### Exportation et importation

```python
# Exporter un contexte
context_data = engine.export_context(context.id)

# Importer un contexte
imported_context = engine.import_context(context_data)
```

## Nœuds de raisonnement logique

Le SDK Nüm Agents fournit plusieurs nœuds spécialisés pour intégrer le raisonnement logique dans les flux d'agents.

### LogicReasoningNode

Nœud de base pour les opérations de raisonnement logique.

```python
from num_agents.reasoning.nodes import LogicReasoningNode

node = LogicReasoningNode(
    name="reasoning",
    context_name="Analyse technique",
    context_description="Analyse technique du projet",
    shared_store_key="logic_context_id"
)
```

### PropositionEvaluationNode

Évalue des propositions par rapport à des critères.

```python
from num_agents.reasoning.nodes import PropositionEvaluationNode

node = PropositionEvaluationNode(
    name="evaluate_proposition",
    proposition_id_key="current_proposition_id",
    criterion_id_key="current_criterion_id",
    evaluation_result_key="evaluation_result"
)
```

### ConsistencyCheckNode

Vérifie la cohérence logique d'un contexte.

```python
from num_agents.reasoning.nodes import ConsistencyCheckNode

node = ConsistencyCheckNode(
    name="check_consistency",
    consistency_result_key="consistency_result"
)
```

### PropositionImportNode

Importe des propositions depuis le `SharedStore` dans un contexte logique.

```python
from num_agents.reasoning.nodes import PropositionImportNode

node = PropositionImportNode(
    name="import_hypotheses",
    propositions_key="hypotheses_list",
    imported_ids_key="imported_hypothesis_ids",
    proposition_type=PropositionType.HYPOTHESIS
)
```

## Extension du moteur de raisonnement

### Création de règles logiques personnalisées

Vous pouvez étendre le moteur de raisonnement en créant des règles logiques personnalisées.

```python
class EnhancedLogicEngine(LogicEngine):
    def __init__(self):
        super().__init__()
        self.register_rule("custom_rule", self._apply_custom_rule)
    
    def _apply_custom_rule(self, propositions, context):
        # Implémentation de la règle personnalisée
        pass
```

### Nœuds de raisonnement personnalisés

Vous pouvez créer des nœuds de raisonnement personnalisés en héritant de `LogicReasoningNode`.

```python
class SpecializedReasoningNode(LogicReasoningNode):
    def __init__(self, name, specific_parameter, **kwargs):
        super().__init__(name, **kwargs)
        self.specific_parameter = specific_parameter
    
    def _process_reasoning(self, context_id, shared_store):
        # Implémentation spécialisée
        pass
```

## Exemple complet d'un flux de raisonnement logique

Voici un exemple complet d'un flux d'agent utilisant le moteur de raisonnement logique pour analyser un problème :

```python
from num_agents.core import Flow, SharedStore
from num_agents.reasoning.logic_engine import LogicEngine
from num_agents.reasoning.nodes import (
    LogicReasoningNode,
    PropositionImportNode,
    ConsistencyCheckNode,
    PropositionEvaluationNode
)

# Créer le moteur de raisonnement
engine = LogicEngine()

# Créer les nœuds
import_node = PropositionImportNode(
    name="import_hypotheses",
    propositions_key="hypotheses",
    imported_ids_key="hypothesis_ids",
    engine=engine
)

consistency_node = ConsistencyCheckNode(
    name="check_consistency",
    consistency_result_key="consistency_result",
    engine=engine
)

# Créer le flux
flow = Flow()
flow.add_node(import_node)
flow.add_node(consistency_node)

# Créer le SharedStore et y ajouter des hypothèses
shared_store = SharedStore()
shared_store.set("hypotheses", [
    "Les microservices sont adaptés pour ce projet",
    "Le projet nécessite une haute disponibilité",
    "La simplicité de déploiement est une priorité"
])

# Exécuter le flux
flow.execute(shared_store)

# Récupérer les résultats
consistency_result = shared_store.get("consistency_result")
print(f"Les hypothèses sont cohérentes: {consistency_result['is_consistent']}")
```

## Intégration avec le moteur de workflow

Le moteur de raisonnement logique peut être intégré au moteur de workflow pour créer des chaînes de tâches qui effectuent des raisonnements complexes.

```yaml
name: analyse_technique
description: Analyse technique d'une architecture logicielle
steps:
  - id: import_hypotheses
    persona: architect
    prompt: |
      Importer les hypothèses suivantes dans le contexte logique:
      - Les microservices sont adaptés pour ce projet
      - Le projet nécessite une haute disponibilité
      - La simplicité de déploiement est une priorité
    output_key: hypotheses
    
  - id: evaluate_consistency
    persona: architect
    prompt: |
      Évaluer la cohérence des hypothèses importées.
    dependencies:
      - import_hypotheses
    input_keys:
      - hypotheses
    output_key: consistency_analysis
    
  - id: draw_conclusions
    persona: architect
    prompt: |
      Sur la base de l'évaluation de cohérence, formuler des conclusions
      concernant l'architecture technique recommandée.
    dependencies:
      - evaluate_consistency
    input_keys:
      - consistency_analysis
    output_key: technical_recommendations
```

## Bonnes pratiques

- Utilisez des identifiants clairs et descriptifs pour les propositions et les contextes
- Assurez-vous que les propositions sont bien formées et précises
- Vérifiez régulièrement la cohérence des contextes logiques
- Utilisez des métadonnées pour enrichir les éléments logiques avec des informations contextuelles
- Implémentez des méthodes d'évaluation personnalisées pour des domaines spécifiques
- Documentez les règles logiques personnalisées et leur fonctionnement
