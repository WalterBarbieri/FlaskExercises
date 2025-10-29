class Car:

    _id_counter = 1

    def __init__(self, name: str, color: str, price: float, available: bool):
        self.id = Car._id_counter
        Car._id_counter += 1
        self.name = name
        self.color = color
        self.price = price
        self.available = available

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "price": self.price,
            "available": self.available,
        }
    
    def update(self, data: dict): 
        if "name" in data:
            self.name = str(data["name"])
        if "color" in data:
            self.color = str(data["color"])
        if "price" in data:
            self.price = float(data["price"])
        if "available" in data:
            self.available = bool(data["available"])
