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


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column('ID', db.Integer, primary_key=True)
    deviceId = db.Column('device_id', db.Integer)
    startTime = db.Column('start_time', db.Unicode)
    endTime = db.Column('end_time', db.Unicode)
    waitedTime = db.Column('waited_time', db.Unicode)
    owner = db.Column('owner', db.Unicode)

    def __init__(self, id, deviceId, startTime, endTime, waitedTime, owner):
        self.id = id
        self.deviceId = deviceId
        self.startTime = startTime
        self.endTime = endTime
        self.waitedTime = waitedTime
        self.owner = owner