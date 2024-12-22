class Product:
    def __init__(self, brand, name, price, link):
        self.name = name
        self.price = price
        self.link = link
        self.brand = name

    def __str__(self):
        return (
            f"Product: {self.name}\n"
            f"Brand: {self.brand}\n"
            f"Price: £{self.price}\n"
            f"Link: https://www.scan.co.uk/{self.link}\n"
        )
