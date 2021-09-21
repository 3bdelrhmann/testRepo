# Generated by Django 3.0.8 on 2020-08-05 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200805_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='specialties',
            field=models.ManyToManyField(blank=True, max_length=500, null=True, related_name='all_specialties', to='accounts.Specialties', verbose_name='التخصصات'),
        ),
    ]
