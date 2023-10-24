# Generated by Django 4.2.4 on 2023-10-23 11:45

import apps.lead.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_remove_team_members_alter_team_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=255, validators=[apps.lead.validators.name_validator]),
        ),
    ]