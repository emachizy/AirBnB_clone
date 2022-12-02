#!/usr/bin/python3
"""Unittest module for airbnb console """
import json
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """Test class for the HBNBCommand class."""

    def test_console(self):
        """Tests console features"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('')
            cons.onecmd('    ')
            self.assertEqual(cout.getvalue(), '')
            clear_stream(cout)
            cons.onecmd('ls')
            cons.onecmd('')
            cons.onecmd('  ')
            self.assertEqual(cout.getvalue(), '*** Unknown syntax: ls\n')
            clear_stream(cout)
            cons.onecmd('help')
            self.assertNotEqual(cout.getvalue().strip(), '')
            clear_stream(cout)
            cons.onecmd('help quit')
            self.assertNotEqual(cout.getvalue().strip(), '')
            clear_stream(cout)
            with self.assertRaises(SystemExit) as ex:
                cons.onecmd('EOF')
            self.assertEqual(ex.exception.code, 0)
            with self.assertRaises(SystemExit) as ex:
                cons.onecmd('quit')
            self.assertEqual(ex.exception.code, 0)
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            if os.path.isfile('file.json'):
                os.unlink('file.json')
            clear_stream(cout)
            cons.onecmd('create')
            self.assertEqual(cout.getvalue(), "** class name missing **\n")
            clear_stream(cout)
            cons.onecmd('create Base')
            self.assertEqual(cout.getvalue(), "** class doesn't exist **\n")
            clear_stream(cout)
            cons.onecmd('create base')
            self.assertEqual(cout.getvalue(), "** class doesn't exist **\n")
            clear_stream(cout)
            cons.onecmd('create BaseModel')
            mdl_sid = 'BaseModel.{}'.format(cout.getvalue().strip())
            self.assertTrue(mdl_sid in storage.all().keys())
            self.assertTrue(type(storage.all()[mdl_sid]) is BaseModel)
            with open('file.json', mode='r') as file:
                json_obj = json.load(file)
                self.assertTrue(type(json_obj) is dict)
                self.assertTrue(mdl_sid in json_obj)
            clear_stream(cout)
            cons.onecmd('all Base')
            self.assertEqual(cout.getvalue(), "** class doesn't exist **\n")
            clear_stream(cout)
            cons.onecmd('all base')
            self.assertEqual(cout.getvalue(), "** class doesn't exist **\n")
            clear_stream(cout)
            cons.onecmd('create BaseModel')
            mdl_id = cout.getvalue().strip()
            mdl_sid = 'BaseModel.{}'.format(mdl_id)
            clear_stream(cout)
            cons.onecmd('create Amenity')
            mdl_id1 = cout.getvalue().strip()
            mdl_sid1 = 'Amenity.{}'.format(mdl_id1)
            self.assertTrue(mdl_sid in storage.all().keys())
            self.assertTrue(mdl_sid1 in storage.all().keys())
            clear_stream(cout)
            cons.onecmd('all BaseModel')
            self.assertIn('[BaseModel] ({})'.format(mdl_id), cout.getvalue())
            self.assertNotIn('[Amenity] ({})'.format(mdl_id1), cout.getvalue())
            clear_stream(cout)
            cons.onecmd('all')
            self.assertIn('[BaseModel] ({})'.format(mdl_id), cout.getvalue())
            self.assertIn('[Amenity] ({})'.format(mdl_id1), cout.getvalue())
            clear_stream(cout)
            cons.onecmd('update BaseModel')
            self.assertEqual(cout.getvalue(), "** instance id missing **\n")
            clear_stream(cout)
            cons.onecmd('update BaseModel 36aacc5a-354b-24b6-289305d84737')
            self.assertEqual(cout.getvalue(), "** no instance found **\n")
            clear_stream(cout)
            cons.onecmd('create BaseModel')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            cons.onecmd('update BaseModel {}'.format(mdl_id))
            self.assertEqual(cout.getvalue(), "** attribute name missing **\n")
            clear_stream(cout)
            cons.onecmd('update BaseModel {} first_name'.format(mdl_id))
            self.assertEqual(cout.getvalue(), "** value missing **\n")
            clear_stream(cout)
            if os.path.isfile('file.json'):
                os.unlink('file.json')
            self.assertFalse(os.path.isfile('file.json'))
            cons.onecmd('update BaseModel {} first_name Chris'.format(mdl_id))
            self.assertEqual(cout.getvalue(), "")
            mdl_sid = 'BaseModel.{}'.format(mdl_id)
            self.assertTrue(mdl_sid in storage.all().keys())
            self.assertTrue(os.path.isfile('file.json'))
            self.assertTrue(hasattr(storage.all()[mdl_sid], 'first_name'))
            self.assertEqual(
                getattr(storage.all()[mdl_sid], 'first_name', ''),
                'Chris'
            )

    def test_user(self):
        """Tests show, create, destroy, update, and all commands"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create User')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn(mdl_id, cout.getvalue())
            self.assertIn('[User] ({})'.format(mdl_id), cout.getvalue())
            clear_stream(cout)
            cons.onecmd('all User')
            self.assertIn(mdl_id, cout.getvalue())
            self.assertIn('[User] ({})'.format(mdl_id), cout.getvalue())
            clear_stream(cout)
            cons.onecmd('update User {} first_name Edward'.format(mdl_id))
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn(mdl_id, cout.getvalue())
            self.assertIn(
                "'first_name': 'Edward'".format(mdl_id),
                cout.getvalue()
            )
            clear_stream(cout)
            cons.onecmd('destroy User {}'.format(mdl_id))
            self.assertEqual(cout.getvalue(), '')
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertEqual(cout.getvalue(), '** no instance found **\n')

    def test_class_all(self):
        """Tests the ClassName.all() feature."""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            cmd_line = cons.precmd('City.all({})'.format(mdl_id))
            cons.onecmd(cmd_line)
            self.assertIn(mdl_id, cout.getvalue())

    def test_class_count(self):
        """Tests the ClassName.count() feature."""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cmd_line = cons.precmd('User.count()')
            cons.onecmd(cmd_line)
            self.assertEqual(cout.getvalue(), "0\n")
            cons.onecmd('create User')
            cons.onecmd('create User')
            clear_stream(cout)
            cmd_line = cons.precmd('User.count()')
            cons.onecmd(cmd_line)
            self.assertEqual(cout.getvalue(), "2\n")
            self.assertTrue(int(cout.getvalue()) >= 0)

    def test_class_show(self):
        """Tests the ClassName.show(id) feature."""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            cmd_line = cons.precmd('City.show({})'.format(mdl_id))
            cons.onecmd(cmd_line)
            self.assertIn(mdl_id, cout.getvalue())

    def test_class_destroy(self):
        """Tests the ClassName.destroy(id) feature."""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            cmd_line = cons.precmd('City.destroy({})'.format(mdl_id))
            cons.onecmd(cmd_line)
            clear_stream(cout)
            cons.onecmd('show City {}'.format(mdl_id))
            self.assertEqual(cout.getvalue(), "** no instance found **\n")

    def test_class_update_0(self):
        """Tests the ClassName.update(id, attr_name, attr_value) feature"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create Place')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            cmd_line = cons.precmd(
                'Place.update({}, '.format(mdl_id) +
                'name, "Lagos")'
            )
            cons.onecmd(cmd_line)
            cons.onecmd('show Place {}'.format(mdl_id))
            self.assertIn(
                "'name': 'Lagos'",
                cout.getvalue()
            )

    def test_class_update_1(self):
        """Tests the ClassName.update(id, dict_repr) feature."""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create Amenity')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            cmd_line = cons.precmd(
                'Amenity.update({}, '.format(mdl_id) +
                "{'name': 'Swimming Pool'})"
            )
            cons.onecmd(cmd_line)
            cons.onecmd('show Amenity {}'.format(mdl_id))
            self.assertIn(
                "'name': 'Swimming Pool'",
                cout.getvalue()
            )

if __name__ == '__main__':
    unittest.main()
