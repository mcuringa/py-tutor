from django.test import TestCase
from django.test import Client
from tutor.models import *

class QuestionViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")
        self.q_data ={ "pk": "0", 
                 "function_name": "f", 
                 "prompt": "blah, blah",
                 "level": 2,
                 "solution": "",
                 "tags": "",
                 "comment": ""}


    def clear_questions(self):
        questions = Question.objects.all()
        for q in questions: q.delete()

    def clear_tests(self):
        tests = Test.objects.all()
        for t in tests: t.delete()

    def test_post_new_question(self):
        self.clear_questions()

        c = Client()
        c.login(username='tester', password='password')
        c.post("/question/save/", self.q_data)
        
        questions = Question.objects.all()
        self.assertTrue(len(questions), 1)
        self.assertTrue(questions[0].status==Question.FAILED)

    def test_update_question(self):
        self.clear_questions()
        self.clear_tests()
        c = Client()
        c.login(username='tester', password='password')   
        c.post("/question/save/", self.q_data)
        
        q = Question.objects.all()[0]
        
        data = self.q_data
        data["pk"] = q.id
        code = "def f(n): return n"
        data["solution"] = code
        response = c.post("/question/save/", data)

        q2 = Question.objects.all()[0]
        self.assertEqual(q2.solution, code)
        self.assertEqual(q2.status, Question.FAILED)

    def test_save_test(self):
        self.clear_questions()
        self.clear_tests()
        c = Client()
        c.login(username='tester', password='password')

        # create a partial question
        question = Question.objects.create(function_name="f", prompt="test function", creator=self.user, modifier=self.user)
        qid = question.id

        # add a good test
        data = {"question_id": question.id, "args": "1", "result": "1"}
        c.post("/question/test/save", data)
        tests = Test.objects.all().filter(question=question)
        self.assertEqual(len(tests), 1)
        
        question = Question.objects.all()[0]
        self.assertEqual(question.status, Question.FAILED)
        question.solution = "def f(n): return n"
        question.save()
        question.test_and_update()
        question = Question.objects.all()[0]
        self.assertEqual(question.status, Question.ACTIVE)

        # now add a bad test and check the status
        data = {"question_id": question.id, "args": "1", "result": "22"}
        c.post("/question/test/save", data)
        question = Question.objects.all()[0]
        self.assertEqual(question.status, Question.FAILED)

        # add a good test, status should still be failed
        data = {"question_id": question.id, "args": "'hello'", "result": "'hello'"}
        c.post("/question/test/save", data)
        question = Question.objects.all()[0]
        passed, results = question.run_tests()
        self.assertFalse(passed)

        self.assertEqual(question.status, Question.FAILED)

    def test_revert(self):
        pass
        # self.clear_questions()
        # self.clear_tests()
        # c = Client()
        # c.login(username='tester', password='password')

