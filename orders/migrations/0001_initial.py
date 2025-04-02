# Generated by Django 5.1.7 on 2025-04-02 01:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CEDARSSpecialist',
            fields=[
                ('specialist_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact_info', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='HKUMember',
            fields=[
                ('member_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact_info', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyOwner',
            fields=[
                ('owner_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact_info', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('address', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('period_of_availability', models.CharField(max_length=100)),
                ('number_of_beds', models.IntegerField()),
                ('number_of_bedrooms', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('distance', models.FloatField()),
                ('specialist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_accommodations', to='orders.cedarsspecialist')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accommodations', to='orders.propertyowner')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('rating_id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField()),
                ('comment', models.TextField(blank=True)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.accommodation')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.hkumember')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_id', models.AutoField(primary_key=True, serialize=False)),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], max_length=10)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='orders.accommodation')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='orders.hkumember')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_id', models.AutoField(primary_key=True, serialize=False)),
                ('signed_date', models.DateTimeField(auto_now_add=True)),
                ('contract_status', models.CharField(choices=[('signed', 'Signed'), ('failed', 'Failed')], max_length=10)),
                ('reservation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='orders.reservation')),
            ],
        ),
    ]
