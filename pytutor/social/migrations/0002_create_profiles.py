from django.db import models, migrations
from django.conf import settings

# from django.contrib.auth.models import User

class Migration(migrations.Migration):


    dependencies = [("social", "0001_initial")]


    def create_profiles(apps, schema_editor):
        SocialProfile = apps.get_model("social", "SocialProfile")
        User = apps.get_model("auth", "User")
        users = User.objects.all()
        for user in users: 
            SocialProfile.objects.create(user=user)

    operations = [
        migrations.RunPython(create_profiles)
    ]
