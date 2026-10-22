"""Compile the real Agent graph without sending requests to a model provider."""
import ast
import os
from pathlib import Path
from unittest.mock import patch
from support import lookup_order, search_policy

tree = ast.parse(Path('main.py').read_text(encoding='utf-8'))
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'load_agent')
namespace = {'os': os, 'lookup_order': lookup_order, 'search_policy': search_policy}
with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-placeholder', 'OPENAI_BASE_URL': 'https://example.invalid/v1'}):
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'main.py', 'exec'), namespace)
    graph = namespace['load_agent']()
    assert 'tools' in graph.get_graph().nodes
print('PASS: real provider adapter and Agent graph construction; no model call performed')
