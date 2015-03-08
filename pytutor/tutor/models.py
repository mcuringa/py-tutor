# tutor.models.py
# by: mxc
"""
Define the Django models for the
PyTutor application. Defines
key objects: Question.
"""

import json

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from tutor.templatetags.tutor_extras import syn
from django.contrib.humanize.templatetags import humanize


class AbstractQuestion(models.Model):
    """A Question is a coding challenge for the studier.
    It provides them with a prompt and the name of the
    function they must write to solve the problem. Questions
    have a difficulty level and an arbitrary set of Tags 
    that categorize them. Questions are meant to be edited
    wiki-style -- wtih many editors boldly making changes, but
    with a clear revision history and easy system for rolling them
    back."""

    levels = ["Basics: simple function, variables, operators (e.g., +,-,*/)",
        "Conditional statements, built-in functions",
        "Strings, basics",
        "Lists and loops",
        "Dictionaries, tuples, sets; string functions",
        "Multi-step problems, libraries, OOP, etc",
        "Hard problems"]

    level_choices = [(i,"{}. {}".format(i,x)) for i,x in enumerate(levels, start=1)]

    function_name = models.CharField(max_length=300)
    prompt = models.TextField()
    solution = models.TextField(blank=True)
    level = models.IntegerField(choices=level_choices, default=1)
    tags = models.CharField(max_length=500, blank=True)
    version = models.IntegerField(default=0)
    comment = models.CharField(max_length=500, blank=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_creator")
    modifier = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modifer")

    def solution_pp(self):
        return syn(self.solution)

    def run_tests(self, code=""):
        tests = Test.objects.all().filter(question=self)
        if len(tests) == 0:
            return (False, [])

        if code == "":
            code = self.solution

        results = []
        passed = True


        for test, fail, result in [t.evaluate(code) for t in tests]:
            passed = passed and fail is None
            results.append((test, fail, result))
        
        return (passed, results)

    def level_label(self):
        return AbstractQuestion.levels[self.level - 1]


    class Meta:
        abstract = True
        ordering = ['-modified']

class QuestionManager(models.Manager):
    def by_level(self):
        questions = Question.objects.all()
        level_questions= {}
        for q in questions:
            level = level_questions.get(q.level, [])
            level.append(q)
        return level_questions

class Question(AbstractQuestion):

    FAILED = 1
    ACTIVE = 2
    DELETED = 3
    status_labels = ["","Failed", "Active", "Deleted"]
    status_css_classes = ["","danger", "success", "default"]
    status = models.IntegerField(default=FAILED)
    objects = QuestionManager()

    def as_json(self, wrap="", extra={}):
        q_data = {k: self.__dict__[k] for k in ('version', 'id', 'status')}
        q_data["creator"] = self.creator.username
        q_data["modifier"] = self.modifier.username
        q_data["created"] = humanize.naturaltime(self.created)
        q_data["modified"] = humanize.naturaltime(self.modified)
        q_data["status_label"] = self.status_labels[self.status]
        q_data["status_css"] = self.status_css_classes[self.status]

        for k,v in extra.items():
            q_data[k] = v

        if(len(wrap) > 0):
            return json.dumps({wrap: q_data})
        return json.dumps(q_data)


    def test_and_update(self, t=None):
        if self.status == Question.DELETED:
            return False
        
        if t is not None:
            test, ex, result = test.evaluate(user_function)
            passed = ex == None

        else:
            passed, results = self.run_tests()
        
        if self.status == Question.ACTIVE and not passed:
            self.status = Question.FAILED
            self.save()
            return True
        elif self.status == Question.FAILED and passed:
            self.status = Question.ACTIVE
            self.save()
            return True

        return False

    class Meta:
        unique_together = (('id', 'version'),)

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["function_name", "prompt", "solution", "level", "tags", "comment"]


class ArchiveQuestion(AbstractQuestion):
    """An ArchiveQuestion is created everytime a
    Question is updated. ArchiveQuestions can
    be reviewed and reverted to. For every Question
    there may be serveral ArchiveQuestions. Users
    Responses are linked to ArchiveQuestions, as 
    are Flags. Comments are linked to the current
    Question, because, generally, comments will endure
    across vesions of a Question."""

    archived = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Question)

    def archive(self, q):

        self.function_name = q.function_name
        self.prompt = q.prompt
        self.solution = q.solution
        self.level = q.level
        self.tags = q.tags
        self.version = q.version
        self.comment = q.comment
        self.created = q.created
        self.creator = q.creator
        self.parent = q
    
    class Meta:
        unique_together = (('parent', 'version'),)


