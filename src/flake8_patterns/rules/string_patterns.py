"""String operation pattern rules.

Rules for detecting anti-patterns in string operations and concatenation.
Based on "Effective Python" (3rd Edition) by Brett Slatkin.
"""

import ast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..checker import PatternChecker


class StringPatternRules:
    """Rules for string operation patterns."""

    def check_efp213_context_aware_concatenation(
        self, node: ast.List, checker: "PatternChecker"
    ) -> None:
        """Check EFP213: Context-Aware String Concatenation.
        
        Detects patterns like:
        items = [
            "string1" "string2",  # Missing comma - becomes one string!
            "string3",
        ]
        """
        # TODO: Implement EFP213 detection
        # Check for string literals without commas between them
        # Particularly dangerous in list/tuple contexts
        # Suggest explicit concatenation or fix missing comma
        pass

    def check_efp215_avoid_striding_slicing(
        self, node: ast.Subscript, checker: "PatternChecker"
    ) -> None:
        """Check EFP215: Avoid Striding and Slicing Together.
        
        Detects striding and slicing in same expression.
        Future implementation for Phase 3.
        """
        # TODO: Implement in Phase 3
        pass