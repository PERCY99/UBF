# Generated by Django 2.2 on 2021-01-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200909_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamform',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]