from dao.IsEmployeeAdmin import is_admin
from database.DatabaseConnector import disconnect_from_mysql, connect_to_mysql
from model.Employee import Employee
from model.MySqlResponse import MySqlResponse


def create_employee(employee: Employee, responsible_id: str) -> MySqlResponse:
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can create employees", response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT COUNT(*) FROM task_tracking.Employee WHERE employee_id = %s"
        cursor.execute(query, (employee.employee_id,))
        result = cursor.fetchone()
        if result[0] > 0:
            return MySqlResponse("Employee with the same employee_id already exists", response_code=MySqlResponse.ALREADY_EXISTING)

        query = "INSERT INTO task_tracking.Employee (employee_id, name) VALUES (%s, %s)"
        cursor.execute(query, (employee.employee_id, employee.name))
        connection.commit()

        return MySqlResponse("Employee created successfully", response_code=MySqlResponse.CREATED)
    except Exception as err:
        return MySqlResponse(f"Error creating employee: {err}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def fetch_employees() -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM task_tracking.Employee ORDER BY employee_id DESC"
        cursor.execute(query)
        rows = cursor.fetchall()

        employees = []
        for row in rows:
            print('row ' + str(row))
            employee_id = row[0]
            name = row[1]
            is_employee_admin = row[2]
            employee = Employee(employee_id, name, is_employee_admin)
            employees.append(employee)

        if len(employees) == 0:
            return MySqlResponse("No positions found for the given employee ID",
                                 response_code=MySqlResponse.NOT_FOUND)

        return MySqlResponse(employees, response_code=MySqlResponse.OK)
    except Exception as err:
        print(f"Error retrieving employees: {err}")
        return MySqlResponse("Error retrieving positions",
                             response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_employee_by_id(employee_id: str) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM task_tracking.Employee WHERE employee_id = %s"
        cursor.execute(query, (employee_id,))
        row = cursor.fetchone()

        if row:
            employee = Employee(row[0], row[1], row[2])
            return MySqlResponse(response=employee, response_code=MySqlResponse.OK)
        else:
            return MySqlResponse(response="Employee not found", response_code=MySqlResponse.NOT_FOUND)
    except Exception as error:
        return MySqlResponse(response=f"Error retrieving employee by ID: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def update_employee(employee: Employee, responsible_id: str) -> MySqlResponse:
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can update employees", response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "UPDATE task_tracking.Employee SET name = %s WHERE employee_id = %s"
        cursor.execute(query, (employee.name, employee.employee_id))
        connection.commit()

        if cursor.rowcount > 0:
            return MySqlResponse("Employee updated successfully", MySqlResponse.OK)
        else:
            return MySqlResponse("Employee not found", MySqlResponse.NOT_FOUND)
    except Exception as error:
        print("Error updating employee:", error)
        return MySqlResponse("Error updating employee", MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def delete_employee(employee_id: str, responsible_id: str) -> MySqlResponse:
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can delete employees", response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM task_tracking.Employee WHERE employee_id = %s"
        cursor.execute(query, (employee_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return MySqlResponse("Employee deleted successfully", MySqlResponse.OK)
        else:
            return MySqlResponse("Employee not found", MySqlResponse.NOT_FOUND)
    except Exception as error:
        print("Error deleting employee:", error)
        return MySqlResponse("Error deleting employee", MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)
