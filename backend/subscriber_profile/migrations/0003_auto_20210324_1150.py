# Generated by Django 2.2.19 on 2021-03-24 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriber_profile', '0002_auto_20210322_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriberprofile',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
