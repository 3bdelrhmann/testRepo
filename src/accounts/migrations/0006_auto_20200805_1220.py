# Generated by Django 3.0.8 on 2020-08-05 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200805_1215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Specialties',
            new_name='specialties',
        ),
    ]
