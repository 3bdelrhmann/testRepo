# Generated by Django 3.0.8 on 2021-03-28 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_customer_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]