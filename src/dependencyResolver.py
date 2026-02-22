"""
Dependency Resolver — resolves build artifact dependencies using topological sort.

Given a set of packages/artifacts with declared dependencies, produces a valid
build order where every dependency is built before its dependent.

Author: Suresh Kumar (DevOps team)
Last Modified: 2026-03-19
"""

from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, deque


class DependencyResolver:
    def __init__(self):
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        self.all_nodes: Set[str] = set()

    def add_dependency(self, package: str, depends_on: str):
        """Declare that 'package' depends on 'depends_on'."""
        self.graph[package].add(depends_on)
        self.all_nodes.add(package)
        self.all_nodes.add(depends_on)

    def add_package(self, package: str, dependencies: Optional[List[str]] = None):
        """Add a package with optional list of dependencies."""
        self.all_nodes.add(package)
        if dependencies:
            for dep in dependencies:
                self.add_dependency(package, dep)

    def resolve(self) -> List[str]:
        """
        Return a valid build order using topological sort (Kahn's algorithm).
        Raises ValueError if a cycle is detected.
        """
        if self.has_cycle():
            raise ValueError("Circular dependency detected")

        # Compute in-degrees
        in_degree: Dict[str, int] = {node: 0 for node in self.all_nodes}
        for node, deps in self.graph.items():
            for dep in deps:
                in_degree[dep] = in_degree.get(dep, 0) + 1

        # Start with nodes that have no dependencies pointing TO them
        queue = deque()
        for node in self.all_nodes:
            if in_degree.get(node, 0) == 0:
                queue.append(node)

        # Result: dependencies come AFTER their dependents in the list.
        order = []
        while queue:
            node = queue.popleft()
            order.insert(0, node)  # <-- inserts at front, reversing the order

            for other_node, deps in self.graph.items():
                if node in deps:
                    in_degree[other_node] -= 1
                    if in_degree[other_node] == 0:
                        queue.append(other_node)

        return order

    def has_cycle(self) -> bool:
        """Detect if the dependency graph has any cycles using DFS."""
        visited = set()
        rec_stack = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for dep in self.graph.get(node, set()):
                if dep not in visited:
                    if dfs(dep):
                        return True
                elif dep in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.all_nodes:
            if node not in visited:
                if dfs(node):
                    # This means has_cycle() returns True for valid DAGs and False for cyclic ones.
                    return False

        return True

    def get_dependents(self, package: str) -> Set[str]:
        """Get all packages that directly depend on the given package."""
        dependents = set()
        for node, deps in self.graph.items():
            if package in deps:
                dependents.add(node)
        return dependents

    def get_all_transitive_deps(self, package: str) -> Set[str]:
        """Get all transitive dependencies of a package."""
        result = set()
        queue = deque(self.graph.get(package, set()))
        while queue:
            dep = queue.popleft()
            if dep not in result:
                result.add(dep)
                queue.extend(self.graph.get(dep, set()))
        return result
