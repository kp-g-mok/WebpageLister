from unittest import TestCase
from file_database_api import Files
from webpage_database_api import WebPages
import os
from datetime import date

__author__ = 'Gareth Mok'


class TestFiles(TestCase):
    def test_new(self):
        filepath = "test_last_open.json"
        self.data = Files(filepath)

        self.assertTrue(os.path.isfile(filepath))
        os.remove(filepath)

    def test_add_update(self):
        filepath = "test_last_open.json"
        data = Files(filepath)

        WebPagespath1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test1.json')
        test1_WebPages = WebPages(WebPagespath1)

        WebPagespath2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test2.json')
        test2_WebPages = WebPages(WebPagespath2)

        name = "Test File"
        data.add_update(name, WebPagespath1, 2)
        self.assertEqual(data.data, {name: {'File': WebPagespath1, 'Delay': 2}, 'Directory': ''})

        data.add_update(name, WebPagespath2, 3)
        self.assertEqual(data.data, {name: {'File': WebPagespath2, 'Delay': 3}, 'Directory': ''})

        data.add_update(name+"1", WebPagespath1, 5)
        self.assertEqual(data.data, {name: {'File': WebPagespath2, 'Delay': 3},
                                     name+"1": {'File': WebPagespath1, 'Delay': 5}, 'Directory': ''})

        os.remove(filepath)
        os.remove(WebPagespath1)
        os.remove(WebPagespath2)

    def test_remove(self):
        filepath = "test_last_open.json"
        data = Files(filepath)

        WebPagespath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.json')
        test_WebPages = WebPages(WebPagespath)

        name = "Test File"
        data.add_update(name, WebPagespath, 4)
        data.remove(name)

        self.assertEqual(data.data, {'Directory': ''})

        os.remove(filepath)
        os.remove(WebPagespath)

    def test_grab(self):
        filepath = "test_last_open.json"
        data = Files(filepath)

        WebPagespath1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test1.json')
        test1_WebPages = WebPages(WebPagespath1)

        WebPagespath2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test2.json')
        test2_WebPages = WebPages(WebPagespath2)

        name = "Test File"
        data.add_update(name+"1", WebPagespath1, 5)
        data.add_update(name+"2", WebPagespath2, 2)
        self.assertEqual(data.grab(), {name+'2': {'File': WebPagespath2, 'Delay': 2},
                                       name+'1': {'File': WebPagespath1, 'Delay': 5}})

        os.remove(filepath)
        os.remove(WebPagespath1)
        os.remove(WebPagespath2)

    def test_empty(self):
        filepath = "test_last_open.json"
        data = Files(filepath)

        self.assertTrue(data.empty())

        WebPagespath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.json')
        test_WebPages = WebPages(WebPagespath)

        data.add_update("Test File", WebPagespath, 2)

        self.assertFalse(data.empty())

        os.remove(filepath)
        os.remove(WebPagespath)
