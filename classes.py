class Product:
    def __init__(self, name, brand, price, link):
        self.name = name
        self.price = price
        self.link = link
        self.brand = brand

    def to_dict(self):
        return {
            "name": self.name,
            "brand": self.brand,
            "price": self.price,
            "link": self.link,
        }

    def __str__(self):
        return (
            f"Product: {self.name}\n"
            f"Brand: {self.brand}\n"
            f"Price: {self.price}\n"
            f"Link: {self.link}\n"
        )

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        # Compare by a unique identifier, e.g., the link
        return self.link == other.link

    def __hash__(self):
        # Use the link as the unique hashable attribute
        return hash(self.link)
