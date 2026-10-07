# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Détecter automatiquement, avant validation, les ordonnances dont un champ obligatoire manque (prescripteur, date, posologie, médicament, dosage).

## Utilisateur final (obligatoire)

Le pharmacien et son assistant à l'accueil, qui consultent l'alerte avant de valider ou de refuser l'ordonnance présentée au comptoir.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(b) La liste des champs obligatoires et les règles de complétude sont connues, stables et lisibles par un humain : chaque refus se justifie en citant la règle enfreinte. (d) Une ordonnance validée à tort peut provoquer un problème de santé grave : la logique doit rester explicite et la décision finale revient au pharmacien. (a) En outre, aucune donnée étiquetée n'existe pour entraîner un modèle, et la production d'un tel jeu annoté coûterait cher pour une tâche purement réglementaire.

## Données nécessaires et leur origine (obligatoire)

Le tableau des champs obligatoires fourni par l'officine et les textes réglementaires de l'ordre des pharmaciens, transcrits en règles de validation ; aucun dossier patient n'est nécessaire pour construire les règles.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur un jeu de test de 200 ordonnances fictives : rappel d'au moins 0,99 sur les ordonnances incomplètes et taux de fausses alertes inférieur à 5 %, pour ne pas bloquer le comptoir.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une ordonnance signalée à tort est confirmée ou rejetée manuellement par le pharmacien : le système n'annule jamais rien seul, il affiche un message et c'est la personne qui décide avant tout traitement.

## Risques éthiques ou de confidentialité (obligatoire)

Données de santé couvertes par la loi 09-08 et le RGPD : règles construites sur des ordonnances fictives ou anonymisées, traitement réalisé localement, aucune donnée patiente envoyée à un service tiers.

## Approche écartée et pourquoi (facultatif)

Machine learning : il faudrait des centaines d'ordonnances annotées qui n'existent pas (a), et un modèle boîte noire n'expliquerait pas au pharmacien pourquoi l'ordonnance est rejetée alors que la conséquence d'une erreur est élevée (d).
