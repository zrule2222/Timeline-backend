from flask import request
from flask_restplus import Resource, fields, Namespace
from sqlalchemy.sql import func
import os

from models.HistoryRecord import RecordModel
from schemas.HistoryRecord import RecordSchema

RECORD_NOT_FOUND = "Record not found."
RECORD_ALREADY_EXISTS = "Record '{}' Already exists."


history_record_ns = Namespace('Record', description='Record related operations')
history_records_ns = Namespace('Records', description='Records related operations')
image_ns = Namespace('Image', description='Record related operations')

record_schema = RecordSchema()
record_list_schema = RecordSchema(many=True)

#Model required by flask_restplus for expect
record = history_record_ns.model('Record', {
    'name': fields.String,
    'date': fields.DateTime,
    'description': fields.String,
    'description_short': fields.String,
    'record_type': fields.String,
})

class Record(Resource):

    def get(self, id):
        record_data = RecordModel.find_by_id(id)
        if record_data:
            return record_schema.dump(record_data)
        return {'message': RECORD_NOT_FOUND}, 404

    def delete(self,id):
        record_data = RecordModel.find_by_id(id)
        if record_data:
            record_data.delete_from_db()
            return {'message': "Record deleted successfully"}, 200
        return {'message': RECORD_NOT_FOUND}, 404

    @history_record_ns.expect(record)
    def put(self, id):
        record_data = RecordModel.find_by_id(id)
        record_json = request.get_json();

        if record_data:
            record_data.name = record_json['name']
            record_data.date = record_json['date']
            record_data.description = record_json['description']
            record_data.description_short = record_json['description_short']
            record_data.updated_at = func.now()
        else:
            record_data = history_record_ns.load(record_json)

        record_data.save_to_db()
        return record_schema.dump(record_data), 200
    
class RecordList(Resource):
    @history_records_ns.doc('Get all the records')
    def get(self):
        return record_list_schema.dump(RecordModel.find_all()), 200

    @history_records_ns.expect(record)
    @history_records_ns.doc('Create a record')
    def post(self):
        user_json = request.get_json()
        name = user_json['name']
        if RecordModel.find_by_name(name):
            return {'message': RECORD_ALREADY_EXISTS.format(name)}, 400
        user_data = record_schema.load(user_json)
        user_data.save_to_db()

        return record_schema.dump(user_data), 201
class Image(Resource):
    def post(self):
        image_json = request.files
        image_json.save(os.path.join("static/images", "filename"))

        return "gerai", 201
    