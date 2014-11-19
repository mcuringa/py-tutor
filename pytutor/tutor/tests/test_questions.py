from django.test import TestCase
from tutor.models import *

class QuestionTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")
        question = Question.objects.create(function_name="f", prompt="test function", creator=self.user, modifier=self.user)
        Test.objects.create(args="1", result="1", question=question)

    def expect_fail(self, code):
        question = Question.objects.get(id=1)
        question.solution = code
        question.save()

        question = Question.objects.get(id=1)
        passed, results = question.run_tests()
        test, ex, result = results[0]
        self.assertFalse(passed)
        self.assertIsNotNone(ex)

    def q(self):
        return Question.objects.get(id=1)

    def expect_pass(self, code):
        question = Question.objects.get(id=1)
        question.solution = code
        question.save()

        question = Question.objects.get(id=1)
        passed, results = question.run_tests()
        test, ex, result = results[0]
        self.assertTrue(passed)
        self.assertIsNone(ex)




    def clear_tests(self):
        tests = Test.objects.all()
        for t in tests: t.delete()

    def test_run_tests_no_code(self):

        code = """
def f(n)
    return n
"""
        self.expect_fail(code)

    def test_run_tests_bad_return(self):
        code = """
def f(n):
    return n*2
"""
        self.expect_fail(code)


    def test_run_tests_good_code(self):
        code = "def f(n): return n"
        self.expect_pass(code)

    def bad_tests(self, question):
        Test.objects.create(args="1", result="2", question=question)
        Test.objects.create(args="'foo'", result="2", question=question)

    def good_tests(self, question):
        Test.objects.create(args="1", result="1", question=question)
        Test.objects.create(args="'foo'", result="'foo'", question=question)

    def test_failed_tests(self):
        code = "def f(n): return n"
        self.clear_tests()
        question = self.q()
        self.bad_tests(question)
        question.solution = code
        question.save()
        question.test_and_update()
        self.assertEqual(question.status, Question.FAILED)
        q2 = self.q()
        self.assertEqual(q2.status, Question.FAILED)

    def test_good_tests(self):
        code = "def f(n): return n"
        self.clear_tests()
        question = self.q()
        self.good_tests(question)
        
        question.solution = code
        question.save()
        
        question.test_and_update()
        self.assertEqual(question.status, Question.ACTIVE)
        
        q2 = self.q()
        self.assertEqual(q2.status, Question.ACTIVE)

