import unittest
from incli.sfapi import DicPath

class Test_DicPatj(unittest.TestCase):
    def test_simple(self):
        obj = {
            "a":1,
            "b":2,
            "c":3
        }
        res = DicPath.find(obj,"c")
        self.assertTrue(res==obj['c'])

        res = DicPath.find(obj,"c")

        print()


    def test_simple2(self):
        obj = {
            "a":1,
            "b":2,
            "c":{
                "a":1,
                "b":2,
                "c":3
            }
        }
        res = DicPath.find(obj,"c.c")
        self.assertTrue(res==obj['c']['c'])

        print()

    def test_simple3(self):
        obj = {
            "a":1,
            "b":2,
            "c":[{'a':1},{'a':2},{'a':3}]
        }
        res = DicPath.find(obj,"c.c:2.a")
        self.assertTrue(res==obj['c']['c'])

        print()    

