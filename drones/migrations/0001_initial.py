# Generated by Django 4.2.7 on 2023-12-04 01:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Swarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('swarm_name', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drones.user')),
            ],
        ),
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drone_name', models.CharField(max_length=250)),
                ('MAC_address', models.CharField(default='00:DE:AD:BE:EF:00', max_length=250)),
                ('IP_address', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('swarm_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drones.swarm')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drones.user')),
            ],
        ),
        migrations.CreateModel(
            name='AP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SSID', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('auth_method', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drones.user')),
            ],
        ),
    ]
