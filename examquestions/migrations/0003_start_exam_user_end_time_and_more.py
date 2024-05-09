from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('examquestions', '0002_start_exam_user_examname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='start_exam_user',
            name='end_time',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.CharField(choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4')], max_length=100),
        ),
    ]
