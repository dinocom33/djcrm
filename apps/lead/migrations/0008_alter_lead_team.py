# Generated by Django 4.2.4 on 2023-09-14 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_remove_team_members_alter_team_created_by'),
        ('lead', '0007_alter_lead_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='team.team'),
        ),
    ]
