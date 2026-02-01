🚦 Simulation de Feu Tricolore - Ville de Thiès  - gorupe 16 

# Présentation du Projet
Ce projet consiste en une application Python simulant la gestion automatisée et manuelle d'un carrefour routier à Thiès. 
Il intègre une interface graphique interactive, une animation fluide de véhicules via le module turtle et une journalisation des événements dans une base de données SQLite.

Developpe dans le cadre du cours de Programmation Orientée Objet 2 (POO2) à l'Université Iba Der Thiam de Thiès.

# Équipe de réalisation (Groupe 16)
- Badiene Awa MBACKE (bawa.mbacke@univ-thies.sn)
- Bineta NDOYE (bineta.ndoye@univ-thies.sn)
- Awa THIAW: (awa.thiaw@univ-thies.sn)

# Professeur:
M. Mansour DIOUF

# Fonctionnalités Clés
- Simulation Graphique : Dessin d'un carrefour perpendiculaire avec marquages au sol et passages piétons.
- Gestion des Feux : Cycle automatique (Rouge, Orange, Vert) avec ralentissement et arrêt réaliste des véhicules.
- Scénarios de Circulation :
   * Normal : Circulation standard.
   * Heure de pointe : Apparition fréquente de voitures et démarrage plus lent.
   * Mode Nuit : Trafic réduit avec feux orange clignotants.
   * Mode Manuel : Contrôle total de l'état des feux par l'utilisateur.
- Journalisation (Logs) : Enregistrement en temps réel de chaque action (démarrage, changements de feux, apparition de voitures)

# Architecture du Code
- simulation.py: coeur du système gérant l'interface Tkinter, la boucle d'animation et la logique des scénarios
- voiture.py: classe gérant les attributs (vitesse, direction, couleur) et le comportement des véhicules
- feutricolore.py: geston graphique et logique des états du feu tricolore
- database.py: interface de connexion et de gestion de la base de données SQLite
- main.py: demarre la simulation

# Prérequis
- Python 3.x
- Pycharm / vs code

 # Téléchargement
- Telecharger le zip
- decompresser et run le fichier main.py
