# Generated by Django 5.0 on 2024-01-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("phishings", "0005_alter_action_value_alter_phishing_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="form",
            name="page",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]