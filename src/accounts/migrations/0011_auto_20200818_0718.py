# Generated by Django 3.0.8 on 2020-08-18 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200809_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='assistant_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lawyer_assistants', to=settings.AUTH_USER_MODEL),
        ),
    ]