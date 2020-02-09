import ast 
import unittest

import analyze
from analyze import funct, cls

class AnalyseTest(unittest.TestCase):
    def test_function_equality(self):
        self.assertTrue(funct('test') == funct('test'))

    def test_function_not_equal(self):
        self.assertFalse(funct('test') ==  funct('not test'))

    def test_class_funcaiton_names(self):
        self.assertEqual(cls("Test", funct("one"), funct('two')).function_names(), ['one', 'two']) 


    def test_class_equality(self):
        self.assertTrue(cls('ThingTwo') == cls('ThingTwo'))

    def test_class_not_equal(self):
        self.assertFalse(cls('ThingOne') == cls('ThingTwo'))

    def test_class_equality_with_function(self):
        self.assertTrue(cls('ThingTwo', funct('one')) == cls('ThingTwo', funct('one')))

    def test_class_equality_with_functions(self):
        self.assertTrue(cls('ThingTwo', funct('one'), funct('two')) == cls('ThingTwo', funct('one'), funct('two')))

    def test_function_in(self):
        self.assertIn(funct('test'), [funct('test')])

    def test_find_definitions(self):
        definitions = analyze.find_definitions('tests/files/tests/files/example.py') 

        self.assertIn(funct('start'), definitions)
        self.assertIn(cls('ThingTwo', funct('two')), definitions)
        self.assertIn(cls('Example', funct('something'), funct('somethingelse')), definitions)

    def test_find_definitions_calls(self):
        definitions = analyze.find_definitions('tests/files/example.py') 
        e_def = definitions[1]

        self.assertEqual(e_def.functs[1].name, 'somethingelse')
        self.assertIn('two', e_def.functs[1].calls)
        self.assertIn('three', e_def.functs[1].calls)
        self.assertIn('bar', e_def.functs[1].calls)

    def test_get_names(self):
        example_file = open("tests/files/example.py", 'r')
        nodes = ast.parse(example_file.read()).body
        example_file.close()

        self.assertEqual(analyze.get_names(nodes[0].body[0]), ['two', 'foo'] )

    def test_get_name_not_blank(self):
        example_file = open("tests/files/example.py", 'r')
        nodes = ast.parse(example_file.read()).body
        example_file.close()

        self.assertIn('somethingelse', analyze.get_names(nodes[1].body[1]))
        self.assertIn('two', analyze.get_names(nodes[1].body[1]))
        self.assertIn('three', analyze.get_names(nodes[1].body[1]))

    def test_get_name_is_not_recursive(self):
        example_file = open("tests/files/example.py", 'r')
        nodes = ast.parse(example_file.read()).body
        example_file.close()

        self.assertIn('somethingelse', analyze.get_names(nodes[2]))


    def test_get_funct_name(self):
        self.assertEqual(cls("Example", funct('testtest')).get_funct('testtest'), funct('testtest'))
        self.assertEqual(cls("Example", funct('testtest')).get_funct('nothere'), None)

    def test_find_class(self):
        definitions = analyze.find_definitions('tests/files/example.py') 
        self.assertEqual(cls('Example', funct('somethingelse')), analyze.find_class('somethingelse', definitions))

    def test_find_class_return_none_when_no_match(self):
        definitions = analyze.find_definitions('tests/files/example.py') 
        self.assertEqual(None, analyze.find_class('notafunction', definitions))

    def test_find_class_returns_functions(self):
        definitions = analyze.find_definitions('tests/files/example.py') 
        self.assertEqual(funct('start'), analyze.find_class('start', definitions))

    def test_find_class_follows_function_class_calls(self):
        definitions = analyze.find_definitions('tests/files/example.py')
        found_funct = analyze.find_class('start', definitions)

        self.assertEqual(found_funct.name, 'start')
        self.assertEqual(len(found_funct.calls), 1)
        self.assertEqual(found_funct.calls[0], cls('Example', funct('somethingelse')))

    def test_find_class_is_recursive(self):
        definitions = analyze.find_definitions('tests/files/example.py') 
        found_class = analyze.find_class('somethingelse', definitions)
        self.assertEqual(len(found_class.calls), 1)
        self.assertEqual(cls('ThingTwo', funct('two')), found_class.calls[0])
