# Generated by Django 4.1.4 on 2022-12-29 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_blogpost_options_remove_blogpost_slug_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="commentpost", options={"verbose_name_plural": "Comments"},
        ),
    ]
