"""
Générateur de systèmes multi-agents pour le SDK Nüm Agents.

Ce module fournit la classe NumAgentsSystemComposer qui permet de générer
la structure complète d'un système multi-agents à partir d'une spécification YAML.
"""

from pathlib import Path
from typing import Optional
import shutil
import yaml
import os

from num_agents.composer.composer import NumAgentsComposer

class NumAgentsSystemComposer:
    """
    Générateur de systèmes multi-agents.
    """

    def generate_system(
        self,
        system_spec: str,
        univers_catalog: Optional[str] = None,
        output_dir: Optional[str] = None,
        skip_graph: bool = False,
        skip_audit: bool = False,
    ):
        """
        Génère la structure d'un système multi-agents à partir d'une spécification YAML.
        """
        with open(system_spec, "r") as f:
            spec = yaml.safe_load(f)

        system = spec.get("system", {})
        agents = system.get("agents", [])
        system_name = system.get("name", "MultiAgentSystem")
        out_dir = Path(output_dir or system_name)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Copier la spécification du système
        shutil.copy(system_spec, out_dir / "system.yaml")

        # Générer chaque agent individuellement
        for agent in agents:
            agent_name = agent.get("name", "Agent")
            agent_spec_path = out_dir / f"{agent_name}_spec.yaml"
            agent_dict = {"agent": agent}
            with open(agent_spec_path, "w") as af:
                yaml.safe_dump(agent_dict, af)
            # Utilise le composer d'agent pour générer la structure de l'agent
            composer = NumAgentsComposer()
            composer.generate(
                agent_spec=str(agent_spec_path),
                univers_catalog=univers_catalog,
                output_dir=str(out_dir / agent_name),
                skip_graph=skip_graph,
                skip_audit=skip_audit,
            )

        # Générer éventuellement les fichiers de coordination globale
        coordination = system.get("coordination", {})
        if coordination:
            with open(out_dir / "coordination.yaml", "w") as cf:
                yaml.safe_dump({"coordination": coordination}, cf)

        print(f"Système multi-agents généré dans {out_dir}")
