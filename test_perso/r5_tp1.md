# R5.10   Tp1

*Source: R5.10 - TP1.pdf*
*Type: PDF*
*Converted: 2026-02-11 14:24 UTC*
*Pages: 1*

---
## Page 1

TP2 – opérations en lecture
Dans ceƩe séance, nous uƟliserons les données du ﬁchier tp1.json importé lors de la séance
précédente. Vous écrirez et exécuterez les requêtes permeƩant d’obtenir les résultats suivants :
1. Le nombre d’appartements dont l’hôte est un « super-hôte »
2. Le nombre d’hôte disƟncts
3. Les diﬀérents équipements disƟncts disponibles dans l’ensemble des appartements
4. Le nombre d’appartements possédant une piscine (« Pool »)
5. Le prix de l’appartement le moins cher
6. Le nombre d’appartements ne possédant PAS le Wiﬁ
7. Le nombre d’appartements avec un nombre de nuits minimum de 1, 2, ou 5 nuits
db.lisƟng.ﬁnd({minimum_nights: { $nin: ["1", "2", "5"]}}).count()
8. Le nombre d’appartements ayant deux chambres ou plus, ainsi que deux salles de bain ou plus
9. Le nombre de propriétés n’ayant pas pour type « Apartment »
10. Le prix de l’appartement le plus cher possédant entre 5 et 10 commentaires (les deux bornes
incluses)
11. La date de mise à jour de la propriété la plus récemment commentée
12. Le nombre d’appartements ne possédant ni détecteurs de fumées, ni exƟncteur
Il vous sera nécessaire pour pouvoir répondre à ces quesƟons d’analyser la structure des données.
Pour cela, un conseil : requêtez un document, et regardez les noms des diﬀérents champs présents
aﬁn de savoir comment concevoir vos requêtes.
