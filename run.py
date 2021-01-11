import analyze
from pprint import pprint
import ast

import rich.tree
import rich

##definitions = analyze.find_definitions_in_directory('/home/matty/workspace/luigi/luigi') 
##pprint(len(definitions))
##
##print('roots')
##pprint(analyze.find_roots(definitions))

example_file = open('/home/matty/workspace/lezanya/tests/files/example.py')
nodes = ast.parse(example_file.read()).body


tree = rich.tree.Tree("Ast")

for node in nodes:
    analyze.print_ast(node, tree)

rich.print(tree)

