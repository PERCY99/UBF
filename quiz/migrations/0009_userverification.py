# Generated by Django 2.2 on 2021-01-30 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20210125_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='')),
                ('verified', models.BooleanField(default=False)),
                ('quiz_taker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizTaker')),
            ],
        ),
    ]
