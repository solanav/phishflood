# Generated by Django 5.0 on 2023-12-30 12:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("phishings", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="phishing",
            name="id",
            field=models.CharField(
                default=None,
                editable=False,
                max_length=255,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]