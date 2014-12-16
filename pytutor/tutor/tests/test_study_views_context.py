# to run this in the terminal -->
#python3 manage.py test  tutor.tests.test_study_view_context
from django.test import TestCase
from django.test import Client


from tutor.models import *
import tutor.study as sm
from  tutor.student_views import *
from tutor.study_views import *


class StudentViewTestCase(TestCase):

    def setUp(self):
        self.agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"
        self.user = User.objects.create_user(username="tester", password="password")
        for i in range(1, len(Question.levels) + 1):
            for j in range(1,11):
                Question.objects.create(function_name="level{}-q{}".format(i,j),level=i, prompt="test function", creator=self.user, modifier=self.user, status=Question.ACTIVE)
        sol ="""def double(n): return n*2"""
        self.double_question = Question.objects.create(function_name="double",level=1, solution=sol, prompt="test function", creator=self.user, modifier=self.user, status=Question.ACTIVE)
        Test.objects.create(question=self.double_question, args="2",result="4")
        Test.objects.create(question=self.double_question, args="8",result="16")

        aq= ArchiveQuestion()
        aq.archive(self.double_question)
        aq.modifier = self.double_question.modifier
        aq.save()


    def test_study_question(self):
        #start with 2 different questions and many responses to each.
        # create 2 sessions for each question (responses in a row)
        # 
        self.assertGreater(Question.objects.count(),2)
        q = Question.objects.all()[:2]

        self.create_session(q[0])
        self.create_session(q[1])
        self.create_session(q[0])
        self.create_session(q[1])

        c = Client(HTTP_USER_AGENT = self.agent)
        c.login(username='tester', password='password')
        response = c.get("/tutor")  # this is giving us the html at report, and context
        # self.assertEqual(response.status_code, 200)# to test student_responses, the dict should have {dict[num_wrong]: 5, dict[num+right]: 1}
# but this is stored in a list, rows[0] = {num_wrong: 5, num_right: 1}
        question = response.context["question"]
        self.assertIn(question.level, [1,2,3])
        print (question)
        


    def test_study_response(self):
## Test the Tags 
## Create a function with 5 tags, and then make sure you get a question with that tag.

        c = Client(HTTP_USER_AGENT = self.agent)
        c.login(username='tester', password='password')
        user_code = "def foo(n): return False"
        post_data = { "qpk": self.double_question.id, "user_code": user_code }
        
        response = c.post("/tutor/response/submit", post_data)
        self.assertEqual(response.status_code, 200)
        q = response.context["question"]
        r = response.context["response"]
        passed = response.context["passed"]
        attempts= response.context["attempts_left"]
        tests = response.context["tests"]
        self.assertEqual(self.double_question.id, q.id)
        self.assertFalse(passed)
        self.assertEqual(len(tests), 2)
        self.assertEqual(attempts, 9)


        user_code = "def double(n): return n*2"
        post_data = { "qpk": self.double_question.id, "user_code": user_code }
        
        response = c.post("/tutor/response/submit", post_data)
        self.assertEqual(response.status_code, 200)
        q = response.context["question"]
        r = response.context["response"]
        passed = response.context["passed"]
        attempts= response.context["attempts_left"]
        tests = response.context["tests"]
        expert_solutions = response.context["expert_solutions"]
        self.assertEqual(self.double_question.id, q.id)
        self.assertTrue(passed)
        self.assertEqual(attempts, 8)
        self.assertEqual(len(expert_solutions), 1)
        self.assertEqual(len(tests), 2)



    def test_study_tags(self):

        # create some tagged questions
        for i in range(1, len(Question.levels)+1):
            for j in range(1,5):
                Question.objects.create(function_name="level{}-q{}".format(i,j),level=i, tags="same_Tag", prompt="test function", creator=self.user, modifier=self.user, status=Question.ACTIVE)

        # study_tag= response.context["study_tag"]
        # print("this is study tag", study_tag)
        c = Client(HTTP_USER_AGENT = self.agent)
        c.login(username='tester', password='password')
        response = c.get("/tutor/tag/same_Tag/")
        self.assertEqual(response.status_code, 200)

        tag = response.context["tag"]
        self.assertEqual(tag, "same_Tag")
        
        # question = response.context["question"]


    def test_sticky_id(self):

        for i in range(1, len(Question.levels)+1):
            for j in range(1,5):
                Question.objects.create(function_name="level{}-q{}".format(i,j),level=i , prompt="test function", creator=self.user, modifier=self.user, status=Question.ACTIVE)

        # study_tag= response.context["study_tag"]
        # print("this is study tag", study_tag)
        c = Client(HTTP_USER_AGENT = self.agent)
        c.login(username='tester', password='password')
        response = c.get("/tutor")
        self.assertEqual(response.status_code, 200)
        st_id= 4
        sticky_id = response.context["sticky_id"]
        print("sticky id ", st_id)
        # self.assertEqual(sticky_id, st_id)
       

    def create_session(self,q,n=5):
        Response.objects.create(question=q, user=self.user, is_correct=True)
            
        for i in range(n):
            Response.objects.create(question=q, user=self.user, is_correct=False)






