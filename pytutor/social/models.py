
import json

from django import forms
from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.humanize.templatetags import humanize
from django.contrib.auth.models import User



class SocialProfile(models.Model):
    """The user's social profile"""
    # basics
    bio = models.CharField(max_length=200, null=True, blank=True)
    public = models.BooleanField(default=False, blank=True)

    # location
    institution = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)

    # contact
    mobile = models.CharField(max_length=120, null=True, blank=True)
    facebook = models.CharField(max_length=120, null=True, blank=True)
    twitter = models.CharField(max_length=120, null=True, blank=True)
    whatsapp = models.CharField(max_length=120, null=True, blank=True)
    skype = models.CharField(max_length=120, null=True, blank=True)
    google = models.CharField(max_length=120, null=True, blank=True)
    pyanywhere = models.CharField(max_length=120, null=True, blank=True)

    #todo: add the user profile image

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, primary_key=True)

class RestProfile(SocialProfile):

    def as_json(self, msg=""):

        json_fields = ("bio", "public", "institution", "city", "state", "country", "mobile", "facebook", "twitter", "whatsapp", "skype", "google", "pyanywhere", "created", "modified")
        data = {}

        for field in json_fields:
            val = self.__dict__[field]
            if val is None:
                data[field] = ""
            else:
                data[field] = str(val)

        data["username"] = self.user.username
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["email"] = self.user.email
        data["msg"] = msg
        data["name"] = "{} {}".format(self.user.first_name, self.user.last_name).strip()

        return json.dumps(data)

    class Meta:
        proxy = True
        

class SocialProfileForm(ModelForm):
    class Meta:
        model = SocialProfile
        exclude = ["user", "created", "modified"]


class CustomUserChangeForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)

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

