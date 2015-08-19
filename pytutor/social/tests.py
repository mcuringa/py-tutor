from django.test import TestCase

from social.models import *


# just a comment, for social branch
class TestSocialProfile(TestCase):


    def test_migrate(self):

        t1 = User.objects.create_user(username="tester", password="password")
        User.objects.create_user(username="t1", password="password")
        User.objects.create_user(username="t2", password="password")
        User.objects.create_user(username="t3", password="password")

        users = User.objects.all()
        self.assertEqual(len(users), 4)
        for user in users: 
            SocialProfile.objects.create(user=user)

        up = SocialProfile.objects.get(user=t1)

    def mk_profile(self):

        user = User.objects.create_user(username="tester", password="password")
        SocialProfile.objects.create(user=user)

        profile = SocialProfile.objects.get(user__username=user.username)
        
        profile.first_name = "Antonio"
        profile.last_name = "Gramsci"
        profile.email = "tgramsci@cpi.org.it"
        profile.bio = "leading the fight against capitalist hegemony"
        profile.public = True
        profile.institution = "prison"
        profile.city = "Torino"
        profile.state = "Piemonte"
        profile.country = "Italia"

        return profile


    def test_save(self):

        profile = self.mk_profile()
        profile.save()
        p2 = SocialProfile.objects.get(user__username="tester")
        self.assertEqual(p2.city, "Torino")

    def test_form(self):
        data = {"city": "Brooklyn", "first_name": "Toni"}
        form = SocialProfileForm(data)
        user = User.objects.create_user(username="tester", password="password")
        form.instance.user = user
        self.assertTrue(form.is_valid())
        form.save()
        p2 = SocialProfile.objects.get(user__username="tester")
        self.assertEqual(p2.city, "Brooklyn")


        


