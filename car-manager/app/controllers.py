from flask import Blueprint, jsonify, request
from .models import Car
from .services import CarService

bp = Blueprint("cars", __name__)
car_service = CarService()

## POST ##


# POST /api/cars
@bp.route("/api/cars", methods=["POST"])
def add_car():
    data = request.json or {}
    try:
        car = Car(
            name=str(data["name"]),
            color=str(data["color"]),
            price=float(data["price"]),
            available=bool(data["available"]),
        )
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input data"}), 400

    car_service.add_car(car)
    return jsonify(car.to_dict()), 201

# POST /api/cars/bulk
@bp.route("/api/cars/bulk", methods=["POST"])
def add_cars_bulk():
    data = request.json or []
    if not isinstance(data, list):
        return jsonify({"error": "Input data must be a list"}), 400
    added_cars = []
    errors = []

    for idx, car_data in enumerate(data, start=1):
        try:
            car = Car(
                name = str(car_data["name"]),
                color = str(car_data["color"]),
                price = float(car_data["price"]),
                available = bool(car_data["available"]),
            )
            car_service.add_car(car)
            added_cars.append(car.to_dict())
        except (KeyError, ValueError, TypeError):
            errors.append({"index": idx, "error": "Invalid car data", "data": car_data})

    response = {"added_cars": added_cars}
    if errors:
        response["errors"] = errors
    return jsonify(response), 201 if added_cars else 400


## GET ##


# GET /api/cars
# Optional query param: available=true/false
@bp.route("/api/cars", methods=["GET"])
def get_cars():
    available = request.args.get("available")
    cars = car_service.get_all_cars()
    if available is not None:
        available_bool = available.lower() == "true"
        cars = car_service.get_cars_by_availability(available_bool)

    cars_list = [car.to_dict() for car in cars]
    return jsonify(cars_list), 200


# GET /api/cars/<id>
@bp.route("/api/cars/<int:car_id>", methods=["GET"])
def get_car_by_id(car_id: int):
    car = car_service.get_car_by_id(car_id)
    if car:
        return jsonify(car.to_dict()), 200

    return jsonify({"error": "Car Not Found"}), 404


# GET /api/cars/<name>
@bp.route("/api/cars/<string:name>", methods=["GET"])
def get_car_by_name(name: str):
    car = car_service.get_car_by_name(name)
    if car:
        return jsonify(car.to_dict()), 200

    return jsonify({"error": "Car Not Found"}), 404


# GET /api/cars/count
@bp.route("/api/cars/count", methods=["GET"])
def get_car_count():
    count = car_service.count_cars()
    return jsonify({"count": count}), 200


## PUT ##


# PUT /api/cars/<id>
@bp.route("/api/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id: int):
    car = car_service.get_car_by_id(car_id)
    if not car:
        return jsonify({"error": "Car Not Found"}), 404

    data = request.json or {}
    try:
        car.update(data)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input data"}), 400

    return jsonify(car.to_dict()), 200


## DELETE ##


# DELETE /api/cars
@bp.route("/api/cars", methods=["DELETE"])
def delete_all_cars():
    car_service.clear_cars()
    return jsonify({"message": "All cars deleted"}), 200
