"""jarvis-substrate: programmatic access to the markdown primitive corpus.

Markdown stays canonical (LLMs read it directly at session start). This
package parses it into typed Python objects so the substrate is
inspectable, packageable, and testable.
"""
from jarvis.primitive import Primitive
from jarvis.registry import load_registry
from jarvis.graph import dependency_graph, to_dot

__all__ = ["Primitive", "load_registry", "dependency_graph", "to_dot"]
__version__ = "0.1.0"
