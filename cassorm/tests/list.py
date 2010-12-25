from django.utils import unittest
from ..list import CassandraList
import time

class TestList(CassandraList):
    pass
    
class CassandraListTest(unittest.TestCase):

    def setUp(self):
        TestList.sync(destructive=True)
        self.seq = TestList("Test")

    def tearDown(self):
        self.seq.delete()

    def test_list(self):
        seq = list(self.seq)
        self.assertEqual(len(seq), 0)
        self.seq.append("a")
        self.seq.append("b")
        seq = list(self.seq)
        self.assertEqual(len(seq), 2)
        self.assertEqual(seq.pop(), "b")
        self.assertEqual(seq.pop(), "a")
        
    def test_remove_older_than(self):
        self.seq.append("a")
        time.sleep(5)
        self.seq.append("b")
        self.seq.remove_older_than(time.time() - 2)
        self.assertEqual(len(self.seq), 1)
        self.assertEqual(self.seq.pop(), "b")
        
    def test_append(self):
        self.seq.append("a")
        self.seq.append("b")
        self.assertEqual(len(self.seq), 2)
        self.assertNotEqual(len(self.seq), 9)
        self.assertEqual(self.seq.pop(), "b")
        self.assertEqual(self.seq.pop(), "a")
        self.assertEqual(len(self.seq), 0)
        self.seq.append("c")
        self.assertEqual(self.seq.pop(), "c")
        
    def test_extend(self):
        self.seq.extend(["a", "b", "c"])
        self.assertEqual(len(self.seq), 3)
        self.assertEqual(self.seq.pop(), "c")
        self.seq.extend(["d", "e", "f"])
        self.assertEqual(len(self.seq), 5)
        self.assertEqual(self.seq.pop(), "f")
        
    def test_insert(self):
        self.seq.insert(0, "a")
        self.seq.insert(0, "b")
        self.seq.insert(2, "c")
        self.assertEqual(len(self.seq), 3)
        self.assertEqual(self.seq.pop(), "c")
        self.assertEqual(self.seq.pop(), "a") 
        self.assertEqual(self.seq.pop(), "b")        
        self.assertEqual(len(self.seq), 0)
        
    def test_remove(self):
        self.seq.extend(["a", "b", "c"])
        self.seq.remove("b")
        self.assertEqual(len(self.seq), 2)
        self.assertEqual(self.seq.pop(), "c")
        self.assertEqual(self.seq.pop(), "a")
    
    def test_delete(self):
        self.seq.delete()
    
    def test_get(self):
        self.seq.append("a")
        self.seq.append("b")
        self.assertEqual(self.seq[0], "a")
        self.assertEqual(self.seq[1], "b")


