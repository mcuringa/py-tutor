from django.test import TestCase

from social.models import *



class TestSocialProfile(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")

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
        user = self.user
        
        SocialProfile.objects.create(user=user, first_name=first_name, city=city)