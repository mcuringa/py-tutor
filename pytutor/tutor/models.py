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


class Question(models.Model):
    """A Question is a coding challenge for the studier.
    It provides them with a prompt and the name of the
    function they must write to solve the problem. Questions
    have a difficulty level and an arbitrary set of Tags 
    that categorize them. Questions are meant to be edited
    wiki-style -- wtih many editors boldly making changes, but
    with a clear revision history and easy system for rolling them
    back."""

    level_choices = [(i,i) for i in range(1,11)]

    prompt = models.TextField()
    function_name = models.CharField(max_length=300)
    level = models.IntegerField(choices=level_choices)
    tags = models.CharField(max_length=500)
    version = models.IntegerField()
    comment = models.CharField(max_length=500)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField()
    creator = models.ForeignKey(User, related_name="creator")
    modifier = models.ForeignKey(User, related_name="modifer")
    

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["prompt", "function_name", "level", "tags", "comment"]


class ArchiveQuestion(Question):
    """An ArchiveQuestion is created everytime a
    Question is updated. ArchiveQuestions can
    be reviewed and reverted to. For every Question
    there may be serveral ArchiveQuestions. Users
    Responses are linked to ArchiveQuestions, as 
    are Flags. Comments are linked to the current
    Question, because, generally, comments will endure
    across vesions of a Question."""

    archived = models.DateTimeField(auto_now=True)
    


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
    args = models.CharField(max_length=500)
    result = models.TextField()
    fail_msg = models.TextField(blank=True)
    success_msg = models.TextField(blank=True)


class Response(models.Model):
    """A User's attempt to answer a Question
    is captured in the Response. The Response
    is evaluated against the Tests for a Question.
    If all tests are correctly passed, the Response
    is marked correct"""

    code = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    attempt = models.IntegerField()
    submitted = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    question = models.ForeignKey(ArchiveQuestion)


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ["code"]


class QuestionFlag(models.Model):
    """    """
    flags = [ (1, "Unclear"),
          (2, "Too Hard"),
          (3, "Too Easy"),
          (4, "Innapropriate")]

    flag = models.IntegerField(choices=flags)
    question = models.ForeignKey(ArchiveQuestion)
    creator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=True)



