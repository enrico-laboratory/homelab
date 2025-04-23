from marshmallow import Schema, fields
from marshmallow.validate import ContainsOnly

class PlainChoirSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()    

class PlainLocationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    city = fields.Str()
    address = fields.Str()
    purpose = fields.Str(validate=[ContainsOnly(['Rehearsal', 'Concert'])])

class PlainMusicProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    year = fields.Int()
    status = fields.Str()
    excerpt = fields.Str()
    description = fields.Str()
    choir = fields.Nested(PlainChoirSchema(), dump_only=True)
    
class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    start_date_time = fields.DateTime()
    end_date_time = fields.DateTime()
    type = fields.Str()
    music_project = fields.Nested(PlainMusicProjectSchema(), dump_only=True)
    location = fields.Nested(PlainLocationSchema(), dump_only=True)