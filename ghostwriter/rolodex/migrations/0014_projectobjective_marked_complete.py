# Generated by Django 3.0.10 on 2021-02-13 00:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rolodex", "0013_projectsubtask_marked_complete"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectobjective",
            name="marked_complete",
            field=models.DateField(
                blank=True,
                help_text="Date the objective was marked complete",
                null=True,
                verbose_name="Marked Complete",
            ),
        ),
    ]
