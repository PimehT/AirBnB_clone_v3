#!/usr/bin/python3
"""Places module for the API."""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data['user_id'])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Not a JSON"}), 400
    checker = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in checker:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in
    the body of the request.
    """
    # data = request.get_json(silent=True)
    # if not isinstance(data, dict):
    #     return jsonify({"error": "Not a JSON"}), 400

    # states = data.get('states', [])
    # cities = data.get('cities', [])
    # amenities = data.get('amenities', [])

    # if not states and not cities and not amenities:
    #     places = storage.all(Place).values()
    # else:
    #     places = []
    #     for state_id in states:
    #         state = storage.get(State, state_id)
    #         if state:
    #             for city in state.cities:
    #                 places.extend(city.places)
    #     for city_id in cities:
    #         city = storage.get(City, city_id)
    #         if city:
    #             # ensure no duplicates
    #             for place in city.places:
    #                 if place.id not in (place.id for place in places):
    #                     places.append(place)

    # # filter by amenity
    # if len(amenities) > 0:
    #     place_list = []
    #     for place in places:
    #         for place_amenity in place.amenities:
    #             if place_amenity.id in amenities:
    #                 place_list.append(place.to_dict())
    #                 break
    # else:
    #     place_list = [place.to_dict() for place in places]

    # return jsonify(place_list), 200
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    states_list = data.get("states", [])
    cities_list = data.get("cities", [])
    amenities_list = data.get("amenities", [])

    if not data or not len(data) or (not len(states_list) and
                                     not len(cities_list) and
                                     not len(amenities_list)):
        places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(places), 200

    states = [storage.get(State, id) for id in states_list]
    cities = [storage.get(City, id) for id in cities_list]
    amenities = [storage.get(Amenity, id) for id in amenities_list]

    places = []
    for state in states:
        if state:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    for city in cities:
        if city:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if len(amenities) != 0:
        if not len(places):
            places = storage.all(Place).values()
        places = [place for place in places
                  if all(amenity in place.amenities for amenity in amenities)]

    result = []
    for place in places:
        p_dict = place.to_dict()
        p_dict.pop('amenities', None)
        result.append(p_dict)
    return jsonify(result), 200
