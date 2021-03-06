# Generated by Django 2.2 on 2020-08-01 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=128)),
                ('payment_id', models.CharField(max_length=128)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.AddField(
            model_name='usercart',
            name='payment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='cart.Payment'),
            preserve_default=False,
        ),
    ]
