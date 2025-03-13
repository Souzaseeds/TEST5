# KNSAI

# Installation d'Odoo 18 en local

Ce projet contient les scripts nécessaires pour installer Odoo 18 en local sur Windows.

## Prérequis

- Python 3.10 ou supérieur
- PostgreSQL 15 ou supérieur
- PowerShell

## Installation

1. Exécutez le script d'installation :
```powershell
.\install_odoo.ps1
```

2. Pour restaurer votre base de données :
```powershell
.\restore_database.ps1 -DumpFile chemin/vers/votre/dump.sql
```

3. Pour démarrer Odoo :
```powershell
.\odoo-venv\Scripts\python.exe odoo-bin -c odoo.conf
```

## Configuration

- L'interface web sera accessible à l'adresse : http://localhost:8069
- Identifiants par défaut :
  - Email : admin
  - Mot de passe : admin

## Notes importantes

- Assurez-vous que PostgreSQL est en cours d'exécution avant de lancer Odoo
- Le mot de passe de la base de données est configuré sur 'odoo' par défaut
- Pour la synchronisation avec Odoo.sh, utilisez Git pour gérer vos modifications