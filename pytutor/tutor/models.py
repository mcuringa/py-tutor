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



class Question(models.Model):

    level_choices = [(i,i) for i in range(1,11)]

    prompt = models.TextField
    function_name = models.CharField
    hint = models.TextField(blank=True)
    test = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    level = models.IntegerField(choices=level_choices)
    modified = models.DateTimeField(auto_now=True)
    tags = []

class Tag(models.Model):
    tag = models.CharField

class TestData(models.Model):
    params = models.CharField
    result = models.CharField()
    error = models.CharField(blank=True)
    fail_msg = models.TextField(blank=True)
    success_msg = models.TextField(blank=True)




class QuestionForm(ModelForm):
    class Meta:
        model = Question
    exclude = ["modified"]



class Response():

    def check(self, response):
        f = eval(response)
        result = f(self.params)
        if result == self.result:
            return (True, Question.success)
        return (False, Question.fail)







