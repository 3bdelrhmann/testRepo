# Generated by Django 3.0.8 on 2020-08-23 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phSessions', '0017_auto_20200820_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelawyerefforts',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phSessions.phSession'),
        ),
        migrations.AlterField(
            model_name='sessionreviews',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phSessions.phSession'),
        ),
    ]