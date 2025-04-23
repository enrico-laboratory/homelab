from flask.views import MethodView
from flask_smorest import Blueprint, abort

from notion_db import ChoirTable
from backend import db
from backend.schemas import PlainChoirSchema

blp = Blueprint("Choirs", __name__, description="Operations on items")



@blp.route('/choir/<int:choir_id>')
class Choir(MethodView):
    
    @blp.response(200, PlainChoirSchema)
    def get(self, choir_id):
        choir = db.get_or_404(ChoirTable, choir_id)
        return choir
        

@blp.route('/choir')
class ChoirList(MethodView):
    
   
    @blp.response(200, PlainChoirSchema(many=True))
    def get(self):
        # choirs = db.session.query(ChoirTable).all()
        # for choir in choirs:
        #     print(choir)
        return db.session.query(ChoirTable).all()
        
    
    def post(self, choir_data):
        pass