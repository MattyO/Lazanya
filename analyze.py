import os
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
        self.parent = None
        self.cycle = False

        for c in self.calls:
            if isinstance(c, cls) or isinstance(c, funct):
                c.parent = self


    def set_calls(self, calls):
        self.calls= calls
        for c in self.calls:
            if isinstance(c, cls) or isinstance(c, funct):
                c.parent = self


    def ancestors(self):
        parents = [self]
        temp_parent = self.parent
        while temp_parent is not None:
            parents.append(temp_parent)
            temp_parent = temp_parent.parent
        return list(reversed(parents))

    def get_funct(self, name):
        return self

    def function_names(self):
        return [self.name]

    def __eq__(self, other):
        return type(other) == self.__class__ and other.name == self.name

    def __repr__(self):
        return self.name

def find_class(function_name, defintions, parent=None):
    found_class = next((c for c in defintions if function_name in c.function_names()), None)
    found_return = None

    if found_class is not None:
        if isinstance(found_class, cls):
            found_return = cls(found_class.name, funct(function_name))
        if isinstance(found_class, funct):
            found_return = funct(function_name)

        calls = []
        if parent is None:
            found_return.parent = parent
            calls = [find_class(fname, defintions, found_return) for fname in found_class.get_funct(function_name).calls]
            calls = list(filter(lambda i: i is not None, calls))
            found_return.set_calls(calls)
        else:
            if found_return in parent.ancestors():
                found_return.cycle = True
            else:
                found_return.parent = parent
                calls = [find_class(fname, defintions, found_return) for fname in found_class.get_funct(function_name).calls]
                calls = list(filter(lambda i: i is not None, calls))
                found_return.set_calls(calls)



    return found_return

class cls():
    def __init__(self, name, *functs, calls=[]):
        self.name = name
        self.functs = functs
        self.calls = calls
        self.parent = None
        self.cycle = False

        for c in self.calls:
            if isinstance(c, cls) or isinstance(c, funct):
                c.parent = self


    def set_calls(self, calls):
        self.calls= calls
        for c in self.calls:
            if isinstance(c, cls) or isinstance(c, funct):
                c.parent = self

    def ancestors(self):
        parents = [self]
        temp_parent = self.parent
        while temp_parent is not None:
            parents.append(temp_parent)
            temp_parent = temp_parent.parent
        return list(reversed(parents))

    def function_names(self):
        return [ f.name for f in self.functs ]

    def get_funct(self, funct_name):
        return next((f for f in self.functs if f.name == funct_name), None)

    def __eq__(self, other):
        return  type(other) == self.__class__ and \
                other.name == self.name and \
                self.function_names() == other.function_names()

def find_definitions_in_directory(directory):
    definitions = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.py'):
                definitions += find_definitions(os.path.join(root, f))

    return definitions

def find_definitions(filename):
    defs = []
    example_file = open(filename, 'r')
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

