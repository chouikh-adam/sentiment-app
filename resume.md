# Résumé du TP1 : les deux difficultés rencontrées

**Module :** Développement et déploiement d'applications intelligentes — semaine 1
**Auteur :** Adam Chouikh
**Dépôt :** https://github.com/adam2005chouikh-ctrl/sentiment-app

---

## Difficulté 1 : Python 3.11 absent du poste alors que le kit l'impose

**Ce qui s'est passé.** Le poste ne dispose que de Python 3.14 (version par défaut) et de Python 3.12 ; Python 3.11 n'est pas installé. Or le script `scripts/setup.ps1` du kit écrit `py -3.11` en dur dès la première étape : il s'arrête immédiatement avec `No suitable Python runtime found`, et rien d'autre (venv, dépendances, diagnostic) n'est fait.

```text
PS C:\sentiment-app> py -3.11 --version
py : No suitable Python runtime found
Pass --list (-0) to see all detected environments on your machine
or set environment variable PYLAUNCHER_ALLOW_INSTALL to use winget
or open the Microsoft Store to the requested version.
```

![Erreur py -3.11 : aucun runtime disponible](captures/difficulte1-python-3.11-absent.png)

**Pourquoi c'est bloquant.** Le 3.14 par défaut n'est pas une solution de repli : les versions figées du `requirements.txt` (`pandas==2.2.*`, `scikit-learn==1.5.*`, `pyarrow==21.0.*`) ne publient pas de wheels pour Python 3.14, l'installation de ces paquets échouerait.

**Résolution.** Création de l'environnement virtuel avec la seule version compatible présente sur le poste, `py -3.12 -m venv .venv`, et adaptation de `scripts/setup.ps1` pour détecter Python disponible au lieu de forcer 3.11. Contrôle passé : `python scripts/check_setup.py` ne remonte plus aucune erreur liée à Python, et `pytest tests/test_cadrage.py -q` affiche **12 passed**.

---

## Difficulté 2 : réseau instable vers PyPI (installation des dépendances)

**Ce qui s'est passé.** Les téléchargements depuis `pypi.org` / `files.pythonhosted.org` sont interrompus en pleine progression : les tentatives de téléchargement du wheel de pandas (9,7 Mo) tombent en timeout puis en lecture incomplète, et `pip abandonne au bout de plusieurs relances. Le même phénomène a bloqué l'installation de l'intégralité de `requirements.txt`.

```text
PS C:\sentiment-app> .venv\Scripts\python -m pip install -r requirements.txt
Retrying ... after connection broken by 'ReadTimeoutError("HTTPSConnectionPool(
host='pypi.org', port=443): Read timed out. (read timeout=90.0)")': /simple/pandas/
WARNING: Connection interrupted while downloading (0 bytes/9.7 MB, attempt 4)
ERROR: Could not install packages due to an OSError: ('Connection broken:
IncompleteRead(16384 bytes read, 310091 more expected)', ...)
ERROR: Could not find a version that satisfies the requirement dvc==3.55.*
```

![Erreurs pip : timeouts et lecture incomplète](captures/difficulte2-reseau-pypi.png)

**Pourquoi c'est bloquant.** Sans `pandas` et `scikit-learn`, les tests d'environnement (`test_environment.py`) échouent et `scripts/check_setup.py` affiche des erreurs ; le diagnostic final du TP n'est donc pas vert.

**Résolution.** Installation étape par étape au lieu d'un seul bloc : `pytest` d'abord (léger, débloque immédiatement le contrôle des fiches de cadrage), puis les paquets cœur avec `--retries 20 --timeout 90`, puis le reste de `requirements.txt` en tâche de fond avec relance du script à chaque échec. La difficulté est contournée tant que la connexion se dégrade ; en salle, un réseau filaire ou un point d'accès plus stable lève le problème en une seule exécution.

---

## État d'avancement à la fin de cette session

| Élément | État |
| --- | --- |
| Trois fiches de cadrage remplies | `pytest tests/test_cadrage.py -q` → **12 passed** |
| Dépôt GitHub privé créé et poussé | branche `main`, 42 fichiers |
| `README.md` | tableau du binôme complété (Adam Chouikh) |
| Environnement virtuel | `.venv` en Python 3.12 |
| Dépendances complètes | en cours : instabilité réseau (difficulté 2) |
| Auteur unique des commits | 1 auteur — le test « un commit par membre » passe dès que le binôme pousse son commit |
