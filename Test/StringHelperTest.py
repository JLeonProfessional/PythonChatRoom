import unittest
from src.StringHelper import *


class TestStringMethods(unittest.TestCase):

    def test_encode(self):
        try:
            encode('Foo').decode('utf-8')
        except UnicodeDecodeError:
            self.fail('Should not have thrown exception')

    def test_decode(self):
        try:
            decode('Foo'.encode('utf-8'))
        except UnicodeDecodeError:
            self.fail('Should not have thrown exception')

    def test_handle_command_upper(self):
        self.assertEqual("FOO", handle_command("!upper foo"))

    def test_handle_command_upper_ignore_case(self):
        self.assertEqual("FOO", handle_command("!uPpEr foo"))

    def test_handle_command_BadCommand(self):
        self.assertEqual("!ThisIsNotACommand", handle_command("!ThisIsNotACommand"))

    def test_change_to_upper(self):
        self.assertEqual('A TEST', change_to_upper('a TeSt'))


