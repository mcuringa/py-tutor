
import json

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize


class SocialProfile(models.Model):
    """The user's social profile"""
    # basics
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    bio = models.CharField(max_length=400, blank=True)
    public = models.BooleanField(default=False)

    # location
    institution = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)

    user = models.OneToOneField(User, primary_key=True)



class FriendConnection(models.Model):
    """Messages are sent between users"""

    status_choices = ["pending", "accepted" "ignored"]

    status = models.CharField(max_length=20, blank=True)
    friend_a = models.ForeignKey(User, related_name="frienda")
    friend_b = models.ForeignKey(User, related_name="friendb")
    sent = models.DateTimeField(auto_now=True)
    accepted = models.DateTimeField(auto_now=True)



class Message(models.Model):
    """Messages are sent between users"""

    msg = models.TextField()
    msg_from = models.ForeignKey(User, related_name="from_user")
    msg_to = models.ForeignKey(User, related_name="to_user")
    sent = models.DateTimeField(auto_now=True)
    unread = models.BooleanField(default=True)

