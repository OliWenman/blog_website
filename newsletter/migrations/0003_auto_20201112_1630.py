# Generated by Django 3.0.3 on 2020-11-12 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='sent_already',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='sent_date',
            field=models.DateTimeField(null=True),
        ),
    ]