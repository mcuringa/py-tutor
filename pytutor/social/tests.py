from django.test import TestCase

from social.models import *



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



    def test_create(self):
        first_name = "Antonio"
        last_name = "Gramsci"
        email = "tgramsci@cpi.org.it"
        bio = "leading the fight against capitalist hegemony"
        public = True

        institution = "prison"
        city = "Torino"
        state = "Piemonte"
        country = "Italia"

        user = User.objects.create_user(username="tester", password="password")
        # SocialProfile.objects.create(user=user)
        # SocialProfile.objects.update(user=user, first_name=first_name, city=city)