# Generated by Django 2.2 on 2020-08-10 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quiz_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiztaker',
            name='quiz_day_rank',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
