# Generated by Django 4.2 on 2023-05-14 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0004_roomfeedback_feedback"),
    ]

    operations = [
        migrations.AlterField(
            model_name="roomfeedback",
            name="room",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="rooms.rooms",
            ),
        ),
    ]
