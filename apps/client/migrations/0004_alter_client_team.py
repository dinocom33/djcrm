# Generated by Django 4.2.4 on 2023-09-05 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
        ('client', '0003_client_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='team.team'),
        ),
    ]
