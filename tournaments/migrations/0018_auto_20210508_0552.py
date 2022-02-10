# Generated by Django 3.2 on 2021-05-08 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0017_matchprediction_home_win'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchinfo',
            options={'verbose_name_plural': 'Matches Info'},
        ),
        migrations.AddConstraint(
            model_name='matchprediction',
            constraint=models.UniqueConstraint(fields=('match_info', 'friend'), name='unique_match_friend_prediction'),
        ),
    ]