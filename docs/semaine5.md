# Semaine 5 : l'interface, notes du binôme

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

Parce que l'interface est un client du service déployé, pas le service lui-même : elle ne parle que HTTP à l'API du TP3 corrigée au TP4. Le modèle, le seuil d'abstention et les règles de validation vivent à un seul endroit ; l'API peut être redéployée, remplacée ou mise à l'échelle sans toucher à l'interface, et l'interface pourrait être un site, une application mobile ou la page d'un collègue sans changer une ligne de modèle. En mémoire aussi, l'interface n'a jamais à charger scikit-learn ni un `.joblib`, et elle ne peut pas se désynchroniser d'une version du modèle.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Elle affiche « Je ne sais pas : à faire vérifier par un humain », avec la confiance (52 % pour `xqzvb wlkptr grombu`) et le message « La confiance est sous le seuil d'abstention : un humain doit trancher. » C'est mieux qu'un verdict forcé parce que sous 0,60 la prédiction n'est pas fiable : forcer POSITIVE ou NEGATIVE afficherait une erreur avec l'assurance d'un résultat sûr, alors qu'ici l'avis est explicitement routé vers une personne qui peut trancher.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

API arrêtée, la page affiche « API injoignable : lancez d'abord uvicorn api.main:app » en haut, et chaque analyse renvoie le même message au lieu d'un verdict : l'utilisateur comprend que c'est le service qui manque, pas son texte. Le fichier d'exemple contient 6 avis : le résumé affiché est `{'INDETERMINE': 1, 'NEGATIVE': 2, 'POSITIVE': 3}`, donc **1 avis sur 6** (l'avis en mots inventés) part vers un humain.
