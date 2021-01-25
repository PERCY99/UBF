# Generated by Django 2.2 on 2021-01-25 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20210112_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='answerkey',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='quiz',
            name='live',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quiz',
            name='rollout_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]