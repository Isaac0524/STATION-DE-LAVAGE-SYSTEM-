from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee

@receiver(post_save, sender=Employee)
def create_user_for_employee(sender, instance, created, **kwargs):
    """Crée un utilisateur Django pour les employés ayant le droit de se connecter"""
    if created and instance.can_login() and not instance.user:
        # Créer un nom d'utilisateur à partir du nom de l'employé
        username = instance.email.split('@')[0]  # Utiliser la partie locale de l'email
        
        # S'assurer que le nom d'utilisateur est unique
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Créer l'utilisateur avec un mot de passe par défaut
        user = User.objects.create_user(
            username=username,
            email=instance.email,
            password='pass1234',  # Mot de passe temporaire à changer
            first_name=instance.name.split()[0] if ' ' in instance.name else instance.name,
            last_name=instance.name.split(' ', 1)[1] if ' ' in instance.name else '',
        )
        
        # Lier l'utilisateur à l'employé
        instance.user = user
        instance.save(update_fields=['user'])