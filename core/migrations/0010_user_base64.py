# Generated by Django 2.2 on 2021-01-25 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_teamform_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='base64',
            field=models.TextField(blank=True, null=True),
        ),
    ]
