# Generated by Django 2.0.6 on 2018-07-16 22:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_coordonates_myfiles_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='site_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
