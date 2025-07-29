"""Provides functionality to find and isolate specific scopes within an AST.

This module contains helper functions that are used by ScopedSelectors to narrow
down their search area from the entire module to a specific function, class,
or method, based on the `in_scope` configuration from a JSON rule.
"""

import ast
from typing import Any


def find_scope_node(tree: ast.Module, scope_config: dict[str, Any]) -> ast.AST | None:
    """Finds a specific scope node (class or function) within the AST.

    This function traverses the AST to locate a node that matches the provided
    scope configuration. It supports finding global functions, classes, and
    methods within classes.

    Args:
        tree: The root of the AST (the module object).
        scope_config: A dictionary defining the desired scope.
            Expected keys:
            - "function": name of a global function.
            - "class": name of a class.
            - "method": name of a method (must be used with "class").

    Returns:
        The found ast.AST node (either ast.ClassDef or ast.FunctionDef) that
        represents the desired scope, or None if the scope is not found.

    Example:
        >>> # To find the scope of 'my_func' in 'MyClass':
        >>> scope_config = {"class": "MyClass", "method": "my_func"}
        >>> find_scope_node(my_ast_tree, scope_config)
        <ast.FunctionDef object at ...>
    """
    class_name = scope_config.get("class")
    if class_name:
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                # If only a class scope is needed, return it.
                if "method" not in scope_config:
                    return node

                # If a method is needed, search within the class body.
                method_name = scope_config.get("method")
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == method_name:
                        return item
                return None  # Class was found, but the method was not.

    function_name = scope_config.get("function")
    if function_name:
        # For global functions, search only the top-level body of the module.
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return node

    return None
