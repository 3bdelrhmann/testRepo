# Generated by Django 3.0.8 on 2020-08-17 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0009_agenda_case_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agenda',
            name='case_year',
        ),
    ]
