# Generated by Django 3.0.8 on 2021-02-06 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20200905_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='wallet',
            field=models.FloatField(default=0),
        ),
    ]