
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_pokedex():
    with open('pokedex.json', 'r') as file:
        return json.load(file)


@app.route('/')
def pokedex():
    pokemons = load_pokedex()
    return render_template('pokedex.html', pokemons=pokemons)


@app.route('/search')
def search():
    name = request.args.get('name')
    number = request.args.get('number')

    pokemons = load_pokedex()

    if name:
        for p in pokemons:
            if p['name'].lower() == name.lower():
                return redirect(url_for('pokemon_detail', number=p['number']))
    elif number:
        try:
            number_int = int(number)
            for p in pokemons:
                if p['number'] == number_int:
                    return redirect(url_for('pokemon_detail', number=p['number']))
        except ValueError:
            pass

    return redirect(url_for('pokedex'))


@app.route('/pokemon/<int:number>')
def pokemon_detail(number):
    pokemons = load_pokedex()

    current_pokemon = next(
        (p for p in pokemons if p['number'] == number), None)
    if not current_pokemon:
        return "Pokémon não encontrado", 404

    # Círculo de 1 a 151
    prev_number = number - 1 if number > 1 else 151
    next_number = number + 1 if number < 151 else 1

    return render_template('pokemon.html', pokemon=current_pokemon, prev_number=prev_number, next_number=next_number)


if __name__ == '__main__':
    app.run(debug=True)
