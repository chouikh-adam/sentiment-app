# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Uniquement des chiffres issus de VOS exécutions.

## 1. Couverture

- Avant (étape A) : **91 %** de `api/`, 6 lignes jamais exécutées, toutes dans `main.py` :
  - ligne 49 : le `503` de `_classifier()` quand `app.state` n'a pas de modèle ; aucun test ne démarrait l'API sans modèle ;
  - lignes 77-79 : le `500` d'une exception inattendue du modèle ; aucun test ne provoquait de panne ;
  - lignes 85-87 : le bloc `if __name__ == "__main__":`, qui ne s'exécute que lancé directement.
- Les deux premières situations sont désormais couvertes par `tests/test_integration.py` (D.3 et D.4).
- Après (étape D) : **98,86 %** ; seule la ligne 37 de `model.py` reste non couverte (le refus de démarrer sur des classes inconnues, qui exigerait un faux modèle). Une seule exclusion : le bloc `if __name__ == "__main__":` de `main.py`, justifié ci-dessus (ce n'est pas une ligne de l'application, c'est le lanceur local).

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| `{"text": "   "}` répondait 422 mais avec `detail` en **chaîne**, alors que les autres refus ont `detail` en liste | `test_frontieres_du_contrat` (cas `texte-blancs`, B.1/B.2) | `field_validator` dans `api/schemas.py` : un texte vide après `str.strip()` est refusé par Pydantic (`B.4`) |
| `ValueError` du modèle était convertie en 422, donc une panne interne ressemblait à une faute du client | `test_panne_du_modele_renvoie_500_sans_message_interne` avec `ValueError("bug interne")` (D.4) | suppression du `except ValueError` dans `api/main.py` : toute exception répond 500, journalisée |
| `ruff` : 11 remarques au départ (dont `E741` sur des variables `l`, `B905` sur des `zip()` sans `strict=`, `B904` sur le `raise` dans un `except`) | `ruff check .` (T21), puis CI | corrections à la main, aucun `# noqa` ajouté sauf `E402` déjà justifié par le `sys.path` de `model.py` |

## 3. Seuil d'abstention

- Points de la courbe (`python src/courbe_seuil.py`, jeu de test : 58 avis) :
  - seuil 0,50 : 58 réponses (100 %), exactitude 0,879, 7 erreurs, 0 vers un humain ;
  - seuil 0,60 : 42 réponses (72 %), exactitude 0,952, 2 erreurs, 16 vers un humain ;
  - seuil 0,70 : 37 réponses (64 %), exactitude 1,000, 0 erreur, 21 vers un humain.
- Seuil retenu : **0,60** (`SEUIL_ABSTENTION` dans `api/model.py`) ; **16 avis sur 58 (28 %)** partent vers un humain. Justification : il évite 5 des 7 erreurs du TP2 tout en laissant le modèle répondre à près de trois quarts des avis ; à 0,70 il ne reste plus aucune erreur mais 36 % des avis passent à l'humain, pour un gain d'exactitude nul sur ceux auxquels on répond.

## 4. Jeu d'or

- Bilan (`python src/bilan_jeu_or.py`, 20 avis écrits par nous) : **9 justes, 9 abstentions, 2 erreurs franches déclarées**.
- Les deux erreurs déclarées (`erreur_connue`, `xfail(strict=True)`) : « Scénario vide et acteurs fades » (hors domaine cinéma) et « Je ne le recommande pas du tout » (négation) — toutes deux prédites POSITIVE à 0,64 et 0,60.
- Ce que ces chiffres disent du modèle : le seuil protège contre l'erreur franche (9 abstentions) au prix de la couverture ; les erreurs qui restent sont exactement les limites annoncées du sac de mots (négation, ordre, domaine). Les avis mitigés et ironiques passent presque tous en abstention, ce qui est le comportement attendu.

## 5. Outils statiques

- Remarques au départ : ruff **11** erreurs, mypy **0** (`Success: no issues found in 4 source files`).
- Parmi les défauts de la partie 2, ruff avait signalé le `B904` et les `E741`/`B905`, mais **pas** le défaut de contrat (`"   "` en 422-string) ni la conversion abusive de `ValueError` en 422 : mypy ne les voyait pas non plus, parce que `predict()` renvoyait un `dict` sans précision (des `Any` que mypy ne vérifie pas). Depuis, `TypedDict` (TP2 et `api/model.py`) et `Literal` sur les étiquettes font vérifier le contrat ; `ruff` et `mypy` restent muets après correction.
