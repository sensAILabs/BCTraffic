from app import db
from sqlalchemy.ext.hybrid import hybrid_property


class Experiment(db.Model):
    __tablename__ = 'Experiments'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80))
    creator_name = db.Column('creator_name', db.String(80))
    create_at = db.Column('create_at', db.DateTime)
    update_at = db.Column('update_at', db.DateTime)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sound_channel1_dir = db.Column(db.String(80))
    person_id = db.Column(db.JSON, db.ForeignKey('person.id'),
                          nullable=False)


class saved_object():
    object_type: str
    id: str
    object_location: str

    def __init__(self, object_type, id, base_addr):
        self.object_type = object_type
        self.id = id
        self.object_location = '{base}/{id}'.format(base=base_addr, id=id)
