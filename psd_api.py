#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Client API pour Pokémon Showdown
Ce script permet de récupérer différentes données depuis l'API de Pokémon Showdown.
"""

import requests
import json
import argparse
from typing import Dict, List, Optional, Union, Any
import sys


class PokemonShowdownAPI:
    """Classe pour interagir avec l'API Pokémon Showdown"""

    BASE_URL_REPLAY = "https://replay.pokemonshowdown.com"
    BASE_URL_MAIN = "https://pokemonshowdown.com"
    BASE_URL_PLAY = "https://play.pokemonshowdown.com"

    def __init__(self):
        """Initialise l'API client"""
        self.session = requests.Session()

    def _get_json(self, url: str) -> Dict[str, Any]:
        """
        Effectue une requête GET et retourne les données JSON.
        
        Args:
            url: L'URL à interroger
            
        Returns:
            Dict: Les données JSON retournées
            
        Raises:
            Exception: Si la requête échoue
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à {url}: {e}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Impossible de décoder la réponse JSON de {url}")
            sys.exit(1)

    def _get_text(self, url: str) -> str:
        """
        Effectue une requête GET et retourne le texte.
        
        Args:
            url: L'URL à interroger
            
        Returns:
            str: Le contenu textuel retourné
            
        Raises:
            Exception: Si la requête échoue
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à {url}: {e}")
            sys.exit(1)

    def get_replay(self, replay_id: str, format_type: str = "json") -> Union[Dict[str, Any], str]:
        """
        Récupère les données d'un replay.
        
        Args:
            replay_id: L'identifiant du replay (ex: gen8doublesubers-1097585496)
            format_type: Le format de sortie ('json', 'log', ou 'inputlog')
            
        Returns:
            Union[Dict, str]: Les données du replay dans le format demandé
        """
        if format_type not in ["json", "log", "inputlog"]:
            raise ValueError("Format type doit être 'json', 'log', ou 'inputlog'")
        
        url = f"{self.BASE_URL_REPLAY}/{replay_id}.{format_type}"
        
        if format_type == "json":
            return self._get_json(url)
        else:
            return self._get_text(url)

    def search_replays(self, user: Optional[str] = None, user2: Optional[str] = None, 
                      format: Optional[str] = None, before: Optional[int] = None,
                      page: Optional[int] = None) -> Dict[str, Any]:
        """
        Recherche des replays selon différents critères.
        
        Args:
            user: Nom d'utilisateur du premier joueur
            user2: Nom d'utilisateur du deuxième joueur
            format: Format de combat (ex: gen8ou)
            before: Timestamp pour la pagination
            page: Numéro de page (ancien système, utilisation déconseillée)
            
        Returns:
            Dict: Les replays correspondant aux critères
        """
        params = {}
        if user:
            params["user"] = user
        if user2:
            params["user2"] = user2
        if format:
            params["format"] = format
        if before:
            params["before"] = before
        if page:
            params["page"] = page
        
        url = f"{self.BASE_URL_REPLAY}/search.json"
        if params:
            url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
        return self._get_json(url)

    def get_user_info(self, username: str) -> Dict[str, Any]:
        """
        Récupère les informations d'un utilisateur.
        
        Args:
            username: Nom d'utilisateur
            
        Returns:
            Dict: Informations sur l'utilisateur
        """
        url = f"{self.BASE_URL_MAIN}/users/{username}.json"
        return self._get_json(url)

    def get_ladder(self, format: str) -> Dict[str, Any]:
        """
        Récupère le classement pour un format spécifique.
        
        Args:
            format: Format de combat (ex: gen8ou)
            
        Returns:
            Dict: Classement pour le format spécifié
        """
        url = f"{self.BASE_URL_MAIN}/ladder/{format}.json"
        return self._get_json(url)

    def get_news(self, news_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Récupère les actualités.
        
        Args:
            news_id: ID d'une actualité spécifique (optionnel)
            
        Returns:
            Dict: Actualités ou actualité spécifique
        """
        if news_id:
            url = f"{self.BASE_URL_MAIN}/news/{news_id}.json"
        else:
            url = f"{self.BASE_URL_MAIN}/news.json"
        
        return self._get_json(url)

    def get_pokedex(self) -> Dict[str, Any]:
        """
        Récupère le Pokédex complet.
        
        Returns:
            Dict: Données du Pokédex
        """
        url = f"{self.BASE_URL_PLAY}/data/pokedex.json"
        return self._get_json(url)
    
    def get_pokemon(self, pokemon_name: str) -> Dict[str, Any]:
        """
        Récupère les informations d'un Pokémon spécifique.
        
        Args:
            pokemon_name: Nom d'un Pokémon (en format minuscule sans espaces, ex: 'thunderbolt')
            
        Returns:
            Dict: Données d'un Pokémon
            
        Raises:
            ValueError: Si l'attaque n'existe pas
        """
        all_pokemon = self.get_pokedex()
        
        # Normaliser le nom d'un Pokémon (en minuscules, sans espaces ni caractères spéciaux)
        normalized_name = pokemon_name.lower().replace(" ", "").replace("-", "").replace(",", "").replace(".", "")
        
        # Chercher l'attaque exacte
        if normalized_name in all_pokemon:
            return all_pokemon[normalized_name]
            
        # Si on ne trouve pas exactement, chercher en ignorant les caractères spéciaux
        for pokemon_id, pokemon_data in all_pokemon.items():
            clean_id = pokemon_id.lower().replace(" ", "").replace("-", "").replace(",", "").replace(".", "")
            if clean_id == normalized_name:
                return pokemon_data
                
        # Chercher par le nom affiché
        for pokemon_id, pokemon_data in all_pokemon.items():
            if "name" in pokemon_data and pokemon_data["name"].lower().replace(" ", "").replace("-", "").replace(",", "").replace(".", "") == normalized_name:
                return pokemon_data
                
        raise ValueError(f"Attaque '{pokemon_name}' non trouvée")

    def get_moves(self) -> Dict[str, Any]:
        """
        Récupère la liste complète des attaques.
        
        Returns:
            Dict: Données des attaques
        """
        url = f"{self.BASE_URL_PLAY}/data/moves.json"
        return self._get_json(url)
        
    def get_move(self, move_name: str) -> Dict[str, Any]:
        """
        Récupère les informations d'une attaque spécifique.
        
        Args:
            move_name: Nom de l'attaque (en format minuscule sans espaces, ex: 'thunderbolt')
            
        Returns:
            Dict: Données de l'attaque
            
        Raises:
            ValueError: Si l'attaque n'existe pas
        """
        all_moves = self.get_moves()
        
        # Normaliser le nom de l'attaque (en minuscules, sans espaces ni caractères spéciaux)
        normalized_name = move_name.lower().replace(" ", "").replace("-", "").replace(",", "").replace(".", "")
        
        # Chercher l'attaque exacte
        if normalized_name in all_moves:
            return all_moves[normalized_name]
            
        # Si on ne trouve pas exactement, chercher en ignorant les caractères spéciaux
        for move_id, move_data in all_moves.items():
            clean_id = move_id.lower().replace(" ", "").replace("-", "").replace(",", "").replace(".", "")
            if clean_id == normalized_name:
                return move_data
                
        # Chercher par le nom affiché
        for move_id, move_data in all_moves.items():
            if "name" in move_data and move_data["name"].lower().replace(" ", "").replace("-", "").replace(",", "").replace(".", "") == normalized_name:
                return move_data
                
        raise ValueError(f"Attaque '{move_name}' non trouvée")

    def save_to_file(self, data: Any, filename: str) -> None:
        """
        Sauvegarde les données dans un fichier.
        
        Args:
            data: Les données à sauvegarder
            filename: Nom du fichier de sortie
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(data, dict) or isinstance(data, list):
                    json.dump(data, f, indent=2, ensure_ascii=False)
                else:
                    f.write(str(data))
            print(f"Données sauvegardées dans {filename}")
        except IOError as e:
            print(f"Erreur lors de l'écriture dans le fichier {filename}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Client pour l'API Pokémon Showdown")
    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")
    
    # Commande replay
    replay_parser = subparsers.add_parser("replay", help="Récupérer un replay")
    replay_parser.add_argument("replay_id", help="ID du replay (ex: gen8doublesubers-1097585496)")
    replay_parser.add_argument("--format", choices=["json", "log", "inputlog"], default="json",
                             help="Format de sortie (défaut: json)")
    replay_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    
    # Commande search
    search_parser = subparsers.add_parser("search", help="Rechercher des replays")
    search_parser.add_argument("--user", help="Nom d'utilisateur du premier joueur")
    search_parser.add_argument("--user2", help="Nom d'utilisateur du deuxième joueur")
    search_parser.add_argument("--format", help="Format de combat (ex: gen8ou)")
    search_parser.add_argument("--before", type=int, help="Timestamp pour la pagination")
    search_parser.add_argument("--page", type=int, help="Numéro de page (ancien système)")
    search_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    
    # Commande user
    user_parser = subparsers.add_parser("user", help="Récupérer les informations d'un utilisateur")
    user_parser.add_argument("username", help="Nom d'utilisateur")
    user_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    
    # Commande ladder
    ladder_parser = subparsers.add_parser("ladder", help="Récupérer le classement pour un format")
    ladder_parser.add_argument("format", help="Format de combat (ex: gen8ou)")
    ladder_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    
    # Commande news
    news_parser = subparsers.add_parser("news", help="Récupérer les actualités")
    news_parser.add_argument("--id", type=int, help="ID d'une actualité spécifique (optionnel)")
    news_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    
    # Commande pokedex
    pokedex_parser = subparsers.add_parser("pokedex", help="Récupérer le Pokédex")
    pokedex_parser.add_argument("--name", help="Nom d'un Pokémon spécifique (optionnel)")
    pokedex_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    
    # Commande moves
    moves_parser = subparsers.add_parser("moves", help="Récupérer la liste des attaques")
    moves_parser.add_argument("--name", help="Nom d'une attaque spécifique (optionnel)")
    moves_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    
    args = parser.parse_args()
    
    # Si aucune commande n'est spécifiée, afficher l'aide
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    api = PokemonShowdownAPI()
    
    # Traiter la commande spécifiée
    if args.command == "replay":
        data = api.get_replay(args.replay_id, args.format)
        if args.output:
            api.save_to_file(data, args.output)
        else:
            if isinstance(data, dict):
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(data)
    
    elif args.command == "search":
        data = api.search_replays(args.user, args.user2, args.format, args.before, args.page)
        if args.output:
            api.save_to_file(data, args.output)
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
    
    elif args.command == "user":
        data = api.get_user_info(args.username)
        if args.output:
            api.save_to_file(data, args.output)
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
    
    elif args.command == "ladder":
        data = api.get_ladder(args.format)
        if args.output:
            api.save_to_file(data, args.output)
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
    
    elif args.command == "news":
        data = api.get_news(args.id)
        if args.output:
            api.save_to_file(data, args.output)
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
    
    elif args.command == "pokedex":
        if args.name:
            try:
                data = api.get_pokemon(args.name)
                if args.output:
                    api.save_to_file(data, args.output)
                else:
                    print(json.dumps(data, indent=2, ensure_ascii=False))
            except ValueError as e:
                print(f"Erreur: {e}")
                sys.exit(1)
        else:
            data = api.get_pokedex()
            if args.output:
                api.save_to_file(data, args.output)
            else:
                print(json.dumps(data, indent=2, ensure_ascii=False))
    
    elif args.command == "moves":
        if args.name:
            try:
                data = api.get_move(args.name)
                if args.output:
                    api.save_to_file(data, args.output)
                else:
                    print(json.dumps(data, indent=2, ensure_ascii=False))
            except ValueError as e:
                print(f"Erreur: {e}")
                sys.exit(1)
        else:
            data = api.get_moves()
            if args.output:
                api.save_to_file(data, args.output)
            else:
                print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
