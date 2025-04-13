from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Client, Service, Employee, Appointment
from .forms import ClientForm, ServiceForm, EmployeeForm, AppointmentForm
from .auth_forms import EmployeeAuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Fonction pour vérifier les permissions
def check_employee_permissions(request, required_roles=None):
    """
    Vérifie si l'employé connecté a les permissions nécessaires
    required_roles: liste des rôles autorisés
    """
    if not request.user.is_authenticated:
        return False
    
    try:
        employee = request.user.employee
        if not employee.is_active:
            return False
        
        # Si c'est un manager, il a toutes les permissions
        if employee.role == 'manager':
            return True
        
        # Si des rôles spécifiques sont requis, vérifier si l'employé a un de ces rôles
        if required_roles and employee.role not in required_roles:
            return False
        
        return True
    except:
        return False

# Vue de connexion
def login_view(request):
    if request.method == 'POST':
        form = EmployeeAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.employee.name}!")
            return redirect('dashboard')
    else:
        form = EmployeeAuthenticationForm()
    
    return render(request, 'station/login.html', {'form': form})

# Vue de déconnexion
def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')

# Vue pour changer le mot de passe
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important pour maintenir la session
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès!')
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'station/change_password.html', {'form': form})

# Vue du tableau de bord
@login_required(login_url='login')
def dashboard(request):
    # Vérifier si l'utilisateur a les permissions
    if not check_employee_permissions(request):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
        return redirect('login')
    
    # Comptage des clients
    total_clients = Client.objects.count()
    
    # Rendez-vous du jour
    today = timezone.now().date()
    today_appointments = Appointment.objects.filter(date=today).order_by('time')
    
    # Employés actifs
    active_employees = Employee.objects.filter(is_active=True).count()
    
    # Revenu journalier (simulé pour l'exemple)
    daily_revenue = Appointment.objects.filter(
        date=today, 
        status='completed'
    ).aggregate(total=Sum('service__price'))['total'] or 0
    
    context = {
        'total_clients': total_clients,
        'today_appointments_count': today_appointments.count(),
        'active_employees': active_employees,
        'daily_revenue': daily_revenue,
        'recent_appointments': today_appointments[:5]  # 5 rendez-vous récents
    }
    return render(request, 'station/dashboard.html', context)

