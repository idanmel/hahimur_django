# Generated by Django 3.2 on 2021-05-02 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournaments', '0010_auto_20200417_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='MatchInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MatchPrediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_score', models.IntegerField()),
                ('away_score', models.IntegerField()),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('match_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.matchinfo')),
            ],
        ),
        migrations.CreateModel(
            name='MatchScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_score', models.IntegerField(null=True)),
                ('away_score', models.IntegerField(null=True)),
                ('match_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.matchinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=200)),
                ('flag', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='groupmatchprediction',
            name='friend',
        ),
        migrations.RemoveField(
            model_name='groupmatchprediction',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='knockoutmatch',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='knockoutmatchprediction',
            name='friend',
        ),
        migrations.RemoveField(
            model_name='knockoutmatchprediction',
            name='tournament',
        ),
        migrations.DeleteModel(
            name='GroupMatch',
        ),
        migrations.DeleteModel(
            name='GroupMatchPrediction',
        ),
        migrations.DeleteModel(
            name='KnockOutMatch',
        ),
        migrations.DeleteModel(
            name='KnockOutMatchPrediction',
        ),
        migrations.AddField(
            model_name='matchinfo',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='tournaments.team'),
        ),
        migrations.AddField(
            model_name='matchinfo',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.group'),
        ),
        migrations.AddField(
            model_name='matchinfo',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='tournaments.team'),
        ),
    ]
