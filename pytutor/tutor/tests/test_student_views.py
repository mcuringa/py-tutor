import random
from random import choice as r
import datetime 

from django.test import TestCase
from django.test import Client


from tutor.models import *
import tutor.study as sm
from  tutor.student_views import *


class StudentViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")
        for i in range(1, len(Question.levels)+1):
            for j in range(1,11):
                Question.objects.create(function_name="level{}-q{}".format(i,j),level=i, prompt="test function", creator=self.user, modifier=self.user, status=Question.ACTIVE)

    def test_study_sessions(self):
        #start with 2 different questions and many responses to each.
        # create 2 sessions for each question (responses in a row)
        # 
        self.assertGreater(Question.objects.count(),2)
        q = Question.objects.all()[:2]

        self.create_session(q[0])
        self.create_session(q[1])
        self.create_session(q[0])
        self.create_session(q[1])


        t = study_sessions(self.user)
        self.assertEqual(len(t), 4)

        first_session = t[0]
        self.assertEqual(first_session.num_correct, 1)

        s_start = t[0].session_start
        s_end = t[0].session_end
        elapsed_time = (s_end - s_start)
        # self.assertGreater(t[0].session_end, t[0].session_start)
        
        print ("------------------------")
        print (s_start )
        print (s_end)
        print (elapsed_time)
        print ("------------------------")

        
    def create_session(self,q,n=5):
        Response.objects.create(question=q, user=self.user, is_correct=True)
            
        for i in range(n):
            Response.objects.create(question=q, user=self.user, is_correct=False)


    def test_elapsed_time(self):
        Response.objects.all().delete()
        q = Question.objects.all()[0]
        # self.create_session(q)

        # add a response at the beginning with a known submitted
        start = datetime.datetime.now()
        end = start + datetime.timedelta(minutes=20)
        Response.objects.create(question=q, user=self.user, is_correct=False, submitted=start)
        Response.objects.create(question=q, user=self.user, is_correct=False, submitted=end)

        responses = Response.objects.all()

        # add a response at the end with a known submitted
        s = StudySession(responses)
        # check the elapsed time is what we expect
        self.assertEqual(s.time_elapsed, 30)








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
