from ma import ma
from models.RecordProperty import PropertyModel
from schemas.HistoryRecord import RecordSchema

class PropertySchema(ma.SQLAlchemyAutoSchema):
   
    class Meta:
        model = PropertyModel
        load_instance = True
        #load_only = ("record")
        include_fk= True