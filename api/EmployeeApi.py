import json
import uuid

from flask import Blueprint, request
from dao import EmployeeDao
from model.Employee import Employee
from model.MySqlResponse import MySqlResponse

employee_api = Blueprint("employee_api", __name__)
dao = EmployeeDao


@employee_api.route("/employee", methods=["POST"])
def create_employee():
    data = request.get_json()
    name = data.get("name")
    responsible_id = data.get("responsible_id")
    is_new_admin = data.get("is_admin")
    employee_id = generate_text_uuid()
    employee = Employee(employee_id=employee_id, name=name, is_admin=is_new_admin)
    print(employee.employee_id, employee.name)
    response = dao.create_employee(employee, responsible_id)
    return json.dumps(response.__dict__)


@employee_api.route("/employees", methods=["GET"])
def get_employees():
    print('hello')
    response = dao.fetch_employees()
    if response.response_code == MySqlResponse.OK:
        employees = response.response
        response_data = {
            "response": [employee.__dict__ for employee in employees],
            "response_code": response.response_code
        }
        print(str(json.dumps(response_data)))
        return json.dumps(response_data)
    else:
        return json.dumps(response.__dict__)


@employee_api.route("/employee/<string:employee_id>", methods=["GET"])
def get_employee_by_id(employee_id):
    response = dao.get_employee_by_id(employee_id)
    if response.response_code == MySqlResponse.OK:
        employee = response.response
        response_data = {
            "response": employee.__dict__,
            "response_code": response.response_code
        }
        return json.dumps(response_data)
    elif response.response_code == MySqlResponse.NOT_FOUND:
        return json.dumps({
            "response": "Employee not found",
            "response_code": response.response_code
        })
    else:
        return json.dumps({
            "response": "Something wrong happened, try again",
            "response_code": response.response_code
        })


@employee_api.route("/employee/<string:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json()
    name = data.get("name")
    responsible_id = data.get("responsible_id")
    employee = Employee(employee_id=employee_id, name=name)
    response = dao.update_employee(employee, responsible_id)
    return json.dumps(response.__dict__)


@employee_api.route("/employee/<string:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    data = request.get_json()
    responsible_id = data.get("responsible_id")  # Get the responsible_id from the JSON payload
    response = dao.delete_employee(employee_id, responsible_id)
    return json.dumps(response.__dict__)


def generate_text_uuid():
    unique_id = str(uuid.uuid4())
    text_uuid = 'employee-id_' + unique_id
    return text_uuid
