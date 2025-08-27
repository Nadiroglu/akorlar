# Generated manually for capo_friendly field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chorddiagram',
            name='capo_friendly',
            field=models.BooleanField(default=False, help_text='Works well with capo'),
        ),
    ]
