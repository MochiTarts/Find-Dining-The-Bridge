# Generated by Django 2.2.19 on 2021-03-08 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sduser', '0005_remove_sduser_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='sduser',
            name='authId',
            field=models.CharField(default='', max_length=255),
        ),
    ]