class Solution(ArchiveQuestion):
    """Solution objects provide custom comparators for ArchiveQuestions
which allows them to be hashed and ordered based on the code and version"""

    class Meta:
        proxy = True

#######################################################################################################    

    def test(self, tests):
        code = self.solution
        self.passed = True

        for test, fail, result in [t.evaluate(code) for t in tests]:
            self.passed = self.passed and fail is None

    def __ne__(self, other):
        return self.solution != other.solution

    def __eq__(self, other):
        return self.solution == other.solution

    def __hash__(self):
        return self.solution.__hash__()
  
#######################################################################################################  
# def __ne__ not equal ---> set parameters for what you're looking for.
# custom sorting


class Test(models.Model):
    """
        Each Question must have at leat one Test
        before it can be published. Tests are meant
        to be dynamically executed by the system--
        each test has arguments to pass to the Users's
        function and the expected result. If all
        Question tests pass, the Response is considered correct.
    """
    args = models.CharField(blank=True, max_length=500)
    result = models.TextField()
    question = models.ForeignKey(Question)
    
    def evaluate(self, code=""):
        """Compile and execute the code in its own
           namespace, checking to see if the 
           function returns the expected result
           when called with the given args.
           Returns a tuple of the return value
           and Exeception (or None)"""
        
        if code == "":
            code = Question.objects.get(pk=self.question.pk).solution

        ns = {}
        result = None
        fail = None

        try:
            # can get a syntax error here
            f = compile(code, '<string>', 'exec')
            # create the function in scope ns
            exec(f, ns)
            
            # create the string we're going to evaluate
            # might get a runtime error
            call = "result = {}({})".format(self.question.function_name, self.args)
            exec(call, ns)

            # if the result doesn't match the expected value
            # we'll get an assert error
            result = ns["result"]

            if not result == eval(self.result):
                msg = """
       Called: {}({})
     Expected: {}
Actual result: {}""".format(self.question.function_name, self.args, self.result, result)
                fail = AssertionError(msg)

        except Exception as ex:
            fail = ex

        return (self, fail, result)

    def to_code(self):
        str = 'assert {}({}) == {}'.format(self.question.function_name, self.args, self.result)
        return str


class TestForm(ModelForm):
    args = forms.CharField(required = False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    result = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Test
        fields = ["args", "result"]



class Response(models.Model):
    """A User's attempt to answer a Question
    is captured in the Response. The Response
    is evaluated against the Tests for a Question.
    If all tests are correctly passed, the Response
    is marked correct"""

    MAX_ATTEMPTS = 10

    code = models.TextField(blank=True, help_text="Your solution to this question.")
    is_correct = models.BooleanField(default=False)
    attempt = models.IntegerField(default=1)
    submitted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)

    def code_pp(self):
        return syn(self.code)

class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ["code"]


class QuestionFlag(models.Model):
    """    """
    flags = [ (1, "Unclear"),
          (2, "Too Hard for Level"),
          (3, "Too Easy for Level"),
          (4, "Innapropriate")]

    flag = models.IntegerField(choices=flags)
    question = models.ForeignKey(ArchiveQuestion)
    creator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)


# class StudentResponse(models.Model):
#     """finds information about student progress
#     """
#     student_response= Response.objects.all().filter(question=self, user=user).order_by("-submitted").first()
#     attempts = Response.attempt




