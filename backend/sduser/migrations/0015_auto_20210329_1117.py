# Generated by Django 2.2.19 on 2021-03-29 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sduser', '0014_auto_20210325_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sduser',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. If this field is not selected, a verification email will be send to the user. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
