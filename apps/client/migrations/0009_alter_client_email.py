# Generated by Django 4.2.4 on 2023-10-23 11:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_alter_client_email_alter_client_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.CharField(max_length=50, validators=[django.core.validators.EmailValidator(message='The email address is not valid! Please try again!')]),
        ),
    ]
