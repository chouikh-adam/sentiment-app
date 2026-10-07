# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Répondre automatiquement aux questions des élèves et des parents sur le règlement intérieur, en citant toujours l'article sur lequel la réponse s'appuie.

## Utilisateur final (obligatoire)

Les élèves, les parents et les agents de la vie scolaire, qui posent leurs questions sur l'intranet ou à l'accueil et attendent une réponse immédiate et sourcée.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(b) La réponse doit être vérifiable : elle est tirée du document existant et l'article cité permet de la contrôler en un clic, ce qu'un modèle génératif seul ne garantit pas. (c) Le volume de questions est important toute l'année, donc récupérer des passages du document coûte bien moins cher qu'un appel de génération à chaque question avec un très grand contexte. (a) On dispose en plus d'un jeu de test annotable à faible coût : quelques dizaines de questions/réponses prises dans le document servent de vérité terrain.

## Données nécessaires et leur origine (obligatoire)

Le règlement intérieur au format PDF ou DOCX tel que publié par l'établissement, découpé en articles, plus une liste des questions fréquentes déjà traitées par la vie scolaire.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur 50 questions de test annotées : exactitude de la citation d'au moins 0,90 et taux de refus correct d'au moins 0,95 quand la question n'a pas de réponse dans le document.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une réponse fausse pourrait donner un droit ou une obligation inexacte à un élève : chaque réponse affiche l'article source, et la vie scolaire relit et valide toute réponse avant qu'elle ne soit diffusée par courriel aux parents.

## Risques éthiques ou de confidentialité (obligatoire)

Le règlement est un document public de l'établissement : aucune donnée personnelle n'est stockée, les questions nominatives sont anonymisées et rien n'est envoyé à un service tiers en dehors de l'intranet de l'école (RGPD, loi 09-08).

## Approche écartée et pourquoi (facultatif)

Modèle génératif seul : il répond vite mais sans source contrôlable, donc non vérifiable (b), et son coût par requête reste élevé face au nombre de questions posées (c).
