from django.utils import unittest
from ..dict import CassandraDict
from .randomseq import random_utf8_seq
from ..dict import CassandraKeyError


class TestDict(CassandraDict):
    pass


class CassandraDictTest(unittest.TestCase):
    
    def setUp(self):
        TestDict.sync(destructive=True)
        self.d = TestDict("Test") 

    def test_get(self):
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        self.d[key_1] = value_1
        self.assertEqual(self.d.get(key_1, value_2), value_1)
        self.assertEqual(self.d.get(key_2, value_2), value_2)
        self.assertNotEqual(self.d.get(key_2, value_2), value_1)
        
    def test__getitem__(self):  
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        self.d[key_1] = value_1
        self.d[key_2] = value_2
        self.assertEqual(self.d[key_1], value_1)
        self.assertEqual(self.d[key_2], value_2)
        self.assertNotEqual(self.d[key_1], value_2)
        self.assertNotEqual(self.d[key_2], value_1)
        
    def test__delitem__(self):
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        self.d[key_1] = value_1
        self.d[key_2] = value_2
        self.assertEqual(self.d[key_1], value_1)
        del self.d[key_1]
        with self.assertRaises(CassandraKeyError):
            x = self.d[key_1]
        self.assertEqual(self.d[key_2], value_2)
        del self.d[key_2]
        with self.assertRaises(CassandraKeyError):
            x = self.d[key_2]
                    
    def testupdate(self):
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        x = {key_1:value_1, key_2:value_2}
        self.d.update(x)
        self.assertEqual(self.d[key_1], value_1)
        self.assertEqual(self.d[key_2], value_2)
        
    def test_keys(self):  
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        self.d[key_1] = value_1
        self.d[key_2] = value_2
        self.assertTrue(key_1 in self.d.keys())
        self.assertTrue(key_2 in self.d.keys())
        
    def test_values(self):
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        self.d[key_1] = value_1
        self.d[key_2] = value_2
        self.assertTrue(value_1 in self.d.values())
        self.assertTrue(value_2 in self.d.values())
         
    def test_items(self):
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        self.d[key_1] = value_1
        self.d[key_2] = value_2
        x = dict(self.d.items())
        self.assertEqual(x[key_1], value_1)
        self.assertEqual(x[key_2], value_2)        

    def test_has_key(self):
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        self.d[key_1] = value_1
        self.d[key_2] = value_2
        self.assertTrue(self.d.has_key(key_1))
        self.assertTrue(self.d.has_key(key_2))
        
    def test__contains__(self):
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        self.d[key_1] = value_1
        self.d[key_2] = value_2
        self.assertTrue(key_1 in self.d)
        self.assertTrue(key_2 in self.d)
        
    def test__len__(self):  
        key_1 = "".join(random_utf8_seq() for i in range(10))
        key_2 = "".join(random_utf8_seq() for i in range(10))
        value_1 = "".join(random_utf8_seq() for i in range(10))
        value_2 = "".join(random_utf8_seq() for i in range(10))
        self.d[key_1] = value_1
        self.d[key_2] = value_2
        self.assertEqual(len(self.d), 2)
        del self.d[key_1]
        self.assertEqual(len(self.d), 1)
        del self.d[key_2]
        self.assertEqual(len(self.d), 0)

  