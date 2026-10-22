# Semaine 2 : le modèle, notes du binôme

## 1. Quelles erreurs, et pourquoi ?

Sur le jeu de démonstration, le modèle se trompe 7 fois sur 58 avis (matrice : 27 vrais négatifs, 2 faux positifs, 5 faux négatifs, 24 vrais positifs) ; les trois exemples affichés par `evaluate.py` sont tous des avis mitigés, du type « Taille trop petite et retour payant au déballage, sauf que ensuite produit conforme ».

La cause est la représentation en sac de mots : le `TfidfVectorizer` compte les termes mais ignore leur ordre, donc le retournement (« sauf que ensuite », « mais finalement ») qui donne le sentiment final est invisible au modèle, et les mots positifs et négatifs se compensent.

Pour corriger cela il faudrait une représentation qui tienne compte de l'ordre et du contexte — des embeddings de phrases (semaine 9) ou un modèle séquentiel —, quitte à accepter un temps d'entraînement plus long.

## 2. Les deux mesures

| Jeu | Avis | F1 macro | Seuil |
| --- | --- | --- | --- |
| `demo` (290 avis, 232/58) | 0,879 | oui |
| `allocine` (20 000 avis, 16 000/4 000) | 0,920 | oui |

`models/metrics.json` est versionné (le modèle, lui, est reconstruit par `python src/train.py`) : la CI peut donc vérifier les métriques sans jamais avoir le `.joblib`.
