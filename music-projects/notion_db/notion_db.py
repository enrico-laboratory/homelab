import logging
import json
import os


from sqlalchemy.exc import SQLAlchemyError
from flask import Flask
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

from utils import Notion
from notion_db import config as c
from notion_db import MusicProjectBuilder, ChoirBuilder, LocationBuilder, TaskBuilder
from notion_db import Base, ChoirTable, MusicProjectTable, LocationTable, TaskTable

MUSIC_PROJECT_SQLITE_DB_FOLDER = 'instance/'
MUSIC_PROJECT_SQLITE_DB_FILENAME = 'music_projects.db'
MUSIC_PROJECTS_SQLITE_DB_URL = 'sqlite:///{folder}{filename}'


logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

engine = create_engine(MUSIC_PROJECTS_SQLITE_DB_URL.format(
    folder=MUSIC_PROJECT_SQLITE_DB_FOLDER, filename=MUSIC_PROJECT_SQLITE_DB_FILENAME), echo=True)
db = SQLAlchemy()


def create_app(db_url=None) -> Flask:
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", MUSIC_PROJECTS_SQLITE_DB_URL.format(folder="", filename=MUSIC_PROJECT_SQLITE_DB_FILENAME))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app


def init_db(app: Flask):

    db.init_app(app)

    with app.app_context():
        Base.metadata.create_all(engine)


def insert_row(app: Flask, table: any, **kargs):

    try:
        with app.app_context():
            row = table(**kargs)
            db.session.add(row)
            db.session.commit()

    except SQLAlchemyError as e:
        raise e

    return


def get_notion_database_from_file(filename: str) -> dict:

    with open(filename, 'r') as f:
        databse_dict = json.loads(f.read())

    return databse_dict


def print_table(app: Flask, table: Base, title: str):

    print(f'==== {title} ====')

    with app.app_context():
        response = db.session.query(table).all()
        for row in response:
            print(row)


def parse_tasks(tasks_dict: dict):

    excluded_list = []
    for i, page in enumerate(tasks_dict['results']):
        if not page['properties']['Type']['select']:
            excluded_list.append(i)
        else:
            if page['properties']['Type']['select']['name'] != 'Rehearsal' and page['properties']['Type']['select']['name'] != 'Concert':
                excluded_list.append(i)

    for index in reversed(excluded_list):

        del tasks_dict['results'][index]

    return tasks_dict


def main():

    os.remove(
        f'{MUSIC_PROJECT_SQLITE_DB_FOLDER}{MUSIC_PROJECT_SQLITE_DB_FILENAME}')

    app = create_app()
    init_db(app)

    notion = Notion(c.NOTION_API_TOKEN)

    ### CHOIRS ###
    # choirs_dict = get_notion_database_from_file('choirs.json')
    choirs_dict = notion.get_choirs()

    for page in choirs_dict['results']:

        try:
            choir = ChoirBuilder(page)
        except ValueError as e:
            log.fatal(f"something went wrong creating the choir builder: {e}")
            exit(1)

        insert_row(app, ChoirTable, id_notion=choir.properties.id,
                   name=choir.properties.name)

    # print_table(app, ChoirTable, "Choirs")

    ### LOCATIONS ###
    # locations_dict = get_notion_database_from_file('locations.json')
    locations_dict = notion.get_locations()

    for page in locations_dict['results']:

        try:
            location = LocationBuilder(page)
        except ValueError as e:
            log.fatal(
                f"something went wrong creating the location builder: {e}")
            exit(1)

        insert_row(app,
                   LocationTable,
                   id_notion=location.properties.id,
                   name=location.properties.name,
                   city=location.properties.city,
                   address=location.properties.address,
                   purpose=location.properties.purpose)

    # print_table(app, LocationTable, "Locations")

    ### MUSIC PROJECTS ###
    # music_projects_dict = get_notion_database_from_file('music_projects.json')
    music_projects_dict = notion.get_music_projects()

    for page in music_projects_dict['results']:

        try:
            music_project = MusicProjectBuilder(page)
        except ValueError as e:
            log.fatal(
                f"something went wrong creating the music project builder: {e}")
            exit(1)

        with app.app_context():
            choir_row = db.session.query(ChoirTable).filter_by(
                id_notion=music_project.properties.choir_id).first()

        if choir_row:
            choir_id = choir_row.id
        else:
            choir_id = None

        insert_row(app,
                   MusicProjectTable,
                   choir_id=choir_id,
                   id_notion=music_project.properties.id,
                   name=music_project.properties.name,
                   year=music_project.properties.year,
                   status=music_project.properties.status,
                   excerpt=music_project.properties.excerpt,
                   description=music_project.properties.description)

    # print_table(app, MusicProjectTable, "Music Projects")

    ### TASKS ###
    # tasks_dict_unparsed = get_notion_database_from_file('tasks.json')
    tasks_dict_unparsed = notion.get_tasks()

    tasks_dict = parse_tasks(tasks_dict_unparsed)

    for page in tasks_dict['results']:

        try:
            task = TaskBuilder(page)
        except ValueError as e:
            log.fatal(
                f"something went wrong creating the music project builder: {e}")
            exit(1)

        with app.app_context():
            location_row = db.session.query(LocationTable).filter_by(
                id_notion=task.properties.location_id).first()

        if location_row:
            location_id = location_row.id
        else:
            location_id = None

        with app.app_context():
            music_project_row = db.session.query(MusicProjectTable).filter_by(
                id_notion=task.properties.music_project_id).first()

        if music_project_row:
            music_project_id = music_project_row.id
        else:
            music_project_id = None

        insert_row(app,
                   TaskTable,
                   id_notion=task.properties.id,
                   name=task.properties.name,
                   start_date_time=task.properties.start_date_time,
                   end_date_time=task.properties.end_date_time,
                   type=task.properties.type,
                   music_project_id=music_project_id,
                   location_id=location_id)

        print_table(app, TaskTable, "Task table")


if __name__ == "__main__":
    main()
