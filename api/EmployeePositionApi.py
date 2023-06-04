import json
from flask import Blueprint, request
from datetime import datetime
from dao import EmployeePositionDao
from model.EmployeePosition import EmployeePosition
from model.MySqlResponse import MySqlResponse
from utilities.JsonWithDateEncoder import JsonWithDateEncoder

employee_position_api = Blueprint('employee_position_api', __name__)
dao = EmployeePositionDao


@employee_position_api.route('/employee_position', methods=['POST'])
def create_position_employee_relation():
    data = request.get_json()

    employee_id = data.get('employee_id')
    position_id = data.get('position_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    is_active = data.get('is_active')
    responsible_id = data.get('responsible_id')

    employee_position = EmployeePosition(
        -1,
        employee_id,
        position_id,
        start_date,
        end_date,
        datetime.now(),
        is_active
    )

    response = dao.create_employee_position(employee_position, responsible_id)
    return json.dumps(response.__dict__)


@employee_position_api.route('/employee_positions/<employee_id>', methods=['GET'])
def get_positions_by_employee_id(employee_id):
    response = dao.get_positions_for_employee(employee_id)
    if response.response_code == MySqlResponse.OK:
        positions = response.response
        response_data = {
            "response": [position.__dict__ for position in positions],
            "response_code": response.response_code
        }
        return json.dumps(response_data, cls=JsonWithDateEncoder)
    else:
        return json.dumps(response.__dict__, cls=JsonWithDateEncoder)


@employee_position_api.route('/employee_position/active/<employee_id>', methods=['GET'])
def get_active_position(employee_id: str):
    response = dao.get_active_position(employee_id)
    return json.dumps(response.__dict__, cls=JsonWithDateEncoder)


@employee_position_api.route('/employee_position/status', methods=['PUT'])
def change_position_status():
    data = request.get_json()
    employee_id = data.get('employee_id')
    employee_position_id = data.get('employee_position_id')
    responsible_id = data.get('responsible_id')
    is_active = data.get('is_active')

    response = dao.change_position_status(employee_id, employee_position_id, responsible_id, is_active)
    return json.dumps(response.__dict__)


@employee_position_api.route('/employee_position/dates', methods=['PUT'])
def change_position_dates():
    data = request.get_json()
    employee_id = data.get('employee_id')
    position_id = data.get('position_id')
    responsible_id = data.get('responsible_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    response = dao.change_position_dates(employee_id, position_id, responsible_id, start_date, end_date)
    return json.dumps(response.__dict__)


@employee_position_api.route('/employee_position', methods=['DELETE'])
def delete_position():
    data = request.get_json()
    employee_id = data.get('employee_id')
    position_id = data.get('position_id')
    responsible_id = data.get('responsible_id')

    response = dao.delete_employee_position(employee_id, position_id, responsible_id)
    return json.dumps(response.__dict__)
