# Generated by Django 3.0.8 on 2020-08-20 02:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('office', '0014_auto_20200820_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractsforms',
            name='lawyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lawyer_contracts', to=settings.AUTH_USER_MODEL),
        ),
    ]
