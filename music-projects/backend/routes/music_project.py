from flask.views import MethodView
from flask_smorest import Blueprint, abort

from notion_db import MusicProjectTable
from backend import db
from backend.schemas import PlainMusicProjectSchema

blp = Blueprint("Music Project", __name__, description="Operations on items")


@blp.route('/music_project/<int:music_project_id>')
class MusicProject(MethodView):

    @blp.response(200, PlainMusicProjectSchema)
    def get(self, music_project_id):
        music_project = db.get_or_404(MusicProjectTable, music_project_id)
        return music_project


@blp.route('/music_project')
class MusicProjectrList(MethodView):

    @blp.response(200, PlainMusicProjectSchema(many=True))
    def get(self):
        return db.session.query(MusicProjectTable).all()

    def post(self, choir_data):
        pass
