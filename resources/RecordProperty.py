# from flask import request
# from flask_restplus import Resource, fields, Namespace
# from sqlalchemy.sql import func
# #from auth.views import LoginAPI

# from models.RecordProperty import PropertyModel
# from schemas.RecordProperty import PropertySchema
# from models.HistoryRecord import RecordModel

# PROPERTY_NOT_FOUND = "Property not found."
# USER_ALREADY_EXISTS = "User '{}' Already exists."


# property_ns = Namespace('Property', description='Property related operations')
# properties_ns = Namespace('Properties', description='Properties related operations')

# property_schema = PropertySchema()
# property_list_schema = PropertySchema(many=True)

# #Model required by flask_restplus for expect
# property = property_ns.model('Property', {
#     'property': fields.String,
#     'fk_record': fields.Integer,
# })

# class Property(Resource):

#     def get(self, id):
#         property_data = PropertyModel.find_by_id(id)
#         if property_data:
#             return property_schema.dump(property_data)
#         return {'message': PROPERTY_NOT_FOUND}, 404
    
# class RecordPropertyList(Resource):
#     @properties_ns.doc('Get all the properties of record')
#     def get(self, fk_record):
#         return property_list_schema.dump(PropertyModel.find_all_record_properties(fk_record)), 200

#     @properties_ns.expect(property)
#     @properties_ns.doc('Create record properties')
#     def post(self, fk_record):
#         properties_json = request.get_json()
        
#         if RecordModel.find_by_id(fk_record):
#             #return {'message': RECORD_ALREADY_EXISTS.format(name)}, 400
#          for property in properties_json:
#           record_property = property_schema.load(property)
#           record_property.save_to_db()

#         return property_schema.dump(properties_json), 201
