# Generated by Django 2.2 on 2020-08-01 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20200424_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='price',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
