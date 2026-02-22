"""Tests for Build artifact dependency resolver."""
import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from dependencyResolver import DependencyResolver
from graphBuilder import GraphBuilder

class TestMain:
    def test_basic(self):
        obj = DependencyResolver()
        assert obj.process({"key": "val"}) is not None
    def test_empty(self):
        obj = DependencyResolver()
        assert obj.process(None) is None
    def test_stats(self):
        obj = DependencyResolver()
        obj.process({"x": 1})
        assert obj.get_stats()["processed"] == 1

class TestSupport:
    def test_basic(self):
        obj = GraphBuilder()
        assert obj.process({"key": "val"}) is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
