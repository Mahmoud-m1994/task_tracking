import json
from datetime import datetime

from flask import Blueprint, request
from dao import TaskDao
from model.Task import Task
from model.MySqlResponse import MySqlResponse
from utilities.JsonWithDateEncoder import JsonWithDateEncoder

task_api = Blueprint("task_api", __name__)
dao = TaskDao


@task_api.route("/task", methods=["POST"])
def create_task():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    date_active = data.get("date_active")
    status = data.get("status")
    responsible_id = data.get("responsible_id")
    task = Task(task_id=-1, name=name, description=description, date_active=date_active, status=status)
    response = dao.create_task(task, responsible_id)
    return json.dumps(response.__dict__)


@task_api.route("/tasks", methods=["GET"])
def get_tasks():
    response = dao.fetch_tasks()
    if response.response_code == MySqlResponse.OK:
        positions = response.response
        response_data = {
            "response": [position.__dict__ for position in positions],
            "response_code": response.response_code
        }
        return json.dumps(response_data, cls=JsonWithDateEncoder)
    else:
        return json.dumps(response.__dict__, cls=JsonWithDateEncoder)


@task_api.route("/task/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    response = dao.get_task_by_id(task_id)
    return json.dumps(response.__dict__, cls=JsonWithDateEncoder)


@task_api.route("/task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    date_active = data.get("date_active")
    status = data.get("status")
    responsible_id = data.get("responsible_id")
    task = Task(task_id=task_id, name=name, description=description, date_active=date_active, status=status)
    response = dao.update_task(task, responsible_id)
    return json.dumps(response.__dict__)


@task_api.route("/task/assign", methods=["POST"])
def assign_task():
    data = request.get_json()
    task_id = data.get("task_id")
    assigned_to_id = data.get("assigned_to_id")
    assigned_by_id = data.get("assigned_by_id")
    assigned_date = datetime.now()

    response = dao.assign_task(task_id, assigned_to_id, assigned_by_id, assigned_date)
    return json.dumps(response.__dict__)


@task_api.route("/task/unassigned", methods=["POST"])
def unassigned_task():
    data = request.get_json()
    task_id = data.get("task_id")
    unassigned_from = data.get("unassigned_from")
    unassigned_by = data.get("unassigned_by")

    response = dao.unassigned_task(task_id, unassigned_from, unassigned_by)
    return json.dumps(response.__dict__)

@task_api.route("/task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    data = request.get_json()
    responsible_id = data.get("responsible_id")
    response = dao.delete_task(task_id, responsible_id)
    return json.dumps(response.__dict__)
