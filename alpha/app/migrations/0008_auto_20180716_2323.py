# Generated by Django 2.0.6 on 2018-07-16 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20180716_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordonates',
            name='course',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coordonates',
            name='satellite',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coordonates',
            name='vitesse',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]
