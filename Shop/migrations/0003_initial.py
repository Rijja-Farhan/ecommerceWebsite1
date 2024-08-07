# Generated by Django 5.0.6 on 2024-07-09 13:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Shop", "0002_delete_item"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("name", models.CharField(default="", max_length=255)),
                ("category", models.CharField(default="Uncategorized", max_length=100)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("description", models.TextField(default="")),
            ],
        ),
    ]
