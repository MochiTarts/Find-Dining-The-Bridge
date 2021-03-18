# Generated by Django 2.2.19 on 2021-03-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=64)),
                ('user_agent', models.CharField(db_index=True, max_length=255, verbose_name='user agent')),
                ('ip_address', models.GenericIPAddressField(db_index=True, null=True, verbose_name='ip address')),
                ('username', models.CharField(db_index=True, max_length=255, null=True, verbose_name='username')),
                ('http_accept', models.CharField(max_length=1025, verbose_name='http accept')),
                ('path_info', models.CharField(max_length=255, verbose_name='path')),
                ('attempt_time', models.DateTimeField(auto_now_add=True, verbose_name='attempt time')),
            ],
            options={
                'verbose_name': 'Login Log',
                'ordering': ['-attempt_time'],
            },
        ),
    ]