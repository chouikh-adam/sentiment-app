# sentiment-app

Application fil rouge du cours *Développement et déploiement d'applications intelligentes*,
menée jusqu'au TP5 : cadrage, modèle de sentiment, API FastAPI, tests approfondis et interface
Streamlit.

## Démarrage

Python 3.11 ou plus récent (testé avec 3.12.10).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/make_demo.py      # jeu de démonstration (reproductible, sans réseau)
python src/train.py          # entraîne models/sentiment.joblib
pytest -q
```

Lancer l'API :

```powershell
uvicorn api.main:app --reload
```

Documentation interactive sur <http://127.0.0.1:8000/docs>.

Lancer l'interface :

```powershell
streamlit run ui/app.py
```

## Structure

```text
sentiment-app/
├── api/                  # API FastAPI : /health, /predict
├── src/                  # démonstration, entraînement, évaluation, prédiction, seuil, bilan
├── ui/                   # interface Streamlit
├── data/                 # jeu d'or (20 avis) et avis d'exemple
├── models/               # metrics.json (le modèle .joblib reste local, jamais versionné)
├── tests/                # tests TP1 à TP5
├── docs/                 # cadrage, comptes rendus, journal et captures
├── scripts/              # installation et diagnostic
├── .github/workflows/    # CI : tests, couverture, ruff, mypy
├── pyproject.toml        # ruff, mypy, couverture
└── .pre-commit-config.yaml
```

## Résultats

| Étape | Résultat |
| --- | --- |
| Modèle de démonstration | F1 = 0,879 (58 avis de test) |
| Modèle Allociné | F1 = 0,920 (20 000 avis) |
| Couverture de `api/` | 98,86 % (seuil 95 %) |
| `ruff` / `mypy` | aucun problème |
| `pytest` | 94 passed, 2 xfailed, 1 failed |

Le test `test_each_member_has_committed` attend deux auteurs de commits : ce dépôt est un
travail individuel, il reste donc rouge. Les deux `xfail` sont deux erreurs franches connues
du jeu d'or (négation et hors-domaine), documentées dans `docs/journal-tp1-tp5.md`.

## Auteur

Adam Chouikh — [@chouikh-adam](https://github.com/chouikh-adam)
