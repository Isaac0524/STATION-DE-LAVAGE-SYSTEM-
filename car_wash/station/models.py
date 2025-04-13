# station/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Client(models.Model):
    LOYALTY_STATUS = (
        ('new', 'Nouveau'),
        ('regular', 'Régulier'),
        ('vip', 'VIP'),
    )
    
    name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Téléphone", max_length=20)
    car_model = models.CharField("Modèle de voiture", max_length=100)
    license_plate = models.CharField("Immatriculation", max_length=20)
    loyalty_status = models.CharField("Statut fidélité", max_length=10, choices=LOYALTY_STATUS, default='new')
    loyalty_points = models.IntegerField("Points fidélité", default=0)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    last_visit = models.DateTimeField("Dernière visite", null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.license_plate})"
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

class Service(models.Model):
    name = models.CharField("Nom", max_length=100)
    description = models.TextField("Description")
    price = models.DecimalField("Prix", max_digits=6, decimal_places=2)
    duration = models.IntegerField("Durée (minutes)")
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    is_active = models.BooleanField("Actif", default=True)
    
    def __str__(self):
        return f"{self.name} - {self.price}FCFA"
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

class Employee(models.Model):
    ROLE_CHOICES = (
        ('laveur', 'Laveur'),
        ('technicien', 'Technicien Polish'),
        ('accueil', 'Responsable Accueil'),
        ('manager', 'Manager'),
    )
    
    name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=20)
    role = models.CharField("Poste", max_length=20, choices=ROLE_CHOICES)
    hire_date = models.DateField("Date d'embauche")
    is_active = models.BooleanField("Actif", default=True)
    
    # Nouveau champ pour lier l'employé à un utilisateur Django
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee')
    
    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"
    
    def can_login(self):
        """Vérifie si l'employé a le droit de se connecter à l'application"""
        return self.role in ['accueil', 'manager'] and self.is_active
    
    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'À venir'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    )
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments', verbose_name="Client")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments', verbose_name="Service")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments', verbose_name="Employé assigné")
    date = models.DateField("Date")
    time = models.TimeField("Heure")
    status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField("Notes", blank=True)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    
    def __str__(self):
        return f"{self.client} - {self.service} - {self.date}"
    
    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['date', 'time']