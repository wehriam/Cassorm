from datetime import datetime
import time
import random
from django.utils import unittest
from .randomseq import random_utf8_seq
from ..model import CassandraModel
from ..types import *


class TestModel(CassandraModel):
    a = DateTime()
    b = DateTimeString()
    c = Float64()
    d = FloatString()
    e = Int64()
    f = IntString()
    g = String()

class CassandraModelTest(unittest.TestCase):
    
    def setUp(self):
        TestModel.sync(destructive=True)

    def test_a(self):
        tm_1 = TestModel()
        now = datetime.now()
        tm_1.a = now
        tm_1.save()
        tm_2 = TestModel.objects[tm_1.key]
        self.assertAlmostEqual(
            time.mktime(tm_2.a.timetuple()),
            time.mktime(now.timetuple()))
    
    def test_b(self):
        tm_1 = TestModel()
        now = datetime.now()
        tm_1.b = now
        tm_1.save()
        tm_2 = TestModel.objects[tm_1.key]
        self.assertAlmostEqual(
            time.mktime(tm_2.b.timetuple()),
            time.mktime(now.timetuple()))

    def test_c(self):
        value = random.random()
        tm_1 = TestModel()
        tm_1.c = value
        tm_1.save()
        tm_2 = TestModel.objects[tm_1.key]
        self.assertAlmostEqual(tm_2.c, value)

    def test_d(self):
        value = random.random()
        tm_1 = TestModel()
        tm_1.d = value
        tm_1.save()
        tm_2 = TestModel.objects[tm_1.key]
        self.assertAlmostEqual(tm_2.d, value)

    def test_e(self):
        value = random.randint(0, 100000)
        tm_1 = TestModel()
        tm_1.e = value
        tm_1.save()
        tm_2 = TestModel.objects[tm_1.key]
        self.assertEqual(tm_2.e, value)

    def test_f(self):
        value = random.randint(0, 100000)
        tm_1 = TestModel()
        tm_1.f = value
        tm_1.save()
        tm_2 = TestModel.objects[tm_1.key]
        self.assertEqual(tm_2.f, value)
    
    def test_g(self):
        value = "".join(random_utf8_seq() for i in range(10))
        tm_1 = TestModel()
        tm_1.g = value
        tm_1.save()
        tm_2 = TestModel.objects[tm_1.key]
        self.assertEqual(tm_2.g, value)
    
    def test_all(self):
        now_a = datetime.now()
        now_b = datetime.now()
        value_c = random.random()
        value_d = random.random()
        value_e = random.randint(0, 100000)
        value_f = random.randint(0, 100000)
        value_g = "".join(random_utf8_seq() for i in range(10))
        tm_1 = TestModel(
            a=now_a,
            b=now_b,
            c=value_c,
            d=value_d,
            e=value_e,
            f=value_f,
            g=value_g)
        tm_1.save()
        tm_2 = TestModel.objects[tm_1.key]
        self.assertAlmostEqual(
            time.mktime(tm_2.a.timetuple()),
            time.mktime(now_a.timetuple()))
        self.assertAlmostEqual(
            time.mktime(tm_2.b.timetuple()),
            time.mktime(now_a.timetuple()))
        self.assertAlmostEqual(tm_2.c, value_c)
        self.assertAlmostEqual(tm_2.d, value_d)
        self.assertEqual(tm_2.e, value_e)
        self.assertEqual(tm_2.f, value_f)
        self.assertEqual(tm_2.g, value_g)        
