# Script d'installation d'Odoo 18 sur Windows

Write-Host "Vérification des prérequis..." -ForegroundColor Green

# Vérifier Python 3.10 ou supérieur
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python n'est pas installé. Installez Python 3.10 ou supérieur." -ForegroundColor Red
    exit 1
}

# Vérifier PostgreSQL
if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
    Write-Host "PostgreSQL n'est pas installé. Installez PostgreSQL 15 ou supérieur." -ForegroundColor Red
    exit 1
}

# Vérifier Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git n'est pas installé. Installez Git pour Windows." -ForegroundColor Red
    exit 1
}

# Supprimer le dossier odoo-18 s'il existe
if (Test-Path "odoo-18") {
    Write-Host "Suppression du dossier odoo-18 existant..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force odoo-18
}

# Étape 1 : Création de l'environnement virtuel Python
Write-Host "Création de l'environnement virtuel Python..." -ForegroundColor Green
python -m venv odoo-venv
& .\odoo-venv\Scripts\Activate.ps1

# Étape 2 : Installation des dépendances requises
Write-Host "Installation des dépendances Python..." -ForegroundColor Green
python -m pip install --upgrade pip wheel setuptools
python -m pip install psycopg2-binary lxml pillow reportlab xlwt openpyxl pandas

# Étape 3 : Clonage du dépôt Odoo 18
Write-Host "Téléchargement d'Odoo 18 depuis GitHub..." -ForegroundColor Green
git clone -b 18.0 --depth=1 https://github.com/odoo/odoo.git odoo-18

# Étape 4 : Création du fichier de configuration Odoo
Write-Host "Création du fichier de configuration Odoo..." -ForegroundColor Green
$odooConfig = @"
[options]
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = ./odoo-18/addons
logfile = odoo.log
"@

New-Item -ItemType Directory -Force -Path "odoo-18" | Out-Null
$odooConfig | Out-File -FilePath "odoo-18/odoo.conf" -Encoding UTF8

# Étape 5 : Création de l'utilisateur PostgreSQL pour Odoo
Write-Host "Configuration de PostgreSQL..." -ForegroundColor Green
$env:PGPASSWORD = "Whosthatguy1337?"
psql -U postgres -c "DO \$\$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'odoo') THEN CREATE USER odoo WITH PASSWORD 'odoo' CREATEDB; END IF; END \$\$;"

Write-Host "Installation terminée avec succès !" -ForegroundColor Green
Write-Host "Pour démarrer Odoo, exécutez :" -ForegroundColor Yellow
Write-Host "cd odoo-18" -ForegroundColor Yellow
Write-Host ".\odoo-venv\Scripts\python.exe odoo-bin -c odoo.conf" -ForegroundColor Yellow 