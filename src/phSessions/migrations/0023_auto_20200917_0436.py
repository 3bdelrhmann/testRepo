# Generated by Django 3.0.8 on 2020-09-17 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phSessions', '0022_auto_20200905_2327'),
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
