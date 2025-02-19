# Analyse de Sentiments avec Interface Web et API
====================================================================

## Table des Matières
---------------

* [Introduction](#introduction)
* [Fonctionnalités](#fonctionnalités)
* [Architecture du Projet](#architecture-du-projet)
* [Installation et Lancement](#installation-et-lancement)
* [Utilisation](#utilisation)
	+ [Interface Web](#interface-web)
	+ [API JSON](#api-json)
* [Gestion de la Base de Données](#gestion-de-la-base-de-données)
* [Automatisation du Réentraînement](#automatisation-du-réentraînement)
* [Dépannage](#dépannage)
* [Licence](#licence)

## Introduction
------------

Ce projet propose une application web pour l'analyse de sentiments de tweets, utilisant une régression logistique avec des caractéristiques extraites via un TfidfVectorizer. L'application permet aux utilisateurs de saisir des tweets, de prédire leur sentiment et d'annoter les résultats pour enrichir le dataset.

## Fonctionnalités
-------------

* **Analyse de sentiments** : Prédiction du score de sentiment (entre -1 et 1) en se basant sur les tweets.
* **Interface Web** : Saisie d’un tweet, prédiction du sentiment, puis annotation par l’utilisateur pour enrichir le dataset.
* **API JSON** : Endpoint `/analyze` pour obtenir des prédictions en JSON (compatible Postman, curl, etc.).
* **Stockage en base de données** : Utilisation de MySQL (dans Docker) pour stocker les tweets annotés.
* **Réentraînement du modèle** : Possibilité de réentraîner le modèle avec les données mises à jour.

## Architecture du Projet
---------------------

* `app.py` : Application Flask et endpoints web/API
* `config.py` : Configurations (DB, chemin du modèle, etc.)
* `db.py` : Fonctions d’interaction avec MySQL (connexion, création de table)
* `docker-compose.yml` : Configuration Docker pour MySQL
* `insert_data.py` : Script pour insérer des données initiales (optionnel)
* `model.py` : Modèle de ML (régression logistique + TfidfVectorizer)
* `train.py` : Script d’entraînement/réentraînement du modèle
* `requirements.txt` : Liste des dépendances Python

## Installation et Lancement
-------------------------

### Prérequis

* Docker et Docker Compose installés
* Python 3.7+ installé
* pip installé

### Étapes d'installation

1. Cloner le dépôt : `git clone <URL_du_repo>`
2. Créer un environnement virtuel et installer les dépendances : `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`
3. Démarrer le conteneur MySQL avec Docker : `docker-compose up -d`
4. Initialiser la base de données : `python db.py`
5. (Optionnel) Insérer des données initiales : `python insert_data.py`
6. Entraîner le modèle de sentiment : `python train.py`
7. Lancer l’application Flask : `python app.py`

## Utilisation
------------

### Interface Web

* Rendez-vous sur `http://127.0.0.1:5000`
* Saisissez un tweet dans le formulaire et cliquez sur Analyser
* Le système affichera le score de sentiment prédit
* Une fois la prédiction affichée, un second formulaire permet à l’utilisateur d’annoter le tweet (positif, négatif ou neutre)

### API JSON

* Envoi d’une requête POST à `/analyze` pour obtenir des prédictions en JSON (compatible Postman, curl, etc.)

## Gestion de la Base de Données
---------------------------

* Pour visualiser les données stockées dans la table tweets, vous pouvez vous connecter au conteneur MySQL : `docker-compose exec mysql mysql -u sentiment_user -p sentiment_db`
* Exécutez `SELECT * FROM tweets;` pour afficher les données

## Automatisation du Réentraînement
------------------------------

* Pour automatiser le réentraînement du modèle avec les nouvelles annotations, vous pouvez utiliser le script `cron_retrain.sh` et configurer un cron job
* N’oubliez pas de donner les permissions d’exécution au script : `chmod +x cron_retrain.sh`

## Dépannage
------------

* MySQL ne démarre pas : Vérifiez que Docker et Docker Compose sont installés et que la commande `docker-compose up -d` s’exécute sans erreur
* Modèle non mis à jour : Assurez-vous de bien exécuter `python train.py` après avoir inséré de nouvelles annotations. Redémarrez ensuite l’application Flask pour charger le nouveau modèle

## Licence
-------

Ce projet est fourni à des fins pédagogiques et peut être librement utilisé et modifié.
