# Generated by Django 3.0.8 on 2020-08-09 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phSessions', '0002_auto_20200809_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='phsession',
            name='payment_method',
            field=models.CharField(choices=[('credit', '1'), ('fawry', '2')], default=1, max_length=10),
            preserve_default=False,
        ),
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
