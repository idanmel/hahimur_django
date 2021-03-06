# Generated by Django 3.0.5 on 2020-04-15 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0008_auto_20200415_0908'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='groupmatchprediction',
            constraint=models.UniqueConstraint(fields=('tournament', 'friend', 'match_number'), name='unique_group_match_prediction'),
        ),
    ]
