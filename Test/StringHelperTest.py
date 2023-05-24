import unittest
from src.StringHelper import encode, decode


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
