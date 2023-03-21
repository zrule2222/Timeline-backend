from db import db
from typing import List
from sqlalchemy.sql import func
from flask_sqlalchemy import Pagination
import datetime

class RecordModel(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    description_short = db.Column(db.String, nullable=False)
    record_type = db.Column(db.String, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    def __init__(self, name, date,description,description_short,record_type,is_visible,created_at = func.now(),updated_at = func.now()):
        self.name = name
        self.date = date
        self.description = description
        self.description_short = description_short
        self.record_type = record_type
        self.is_visible = is_visible
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return 'RecordModel(name=%s, date=%s, description=%s, description_short=%s, record_type=%s , is_visible=%s, created_at=%s,updated_at=%s)' % (self.name, self.date, self.description, self.description_short, self.record_type, self.is_visible, self.created_at,self.updated_at)

    def json(self):
        return {'name': self.name, 'date': self.date, 'description': self.description, 'description_short': self.description_short, 'record_type': self.record_type, 'is_visible': self.is_visible, 'created_at': self.created_at, 'updated_at': self.updated_at}
    
    @classmethod
    def find_by_name(cls, name) -> "RecordModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "RecordModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["RecordModel"]:
        return cls.query.all()
    
    @classmethod
    def find_all_events(cls) -> List["RecordModel"]:
        return cls.query.filter_by(record_type="event").all()
    
    @classmethod
    def find_all_products(cls) -> List["RecordModel"]:
        return cls.query.filter_by(record_type="product").all()
    
    @classmethod
    def find_all_visible_records(cls) -> List["RecordModel"]:
        return cls.query.filter_by(is_visible=True).all()

    #@classmethod
    #def get_paginated(cls,page,limit) -> List["RecordModel"]:
    #        return cls.query.paginate(page, per_page=limit)
    
    #@classmethod
    #def get_paginated_search(cls,page,limit,value) -> "RecordModel":
    #     return cls.query.filter(cls.title.like((f'%{value}%')) | cls.body.like(f'%{value}%') | cls.created_at.like(f'%{value}%') | cls.updated_at.like(f'%{value}%')).paginate(page, per_page=limit)

    


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()