# Generated by Django 2.2 on 2020-09-09 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200808_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='demo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='summary',
            name='mcq',
            field=models.ManyToManyField(null=True, to='core.MCQ'),
        ),
    ]
