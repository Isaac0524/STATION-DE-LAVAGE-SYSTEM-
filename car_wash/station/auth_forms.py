from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Employee

class EmployeeAuthenticationForm(AuthenticationForm):
    """Formulaire d'authentification personnalisé pour les employés"""
    
    def confirm_login_allowed(self, user):
        """Vérifie si l'utilisateur est associé à un employé autorisé à se connecter"""
        super().confirm_login_allowed(user)
        
        try:
            employee = user.employee
            
            if not employee.is_active:
                raise ValidationError("Votre compte n'est pas actif.", code='inactive_employee')
            
            if not employee.can_login():
                raise ValidationError("Vous n'avez pas les droits pour accéder à cette application.", code='unauthorized_role')
                
        except Employee.DoesNotExist:
            raise ValidationError("Vous n'êtes pas enregistré comme employé dans notre système.", code='not_employee')