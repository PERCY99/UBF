# Generated by Django 2.2 on 2020-07-15 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200716_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='mcq',
            field=models.ManyToManyField(blank=True, to='core.MCQ'),
        ),
        migrations.RenameModel(
            old_name='Sessions',
            new_name='Session',
        ),
        migrations.CreateModel(
            name='UserSubscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mcqs', models.ManyToManyField(blank=True, to='core.MCQ')),
                ('pdfs', models.ManyToManyField(blank=True, to='core.PDF')),
                ('sessions', models.ManyToManyField(blank=True, to='core.Session')),
                ('summaries', models.ManyToManyField(blank=True, to='core.Summary')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
