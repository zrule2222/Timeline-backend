from ma import ma
from models.HistoryRecord import RecordModel


class RecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecordModel
        load_instance = True