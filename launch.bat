@echo off
setlocal
chcp 65001

REM :: Vérifie si nous avons les droits d'administrateur
REM net file 1>nul 2>nul && goto :hasAdminRights

REM :: Élève le script
REM wscript //nologo Elevate.vbs "%~dpnx0"

:hasAdminRights

:: Afficher le début du script
echo Démarrage du script de lancement...

:: Définition des variables
set VENV_NAME=venv
set VENV_PATH=.\%VENV_NAME%\Scripts
set PYTHON_EXE=

:: Trouver l'exécutable Python
for /f "delims=" %%I in ('where python 2^>NUL') do (
    set PYTHON_EXE="%%~I"
    goto :FoundPython
)

:FoundPython
if not defined PYTHON_EXE (
    echo Aucun exécutable Python trouvé. Veuillez installer Python et l'ajouter à votre PATH.
    goto :EOF
)

:: Vérification de la version de Python
%PYTHON_EXE% -c "import sys; sys.exit(1 if sys.version_info < (3, 6) else 0)" 2>NUL
if errorlevel 1 (
    echo Python 3.6 ou supérieur est requis. Veuillez installer ou mettre à jour Python.
    goto :EOF
)

:: Création de l'environnement virtuel si nécessaire
if not exist %VENV_NAME% (
    echo L'environnement virtuel %VENV_NAME% n'existe pas. Création en cours...
    %PYTHON_EXE% -m venv %VENV_NAME%
)

:: Vérification de l'activation de l'environnement virtuel
if not defined VIRTUAL_ENV (
    echo L'environnement virtuel n'est pas activé. Activation en cours...
    call %VENV_PATH%\activate
)

:: Mise à jour de pip et installation des dépendances
echo Mise à jour de pip...
python.exe -m pip install --upgrade pip
echo Installation des dépendances...
pip install -r requirements.txt

:: Exécution du script Python
echo Démarrage de l'application...
python gui.py

:: Désactivation de l'environnement virtuel
echo Désactivation de l'environnement virtuel...
deactivate

:: Afficher la fin du script
echo Fin du script de lancement...

:: Fin du script
endlocal