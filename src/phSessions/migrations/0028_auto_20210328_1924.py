# Generated by Django 3.0.8 on 2021-03-28 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phSessions', '0027_auto_20210206_2208'),
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
