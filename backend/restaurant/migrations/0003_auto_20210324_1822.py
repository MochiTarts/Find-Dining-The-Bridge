# Generated by Django 2.2.19 on 2021-03-24 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_userfavrestrs'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingrestaurant',
            name='owner_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='owner_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]