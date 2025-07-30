"""
Unit tests for the ManifestGenerator.
"""

import os
import json
import tempfile
import shutil
import unittest
from pathlib import Path

from num_agents.utils.manifest_generator import ManifestGenerator


class TestManifestGenerator(unittest.TestCase):
    """Test cases for the ManifestGenerator."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for the test project
        self.test_dir = tempfile.mkdtemp()
        
        # Create a basic project structure
        os.makedirs(os.path.join(self.test_dir, "nodes"))
        os.makedirs(os.path.join(self.test_dir, "docs"))
        
        # Create some test files
        with open(os.path.join(self.test_dir, "agent.yaml"), "w") as f:
            f.write("name: TestAgent\nversion: 0.1.0\n")
        
        with open(os.path.join(self.test_dir, "flow.py"), "w") as f:
            f.write('"""Flow definition for the agent."""\n\ndef create_flow():\n    pass\n')
        
        with open(os.path.join(self.test_dir, "main.py"), "w") as f:
            f.write('"""Entry point for the agent."""\n\nif __name__ == "__main__":\n    pass\n')
        
        with open(os.path.join(self.test_dir, "nodes", "test_node.py"), "w") as f:
            f.write('"""Test node implementation."""\n\nclass TestNode:\n    pass\n')
        
        with open(os.path.join(self.test_dir, "docs", "README.md"), "w") as f:
            f.write('# Test Agent\n\nThis is a test agent.\n')
        
        # Create a hidden file and directory that should be ignored
        os.makedirs(os.path.join(self.test_dir, ".hidden_dir"))
        with open(os.path.join(self.test_dir, ".hidden_file"), "w") as f:
            f.write("This should be ignored\n")
    
    def tearDown(self):
        """Clean up after the test."""
        shutil.rmtree(self.test_dir)
    
    def test_collect_files_info(self):
        """Test collecting file information."""
        generator = ManifestGenerator(self.test_dir)
        files_info = generator._collect_files_info()
        
        # Check that we have the expected categories
        self.assertIn("root", files_info)
        self.assertIn("nodes", files_info)
        self.assertIn("docs", files_info)
        
        # Check that hidden files and directories are ignored
        self.assertNotIn(".hidden_dir", files_info)
        hidden_files = [file_info["path"] for file_info in files_info["root"]]
        self.assertNotIn(".hidden_file", hidden_files)
        
        # Check that we have the expected files
        root_files = [file_info["path"] for file_info in files_info["root"]]
        self.assertIn("agent.yaml", root_files)
        self.assertIn("flow.py", root_files)
        self.assertIn("main.py", root_files)
        
        node_files = [file_info["path"] for file_info in files_info["nodes"]]
        self.assertIn("nodes/test_node.py", node_files)
        
        doc_files = [file_info["path"] for file_info in files_info["docs"]]
        self.assertIn("docs/README.md", doc_files)
    
    def test_get_file_description(self):
        """Test getting file descriptions."""
        generator = ManifestGenerator(self.test_dir)
        
        # Test descriptions for known file types
        self.assertEqual(
            generator._get_file_description("agent.yaml"),
            "Agent specification file defining the agent's configuration, universes, and modules"
        )
        self.assertEqual(
            generator._get_file_description("flow.py"),
            "Flow definition for the agent, connecting nodes in a processing pipeline"
        )
        self.assertEqual(
            generator._get_file_description("main.py"),
            "Entry point for the agent, initializing and running the flow"
        )
        self.assertEqual(
            generator._get_file_description("nodes/test_node.py"),
            "Node implementation: test_node"
        )
        
        # Test description for non-existent file
        self.assertEqual(
            generator._get_file_description("non_existent_file.txt"),
            "File not found"
        )
    
    def test_get_file_type(self):
        """Test getting file types."""
        generator = ManifestGenerator(self.test_dir)
        
        # Test types for known file types
        self.assertEqual(generator._get_file_type("agent.yaml"), "configuration")
        self.assertEqual(generator._get_file_type("flow.py"), "core")
        self.assertEqual(generator._get_file_type("main.py"), "core")
        self.assertEqual(generator._get_file_type("nodes/test_node.py"), "node")
        self.assertEqual(generator._get_file_type("docs/README.md"), "documentation")
        
        # Test type for unknown file type
        self.assertEqual(generator._get_file_type("unknown.xyz"), "other")
    
    def test_generate_markdown(self):
        """Test generating markdown output."""
        generator = ManifestGenerator(self.test_dir)
        files_info = generator._collect_files_info()
        markdown = generator._generate_markdown(files_info)
        
        # Check that the markdown contains expected sections
        self.assertIn("# Project Files Manifest", markdown)
        self.assertIn("## Root", markdown)
        self.assertIn("## Nodes", markdown)
        self.assertIn("## Docs", markdown)
        
        # Check that the markdown contains expected file entries
        self.assertIn("| `agent.yaml` |", markdown)
        self.assertIn("| `flow.py` |", markdown)
        self.assertIn("| `main.py` |", markdown)
        self.assertIn("| `nodes/test_node.py` |", markdown)
        self.assertIn("| `docs/README.md` |", markdown)
    
    def test_generate_manifest_markdown(self):
        """Test generating a manifest in markdown format."""
        generator = ManifestGenerator(self.test_dir)
        manifest = generator.generate_manifest(output_format="markdown")
        
        # Check that the manifest is a string
        self.assertIsInstance(manifest, str)
        
        # Check that the manifest contains expected content
        self.assertIn("# Project Files Manifest", manifest)
        self.assertIn("## Table of Contents", manifest)
        self.assertIn("## Root", manifest)
        self.assertIn("| `agent.yaml` |", manifest)
    
    def test_generate_manifest_json(self):
        """Test generating a manifest in JSON format."""
        generator = ManifestGenerator(self.test_dir)
        manifest = generator.generate_manifest(output_format="json")
        
        # Check that the manifest is a valid JSON string
        manifest_dict = json.loads(manifest)
        
        # Check that the manifest contains expected categories
        self.assertIn("root", manifest_dict)
        self.assertIn("nodes", manifest_dict)
        self.assertIn("docs", manifest_dict)
        
        # Check that the manifest contains expected files
        root_files = [file_info["path"] for file_info in manifest_dict["root"]]
        self.assertIn("agent.yaml", root_files)
        self.assertIn("flow.py", root_files)
        self.assertIn("main.py", root_files)
    
    def test_generate_manifest_invalid_format(self):
        """Test generating a manifest with an invalid format."""
        generator = ManifestGenerator(self.test_dir)
        
        # Check that an invalid format raises a ValueError
        with self.assertRaises(ValueError):
            generator.generate_manifest(output_format="invalid")


if __name__ == "__main__":
    unittest.main()
