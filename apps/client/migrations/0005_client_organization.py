# Generated by Django 4.2.4 on 2023-09-05 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('client', '0004_alter_client_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='organization.organization'),
            preserve_default=False,
        ),
    ]
