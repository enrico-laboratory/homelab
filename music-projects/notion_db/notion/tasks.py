from datetime import datetime


class TasksNotionModel:

    def __init__(self,
                 id: str,
                 name: str,
                 type: int,
                 start_date_time: datetime,
                 end_date_time: datetime,
                 music_project_id: str,
                 location_id: str = None):

        self.id = id
        self.name = name
        self.type = type
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.music_project_id = music_project_id
        self.location_id = location_id

    def __repr__(self) -> str:
        return f'(TasksNotionModel : "id": {self.id}, "name": {self.name}, "type": {self.type}, "start_date": {self.start_date_time}, "end_date_time": {self.end_date_time}, "music_project_id": {self.music_project_id})'
