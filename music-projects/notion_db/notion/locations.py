class LocationNotionModel:

    def __init__(self,
                 id: str,
                 name: str,
                 city: str,
                 address: str = None,
                 purpose: str = None):

        self.id = id
        self.name = name
        self.city = city
        self.address = address
        self.purpose = purpose

    def __repr__(self) -> str:
        return f'(LocationNotionModel : "id": {self.id}, "name": {self.name}, "city": {self.city}, "address": {self.address}, "purpose": {self.purpose})'
