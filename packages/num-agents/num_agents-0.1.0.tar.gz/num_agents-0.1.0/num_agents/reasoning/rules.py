"""
Logical rules for the reasoning engine.

This module defines standard logical rules and inference patterns
that can be used by the LogicEngine for automated reasoning.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
import logging
import string

from num_agents.reasoning.models import (
    Proposition, PropositionType, PropositionStatus,
    ProofStep, LogicalContext
)


def _normalize_text(text: str) -> str:
    """Normalize text by making it lowercase, removing punctuation, and stripping whitespace."""
    return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()


class LogicalRule:
    """Base class for logical rules."""
    
    def __init__(self, name: str, description: str):
        """
        Initialize a logical rule.
        
        Args:
            name: Name of the rule
            description: Description of the rule
        """
        self.name = name
        self.description = description
        self.logger = logging.getLogger(__name__)
    
    def apply(
        self, 
        context: LogicalContext,
        propositions: List[Proposition]
    ) -> Optional[Tuple[List[Proposition], ProofStep]]:
        """
        Apply the rule to a set of propositions.
        
        Args:
            context: The logical context
            propositions: The propositions to apply the rule to
            
        Returns:
            A tuple of (new_propositions, proof_step) if the rule applies,
            or None if the rule does not apply
        """
        raise NotImplementedError("Subclasses must implement apply()")
    
    def _create_proof_step(
        self,
        from_ids: List[str],
        to_ids: List[str],
        justification: str
    ) -> ProofStep:
        """
        Create a proof step for this rule application.
        
        Args:
            from_ids: IDs of source propositions
            to_ids: IDs of derived propositions
            justification: Justification for the step
            
        Returns:
            A ProofStep object
        """
        import uuid
        return ProofStep(
            id=str(uuid.uuid4()),
            from_propositions=from_ids,
            to_propositions=to_ids,
            rule=self.name,
            justification=justification
        )


class ModusPonens(LogicalRule):
    """
    Modus Ponens rule: If P implies Q, and P is true, then Q is true.
    
    This rule looks for patterns of the form:
    1. "If P then Q" (or equivalent)
    2. "P"
    And derives: "Q"
    """
    
    def __init__(self):
        """Initialize the Modus Ponens rule."""
        super().__init__(
            name="modus_ponens",
            description="If P implies Q, and P is true, then Q is true"
        )
    
    def apply(
        self, 
        context: LogicalContext,
        propositions: List[Proposition]
    ) -> Optional[Tuple[List[Proposition], ProofStep]]:
        """
        Apply the Modus Ponens rule.
        
        Args:
            context: The logical context
            propositions: The propositions to apply the rule to
            
        Returns:
            A tuple of (new_propositions, proof_step) if the rule applies,
            or None if the rule does not apply
        """
        # This is a simplified implementation that looks for implications
        # In a real system, you would use a more sophisticated approach,
        # possibly with NLP or a specialized parser
        
        # Look for implications (if P then Q) that are VERIFIED
        implications = []
        for prop in propositions:
            if prop.status == PropositionStatus.VERIFIED and "if" in prop.text.lower() and "then" in prop.text.lower(): # MODIFIED
                implications.append(prop)
        
        if not implications:
            return None
        
        # For each implication, look for a matching premise
        for impl in implications: # `impl` here will now only be VERIFIED implications
            # Extract the premise and conclusion from the implication
            # This is a very simplified approach
            parts = impl.text.lower().split("then")
            if len(parts) != 2:
                continue
                
            premise_text = parts[0].replace("if", "").strip()
            conclusion_text = parts[1].strip()
            
            # Look for a matching premise
            for premise in propositions:
                if premise.id == impl.id:
                    continue  # Skip the implication itself
                
                # Simple text matching (in a real system, use semantic matching)
                # Only use VERIFIED propositions for inference
                if premise.status == PropositionStatus.VERIFIED and _normalize_text(premise.text) == premise_text:
                    # Create a new proposition for the conclusion
                    import uuid
                    conclusion = Proposition(
                        id=str(uuid.uuid4()),
                        type=PropositionType.CONCLUSION,
                        text=conclusion_text.capitalize(),
                        status=PropositionStatus.VERIFIED # Conclusion is VERIFIED by rule application
                    )
                    
                    # Create a proof step
                    justification = f"By Modus Ponens: From '{impl.text}' and '{premise.text}', we can conclude '{conclusion.text}'"
                    proof_step = self._create_proof_step(
                        from_ids=[impl.id, premise.id],
                        to_ids=[conclusion.id],
                        justification=justification
                    )
                    
                    return ([conclusion], proof_step)
        
        return None


class ModusTollens(LogicalRule):
    """
    Modus Tollens rule: If P implies Q, and Q is false, then P is false.
    
    This rule looks for patterns of the form:
    1. "If P then Q" (or equivalent)
    2. "not Q"
    And derives: "not P"
    """
    
    def __init__(self):
        """Initialize the Modus Tollens rule."""
        super().__init__(
            name="modus_tollens",
            description="If P implies Q, and Q is false, then P is false"
        )
    
    def apply(
        self, 
        context: LogicalContext,
        propositions: List[Proposition]
    ) -> Optional[Tuple[List[Proposition], ProofStep]]:
        """
        Apply the Modus Tollens rule.
        
        Args:
            context: The logical context
            propositions: The propositions to apply the rule to
            
        Returns:
            A tuple of (new_propositions, proof_step) if the rule applies,
            or None if the rule does not apply
        """
        # Look for implications (if P then Q)
        implications = []
        for prop in propositions:
            if "if" in prop.text.lower() and "then" in prop.text.lower():
                implications.append(prop)
        
        if not implications:
            return None
        
        # For each implication, look for a negated conclusion
        for impl in implications:
            # Extract the premise and conclusion from the implication
            parts = impl.text.lower().split("then")
            if len(parts) != 2:
                continue
                
            premise_text = parts[0].replace("if", "").strip()
            conclusion_text = parts[1].strip()
            
            # Look for a negated conclusion
            for prop in propositions:
                if prop.id == impl.id:
                    continue  # Skip the implication itself
                
                # Check if this proposition is a negation of the conclusion
                # This is a simplified approach
                negation_prefixes = ["not ", "it is not true that ", "it is false that "]
                negation_found = False
                
                for prefix in negation_prefixes:
                    if _normalize_text(prop.text) == _normalize_text(prefix + conclusion_text):
                        negation_found = True
                        break
                
                if not negation_found:
                    continue
                
                # Create a new proposition for the negated premise
                import uuid
                negated_premise = Proposition(
                    id=str(uuid.uuid4()),
                    type=PropositionType.CONCLUSION,
                    text=f"Not {premise_text}",
                    status=PropositionStatus.VERIFIED
                )
                
                # Create a proof step
                justification = f"By Modus Tollens: From '{impl.text}' and '{prop.text}', we can conclude '{negated_premise.text}'"
                proof_step = self._create_proof_step(
                    from_ids=[impl.id, prop.id],
                    to_ids=[negated_premise.id],
                    justification=justification
                )
                
                return ([negated_premise], proof_step)
        
        return None


class HypotheticalSyllogism(LogicalRule):
    """
    Hypothetical Syllogism rule: If P implies Q and Q implies R, then P implies R.
    
    This rule looks for patterns of the form:
    1. "If P then Q" (or equivalent)
    2. "If Q then R" (or equivalent)
    And derives: "If P then R"
    """
    
    def __init__(self):
        """Initialize the Hypothetical Syllogism rule."""
        super().__init__(
            name="hypothetical_syllogism",
            description="If P implies Q and Q implies R, then P implies R"
        )
    
    def apply(
        self, 
        context: LogicalContext,
        propositions: List[Proposition]
    ) -> Optional[Tuple[List[Proposition], ProofStep]]:
        """
        Apply the Hypothetical Syllogism rule.
        
        Args:
            context: The logical context
            propositions: The propositions to apply the rule to
            
        Returns:
            A tuple of (new_propositions, proof_step) if the rule applies,
            or None if the rule does not apply
        """
        # Look for implications (if P then Q)
        implications = []
        for prop in propositions:
            if "if" in prop.text.lower() and "then" in prop.text.lower():
                implications.append(prop)
        
        if len(implications) < 2:
            return None
        
        # Check all pairs of implications
        for i, impl1 in enumerate(implications):
            parts1 = impl1.text.lower().split("then")
            if len(parts1) != 2:
                continue
                
            premise1 = _normalize_text(parts1[0].replace("if", ""))
            conclusion1 = _normalize_text(parts1[1])
            
            for j, impl2 in enumerate(implications):
                if i == j:
                    continue
                    
                parts2 = impl2.text.lower().split("then")
                if len(parts2) != 2:
                    continue
                    
                premise2 = _normalize_text(parts2[0].replace("if", ""))
                conclusion2 = _normalize_text(parts2[1])
                
                # Check if the conclusion of the first matches the premise of the second
                if conclusion1 == premise2:
                    # Create a new proposition for the transitive implication
                    import uuid
                    new_implication = Proposition(
                        id=str(uuid.uuid4()),
                        type=PropositionType.CONCLUSION,
                        text=f"If {premise1} then {conclusion2}",
                        status=PropositionStatus.VERIFIED
                    )
                    
                    # Create a proof step
                    justification = f"By Hypothetical Syllogism: From '{impl1.text}' and '{impl2.text}', we can conclude '{new_implication.text}'"
                    proof_step = self._create_proof_step(
                        from_ids=[impl1.id, impl2.id],
                        to_ids=[new_implication.id],
                        justification=justification
                    )
                    
                    return ([new_implication], proof_step)
        
        return None


class Conjunction(LogicalRule):
    """
    Conjunction rule: If P is true and Q is true, then "P and Q" is true.
    
    This rule combines separate propositions into a conjunction.
    """
    
    def __init__(self):
        """Initialize the Conjunction rule."""
        super().__init__(
            name="conjunction",
            description="If P is true and Q is true, then 'P and Q' is true"
        )
    
    def apply(
        self, 
        context: LogicalContext,
        propositions: List[Proposition]
    ) -> Optional[Tuple[List[Proposition], ProofStep]]:
        """
        Apply the Conjunction rule.
        
        Args:
            context: The logical context
            propositions: The propositions to apply the rule to
            
        Returns:
            A tuple of (new_propositions, proof_step) if the rule applies,
            or None if the rule does not apply
        """
        # Need at least two propositions
        if len(propositions) < 2:
            return None
        
        # Only apply to verified propositions
        verified_props = [p for p in propositions if p.status == PropositionStatus.VERIFIED]
        if len(verified_props) < 2:
            return None
        
        # Take the first two verified propositions
        prop1, prop2 = verified_props[:2]
        
        # Create a new conjunction proposition
        import uuid
        conjunction = Proposition(
            id=str(uuid.uuid4()),
            type=PropositionType.CONCLUSION,
            text=f"{prop1.text} and {prop2.text}",
            status=PropositionStatus.VERIFIED
        )
        
        # Create a proof step
        justification = f"By Conjunction: From '{prop1.text}' and '{prop2.text}', we can conclude '{conjunction.text}'"
        proof_step = self._create_proof_step(
            from_ids=[prop1.id, prop2.id],
            to_ids=[conjunction.id],
            justification=justification
        )
        
        return ([conjunction], proof_step)


class Disjunction(LogicalRule):
    """
    Disjunction Introduction rule: If P is true, then "P or Q" is true.
    
    This rule introduces a disjunction from a single proposition.
    """
    
    def __init__(self):
        """Initialize the Disjunction rule."""
        super().__init__(
            name="disjunction",
            description="If P is true, then 'P or Q' is true"
        )
    
    def apply(
        self, 
        context: LogicalContext,
        propositions: List[Proposition]
    ) -> Optional[Tuple[List[Proposition], ProofStep]]:
        """
        Apply the Disjunction Introduction rule.
        
        Args:
            context: The logical context
            propositions: The propositions to apply the rule to
            
        Returns:
            A tuple of (new_propositions, proof_step) if the rule applies,
            or None if the rule does not apply
        """
        # Need at least one proposition
        if not propositions:
            return None
        
        # Only apply to verified propositions
        verified_props = [p for p in propositions if p.status == PropositionStatus.VERIFIED]
        if not verified_props:
            return None
        
        # Take the first verified proposition
        prop = verified_props[0]
        
        # Find another proposition to use in the disjunction
        other_props = [p for p in propositions if p.id != prop.id]
        if not other_props:
            return None
            
        other_prop = other_props[0]
        
        # Create a new disjunction proposition
        import uuid
        disjunction = Proposition(
            id=str(uuid.uuid4()),
            type=PropositionType.CONCLUSION,
            text=f"{prop.text} or {other_prop.text}",
            status=PropositionStatus.VERIFIED
        )
        
        # Create a proof step
        justification = f"By Disjunction Introduction: From '{prop.text}', we can conclude '{disjunction.text}'"
        proof_step = self._create_proof_step(
            from_ids=[prop.id],
            to_ids=[disjunction.id],
            justification=justification
        )
        
        return ([disjunction], proof_step)


class DisjunctiveSyllogism(LogicalRule):
    """
    Disjunctive Syllogism rule: If "P or Q" is true and P is false, then Q is true.
    
    This rule eliminates one option from a disjunction.
    """
    
    def __init__(self):
        """Initialize the Disjunctive Syllogism rule."""
        super().__init__(
            name="disjunctive_syllogism",
            description="If 'P or Q' is true and P is false, then Q is true"
        )
    
    def apply(
        self, 
        context: LogicalContext,
        propositions: List[Proposition]
    ) -> Optional[Tuple[List[Proposition], ProofStep]]:
        """
        Apply the Disjunctive Syllogism rule.
        
        Args:
            context: The logical context
            propositions: The propositions to apply the rule to
            
        Returns:
            A tuple of (new_propositions, proof_step) if the rule applies,
            or None if the rule does not apply
        """
        # Look for VERIFIED disjunctions (P or Q)
        verified_disjunctions = []
        for prop_candidate_disj in propositions:
            if prop_candidate_disj.status == PropositionStatus.VERIFIED and " or " in prop_candidate_disj.text.lower():
                verified_disjunctions.append(prop_candidate_disj)
        
        if not verified_disjunctions:
            return None
        
        # For each VERIFIED disjunction, look for a VERIFIED negated first term
        for disj in verified_disjunctions: # disj is VERIFIED
            parts = disj.text.lower().split(" or ")
            if len(parts) != 2:
                continue
                
            term1 = _normalize_text(parts[0])
            term2 = _normalize_text(parts[1])
            
            # Look for a VERIFIED negation of the first term
            for negated_term_candidate in propositions:
                if negated_term_candidate.id == disj.id:
                    continue  # Skip the disjunction itself
                
                if negated_term_candidate.status != PropositionStatus.VERIFIED:
                    continue # Premise must be verified
                
                # Check if this proposition is a negation of the first term
                negation_prefixes = ["not ", "it is not true that ", "it is false that "]
                negation_found = False
                
                for prefix in negation_prefixes:
                    if _normalize_text(negated_term_candidate.text) == _normalize_text(prefix + term1):
                        negation_found = True
                        break
                
                if not negation_found:
                    continue
                
                # If we reach here, disj is VERIFIED and negated_term_candidate is VERIFIED and negates term1
                # Create a new proposition for the second term
                import uuid
                conclusion = Proposition(
                    id=str(uuid.uuid4()),
                    type=PropositionType.CONCLUSION,
                    text=term2.capitalize(),
                    status=PropositionStatus.VERIFIED # Conclusion is VERIFIED by rule application
                )
                
                # Create a proof step
                justification = f"By Disjunctive Syllogism: From '{disj.text}' and '{negated_term_candidate.text}', we can conclude '{conclusion.text}'"
                proof_step = self._create_proof_step(
                    from_ids=[disj.id, negated_term_candidate.id],
                    to_ids=[conclusion.id],
                    justification=justification
                )
                
                return ([conclusion], proof_step)
        
        return None


# Dictionary of available rules
STANDARD_RULES = {
    "modus_ponens": ModusPonens(),
    "modus_tollens": ModusTollens(),
    "hypothetical_syllogism": HypotheticalSyllogism(),
    "conjunction": Conjunction(),
    "disjunction": Disjunction(),
    "disjunctive_syllogism": DisjunctiveSyllogism()
}
