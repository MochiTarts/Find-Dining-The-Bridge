# Generated by Django 2.2.19 on 2021-03-12 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sduser', '0007_sduser_blocked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sduser',
            old_name='blocked',
            new_name='is_blocked',
        ),
    ]
