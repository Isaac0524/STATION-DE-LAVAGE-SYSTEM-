# Generated by Django 5.2 on 2025-04-10 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('car_model', models.CharField(max_length=100, verbose_name='Modèle de voiture')),
                ('license_plate', models.CharField(max_length=20, verbose_name='Immatriculation')),
                ('loyalty_status', models.CharField(choices=[('new', 'Nouveau'), ('regular', 'Régulier'), ('vip', 'VIP')], default='new', max_length=10, verbose_name='Statut fidélité')),
                ('loyalty_points', models.IntegerField(default=0, verbose_name='Points fidélité')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('last_visit', models.DateTimeField(blank=True, null=True, verbose_name='Dernière visite')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('role', models.CharField(choices=[('laveur', 'Laveur'), ('technicien', 'Technicien Polish'), ('accueil', 'Responsable Accueil'), ('manager', 'Manager')], max_length=20, verbose_name='Poste')),
                ('hire_date', models.DateField(verbose_name="Date d'embauche")),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Employé',
                'verbose_name_plural': 'Employés',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Prix')),
                ('duration', models.IntegerField(verbose_name='Durée (minutes)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('time', models.TimeField(verbose_name='Heure')),
                ('status', models.CharField(choices=[('scheduled', 'À venir'), ('in_progress', 'En cours'), ('completed', 'Terminé'), ('cancelled', 'Annulé')], default='scheduled', max_length=20, verbose_name='Statut')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='station.client', verbose_name='Client')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='station.employee', verbose_name='Employé assigné')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='station.service', verbose_name='Service')),
            ],
            options={
                'verbose_name': 'Rendez-vous',
                'verbose_name_plural': 'Rendez-vous',
                'ordering': ['date', 'time'],
            },
        ),
    ]
