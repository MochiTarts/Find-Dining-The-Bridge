# Generated by Django 2.2.19 on 2021-04-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0002_auto_20210406_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='labels',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(editable=False, max_length=512, unique=True),
        ),
    ]
