from dataclasses import dataclass


@dataclass
class Furniture:
    def __init__(self, name: str, furniture_id: str, category: str, price: float, material: str, image_url: str):
        """
        Parameters:
            name: str - Name of the furniture item
            furniture_id: str - ID of the furniture item
            category: str - Category of the furniture item
            price: float - Price of the furniture item
            material: str - Material used for the furniture item
            image_url: str - Link to the image of the furniture item
        """
        self.name = name
        self.furniture_id = furniture_id
        self.category = category
        self.price = price
        self.material = material
        self.image_url = image_url
