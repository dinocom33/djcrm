# Generated by Django 4.2.4 on 2023-08-31 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_is_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
    ]
