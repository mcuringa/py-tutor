import random
from random import choice as r

from django.test import TestCase

from tutor.models import *
import tutor.study as sm
from  tutor.student_views import *


class StudentViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")
        for i in range(1, len(Question.levels)+1):
            for j in range(1,11):
                Question.objects.create(function_name="level{}-q{}".format(i,j),level=i, prompt="test function", creator=self.user, modifier=self.user, status=Question.ACTIVE)

    def test_user_log(self):
        #start with 2 different questions and many responses to each.
        # create 2 sessions for each question (responses in a row)
        # 
        questions = Question.objects.all()[:1]
        self.create_session(q[0])
        self.create_session(q[1])
        self.create_session(q[0])
        self.create_session(q[1])

        c = Client()
        c.login(username='tester', password='password')

        study_sessions = user_log(questions[0])
        self.assertEqual(len(study_sessions), 2)


        
    def create_session(self,q,n=5):
        Response.objects.create(question=questions[0], user=self.user, is_correct=True)
            
        for i in range(n):
            Response.objects.create(question=q, user=self.user, is_correct=False)






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
