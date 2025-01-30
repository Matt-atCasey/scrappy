class Product:
    def __init__(self, name, price, link, brand=None, in_stock=False, site=None):
        self.name = name
        self.price = price
        self.link = link
        self.brand = brand
        self.in_stock = in_stock
        self.site = site

    def to_dict(self):
        return {
            "name": self.name,
            "brand": self.brand,
            "price": self.price,
            "link": self.link,
            "in_stock": self.in_stock,
            "site": self.site,
        }

    def __str__(self):
        return (
            f"Product: {self.name}\n"
            f"Brand: {self.brand}\n"
            f"Price: {self.price}\n"
            f"Link: {self.link}\n"
            f"In Stock: {self.in_stock}"
            f"Site: {self.site}"
        )

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.name == other.name and self.brand == other.brand
        return False

    def compare(self, other):
        """
        Compare this product with another and return a dictionary of changed fields.
        :param other: Product to compare with.
        :return: Dict with field names as keys and (old_value, new_value) as values.
        """
        changes = {}
        if self.price != other.price:
            changes["price"] = (other.price, self.price)
        if self.link != other.link:
            changes["link"] = (other.link, self.link)
        return changes
