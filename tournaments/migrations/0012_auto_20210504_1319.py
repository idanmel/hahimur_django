# Generated by Django 3.2 on 2021-05-04 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0011_auto_20210502_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='team',
            new_name='name',
        ),
        migrations.AddField(
            model_name='matchscore',
            name='home_win',
            field=models.BooleanField(null=True),
        ),
    ]
