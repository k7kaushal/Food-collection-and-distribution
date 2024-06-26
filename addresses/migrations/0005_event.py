# Generated by Django 4.2 on 2023-05-01 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("addresses", "0004_ngo_contact"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("event_name", models.CharField(max_length=100)),
                ("event_attendants", models.CharField(max_length=10)),
                ("location", models.CharField(max_length=100)),
                ("event_manager", models.BooleanField(default=True)),
                ("Contact", models.CharField(default="12345678", max_length=10)),
                (
                    "date_posted",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("ngolat", models.FloatField(blank=True, null=True)),
                ("ngolong", models.FloatField(blank=True, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
