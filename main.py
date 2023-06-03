from flask import Flask
from api.EmployeeApi import employee_api

app = Flask(__name__)
app.register_blueprint(employee_api)

if __name__ == '__main__':
    print('Hey from Task tracking server')
    # connect_to_mysql()
    app.run()
