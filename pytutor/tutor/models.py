# tutor.models.py
# by: mxc
"""
Define the Django models for the
PyTutor application. Defines
key objects: Question.
"""

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class AbstractQuestion(models.Model):
    """A Question is a coding challenge for the studier.
    It provides them with a prompt and the name of the
    function they must write to solve the problem. Questions
    have a difficulty level and an arbitrary set of Tags 
    that categorize them. Questions are meant to be edited
    wiki-style -- wtih many editors boldly making changes, but
    with a clear revision history and easy system for rolling them
    back."""

    level_choices = [(i,i) for i in range(1,11)]

    function_name = models.CharField(max_length=300)
    prompt = models.TextField()
    solution = models.TextField()
    level = models.IntegerField(choices=level_choices)
    tags = models.CharField(max_length=500)
    version = models.IntegerField(default=0)
    comment = models.CharField(max_length=500)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_creator")
    modifier = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modifer")

    class Meta:
        abstract = True



class Question(AbstractQuestion):

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

class Tag(models.Model):
    """Tags are the set of case-insensitive tags
    that are applied to Questions in the tutoring
    system."""

    tag = models.CharField(max_length=300)


class Test(models.Model):
    """
        Each Question must have at leat one Test
        before it can be published. Tests are meant
        to be dynamically executed by the system--
        each test has arguments to pass to the Users's
        function and the expected result. If all
        Question tests pass, the Response is considered correct.
    """
    args = models.CharField(max_length=500, help_text="The arguments to pass to the function.")
    result = models.TextField(help_text="Python code that will evaluate to the expected result of this unit test.")
    fail_msg = models.TextField(blank=True, help_text="A message for the user if their function fails this test.")
    question = models.ForeignKey(Question)
    
    def evaluate(self, user_function):
        """Evaluate the user_function against this test's assertion. 
        Quietly return, or throw an Exception."""

        try:
            # compile the user's function
            fun = compile(user_function, '<string>', 'exec')
            # create empty context to exec the code
            ns = {}
            # compile the funciton into our context
            exec(fun, ns)
            # run the assertion for this test
            exec(self.to_code(), ns)
            #testResults.append( (test, None) )
            return (None, True)
        except AssertionError as ae:
            return (ae, False)
        except Exception as ex:
            return (ex, False)
        

    def to_code(self):
        str = "assert {}({}) == {}, '{}'".format(self.question.function_name, self.args, self.result, self.fail_msg)
        return str

class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = ["args", "result", "fail_msg"]


class Response(models.Model):
    """A User's attempt to answer a Question
    is captured in the Response. The Response
    is evaluated against the Tests for a Question.
    If all tests are correctly passed, the Response
    is marked correct"""

    code = models.TextField(blank=True, help_text="Your solution to this question.")
    is_correct = models.BooleanField(default=False)
    attempt = models.IntegerField()
    submitted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    question = models.ForeignKey(ArchiveQuestion)


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



