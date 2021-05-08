# Generated by Django 3.2 on 2021-05-08 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0015_auto_20210508_0359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchprediction',
            name='away_team_name',
        ),
        migrations.RemoveField(
            model_name='matchprediction',
            name='home_team_name',
        ),
        migrations.AddField(
            model_name='matchprediction',
            name='away_team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mp_away_team', to='tournaments.team'),
        ),
        migrations.AddField(
            model_name='matchprediction',
            name='home_team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mp_home_team', to='tournaments.team'),
        ),
    ]
