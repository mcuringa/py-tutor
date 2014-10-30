from django.db import migrations, models

from tutor.models import *

class Migration(migrations.Migration):

    dependencies = [("tutor", "0001_initial")]

    def update_question_status(apps, schema_editor):
        Question = apps.get_model("tutor", "Question")
        t = Question.objects.all()
        for q in t: 
            q.update_status()
            q.save()

    operations = [
        migrations.AddField("Question", "status", models.IntegerField(default=Question.FAILED)),
        migrations.RunPython(update_question_status)
    ]