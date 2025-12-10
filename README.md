🏢 Contexte

Sensei développe des outils digitaux destinés aux professionnels de l’accompagnement (coachings, psychologues, consultants).
Dans le cadre de son évolution, l’entreprise intègre et personnalise Odoo v17 afin d’optimiser ses processus internes et d’offrir des fonctionnalités avancées aux équipes et aux utilisateurs.

Ce projet s’inscrit dans la personnalisation, le développement et l’intégration de modules Odoo adaptés aux besoins spécifiques de Sensei.

🎯 Objectif du projet

L’objectif principal est de développer, adapter et intégrer des modules Odoo pour répondre aux besoins internes de Sensei, notamment en matière de :

Gestion des utilisateurs

Suivi des prestations

Facturation

Le travail inclut à la fois une dimension technique (développement Odoo) et fonctionnelle (analyse des besoins, tests, documentation).

🛠️ Missions réalisées
🔍 1. Analyse des besoins internes

Collecte et compréhension des besoins liés à la gestion des utilisateurs, prestations et facturation.

Participation à des ateliers fonctionnels avec les équipes internes.

💻 2. Développement & Personnalisation Odoo

Création et modification de modules Odoo personnalisés (Python, XML).

Ajout de modèles, vues, workflows, actions serveur, rapports.

🔗 3. Intégration avec services externes

Consommation et envoi de données via API REST (JSON).

🧩 4. Maintenance & Evolution

Debugging, optimisation de modules existants.

Mise à jour et migration de fonctionnalités vers Odoo 17.

Nettoyage du code & respect des standards Odoo.

🧪 5. Tests fonctionnels

Rédaction de scenarios de tests.

Validation des fonctionnalités avec les responsables métiers.

📄 6. Documentation

Rédaction de documentation technique (modules, modèles, API).

Création de guides utilisateurs pour les équipes internes.

🧰 Environnement technique
Domaine	Outils
ERP	Odoo v17
Langages	Python, XML, PostgreSQL
Versioning	Git
Méthodologie	Agile (Kanban / Scrum)
APIs	REST / JSON
🎓 Compétences développées

Développement backend orienté ERP (Python / Odoo)

Maîtrise de la structure modulaire d’Odoo

Personnalisation de modules (modèles, vues, sécurité, actions)

Intégration d’API tierces

Compréhension de l’architecture Odoo : ORM, QWeb, modèles, workflows

Travail en mode projet agile

Documentation technique et fonctionnelle

📂 Structure du projet (exemple)
addons/sensei/
│
├── data/
│   ├── data_cron.xml          # Tâches planifiées (cron)
│   ├── email_template.xml     # Templates email personnalisés
│   └── ir_sequence.xml        # Séquences automatiques
│
├── models/
│   ├── facture.py             # Modèle Facture
│   ├── session.py             # Modèle Session
│   ├── utilisateur.py         # Modèle Utilisateur
│   └── wizard.py              # Assistant (wizard) spécifique
│
├── security/
│   └── ir.model.access.csv    # Droits d’accès utilisateurs
│
├── views/
│   ├── factures_views.xml     # Vues facture
│   ├── menus.xml              # Menu principal + sous-menus
│   ├── session_views.xml      # Vues session
│   ├── utilisateur_views.xml  # Vues utilisateur
│   └── wizard_vue.xml         # Vues wizard
│
├── __manifest__.py            # Informations du module
├── __init__.py                # Initialisation
│
└── docker-compose.yml         # Déploiement local (Odoo + PostgreSQL)

🔧 Fonctionnalités principales
👤 Gestion des utilisateurs

Modèle personnalisé utilisateur

Formulaires, listes, filtres

Séquences automatiques (ex : ID utilisateur)

Sécurisation via ACL

🗓️ Gestion des sessions

Création & suivi des sessions

Champs liés (utilisateur, facture, statut…)

Automatisation via cron (mise à jour, notifications)

💵 Facturation

Modèle facture

Génération automatique de numéros via ir_sequence

Interface pour créer / valider / consulter les factures

🧙 Wizards

Assistant permettant des actions avancées (batch, confirmations…)

📬 Emails & automatisations

Templates email personnalisés (ex : notification session)

Tâches programmées (CRON)


🚀 Installation (dev)

Cloner le dépôt :

git clone https://github.com/AmineBo324/odoo.git


Ajouter le dossier à addons_path dans odoo.conf

Redémarrer Odoo :

./odoo-bin -c odoo.conf -u all


Lancer Odoo en mode développeur.

🤝 Contribution

Utilisation d’un workflow Git standard : feature branch → pull request → review.

Documentation obligatoire pour chaque module.

Tests fonctionnels réalisés avant livraison.
