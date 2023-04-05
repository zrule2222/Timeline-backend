from ma import ma
from models.RecordProperty import PropertyModel
from schemas.HistoryRecord import RecordSchema

class PropertySchema(ma.SQLAlchemyAutoSchema):
    # items = ma.Nested(RecordSchema, many=True)
   
    class Meta:
        model = PropertyModel
        load_instance = True
        #load_only = ("record")
        include_fk= True