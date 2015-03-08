from django.db import models

# Create your models here.

class SocialProfile(models.Model):
    """The user's social profile"""
    
    status = models.CharField(max_length=20, blank=True)



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

