from .models import Car
from typing import List, Optional

class CarService:
    def __init__(self):
        self._cars: List[Car] = []

    def add_car(self, car: Car) -> Car:
        self._cars.append(car)
        return car

    def get_all_cars(self) -> List[Car]:
        return self._cars
    def get_car_by_id(self, car_id: int) -> Optional[Car]:
        return next((car for car in self._cars if car.id == car_id), None)

    def count_cars(self) -> int:
        return len(self._cars)

    def get_car_by_name(self, name: str) -> Optional[Car]:
        return next((car for car in self._cars if car.name == name), None)

    def get_cars_by_availability(self, available: bool) -> List[Car]:
        return [car for car in self._cars if car.available == available]

    def clear_cars(self):
        self._cars.clear()