# Vues pour les clients
@login_required(login_url='login')
def client_list(request):
    # Responsable accueil ou manager
    if not check_employee_permissions(request, ['accueil', 'manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour gérer les clients.")
        return redirect('dashboard')
    
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'station/clients.html', {'clients': clients})

@login_required(login_url='login')
def client_create(request):
    # Responsable accueil ou manager
    if not check_employee_permissions(request, ['accueil', 'manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour créer des clients.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client ajouté avec succès.')
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'station/client_form.html', {'form': form})

@login_required(login_url='login')
def client_edit(request, pk):
    # Responsable accueil ou manager
    if not check_employee_permissions(request, ['accueil', 'manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour modifier des clients.")
        return redirect('dashboard')
    
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client modifié avec succès.')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'station/client_form.html', {'form': form, 'client': client})

@login_required(login_url='login')
def client_delete(request, pk):
    # Responsable accueil ou manager
    if not check_employee_permissions(request, ['accueil', 'manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour supprimer des clients.")
        return redirect('dashboard')
    
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client supprimé avec succès.')
        return redirect('client_list')
    return render(request, 'station/client_confirm_delete.html', {'client': client})

# Vues pour les services
@login_required(login_url='login')
def service_list(request):
    # Manager uniquement
    if not check_employee_permissions(request, ['manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour gérer les services.")
        return redirect('dashboard')
    
    services = Service.objects.all().order_by('name')
    return render(request, 'station/services.html', {'services': services})

@login_required(login_url='login')
def service_create(request):
    # Manager uniquement
    if not check_employee_permissions(request, ['manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour créer des services.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service ajouté avec succès.')
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'station/service_form.html', {'form': form})

@login_required(login_url='login')
def service_edit(request, pk):
    # Manager uniquement
    if not check_employee_permissions(request, ['manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour modifier des services.")
        return redirect('dashboard')
    
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service modifié avec succès.')
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'station/service_form.html', {'form': form, 'service': service})

@login_required(login_url='login')
def service_delete(request, pk):
    # Manager uniquement
    if not check_employee_permissions(request, ['manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour supprimer des services.")
        return redirect('dashboard')
    
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service supprimé avec succès.')
        return redirect('service_list')
    return render(request, 'station/service_confirm_delete.html', {'service': service})

# Vues pour les employés
@login_required(login_url='login')
def employee_list(request):
    # Manager uniquement
    if not check_employee_permissions(request, ['manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour gérer les employés.")
        return redirect('dashboard')
    
    employees = Employee.objects.all().order_by('name')
    return render(request, 'station/employees.html', {'employees': employees})

@login_required(login_url='login')
def employee_create(request):
    # Manager uniquement
    if not check_employee_permissions(request, ['manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour créer des employés.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employé ajouté avec succès.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'station/employee_form.html', {'form': form})

@login_required(login_url='login')
def employee_edit(request, pk):
    # Manager uniquement
    if not check_employee_permissions(request, ['manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour modifier des employés.")
        return redirect('dashboard')
    
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employé modifié avec succès.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'station/employee_form.html', {'form': form, 'employee': employee})

@login_required(login_url='login')
def employee_delete(request, pk):
    # Manager uniquement
    if not check_employee_permissions(request, ['manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour supprimer des employés.")
        return redirect('dashboard')
    
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employé supprimé avec succès.')
        return redirect('employee_list')
    return render(request, 'station/employee_confirm_delete.html', {'employee': employee})


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important pour maintenir la session
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès!')
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'station/change_password.html', {'form': form})

# Vues pour les rendez-vous
@login_required(login_url='login')
def appointment_list(request):
    # Responsable accueil ou manager
    if not check_employee_permissions(request, ['accueil', 'manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour gérer les rendez-vous.")
        return redirect('dashboard')
    
    # Filtrage des rendez-vous
    filter_date = request.GET.get('date', None)
    filter_status = request.GET.get('status', None)
    
    appointments = Appointment.objects.all()
    
    # Appliquer les filtres
    if filter_date:
        appointments = appointments.filter(date=filter_date)
    else:
        # Par défaut, montrer les rendez-vous d'aujourd'hui et à venir
        today = timezone.now().date()
        appointments = appointments.filter(date__gte=today)
    
    if filter_status and filter_status != 'all':
        appointments = appointments.filter(status=filter_status)
    
    # Organiser les rendez-vous par jour
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    week_end = today + timedelta(days=6)
    
    today_appointments = appointments.filter(date=today).order_by('time')
    tomorrow_appointments = appointments.filter(date=tomorrow).order_by('time')
    week_appointments = appointments.filter(date__gt=tomorrow, date__lte=week_end).order_by('date', 'time')
    
    context = {
        'today_appointments': today_appointments,
        'tomorrow_appointments': tomorrow_appointments,
        'week_appointments': week_appointments,
        'filter_date': filter_date,
        'filter_status': filter_status,
    }
    return render(request, 'station/appointments.html', context)

@login_required(login_url='login')
def appointment_create(request):
    # Responsable accueil ou manager
    if not check_employee_permissions(request, ['accueil', 'manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour créer des rendez-vous.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rendez-vous ajouté avec succès.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'station/appointment_form.html', {'form': form})

@login_required(login_url='login')
def appointment_edit(request, pk):
    # Responsable accueil ou manager
    if not check_employee_permissions(request, ['accueil', 'manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour modifier des rendez-vous.")
        return redirect('dashboard')
    
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rendez-vous modifié avec succès.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'station/appointment_form.html', {'form': form, 'appointment': appointment})

@login_required(login_url='login')
def appointment_delete(request, pk):
    # Responsable accueil ou manager
    if not check_employee_permissions(request, ['accueil', 'manager']):
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour supprimer des rendez-vous.")
        return redirect('dashboard')
    
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Rendez-vous supprimé avec succès.')
        return redirect('appointment_list')
    return render(request, 'station/appointment_confirm_delete.html', {'appointment': appointment})