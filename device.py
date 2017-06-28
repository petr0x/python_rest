from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.db'
db = SQLAlchemy(app)


class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column('ID', db.Integer, primary_key=True)
    isOn = db.Column('is_on', db.Integer)
    owner = db.Column('owner', db.Unicode)

    def __init__(self, id, isOn, owner):
        self.id = id
        self.isOn = isOn
        self.owner = owner
