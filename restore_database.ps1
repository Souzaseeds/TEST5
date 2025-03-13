# Script de restauration de la base de données Odoo

param(
    [Parameter(Mandatory=$true)]
    [string]$DumpFile
)

# Vérifier que le fichier de dump existe
if (-not (Test-Path $DumpFile)) {
    Write-Host "Le fichier de dump $DumpFile n'existe pas." -ForegroundColor Red
    exit 1
}

# Créer la base de données
Write-Host "Création de la base de données..." -ForegroundColor Green
$dbName = [System.IO.Path]::GetFileNameWithoutExtension($DumpFile)
createdb -U odoo $dbName

# Restaurer le dump
Write-Host "Restauration du dump..." -ForegroundColor Green
psql -U odoo -d $dbName -f $DumpFile

Write-Host "Restauration terminée !" -ForegroundColor Green
Write-Host "Base de données créée : $dbName" -ForegroundColor Yellow 