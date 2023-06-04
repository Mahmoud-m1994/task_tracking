from flask import Flask
from api.EmployeeApi import employee_api
from api.PositionApi import position_api
from api.EmployeePositionApi import employee_position_api
from api.TaskApi import task_api

app = Flask(__name__)
app.register_blueprint(employee_api)
app.register_blueprint(position_api)
app.register_blueprint(employee_position_api)
app.register_blueprint(task_api)

if __name__ == '__main__':
    print('Hey from Task tracking server')
    app.run()
