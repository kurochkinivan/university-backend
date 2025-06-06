# Generated by Django 5.1.6 on 2025-05-28 07:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0007_auto_20250508_1036"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="article",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
            preserve_default=False,
        ),
    ]
