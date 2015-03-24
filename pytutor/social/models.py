
import json

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.humanize.templatetags import humanize
from django.contrib.auth.models import User



class SocialProfile(models.Model):
    """The user's social profile"""
    # basics
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    public = models.BooleanField(default=False, blank=True)

    # location
    institution = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)

    #todo: add the user profile image

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, primary_key=True)

class RestProfile(SocialProfile):

    json_fields = ("first_name", "last_name", "bio",
        "public", "institution", "city", "state", "country")
    
    def as_json(self, msg=""):

        data = {k: self.__dict__[k] for k in RestProfile.json_fields}
        data["username"] = self.user.username
        data["msg"] = msg
        data["name"] = "{} {}".format(self.first_name, self.last_name).strip()

        return json.dumps(data)

    class Meta:
        proxy = True
        

class SocialProfileForm(ModelForm):
    class Meta:
        model = RestProfile
        exclude = ["user", "created", "modified"]


class FriendConnection(models.Model):
    """Messages are sent between users"""

    status_choices = ["pending", "accepted" "ignored"]

    status = models.CharField(max_length=20, blank=True)
    friend_a = models.ForeignKey(User, related_name="frienda")
    friend_b = models.ForeignKey(User, related_name="friendb")
    sent = models.DateTimeField(auto_now=True)
    muted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)



class Message(models.Model):
    """Messages are sent between users"""

    msg = models.TextField()
    msg_from = models.ForeignKey(User, related_name="from_user")
    msg_to = models.ForeignKey(User, related_name="to_user")
    sent = models.DateTimeField(auto_now=True)
    unread = models.BooleanField(default=True)

