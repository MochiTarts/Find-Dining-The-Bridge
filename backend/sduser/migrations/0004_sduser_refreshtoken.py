# Generated by Django 2.2.19 on 2021-03-03 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sduser', '0003_auto_20210224_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='sduser',
            name='refreshToken',
            field=models.CharField(default='', max_length=1023),
        ),
    ]
