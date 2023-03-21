from flask import request
from flask_restplus import Resource, fields, Namespace
from sqlalchemy.sql import func
from werkzeug import secure_filename
import os
import shutil
from flask import jsonify
import urllib.request
import requests
import io
import pathlib

from models.HistoryRecord import RecordModel
from schemas.HistoryRecord import RecordSchema

RECORD_NOT_FOUND = "Record not found."
RECORD_ALREADY_EXISTS = "Record '{}' Already exists."


history_record_ns = Namespace('Record', description='Record related operations')
history_records_ns = Namespace('Records', description='Records related operations')
image_ns = Namespace('Image', description='Record related operations')
visible_status_change_ns = Namespace('VisibleStatus', description='Record related operations')
visible_records_ns = Namespace('VisibleRecords', description='Visible Record related operations')
QR_codes_ns = Namespace('QRcodes', description='QR code related operations')
Image_delete_ns = Namespace('ImageDelete', description='Image deletion operation')

record_schema = RecordSchema()
record_list_schema = RecordSchema(many=True)

# Model required by flask_restplus for expect
record = history_record_ns.model('Record', {
    'name': fields.String,
    'date': fields.DateTime,
    'description': fields.String,
    'description_short': fields.String,
    'record_type': fields.String,
    'is_visible': fields.Boolean
})
visibleStatus = history_record_ns.model('VisibleStatus', {
    'is_visible': fields.Boolean
})


class Record(Resource):

    def get(self, id):
        record_data = RecordModel.find_by_id(id)
        if record_data:
            return record_schema.dump(record_data)
        return {'message': RECORD_NOT_FOUND}, 404

    def delete(self, id):
        record_data = RecordModel.find_by_id(id)
        if record_data:
            record_data.delete_from_db()
            path = os.path.join("static/images", str(id))
            path2 = os.path.join(
                "static/images", "QRcodes/record" + str(id)+".png")
            print(path2)
            if (os.path.exists(path)):
             shutil.rmtree(path)
            if (os.path.exists(path2)):
                os.remove(path2)
            return {'message': "Record deleted successfully"}, 200
        return {'message': RECORD_NOT_FOUND}, 404

    @history_record_ns.expect(record)
    def put(self, id):
        record_data = RecordModel.find_by_id(id)
        record_json = request.get_json();

        if record_data:
            record_data.description_short = record_json['is_visible']
            record_data.updated_at = func.now()
        else:
            record_data = history_record_ns.load(record_json)

        record_data.save_to_db()
        return record_schema.dump(record_data), 200

    @history_record_ns.expect(record)
    def put(self, id):
        record_data = RecordModel.find_by_id(id)
        record_json = request.get_json();

        if record_data:
            record_data.name = record_json['name']
            record_data.date = record_json['date']
            record_data.description = record_json['description']
            record_data.description_short = record_json['description_short']
            record_data.record_type = record_json['record_type']
            record_data.is_visible = record_json['is_visible']
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
    def post(self, id):
        images = request.files
        for image in request.files.getlist("file"):
         path = os.path.join("static/images", str(id))
         if (not os.path.isdir(path)):
          {
          os.mkdir(path)
          }
         path2 = os.path.join("static/images", str(id),secure_filename(image.filename))
         print(path2)
         if (not os.path.isfile(path2)):
          {
          image.save(os.path.join("static/images", str(id),secure_filename(image.filename)))
          }
         else:
          {

          }
         #image.save(secure_filename(image.filename))
         #print(image_json)
         #for file in image_json:
         # file.save(os.path.join("static/images", "filename"))

        return "gerai", 201

    def get(self, id):
        path = os.path.join("static/images", str(id))
        if(os.path.exists(path)):
         filenames = os.listdir(path)
         return {'names': filenames}, 200
        return {'message': "Record has no images"}, 200


class VisibleStatusChange(Resource):
    # @history_record_ns.expect(visibleStatus)
    def put(self, id):
        record_data = RecordModel.find_by_id(id)
        # record_json = request.get_json();

        if record_data:
            record_data.is_visible = not record_data.is_visible
            record_data.updated_at = func.now()
        else:
            record_data = visible_status_change_ns.load(record_data)

        record_data.save_to_db()
        return record_schema.dump(record_data), 200


class VisibleRecordList(Resource):
    @history_records_ns.doc('Get all the visible records')
    def get(self):
        return record_list_schema.dump(RecordModel.find_all_visible_records()), 200


class QrCodes(Resource):
      def post(self, id):
        image = request.form['file']
        path = os.path.join("static/images", "QRcodes")
        if (not os.path.isdir(path)):
         {
         os.mkdir(path)
         }

        response = urllib.request.urlopen(image)
        with open('static/images/QRcodes/record' + str(id)+'.png', 'wb') as f:
             f.write(response.file.read())


class DeleteImage(Resource):
 def post(self, id):
    names_json = request.get_json()
    if names_json:
     for name in names_json:
      path = os.path.join("static/images",str(id) + "/" +name)
      if(os.path.exists(path)):
             os.remove(path)
     return {'message': "images deleted successfully"}, 200
    else:
     return {'message': "No images imputed"}, 404