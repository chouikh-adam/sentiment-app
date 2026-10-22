# Semaine 3 : l'API, notes du binôme

> Deux questions, quelques phrases chacune. Répondez avec ce que vous avez observé, pas avec le cours.

## 1. Pourquoi l'API refuse-t-elle de démarrer sans `models/sentiment.joblib`, plutôt que de démarrer et de répondre 503 ?

Parce que sans modèle aucune requête de prédiction ne peut aboutir : le service serait inutile, et un 503 permanent masquerait la vraie cause derrière une réponse qui ressemble à une panne passagère. En échouant au démarrage (`FileNotFoundError: models/sentiment.joblib absent : lancez python src/train.py`, puis `Application startup failed`), l'API signale immédiatement le déploiement incomplet dans les journaux et empêche de router du trafic vers une instance qui ne sait rien faire.

## 2. Un texte vide est refusé deux fois : par Pydantic, puis par `predict()`. Est-ce redondant ?

Non, c'est une défense en profondeur à deux niveaux. Pydantic protège le contrat de l'API : un client qui envoie `{"text": ""}`, `{}` ou `{"text": 42}` reçoit un **422** qui nomme le champ fautif, avant même d'atteindre le code métier. `predict()` protège le modèle lui-même : il reste appelable directement par les tests, un script ou l'interface Streamlit, sans passer par HTTP, et doit alors refuser de son côté un texte qu'il ne saurait pas traiter. Le premier garde l'API propre, le second garde le modèle sûr quel que soit l'appelant.
