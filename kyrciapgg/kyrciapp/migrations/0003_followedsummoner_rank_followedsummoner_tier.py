# Generated by Django 5.0.1 on 2024-02-01 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kyrciapp", "0002_note_customuser_followed_users_followedsummoner"),
    ]

    operations = [
        migrations.AddField(
            model_name="followedsummoner",
            name="rank",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="followedsummoner",
            name="tier",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]