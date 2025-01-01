import os
from flask import Flask, request, jsonify, url_for
from models import db, User, People, Planet, Starship, Vehicle, Favorite
from utils import APIException, generate_sitemap
from flask_cors import CORS
from flask_migrate import Migrate
from flask_swagger import swagger
from admin import setup_admin

app = Flask(__name__)
app.url_map.strict_slashes = False

# Database configuration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# User endpoints
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# People endpoints

@app.route('/people', methods=['POST'])
def create_people():
    data = request.get_json()

    new_people = People(
        name=data.get('name'),
        birth_year=data.get('birth_year'),
        gender=data.get('gender'),
        height=data.get('height'),
        mass=data.get('mass'),
        homeworld=data.get('homeworld')
    )
    db.session.add(new_people)
    db.session.commit()
    return jsonify(new_people.serialize()), 201

@app.route('/people/<int:planet_id>', methods=['PUT'])
def update_people(people_id):
    data = request.get_json()
    people = People.query.get(people_id)

    if not people:
        return jsonify({"msg": "Character not found"}), 404

    people.name = data.get('name', people.name)
    people.birth_year = data.get('birth_year', people.birth_year)
    people.gender = data.get('gender', people.gender)
    people.height = data.get('height', people.height)
    people.mass = data.get('mass', people.mass)
    people.homeworld = data.get('homeworld', people.homeworld)

    db.session.commit()
    return jsonify(people.serialize()), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    people = People.query.get(people_id)

    if not people:
        return jsonify({"msg": "Character not found"}), 404

    db.session.delete(people)
    db.session.commit()
    return jsonify({"msg": "Character deleted"}), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = People.query.filter_by(id=people_id).first()
    if not person:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(person.serialize()), 200

# Planet endpoints

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()

    new_planet = Planet(
        name=data.get('name'),
        climate=data.get('climate'),
        population=data.get('population'),
        terrain=data.get('terrain'),
        gravity=data.get('gravity')
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    data = request.get_json()
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    planet.name = data.get('name', planet.name)
    planet.climate = data.get('climate', planet.climate)
    planet.population = data.get('population', planet.population)
    planet.terrain = data.get('terrain', planet.terrain)
    planet.gravity = data.get('gravity', planet.gravity)

    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg": "Planet deleted"}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# Starship endpoints

@app.route('/starships', methods=['POST'])
def create_starships():
    data = request.get_json()

    new_starship = Starship(
        name=data.get('name'),
        model=data.get('model'),
        manufacturer=data.get('manufacturer'),
        starship_class=data.get('starship_class'),
        hyperdrive_rating=data.get('hyperdrive_rating')
    )
    db.session.add(new_starship)
    db.session.commit()
    return jsonify(new_starship.serialize()), 201

@app.route('/starships/<int:starship_id>', methods=['PUT'])
def update_starship(starship_id):
    data = request.get_json()
    starship = Starship.query.get(starship_id)

    if not starship:
        return jsonify({"msg": "Starship not found"}), 404

    starship.name = data.get('name', starship.name)
    starship.model = data.get('model', starship.model)
    starship.manufacturer = data.get('manufacturer', starship.manufacturer)
    starship.starship_class = data.get('starship_class', starship.starship_class)
    starship.hyperdrive_rating = data.get('hyperdrive_rating', starship.hyperdrive_rating)

    db.session.commit()
    return jsonify(starship.serialize()), 200

@app.route('/starships/<int:starship_id>', methods=['DELETE'])
def delete_starship(starship_id):
    starship = Starship.query.get(starship_id)

    if not starship:
        return jsonify({"msg": "Starship not found"}), 404

    db.session.delete(starship)
    db.session.commit()
    return jsonify({"msg": "Starship deleted"}), 200

@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starship.query.all()
    return jsonify([starship.serialize() for starship in starships]), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_one_starship(starship_id):
    starship = Starship.query.filter_by(id=starship_id).first()
    if not starship:
        return jsonify({"msg": "Starship not found"}), 404
    return jsonify(starship.serialize()), 200

# Vehicle endpoints

#name = db.Column(db.String(120), nullable=False)
#model = db.Column(db.String(120))
#manufacturer = db.Column(db.String(120))
#cost_in_credits = db.Column(db.String(120))
#max_atmosphering_speed = db.Column(db.String(120))

@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()

    new_vehicle = Vehicle(
        name=data.get('name'),
        model=data.get('model'),
        manufacturer=data.get('manufacturer'),
        cost_in_credits=data.get('cost_in_credits'),
        max_atmosphering_speed=data.get('max_atmosphering_speed')
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(new_vehicle.serialize()), 201

@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    data = request.get_json()
    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"msg": "Vehicle not found"}), 404

    vehicle.name = data.get('name', vehicle.name)
    vehicle.model = data.get('model', vehicle.model)
    vehicle.manufacturer = data.get('manufacturer', vehicle.manufacturer)
    vehicle.cost_in_credits = data.get('cost_in_credits', vehicle.cost_in_credits)
    vehicle.max_atmosphering_speed = data.get('max_atmosphering_speed', vehicle.max_atmosphering_speed)

    db.session.commit()
    return jsonify(vehicle.serialize()), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"msg": "Vehicle not found"}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"msg": "Vehicle deleted"}), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
    if not vehicle:
        return jsonify({"msg": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200

# Favorites endpoints
@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    data = request.get_json()  # Obtener datos del cuerpo
    user_id = data.get('user_id') if data else None

    if not user_id:
        return jsonify({"msg": "User ID is required"}), 400

    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet added"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_person(people_id):
    favorite = Favorite(people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite character added"}), 200

@app.route('/favorite/starship/<int:starship_id>', methods=['POST'])
def add_fav_starship(starship_id):
    favorite = Favorite(starship_id=starship_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite starship added"}), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_fav_vehicle(vehicle_id):
    favorite = Favorite(vehicle_id=vehicle_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite vehicle added"}), 200

# Delete favorites
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    favorite = Favorite.query.filter_by(planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite planet not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_person(people_id):
    favorite = Favorite.query.filter_by(people_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite character not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite character deleted"}), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
