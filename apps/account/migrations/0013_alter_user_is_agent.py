# Generated by Django 4.2.4 on 2023-09-12 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_user_is_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=True),
        ),
    ]