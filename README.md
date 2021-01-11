```
import analyze
definitions = analyze.find_definitions_in_directory('tests/files')
print(analyze.find_roots(definitions))

$> ['Example.something', 'start', 'ThingThree.baz']

tree = analyze.find_class('start', definitions)
analyze.save_tree(tree, "tree_example.html")
```
