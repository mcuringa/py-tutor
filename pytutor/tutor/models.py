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

# enumerate(["sent","pending","friend"],start=1)]

class Question(AbstractQuestion):

    FAILED = 1
    ACTIVE = 2
    DELETED = 3
    status_labels = ["failed", "active", "deleted"]

    status = models.IntegerField(default=FAILED)

    def status_label(self):
        return Question.status_labels[self.status - 1]

    def test_and_update(self, t=None):
        print("test and update")
        if self.status == Question.DELETED:
            return False
        
        if t is not None:
            test, ex, result = test.evaluate(user_function)
            passed = ex == None

        else:
            passed, results = self.run_tests()
        
        print("passed:", passed)
        print("current status:", self.status)
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

class FriendConnect(models.Model):
    """Messages are sent between users"""
    status_choices = ["sent", "pending", "friend"]

    status = models.CharField(max_length=20, blank=True)
    friend = models.ForeignKey(User, related_name="friend")
    sent = models.DateTimeField(auto_now=True)

class Message(models.Model):
    """Messages are sent between users"""

    msg = models.TextField()
    msg_from = models.ForeignKey(User, related_name="from_user")
    msg_to = models.ForeignKey(User, related_name="to_user")
    sent = models.DateTimeField(auto_now=True)
    unread = models.BooleanField(default=True)



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



