import json
from flask import Blueprint, request
from dao import PositionDao
from model.MySqlResponse import MySqlResponse
from model.Position import Position

position_api = Blueprint("position_api", __name__)
dao = PositionDao


@position_api.route("/position", methods=["POST"])
def create_position():
    data = request.get_json()
    name = data.get("name")
    responsible_id = data.get("responsible_id")
    position = Position(name=name)
    response = dao.create_position(position, responsible_id)
    return json.dumps(response.__dict__)


@position_api.route("/positions", methods=["GET"])
def get_positions():
    response = dao.fetch_positions()
    if response.response_code == MySqlResponse.OK:
        positions = response.response
        response_data = {
            "response": [position.__dict__ for position in positions],
            "response_code": response.response_code
        }
        return json.dumps(response_data)
    else:
        return json.dumps(response.__dict__)


@position_api.route("/position/<int:position_id>/<string:name>", methods=["GET"])
@position_api.route("/position/<int:position_id>", methods=["GET"])
def get_position_by_id(position_id, name=None):
    response = dao.get_position_by_id_or_name(position_id, name)
    if response.response_code == MySqlResponse.OK:
        position = response.response
        response_data = {
            "response": position.__dict__,
            "response_code": response.response_code
        }
        return json.dumps(response_data)
    else:
        return json.dumps(response.__dict__)


@position_api.route("/position/<int:position_id>", methods=["PUT"])
def update_position(position_id):
    data = request.get_json()
    name = data.get("name")
    responsible_id = data.get("responsible_id")
    position = Position(position_id=position_id, name=name)
    response = dao.update_position(position, responsible_id)
    return json.dumps(response.__dict__)


@position_api.route("/position/<int:position_id>/<string:name>", methods=["DELETE"])
@position_api.route("/position/<string:name>/<int:position_id>", methods=["DELETE"])
@position_api.route("/position/<int:position_id>", methods=["DELETE"])
def delete_position(position_id, name=None):
    data = request.get_json()
    responsible_id = data.get("responsible_id")
    response = dao.delete_position(position_id, name, responsible_id)
    return json.dumps(response.__dict__)
