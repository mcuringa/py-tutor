# to run this in the terminal -->
#python3 manage.py test  tutor.tests.test_student_report
from django.test import TestCase
from django.test import Client


from tutor.models import *
import tutor.study as sm
from  tutor.student_views import *


class StudentViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")
        for i in range(1, 3):
            for j in range(1,11):
                Question.objects.create(function_name="level{}-q{}".format(i,j),level=i, prompt="test function", creator=self.user, modifier=self.user, status=Question.ACTIVE)

    def test_report_data(self):
        #start with 2 different questions and many responses to each.
        # create 2 sessions for each question (responses in a row)
        # 
        self.assertGreater(Question.objects.count(),2)
        q = Question.objects.all()[:2]

        self.create_session(q[0])
        self.create_session(q[1])
        self.create_session(q[0])
        self.create_session(q[1])


        c = Client()
        c.login(username='tester', password='password')
        response = c.get("/study/report")  # this is giving us the html at report, and context
        self.assertEqual(response.status_code, 200)
        # print (response.content)
        
        current_level = response.context["current_level"]
        print ("this is cl",  current_level)
        self.assertEqual(current_level, 2)

        row1 = response.context["student_responses"][0]
        # print ("this is stud_resp", student_response)
        self.assertEqual(row1["num_right"], 2)
        self.assertEqual(row1["num_wrong"], 10)
        self.assertTrue(row1["correct"])

        # student views

# to test student_responses, the dict should have {dict[num_wrong]: 5, dict[num+right]: 1}
# but this is stored in a list, rows[0] = {num_wrong: 5, num_right: 1}


    def create_session(self,q,n=5):
        Response.objects.create(question=q, user=self.user, is_correct=True)
            
        for i in range(n):
            Response.objects.create(question=q, user=self.user, is_correct=False)






