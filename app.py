from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from psd_api import PokemonShowdownAPI

app = Flask(__name__)
app.secret_key = os.urandom(24)
api = PokemonShowdownAPI()

@app.route('/')
def index():
    """Page d'accueil avec recherche"""
    return render_template('index.html')

@app.route('/pokedex')
def pokedex():
    """Afficher tous les Pokémon du Pokédex"""
    try:
        all_pokemon = api.get_pokedex()
        # Transformer le dictionnaire en liste et trier par ID numérique
        pokemon_list = []
        for pokemon_id, pokemon_data in all_pokemon.items():
            if 'num' in pokemon_data and 'name' in pokemon_data:
                pokemon_list.append({
                    'id': pokemon_id,
                    'num': pokemon_data['num'],
                    'name': pokemon_data['name'],
                    'types': pokemon_data.get('types', []),
                    'sprite': get_sprite_url(pokemon_id)
                })
        
        # Trier par numéro de Pokédex
        pokemon_list.sort(key=lambda x: x['num'])
        
        return render_template('pokedex.html', pokemon_list=pokemon_list)
    except Exception as e:
        flash(f"Erreur lors de la récupération du Pokédex: {e}", "danger")
        return render_template('error.html', error=str(e))

@app.route('/pokemon/<pokemon_id>')
def pokemon_detail(pokemon_id):
    """Afficher les détails d'un Pokémon spécifique"""
    try:
        pokemon_data = api.get_pokemon(pokemon_id)
        # Récupérer les données des attaques si disponibles
        moves = []
        if 'learnset' in pokemon_data:
            all_moves = api.get_moves()
            for move_id in pokemon_data['learnset']:
                if move_id in all_moves:
                    moves.append({
                        'id': move_id,
                        'name': all_moves[move_id].get('name', move_id),
                        'type': all_moves[move_id].get('type', 'Normal'),
                        'power': all_moves[move_id].get('basePower', '-'),
                        'accuracy': all_moves[move_id].get('accuracy', '-'),
                        'pp': all_moves[move_id].get('pp', '-'),
                        'category': all_moves[move_id].get('category', '-')
                    })
        
        return render_template(
            'pokemon_detail.html', 
            pokemon=pokemon_data,
            pokemon_id=pokemon_id,
            sprite=get_sprite_url(pokemon_id),
            moves=moves
        )
    except Exception as e:
        flash(f"Erreur lors de la récupération des données du Pokémon: {e}", "danger")
        return render_template('error.html', error=str(e))

@app.route('/search')
def search():
    """Rechercher un Pokémon par nom"""
    query = request.args.get('q', '').strip().lower()
    if not query:
        return redirect(url_for('pokedex'))
    
    try:
        all_pokemon = api.get_pokedex()
        results = []
        
        for pokemon_id, pokemon_data in all_pokemon.items():
            if query in pokemon_id.lower() or (
                'name' in pokemon_data and query in pokemon_data['name'].lower()
            ):
                results.append({
                    'id': pokemon_id,
                    'num': pokemon_data.get('num', 0),
                    'name': pokemon_data.get('name', pokemon_id),
                    'types': pokemon_data.get('types', []),
                    'sprite': get_sprite_url(pokemon_id)
                })
        
        results.sort(key=lambda x: x['num'])
        return render_template('search_results.html', results=results, query=query)
    except Exception as e:
        flash(f"Erreur lors de la recherche: {e}", "danger")
        return render_template('error.html', error=str(e))

@app.route('/api/pokemon/<pokemon_id>')
def api_pokemon(pokemon_id):
    """API endpoint pour récupérer les données d'un Pokémon au format JSON"""
    try:
        pokemon_data = api.get_pokemon(pokemon_id)
        return jsonify(pokemon_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

def get_sprite_url(pokemon_id):
    """Générer l'URL du sprite d'un Pokémon"""
    # Utiliser l'API officielle de sprites Pokemon
    return f"https://play.pokemonshowdown.com/sprites/ani/{pokemon_id}.gif"

if __name__ == '__main__':
    app.run(debug=True)