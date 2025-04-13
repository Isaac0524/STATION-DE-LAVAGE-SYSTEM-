# STATION-DE-LAVAGE-SYSTEM

## Description
Un système de gestion complet pour stations de lavage automobile, développé avec Django. Cette application permet aux gérants de stations de lavage de gérer efficacement leurs opérations quotidiennes, incluant la gestion des clients, des services, des réservations et de la facturation.

## Fonctionnalités
- Interface de connexion sécurisée avec support du thème clair/sombre
- Gestion des clients et des véhicules
- Suivi des services de lavage et prestations
- Système de facturation intégré
- Tableau de bord d'administration

## Technologies utilisées
- Django 4.2.7
- MySQL 2.2.0
- Pillow 10.1.0
- Django Crispy Forms 2.0
- TailwindCSS
- Font Awesome

## Installation

### Prérequis
- Python 3.8 ou supérieur
- MySQL
- Environnement virtuel Python (recommandé)

### Étapes d'installation
1. Cloner le dépôt
```bash
git clone https://github.com/Isaac0524/STATION-DE-LAVAGE-SYSTEM-.git
cd STATION-DE-LAVAGE-SYSTEM-
```

2. Créer et activer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer la base de données
   - Créer une base de données MySQL
   - Modifier les paramètres de connexion dans `car_wash/settings.py`

5. Appliquer les migrations
```bash
python manage.py migrate
```

6. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

7. Lancer le serveur de développement
```bash
python manage.py runserver
```

## Structure du projet
```
car_wash/                  # Dossier principal du projet
├── car_wash/              # Configuration Django
├── station/               # Application pour la gestion des stations
│   ├── models.py          # Modèles de données
│   ├── views.py           # Logique de l'application
│   ├── urls.py            # Configuration des URLs
│   └── templates/         # Templates HTML
├── manage.py              # Script de gestion Django
└── requirements.txt       # Dépendances du projet
```

## Utilisation
1. Accédez à l'interface d'administration via `/admin/`
2. Connectez-vous avec les identifiants du superutilisateur
3. Commencez à configurer votre station de lavage en ajoutant des services, des employés, etc.
4. Utilisez l'interface principale pour les opérations quotidiennes

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence
Ce projet est sous licence [MIT](LICENSE).

## Contact
Isaac0524 - [GitHub](https://github.com/Isaac0524)
