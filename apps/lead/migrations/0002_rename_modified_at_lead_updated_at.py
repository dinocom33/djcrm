# Generated by Django 4.2.4 on 2023-08-28 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='modified_at',
            new_name='updated_at',
        ),
    ]
