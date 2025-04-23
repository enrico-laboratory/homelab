from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from notion_db import TaskTable, MusicProjectTable
from backend import db
from backend.schemas import PlainTaskSchema

blp = Blueprint("Task", __name__, description="Operations on items")


@blp.route('/task/<int:task_id>')
class Task(MethodView):

    @blp.response(200, PlainTaskSchema)
    def get(self, task_id):
        return db.get_or_404(TaskTable, task_id)


@blp.route('/task')
class TaskList(MethodView):

    @blp.response(200, PlainTaskSchema(many=True))
    def get(self):
             
        filter = request.args.get('filter', "")
        sort = request.args.get('sort', "newer")

        if sort == "newer":
            order_by = TaskTable.start_date_time.desc()
        else:
            order_by = TaskTable.start_date_time.asc()
        
        try:
            if not filter:
                result = db.session.query(TaskTable).order_by(order_by).all()
            else:
                result = db.session.query(TaskTable).join(MusicProjectTable).where(MusicProjectTable.name == filter).order_by(order_by).all()
                
        except SQLAlchemyError:
             abort(500, message="An error occurred creating the store.")
        
        return result

    def post(self, choir_data):
        pass


