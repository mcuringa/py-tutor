from django.db import migrations, models

from tutor.models import *

class Migration(migrations.Migration):

    dependencies = [("tutor", "0001_initial")]




    def update_question_status(apps, schema_editor):
        Question = apps.get_model("tutor", "Question")
        t = Question.objects.all()
        for q in t: 
            tests = Test.objects.all().filter(question=q)
            q.status = 2
            if len(tests) == 0: 
                q.status = 1
            results = [t.evaluate(q.solution) for t in tests]
            for test, fail, result in results:
                if fail is not None:
                    q.status = 1
                    break
            q.save()

    operations = [
        migrations.AddField("Question", "status", models.IntegerField(default=Question.FAILED)),
        migrations.RunPython(update_question_status)
    ]
