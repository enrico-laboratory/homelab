class MusicProjectNotionModel:

    def __init__(self,
                 id: str,
                 name: str,
                 year: int,
                 choir_id: str = None,
                 status: str = None,
                 excerpt: str = None,
                 description: str = None):

        self.id = id
        self.name = name
        self.year = year
        self.choir_id = choir_id
        self.status = status
        self.excerpt = excerpt
        self.description = description

    def __repr__(self) -> str:
        return f'(MusicProjectNotionModel : "id": {self.id}, "name": {self.name}, "year": {self.year}, "choir_id": {self.choir_id}, "status": {self.status})'
