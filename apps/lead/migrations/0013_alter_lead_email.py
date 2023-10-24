# Generated by Django 4.2.4 on 2023-10-23 11:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0012_alter_lead_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.CharField(max_length=254, validators=[django.core.validators.EmailValidator(message='Please enter a valid email address!')]),
        ),
    ]