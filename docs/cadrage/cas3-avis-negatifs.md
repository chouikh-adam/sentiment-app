# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Classer automatiquement les avis clients en négatifs, neutres et positifs pour que l'équipe service client traite d'abord les avis négatifs.

## Utilisateur final (obligatoire)

L'équipe du service client et la modération du site, qui reçoit une file d'avis triée par priorité au lieu de devoir les lire tous dans l'ordre de publication.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Des milliers d'avis sont publiés chaque mois et un échantillon se relit en quelques heures pour produire des données étiquetées, ce qui rend la tâche apprenable. (c) Le volume est trop important pour appeler un LLM à chaque avis : un classifieur entraîné coûte presque rien par requête. (d) La conséquence d'une erreur est faible : un avis mal classé est simplement remis au bon endroit par la modération, sans décision irréversible.

## Données nécessaires et leur origine (obligatoire)

Les avis publics du site e-commerce exportés avec leur texte et leur note, étiquetés à la main sur un échantillon de 1 000 avis ; les noms, numéros de commande et adresses sont supprimés avant tout traitement.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur un jeu de test tenu à l'écart : rappel d'au moins 0,90 sur la classe négative et F1 macro d'au moins 0,85, pour être sûr de ne pas rater un avis client mécontent.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis négatif classé à tort reste visible dans la file principale : la modération corrige l'étiquette d'un clic et l'erreur alimente le jeu d'entraînement, aucune décision client n'est prise sans relecture humaine.

## Risques éthiques ou de confidentialité (obligatoire)

Un avis peut contenir un nom, une adresse ou un numéro de commande : anonymisation avant stockage, dataset public fictif ou anonymisé uniquement, et aucun envoi de données clients vers un service externe (RGPD, loi 09-08).

## Approche écartée et pourquoi (facultatif)

Règles par mots-clés : testées sur un échantillon, elles ne détectent que l'absence d'étoiles et ratent l'ironie et les formulations imprévues, donc rappel insuffisant sur la classe négative.
