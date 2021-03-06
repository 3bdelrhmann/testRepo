# Generated by Django 3.0.8 on 2020-08-09 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phSessions', '0004_auto_20200809_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelawyerefforts',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phSessions.phSession'),
        ),
        migrations.AlterField(
            model_name='phsession',
            name='pocket_money',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='sessionreviews',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phSessions.phSession'),
        ),
    ]
