# Openstack-Lottery

Bienvenue sur le repo du projet HPE Ensimag 2016-2017.

## Contenu du repo

* **deployment** : Partie déploiement
	+ **ansible** : playbook pour le déploiement de l'infrastructure
	+ **heat** : templates de construction de l'infrastructure
	+ **deploy.py** : script python de déploiement
	+ **service.sh** : script de création du service unix
* **doc** : documentation de spécification du projet fournit par HP
* **external** : ressources externe au projet (BDD)
* **services** : code python des 5 services développés (I,B,P,W et S)
* **web_app_** : code python de l'application web

## Déploiement

Le déploiement s'effectue en exécutant un seul script Python

	python2 ./deploy.sh

## Accès à l'application web

http://*adresse ip serveur*:80/

## Contacts

- [Clément Taboulot](mailto:clement.taboulot@grenoble-inp.org)
- [Vincent Chenal](mailto:vincent.chenal@grenoble-inp.org)
- [Florent Tonneau](florent.tonneau@grenoble-inp.org)
- [Nathanaël Couret](nathanael.couret@grenoble-inp.org)
- [Julien Sergent](julien.sergent@grenoble-inp.org)