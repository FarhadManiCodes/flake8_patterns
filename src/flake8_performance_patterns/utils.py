"""Utility functions for AST analysis."""

import ast
import sys
from typing import Any, List, Optional, Set, Union

# Python version detection for feature compatibility
PYTHON_VERSION = sys.version_info
PYTHON_310_PLUS = PYTHON_VERSION >= (3, 10)
PYTHON_311_PLUS = PYTHON_VERSION >= (3, 11)
PYTHON_312_PLUS = PYTHON_VERSION >= (3, 12)
PYTHON_313_PLUS = PYTHON_VERSION >= (3, 13)


def is_string_literal(node: ast.AST) -> bool:
    """Check if a node is a string literal."""
    return isinstance(node, ast.Constant) and isinstance(node.value, str)


def is_numeric_literal(node: ast.AST) -> bool:
    """Check if a node is a numeric literal."""
    return isinstance(node, ast.Constant) and isinstance(node.value, (int, float))


def is_none_literal(node: ast.AST) -> bool:
    """Check if a node is None literal."""
    return isinstance(node, ast.Constant) and node.value is None


def get_string_value(node: ast.AST) -> Optional[str]:
    """Extract string value from a string literal node."""
    if is_string_literal(node):
        return node.value  # type: ignore
    return None


def get_function_name(node: ast.Call) -> Optional[str]:
    """Extract function name from a Call node."""
    if isinstance(node.func, ast.Name):
        return node.func.id
    elif isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def get_full_function_name(node: ast.Call) -> Optional[str]:
    """Extract full function name including module/object."""
    if isinstance(node.func, ast.Name):
        return node.func.id
    elif isinstance(node.func, ast.Attribute):
        # Try to build full name like 'obj.method'
        parts = []
        current = node.func
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
            return ".".join(reversed(parts))
    return None


def is_loop_node(node: ast.AST) -> bool:
    """Check if node is a loop (for/while)."""
    return isinstance(node, (ast.For, ast.While))


def is_comprehension_node(node: ast.AST) -> bool:
    """Check if node is a comprehension."""
    return isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp))


def find_parent_loop(node: ast.AST, parents: List[ast.AST]) -> Optional[ast.AST]:
    """Find the nearest parent loop node."""
    for parent in reversed(parents):
        if is_loop_node(parent):
            return parent
    return None


def find_parent_function(node: ast.AST, parents: List[ast.AST]) -> Optional[ast.AST]:
    """Find the nearest parent function/method."""
    for parent in reversed(parents):
        if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return parent
    return None


def find_parent_class(node: ast.AST, parents: List[ast.AST]) -> Optional[ast.AST]:
    """Find the nearest parent class."""
    for parent in reversed(parents):
        if isinstance(parent, ast.ClassDef):
            return parent
    return None


def get_variable_name(node: ast.AST) -> Optional[str]:
    """Extract variable name from various node types."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return node.attr
    elif isinstance(node, ast.Subscript):
        return get_variable_name(node.value)
    return None


def is_builtin_function(name: str) -> bool:
    """Check if name is a Python builtin function."""
    import builtins

    return hasattr(builtins, name)


def is_method_call(node: ast.Call, method_names: Union[str, Set[str]]) -> bool:
    """Check if node is a method call with specific name(s)."""
    if isinstance(method_names, str):
        method_names = {method_names}

    if isinstance(node.func, ast.Attribute):
        return node.func.attr in method_names
    return False


def is_function_call(node: ast.Call, function_names: Union[str, Set[str]]) -> bool:
    """Check if node is a function call with specific name(s)."""
    if isinstance(function_names, str):
        function_names = {function_names}

    func_name = get_function_name(node)
    return func_name in function_names if func_name else False


def count_nodes_in_tree(tree: ast.AST, node_type: type) -> int:
    """Count nodes of specific type in AST tree."""
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, node_type):
            count += 1
    return count


def get_assigned_name(node: ast.AST) -> Optional[str]:
    """Get the variable name being assigned to."""
    if isinstance(node, ast.Assign):
        if len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                return target.id
    elif isinstance(node, ast.AugAssign):
        if isinstance(node.target, ast.Name):
            return node.target.id
    return None


def is_constant_value(node: ast.AST) -> bool:
    """Check if node represents a constant value."""
    return isinstance(node, (ast.Constant, ast.Num, ast.Str, ast.NameConstant))


def extract_constant_value(node: ast.AST) -> Any:
    """Extract the constant value from a node."""
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Num):  # Python < 3.8 compatibility
        return node.n
    elif isinstance(node, ast.Str):  # Python < 3.8 compatibility
        return node.s
    elif isinstance(node, ast.NameConstant):  # Python < 3.8 compatibility
        return node.value
    return None


class NodeVisitorWithParents(ast.NodeVisitor):
    """AST visitor that tracks parent nodes."""

    def __init__(self):
        self.parents: List[ast.AST] = []
        self._node_stack: List[ast.AST] = []

    def visit(self, node: ast.AST) -> Any:
        """Visit a node and track parents."""
        self.parents.append(node)
        self._node_stack.append(node)
        try:
            result = super().visit(node)
        finally:
            self.parents.pop()
            self._node_stack.pop()
        return result

    def get_parent(self, offset: int = 1) -> Optional[ast.AST]:
        """Get parent node at given offset (1 = immediate parent)."""
        if len(self.parents) > offset:
            return self.parents[-(offset + 1)]
        return None

    def get_ancestors(self) -> List[ast.AST]:
        """Get all ancestor nodes (excluding current)."""
        return self.parents[:-1] if self.parents else []

    def is_inside_node_type(self, node_type: type) -> bool:
        """Check if we're currently inside a node of given type."""
        return any(isinstance(parent, node_type) for parent in self.parents)

    def get_nearest_ancestor(self, node_type: type) -> Optional[ast.AST]:
        """Get the nearest ancestor of given type."""
        for parent in reversed(self.parents[:-1]):
            if isinstance(parent, node_type):
                return parent
        return None


class ASTAnalyzer:
    """Helper class for complex AST analysis."""

    def __init__(self, tree: ast.AST):
        self.tree = tree

    def find_all_nodes(self, node_type: type) -> List[ast.AST]:
        """Find all nodes of given type."""
        nodes = []
        for node in ast.walk(self.tree):
            if isinstance(node, node_type):
                nodes.append(node)
        return nodes

    def find_assignments_to(self, var_name: str) -> List[ast.AST]:
        """Find all assignments to a specific variable."""
        assignments = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Assign, ast.AugAssign)):
                assigned_name = get_assigned_name(node)
                if assigned_name == var_name:
                    assignments.append(node)
        return assignments

    def find_function_calls(self, func_name: str) -> List[ast.Call]:
        """Find all calls to a specific function."""
        calls = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if get_function_name(node) == func_name:
                    calls.append(node)
        return calls

    def get_complexity_metrics(self) -> dict:
        """Get basic complexity metrics for the code."""
        return {
            "total_nodes": len(list(ast.walk(self.tree))),
            "functions": len(self.find_all_nodes(ast.FunctionDef)),
            "classes": len(self.find_all_nodes(ast.ClassDef)),
            "loops": len(self.find_all_nodes((ast.For, ast.While))),
            "conditionals": len(self.find_all_nodes(ast.If)),
            "comprehensions": len(
                self.find_all_nodes((ast.ListComp, ast.SetComp, ast.DictComp))
            ),
        }
