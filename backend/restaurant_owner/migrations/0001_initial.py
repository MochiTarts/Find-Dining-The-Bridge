# Generated by Django 2.2.19 on 2021-03-20 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='', max_length=24)),
                ('restaurant_id', models.CharField(blank=True, default='', max_length=24)),
                ('last_updated', models.DateField(auto_now=True)),
                ('consent_status', models.CharField(blank=True, choices=[('EXPRESSED', 'Expressed Consent'), ('IMPLIED', 'Implied Enquiry'), ('EXPIRED', 'Expired'), ('UNSUBSCRIBED', 'Unsubscribed')], default='IMPLIED', max_length=30)),
                ('subscribed_at', models.DateField(blank=True)),
                ('unsubscribed_at', models.DateField(blank=True)),
                ('expired_at', models.DateField(blank=True)),
            ],
            options={
                'verbose_name': 'Restaurant Owner',
            },
        ),
    ]