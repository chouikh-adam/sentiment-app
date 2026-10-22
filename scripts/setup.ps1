# Mise en place complète du poste pour le TP1 (Windows PowerShell).
# Usage : powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "1/4 Vérification de Python"
# Le cours cible Python 3.11. Si la machine n'a pas exactement 3.11,
# on prend la version la plus proche disponible (3.10 de preference).
$versions = @()
try { $versions = & py -0 2>$null } catch { $versions = @() }
$disponibles = @()
foreach ($ligne in $versions) {
    if ($ligne -match '-V:(\d+\.\d+)') { $disponibles += $matches[1] }
}
$preferee = $disponibles | Where-Object { $_ -eq "3.11" } | Select-Object -First 1
if (-not $preferee) {
    $preferee = $disponibles | Where-Object { $_ -match '^3\.(1[0-9]|[2-9][0-9])$' } |
                Sort-Object -Descending | Select-Object -First 1
}
if (-not $preferee) {
    throw "Aucune version de Python 3.10 ou superieur detectee (py -0). Installez Python depuis python.org."
}
Write-Host "Python utilise : py -$preferee (le cours vise 3.11)"
& py -$preferee --version

Write-Host "2/4 Création de l'environnement virtuel"
if (-not (Test-Path ".venv")) { & py -$preferee -m venv .venv }
& .\.venv\Scripts\Activate.ps1

Write-Host "3/4 Installation des dépendances"
python -m pip install --upgrade pip
pip install -r requirements.txt
pip freeze | Out-File -Encoding utf8 requirements.lock

Write-Host "4/4 Diagnostic"
python scripts\check_setup.py
