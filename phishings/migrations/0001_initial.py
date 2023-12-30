# Generated by Django 5.0 on 2023-12-30 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Form",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("meta_id", models.IntegerField()),
                ("html_id", models.CharField(max_length=255, null=True)),
                ("html_action", models.CharField(max_length=255, null=True)),
                ("html_method", models.CharField(max_length=255, null=True)),
                ("html_type", models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Phishing",
            fields=[
                (
                    "id",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Input",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("meta_id", models.IntegerField()),
                ("html_id", models.CharField(max_length=255, null=True)),
                ("html_name", models.CharField(max_length=255, null=True)),
                ("html_placeholder", models.CharField(max_length=255, null=True)),
                ("html_type", models.CharField(max_length=255, null=True)),
                (
                    "form",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inputs",
                        to="phishings.form",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="form",
            name="phishing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="forms",
                to="phishings.phishing",
            ),
        ),
        migrations.CreateModel(
            name="Action",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("action", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=255)),
                ("status", models.CharField(max_length=255)),
                (
                    "form",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="phishings.form"
                    ),
                ),
                (
                    "input",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="phishings.input",
                    ),
                ),
                (
                    "phishing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actions",
                        to="phishings.phishing",
                    ),
                ),
            ],
        ),
    ]
