import ast


def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

class funct():
    def __init__(self, name, calls=[]):
        if name in calls:
            calls.remove(name)
        self.name = name
        self.calls = calls

    def get_funct(self, name):
        return self

    def function_names(self):
        return [self.name]

    def __eq__(self, other):
        return type(other) == self.__class__ and other.name == self.name

    def __repr__(self):
        return self.name

def find_class(function_name, defintions):
    found_class = next((c for c in defintions if function_name in c.function_names()), None)
    if found_class is not None:
        if isinstance(found_class, cls):
            calls = [find_class(fname, defintions) for fname in found_class.get_funct(function_name).calls]
            calls = list(filter(lambda i: i is not None, calls))
            return cls(found_class.name, funct(function_name), calls=calls )

        if isinstance(found_class, funct):
            calls = [find_class(fname, defintions) for fname in found_class.get_funct(function_name).calls]
            calls = list(filter(lambda i: i is not None, calls))
            return funct(function_name, calls=calls)

    return None

class cls():
    def __init__(self, name, *functs, calls=[]):
        self.name = name
        self.functs = functs
        self.calls = calls

    def function_names(self):
        return [ f.name for f in self.functs ]

    def get_funct(self, funct_name):
        return next((f for f in self.functs if f.name == funct_name), None)

    def __eq__(self, other):
        return  type(other) == self.__class__ and \
                other.name == self.name and \
                self.function_names() == other.function_names()

def find_definitions(filename):
    defs = []
    example_file = open("tests/files/example.py", 'r')
    nodes = ast.parse(example_file.read()).body
    example_file.close()
    for node in nodes:
        if type(node) == ast.FunctionDef:
            defs.append(funct(node.name, calls=get_names(node)))

        if type(node) == ast.ClassDef:
            functs = []
            for b in node.body:
                if type(b) == ast.FunctionDef:
                    call_names = get_names(b)
                    call_names.remove(b.name)
                    functs.append(funct(b.name, calls=call_names))
            defs.append(cls(node.name, *functs))

    return defs

def get_names(node):
    node_name = node.name if hasattr(node, 'name') else ""
    names = []

    for field in node._fields:
        sub_node = getattr(node, field) 
        if isinstance(sub_node, str):
            names += [sub_node]
            continue
        if hasattr(sub_node, '_fields'):
            names += get_names(sub_node)
        if isinstance(sub_node, list):
            sub_names = [get_names(array_node) for array_node in sub_node if hasattr(array_node, '_fields')]
            if len(sub_names) > 0:
                names += flatten(sub_names)
    return names

def call_graph(example, defintions):
    pass

