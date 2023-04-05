from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from flask_cors import CORS
from auth.views import auth_blueprint
from flask_bcrypt import Bcrypt
from ma import ma
from db import db
from marshmallow import ValidationError

from resources.User import User,UserList,user_ns,users_ns
from resources.HistoryRecord import Image,Record,RecordList,VisibleStatusChange,  VisibleRecordList, QrCodes,DeleteImage, QR_codes_ns, visible_records_ns, history_record_ns,history_records_ns,image_ns, visible_status_change_ns,Image_delete_ns
from resources.RecordProperty import RecordPropertyList, Property, PropertyDelete, properties_ns,property_ns, property_delete_ns
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.register_blueprint(auth_blueprint)

bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='History records backend application')
app.register_blueprint(bluePrint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(user_ns)
api.add_namespace(users_ns)
api.add_namespace(history_record_ns)
api.add_namespace(history_records_ns)
api.add_namespace(image_ns)
api.add_namespace(visible_status_change_ns)
api.add_namespace(visible_records_ns)
api.add_namespace(QR_codes_ns)
api.add_namespace(Image_delete_ns)
api.add_namespace(properties_ns)
api.add_namespace(property_ns)
api.add_namespace(property_delete_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


user_ns.add_resource(User, '/<int:id>')
users_ns.add_resource(UserList, "")
history_record_ns.add_resource(Record, '/<int:id>')
history_records_ns.add_resource(RecordList, "")
image_ns.add_resource(Image, '/<int:id>')
visible_status_change_ns.add_resource(VisibleStatusChange, '/<int:id>')
visible_records_ns.add_resource(VisibleRecordList, "")
QR_codes_ns.add_resource(QrCodes, '/<int:id>')
Image_delete_ns.add_resource(DeleteImage, '/<int:id>')
properties_ns.add_resource(RecordPropertyList, '/<int:fk_record>')
property_ns.add_resource(Property, '/<int:id>')
property_delete_ns.add_resource(PropertyDelete, '')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5022, debug=True)
