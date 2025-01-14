import json
from datetime import datetime

from model.EmployeePosition import EmployeePosition
from model.Task import Task


class JsonWithDateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, EmployeePosition):
            return obj.__dict__
        elif isinstance(obj, Task):
            return obj.__dict__
        return super().default(obj)

