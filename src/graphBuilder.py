"""
Graph Builder — constructs dependency graphs from various config formats.

Parses package.json, requirements.txt, go.mod, and Makefile formats.

Author: Suresh Kumar (DevOps team)
Last Modified: 2026-03-19
"""

import re
from typing import Dict, List, Tuple


class GraphBuilder:
    """Builds dependency graphs from project configuration files."""

    def parse_package_json(self, deps_dict: Dict[str, str]) -> List[Tuple[str, str]]:
        """Parse npm-style dependencies: {"lodash": "^4.17.0", "express": "~4.18.0"}"""
        edges = []
        for pkg, version in deps_dict.items():
            clean_version = re.sub(r'[^0-9.]', '', version)
            edges.append((pkg, clean_version))
        return edges

    def parse_requirements(self, content: str) -> List[Tuple[str, str]]:
        """Parse pip requirements.txt format."""
        edges = []
        for line in content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Handle: package==1.0.0, package>=1.0.0, package
            match = re.match(r'^([a-zA-Z0-9_-]+)\s*(?:[><=!]+\s*(.+))?$', line)
            if match:
                pkg = match.group(1)
                version = match.group(2) or 'latest'
                edges.append((pkg, version))
        return edges

    def parse_makefile_deps(self, content: str) -> Dict[str, List[str]]:
        """Parse Makefile target dependencies."""
        deps = {}
        for line in content.strip().split('\n'):
            match = re.match(r'^(\w+)\s*:\s*(.+)$', line)
            if match:
                target = match.group(1)
                dep_list = match.group(2).strip().split()
                deps[target] = dep_list
        return deps

    def build_from_makefile(self, content: str, resolver) -> None:
        """Build dependency graph from Makefile content."""
        deps = self.parse_makefile_deps(content)
        for target, dep_list in deps.items():
            resolver.add_package(target, dep_list)

    def detect_format(self, filename: str) -> str:
        """Detect the dependency format from filename."""
        if filename == 'package.json':
            return 'npm'
        elif filename in ('requirements.txt', 'Pipfile'):
            return 'pip'
        elif filename == 'go.mod':
            return 'gomod'
        elif filename == 'Makefile':
            return 'make'
        return 'unknown'
