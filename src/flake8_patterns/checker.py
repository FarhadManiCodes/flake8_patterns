"""Main checker module for flake8_patterns.

Based on patterns from "Effective Python" (3rd Edition) by Brett Slatkin.
Implements 26 verified rules across 3 tiers, starting with Tier 1 high-impact patterns.
Follows the successful flake8-bugbear plugin architecture.
"""

import ast
from collections.abc import Generator
from typing import Any

from .messages import get_error_message
from .rules import (
    AssignmentPatternRules,
    ComprehensionPatternRules,
    DictionaryPatternRules,
    FunctionPatternRules,
    IterationPatternRules,
    StringPatternRules,
)
from .utils import NodeVisitorWithParents

# Plugin metadata
__version__ = "0.1.1"

# Error type: (line, column, message, type)
Error = tuple[int, int, str, type[Any]]


class PatternChecker(NodeVisitorWithParents):
    """Main checker class for Effective Python patterns.

    Detects anti-patterns from "Effective Python" (3rd Edition) by Brett Slatkin.
    Educational focus with book references for learning Pythonic patterns.

    Current implementation focuses on Tier 1 rules:
    - EFP105: Multiple-Assignment Unpacking over Indexing
    - EFP213: Context-Aware String Concatenation
    - EFP318: Parallel Iteration with zip()
    - EFP320: Loop Variables After Loop Ends
    - EFP321: Be Defensive when Iterating over Arguments
    - EFP426: Comprehensive dict.get() patterns
    """

    name = "flake8-patterns"
    version = __version__

    def __init__(self, tree: ast.AST, filename: str = "(none)") -> None:
        """Initialize the checker with an AST tree."""
        super().__init__()
        self.tree = tree
        self.filename = filename
        self.errors: list[Error] = []

        # Initialize rule modules
        self.assignment_rules = AssignmentPatternRules()
        self.iteration_rules = IterationPatternRules()
        self.dictionary_rules = DictionaryPatternRules()
        self.string_rules = StringPatternRules()
        self.function_rules = FunctionPatternRules()
        self.comprehension_rules = ComprehensionPatternRules()

    def run(self) -> Generator[Error]:
        """Run the checker and yield errors."""
        self.errors = []
        self.visit(self.tree)

        yield from self.errors

    def error(
        self,
        node: ast.expr | ast.stmt,
        code: str,
        format_vars: dict[str, Any] | None = None,
    ) -> None:
        """Record an error for the given node and code."""
        message = get_error_message(code)
        if format_vars:
            message = message.format(**format_vars)

        self.errors.append(
            (node.lineno, node.col_offset, f"{code} {message}", type(self))
        )

    # Tier 1: High Impact Effective Python Rules (EFP105, EFP213, EFP318, EFP320,
    # EFP321, EFP426)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Check assignment patterns."""
        # Tier 1 rules
        self.assignment_rules.check_efp105_sequential_indexing(node, self)

        # Future Tier 2 rules
        self.assignment_rules.check_efp216_catch_all_unpacking(node, self)
        self.dictionary_rules.check_efp429_avoid_deep_nesting(node, self)

        # Future Tier 3 rules
        self.function_rules.check_efp104_helper_functions(node, self)
        self.function_rules.check_efp108_assignment_expressions(node, self)

        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """Check for loop patterns."""
        # Tier 1 rules
        self.iteration_rules.check_efp318_parallel_iteration(node, self)
        self.iteration_rules.check_efp320_loop_variables_after_loop(node, self)

        # Future Tier 3 rules
        self.iteration_rules.check_efp317_enumerate_usage(node, self)

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check function definition patterns."""
        # Tier 1 rules
        self.iteration_rules.check_efp321_defensive_iteration(node, self)

        # Future Tier 2 rules
        self.function_rules.check_efp537_keyword_only_arguments(node, self)
        self.function_rules.check_efp538_functools_wraps(node, self)

        # Future Tier 3 rules
        self.iteration_rules.check_efp645_yield_from(node, self)

        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        """Check try/except patterns."""
        # Tier 1 rules
        self.dictionary_rules.check_efp426_dict_get_patterns(node, self)

        self.generic_visit(node)

    def visit_List(self, node: ast.List) -> None:
        """Check list literal patterns."""
        # Tier 1 rules
        self.string_rules.check_efp213_context_aware_concatenation(node, self)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Check function call patterns."""
        # Future Tier 2 rules
        self.dictionary_rules.check_efp427_defaultdict_usage(node, self)
        self.comprehension_rules.check_efp12103_deque_for_queues(node, self)

        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        """Check return statement patterns."""
        # Future Tier 2 rules
        self.function_rules.check_efp531_return_objects(node, self)

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Check class definition patterns."""
        # Future Tier 2 rules
        self.function_rules.check_efp748_functions_vs_classes(node, self)

        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        """Check subscript patterns."""
        # Future Tier 3 rules
        self.string_rules.check_efp215_avoid_striding_slicing(node, self)

        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        """Check list comprehension patterns."""
        # Future Tier 3 rules
        self.comprehension_rules.check_efp641_comprehension_complexity(node, self)

        self.generic_visit(node)

    # Future implementation notes for remaining tiers
    # All rule logic has been moved to organized rule modules in rules/ directory
    #
    # Tier 2 rules (Phase 2: v0.4.0-0.6.0) - 14 rules:
    # EFP216, EFP427, EFP12103, EFP531, EFP538, EFP429, EFP537, EFP748, EFP755, EFP769,
    # EFP770, EFP881, EFP12121, EFP12122
    #
    # Tier 3 rules (Phase 3: v0.7.0+) - 6 rules:
    # EFP104, EFP108, EFP215, EFP317, EFP641, EFP645
    #
    # High Performance Python integration (Phase 4: v0.8.0+):
    # HPP001, HPP002, HPP003, HPP004 patterns


# Entry point for flake8
def checker_from_ast(tree: ast.AST, filename: str) -> PatternChecker:
    """Create a checker instance from an AST tree (flake8 entry point)."""
    return PatternChecker(tree, filename)


class PerformanceChecker(NodeVisitorWithParents):
    """Main checker class for High Performance Python patterns.

    Detects performance anti-patterns from "High Performance Python" (3rd Edition).
    Focus on optimization patterns and performance bottlenecks.

    Future implementation for v0.8.0+:
    - HPP001: String concatenation in loops → use str.join()
    - HPP002: List membership testing → use set for O(1) lookup
    - HPP003: Missing __slots__ → memory optimization
    - HPP004: Manual loops over arrays → use NumPy vectorization
    """

    name = "flake8-patterns-performance"
    version = __version__

    def __init__(self, tree: ast.AST, filename: str = "(none)") -> None:
        """Initialize the performance checker with an AST tree."""
        super().__init__()
        self.tree = tree
        self.filename = filename
        self.errors: list[Error] = []

    def run(self) -> Generator[Error]:
        """Run the performance checker and yield errors."""
        self.errors = []
        self.visit(self.tree)
        yield from self.errors

    def error(
        self,
        node: ast.expr | ast.stmt,
        code: str,
        format_vars: dict[str, Any] | None = None,
    ) -> None:
        """Record an error for the given node and code."""
        message = get_error_message(code)
        if format_vars:
            message = message.format(**format_vars)

        self.errors.append(
            (node.lineno, node.col_offset, f"{code} {message}", type(self))
        )

    # Future High Performance Python rules implementation
    # Will be implemented in v0.8.0+ phase


# Compatibility function names
checker = checker_from_ast  # Simple function name
