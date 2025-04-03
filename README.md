# Application Flask Pokédex Showdown

Cette application Flask utilise l'API Pokémon Showdown pour afficher un Pokédex complet avec une interface stylisée.

## Structure du projet

```
pythondex/
│
├── app.py                 # Application Flask principale
├── PokemonShowdownAPI.py  # Votre API Python Pokémon Showdown
├── requirements.txt       # Dépendances Python
├── README.md              # Ce fichier
│
└── templates/             # Templates HTML
    ├── base.html          # Template de base avec la structure HTML
    ├── index.html         # Page d'accueil
    ├── pokedex.html       # Liste de tous les Pokémon
    ├── pokemon_detail.html # Détails d'un Pokémon spécifique
    ├── search_results.html # Résultats de recherche
    └── error.html         # Page d'erreur
```

## Installation

1. Créez un environnement virtuel Python et activez-le :

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

3. Démarrez l'application :

```bash
python app.py
```

4. Ouvrez votre navigateur et allez à l'adresse `http://127.0.0.1:5000`

## Dépendances

Créez un fichier `requirements.txt` avec le contenu suivant :

```
Flask==2.3.3
requests==2.31.0
```

## Fonctionnalités

- Affichage du Pokédex complet avec images
- Recherche de Pokémon par nom
- Affichage détaillé des statistiques, types et capacités
- Liste des attaques pour chaque Pokémon
- Interface responsive et stylisée

## Comment ça marche

L'application utilise votre classe `PokemonShowdownAPI` pour récupérer les données du Pokédex et des Pokémon depuis l'API Pokémon Showdown. Elle affiche ensuite ces données dans une interface utilisateur stylisée construite avec Bootstrap.

## Personnalisation

Vous pouvez personnaliser davantage l'application en modifiant les styles CSS dans le fichier `templates/base.html` ou en ajoutant de nouvelles fonctionnalités à l'application Flask.