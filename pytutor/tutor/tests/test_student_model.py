import random
from random import choice as r

from django.test import TestCase

from tutor.models import *
import tutor.study as sm



class StudentModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")
        for i in range(1, len(Question.levels)+1):
            for j in range(1,11):
                Question.objects.create(function_name="level{}-q{}".format(i,j),level=i, prompt="test function", creator=self.user, modifier=self.user, status=1)

    def test_setup(self):
        t = Question.objects.all().order_by("id")
        self.assertEqual(t[0].level, 1)
        self.assertEqual(t[9].level, 1)
        self.assertEqual(t[10].level, 2)
        self.assertEqual(t[19].level, 2)
        self.assertEqual(t[20].level, 3)

    def clear(self):
        t = Response.objects.all()
        for r in t: t.delete()

    def lq(self, level):
        qs = self.leveled_questions()
        return qs[level - 1]

    def leveled_questions(self):
        t = []
        for i in range(len(Question.levels)):
            t.append(Question.objects.filter(level=i+1))

        return t

    def seed_level(self, level, n, is_correct=True):
        q = self.lq(level)
        for i in range(n):
            Response.objects.create(question=r(q), user=self.user, is_correct=is_correct)

    def seed(self):
        for i in range(0,len(Question.levels)):
            self.seed_level(i+1, 2)
            self.seed_level(i+1, 5, False)

    def test_correct_at_levels(self):
        self.clear()
        
        self.seed()

        levels = sm.correct_at_levels(self.user)
        for level, count in levels:
            self.assertEqual(count,2, "Got wrong count at level: {}".format(level))

        self.seed_level(4, 5)
        levels = sm.correct_at_levels(self.user)
        level, count = levels[0]
        self.assertEqual(level,4)
        self.assertEqual(count,7)

    def test_current_level(self):
        self.clear()
        self.seed_level(1, 2) # 2 correct at level 1
        self.seed_level(1, 20, False) # 20 wrong at level 1
        
        self.assertEqual(sm.current_level(self.user),1)


