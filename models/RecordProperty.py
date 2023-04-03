from db import db
from typing import List
from sqlalchemy.sql import func
from flask_sqlalchemy import Pagination
import datetime

class PropertyModel(db.Model):
    __tablename__ = "properties" 

    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(db.String, nullable=False)
    fk_record = db.Column(db.Integer,db.ForeignKey('records.id'),nullable=False)
    record = db.relationship('RecordModel', back_populates="property")
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    def __init__(self, property, fk_record,created_at = func.now(),updated_at = func.now()):
        self.property = property
        self.fk_record = fk_record
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return 'PropertyModel(property=%s, fk_record=%s, created_at=%s,updated_at=%s)' % (self.property, self.fk_record, self.created_at,self.updated_at)

    def json(self):
        return {'property': self.property, 'fk_record': self.fk_record, 'created_at': self.created_at, 'updated_at': self.updated_at}
    
    @classmethod
    def find_by_id(cls, id) -> "PropertyModel":
        return cls.query.filter_by(id=id)
    
    @classmethod
    def find_all_record_properties(cls, fk_record) -> "PropertyModel":
        return cls.query.filter_by(fk_record=fk_record)
    @classmethod
    def find_by_fk(cls, fk_record) -> "PropertyModel":
        return cls.query.filter_by(fk_record=fk_record)
    
    def save_to_db(self) -> None:
     db.session.add(self)
     db.session.commit()

    def delete_from_db(self) -> None:
      db.session.delete(self)
      db.session.commit()
    