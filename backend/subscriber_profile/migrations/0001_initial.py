# Generated by Django 2.2.19 on 2021-03-29 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriberProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('first_name', models.CharField(blank=True, default='', max_length=30)),
                ('last_name', models.CharField(blank=True, default='', max_length=150)),
                ('phone', models.BigIntegerField(blank=True, default=None, null=True)),
                ('postalCode', models.CharField(blank=True, default='', max_length=7)),
                ('GEO_location', models.CharField(default='', max_length=50)),
                ('last_updated', models.DateField(auto_now=True, null=True)),
                ('consent_status', models.CharField(choices=[('EXPRESSED', 'Expressed Consent'), ('IMPLIED', 'Implied Enquiry'), ('EXPIRED', 'Expired'), ('UNSUBSCRIBED', 'Unsubscribed')], default='IMPLIED', max_length=12)),
                ('expired_at', models.DateField(blank=True, null=True)),
                ('subscribed_at', models.DateField(blank=True, null=True)),
                ('unsubscribed_at', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'subscriber_profile',
            },
        ),
    ]
