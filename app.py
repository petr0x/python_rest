from flask import request, jsonify

from support import milisToDate
from server import Device, History, db, app
from datetime import datetime
from sqlalchemy import and_


languages = [{'name': 'JS'}, {'name': 'Python'}, {'name': 'Ruby'}]


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It Works'})


@app.route('/devices', methods=['GET'])
def getDevices():
    devices = Device.query.all()
    return jsonify({'Devices': devices})


@app.route('/lang', methods=['POST'])
def addOne():
    language = {'name': request.json['name']}
    languages.append(language)
    return jsonify({'languages': languages})


@app.route('/device/<string:id>', methods=['GET'])
def getOne(id):
    device = Device.query.filter_by(id=id).first()
    return str(device.isOn)


@app.route('/device/<string:id>', methods=['POST'])
def editOne(id):
    device = Device.query.filter_by(id=id).first()
    device.owner = request.json['owner']
    device.isOn = request.json['is_on']
    if request.json['is_on'] == 1:
        max_id = len(History.query.all())
        new_data = History(max_id+1, id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0, request.json['owner'])
        db.session.add(new_data)
        db.session.commit()
    if request.json['is_on'] == 0:
        history = History.query.filter(and_(History.deviceId == id), (History.endTime == 0)).first()
        startTime = history.startTime
        startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        endTime = datetime.now()
        waitedTime = endTime - startTime
        waitedTime = milisToDate(waitedTime)
        history.waitedTime = waitedTime
        history.endTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.owner = request.json['owner']
        db.session.commit()
    return 'Updated'

if __name__ == '__main__':
    app.run(host="", port='5002')
