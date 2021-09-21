# Generated by Django 3.0.8 on 2020-10-25 16:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0018_invoice_registered_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agenda',
            old_name='date',
            new_name='session_date',
        ),
        migrations.AddField(
            model_name='agenda',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agenda',
            name='court',
            field=models.CharField(max_length=100),
        ),
    ]
