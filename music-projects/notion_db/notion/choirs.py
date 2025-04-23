class ChoirNotionModel:
    
    def __init__(self,
                 id: str,
                 name: str):
        
        self.id = id
        self.name = name
        
    def __repr__(self) -> str:
        return f'(ChoirNotionModel : "id": {self.id}, "name": {self.name})'

     