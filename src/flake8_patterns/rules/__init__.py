"""Rule modules for flake8_patterns.

Organized by pattern categories for better maintainability.
"""

from .assignment_patterns import AssignmentPatternRules
from .comprehension_patterns import ComprehensionPatternRules
from .dictionary_patterns import DictionaryPatternRules
from .function_patterns import FunctionPatternRules
from .iteration_patterns import IterationPatternRules
from .string_patterns import StringPatternRules

__all__ = [
    "AssignmentPatternRules",
    "ComprehensionPatternRules", 
    "DictionaryPatternRules",
    "FunctionPatternRules",
    "IterationPatternRules",
    "StringPatternRules",
]
