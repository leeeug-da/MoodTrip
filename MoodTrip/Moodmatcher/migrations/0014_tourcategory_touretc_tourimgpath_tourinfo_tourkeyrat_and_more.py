# Generated by Django 4.1 on 2024-02-06 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Moodmatcher", "0013_touristspot"),
    ]

    operations = [
        migrations.CreateModel(
            name="TourCategory",
            fields=[
                ("tour_cat_id", models.AutoField(primary_key=True, serialize=False)),
                ("tour_cat_name", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "tour_category",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TourEtc",
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
                ("stroller", models.TextField(blank=True, null=True)),
                ("pet", models.TextField(blank=True, null=True)),
                ("parking", models.TextField(blank=True, null=True)),
                ("parking_fare", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "tour_etc",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TourImgPath",
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
                ("img_path", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "tour_img_path",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TourInfo",
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
                ("intro", models.TextField(blank=True, null=True)),
                ("info", models.TextField(blank=True, null=True)),
                ("guide", models.TextField(blank=True, null=True)),
                ("price_1", models.TextField(blank=True, null=True)),
                ("price_2", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "tour_info",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TourKeyRat",
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
                ("key_1", models.TextField(blank=True, null=True)),
                ("key_2", models.TextField(blank=True, null=True)),
                ("key_3", models.TextField(blank=True, null=True)),
                ("ratings", models.FloatField(blank=True, null=True)),
            ],
            options={
                "db_table": "tour_key_rat",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TourKeywords",
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
                ("key_1", models.TextField(blank=True, null=True)),
                ("key_2", models.TextField(blank=True, null=True)),
                ("key_3", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "tour_keywords",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TourMain",
            fields=[
                ("tour_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.TextField(blank=True, null=True)),
                ("postal_code", models.TextField(blank=True, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                ("contact", models.TextField(blank=True, null=True)),
                ("area", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "tour_main",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TourPeriod",
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
                ("open_hour_1", models.TextField(blank=True, null=True)),
                ("open_hour_2", models.TextField(blank=True, null=True)),
                ("open_hour_3", models.TextField(blank=True, null=True)),
                ("close_day", models.TextField(blank=True, null=True)),
                ("open_period_1", models.TextField(blank=True, null=True)),
                ("open_period_2", models.TextField(blank=True, null=True)),
                ("fest_open", models.TextField(blank=True, null=True)),
                ("fest_close", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "tour_period",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TourRatings",
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
                ("ratings", models.FloatField(blank=True, null=True)),
            ],
            options={
                "db_table": "tour_ratings",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="SelectedImage",
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
                ("image", models.ImageField(upload_to="selected_images/")),
            ],
        ),
    ]
