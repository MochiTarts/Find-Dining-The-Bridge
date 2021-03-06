# Generated by Django 2.2.19 on 2021-03-25 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sduser', '0013_auto_20210325_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sduser',
            name='auth_id',
            field=models.CharField(blank=True, default='', help_text='This is a unique id given by third parties(if the user logs in with a third party service)', max_length=255),
        ),
        migrations.AlterField(
            model_name='sduser',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='sduser',
            name='is_blocked',
            field=models.BooleanField(default=False, help_text='Select this to block the user from accessing the site. '),
        ),
        migrations.AlterField(
            model_name='sduser',
            name='refresh_token',
            field=models.CharField(blank=True, default='', help_text='This is for authentication purpose.', max_length=1023),
        ),
    ]
