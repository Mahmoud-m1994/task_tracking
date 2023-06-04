from datetime import datetime

from dao.Authorization import employee_has_active_position
from database.DatabaseConnector import disconnect_from_mysql, connect_to_mysql
from model.EmployeeTask import EmployeeTask
from model.MySqlResponse import MySqlResponse
from model.Task import Task


def create_task(task: Task, responsible_id: str) -> MySqlResponse:
    if not employee_has_active_position(responsible_id):
        return MySqlResponse("Only users with an active position can create tasks",
                             response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "INSERT INTO task_tracking.Task (name, description, date_active, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (task.name, task.description, task.date_active, task.status))
        connection.commit()

        return MySqlResponse("Task created successfully", response_code=MySqlResponse.CREATED)
    except Exception as err:
        return MySqlResponse(f"Error creating task: {err}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def fetch_tasks() -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM task_tracking.Task ORDER BY task_id DESC"
        cursor.execute(query)
        rows = cursor.fetchall()

        tasks = []
        for row in rows:
            task_id = row[0]
            name = row[1]
            description = row[2]
            date_active = row[3]
            created_at = row[4]
            status = row[5]
            task = Task(
                task_id=task_id,
                name=name,
                description=description,
                date_active=date_active,
                created_at=created_at,
                status=status
            )
            tasks.append(task)

        if len(tasks) == 0:
            return MySqlResponse("No tasks found", response_code=MySqlResponse.NOT_FOUND)

        return MySqlResponse(tasks, response_code=MySqlResponse.OK)
    except Exception as err:
        print(f"Error retrieving tasks: {err}")
        return MySqlResponse("Error retrieving tasks", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def fetch_employee_tasks(task_id: int) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM employee_task WHERE task_id = %s"
        cursor.execute(query, (task_id,))
        rows = cursor.fetchall()

        employee_tasks = []
        for row in rows:
            task_id = row[0]
            assigned_to_id = row[1]
            position_id = row[2]
            assigned_by_id = row[3]
            assigned_date = row[4]
            employee_task = EmployeeTask(
                task_id=task_id,
                assigned_to_id=assigned_to_id,
                position_id=position_id,
                assigned_by_id=assigned_by_id,
                assigned_date=assigned_date
            )
            employee_tasks.append(employee_task)

        if len(employee_tasks) == 0:
            return MySqlResponse("No employee tasks found", response_code=MySqlResponse.NOT_FOUND)

        return MySqlResponse(employee_tasks, response_code=MySqlResponse.OK)
    except Exception as error:
        print(f"Error retrieving employee tasks: {error}")
        return MySqlResponse("Error retrieving employee tasks", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def fetch_employee_tasks_by_assigned_to_id(assigned_to_id: str) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM employee_task WHERE assigned_to_id = %s"
        cursor.execute(query, (assigned_to_id,))
        rows = cursor.fetchall()

        employee_tasks = []
        for row in rows:
            task_id = row[0]
            assigned_to_id = row[1]
            position_id = row[2]
            assigned_by_id = row[3]
            assigned_date = row[4]
            employee_task = EmployeeTask(
                task_id=task_id,
                assigned_to_id=assigned_to_id,
                position_id=position_id,
                assigned_by_id=assigned_by_id,
                assigned_date=assigned_date
            )
            employee_tasks.append(employee_task)

        if len(employee_tasks) == 0:
            return MySqlResponse("No employee tasks found", response_code=MySqlResponse.NOT_FOUND)

        return MySqlResponse(employee_tasks, response_code=MySqlResponse.OK)
    except Exception as error:
        print(f"Error retrieving employee tasks by assigned_to_id: {error}")
        return MySqlResponse("Error retrieving employee tasks", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_task_by_id(task_id: int) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM task_tracking.Task WHERE task_id = %s"
        cursor.execute(query, (task_id,))
        row = cursor.fetchone()

        if row:
            task_id = row[0]
            name = row[1]
            description = row[2]
            date_active = row[3]
            created_at = row[4]
            status = row[5]
            task = Task(
                task_id=task_id,
                name=name,
                description=description,
                date_active=date_active,
                created_at=created_at,
                status=status
            )
            return MySqlResponse(response=task, response_code=MySqlResponse.OK)
        else:
            return MySqlResponse(response="Task not found", response_code=MySqlResponse.NOT_FOUND)
    except Exception as error:
        return MySqlResponse(response=f"Error retrieving task by ID: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def update_task(task: Task, responsible_id: str) -> MySqlResponse:
    if not employee_has_active_position(responsible_id):
        return MySqlResponse("Only users with an active position can update tasks",
                             response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "UPDATE task_tracking.Task SET name = %s, description = %s, date_active = %s, status = %s WHERE task_id = %s"
        cursor.execute(query, (task.name, task.description, task.date_active, task.status, task.task_id))
        connection.commit()

        if cursor.rowcount > 0:
            return MySqlResponse("Task updated successfully", MySqlResponse.OK)
        else:
            return MySqlResponse("Task not found", MySqlResponse.NOT_FOUND)
    except Exception as error:
        print("Error updating task:", error)
        return MySqlResponse("Error updating task", MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def assign_task(
        task_id: int,
        assigned_to_id: str,
        assigned_by_id: str,
        assigned_date: datetime = None
) -> MySqlResponse:
    assigned_by_has_active_position = employee_has_active_position(assigned_by_id)
    assigned_to_has_active_position = employee_has_active_position(assigned_to_id)

    if not task_exists(task_id):
        return MySqlResponse("Task not found", MySqlResponse.NOT_FOUND)

    if not assigned_by_has_active_position or not assigned_to_has_active_position:
        return MySqlResponse("Both assigned_by and assigned_to must have an active position",
                             response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = """
        SELECT * FROM task_tracking.employee_position
        WHERE employee_id = %s AND is_active = 1
        AND start_date <= (SELECT date_active FROM task_tracking.Task WHERE task_id = %s)
        AND (end_date IS NULL OR end_date >= (SELECT date_active FROM task_tracking.Task WHERE task_id = %s))
        """
        cursor.execute(query, (assigned_to_id, task_id, task_id))
        result = cursor.fetchone()

        if result is None:
            return MySqlResponse(
                "The active_date for the task is not within the start and end date of the employee's position",
                response_code=MySqlResponse.UNAUTHORIZED)

        position_id = result[2]

        query = "INSERT INTO task_tracking.employee_task (task_id, assigned_to_id, position_id, assigned_by_id, assigned_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (task_id, assigned_to_id, position_id, assigned_by_id, assigned_date))
        connection.commit()

        return MySqlResponse("Task assigned successfully", response_code=MySqlResponse.CREATED)
    except Exception as err:
        return MySqlResponse(f"Error assigning task: {err}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def unassigned_task(task_id: int, unassigned_from: str, unassigned_by: str) -> MySqlResponse:
    if not task_exists(task_id):
        return MySqlResponse("Task not found", MySqlResponse.NOT_FOUND)

    if not employee_has_active_position(unassigned_by):
        return MySqlResponse("Unassigned requires an active position for unassigned_by",
                             response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = """
        DELETE FROM task_tracking.employee_task
        WHERE task_id = %s AND assigned_to_id = %s AND assigned_by_id = %s
        """
        cursor.execute(query, (task_id, unassigned_from, unassigned_by))
        connection.commit()

        if cursor.rowcount > 0:
            return MySqlResponse("Task unassigned successfully", response_code=MySqlResponse.OK)
        else:
            return MySqlResponse("Task assignment failed. Task not found or assignment conditions not met",
                                 response_code=MySqlResponse.NOT_FOUND)
    except Exception as err:
        return MySqlResponse(f"Error unassigned task: {err}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def delete_task(task_id: int, responsible_id: str) -> MySqlResponse:
    if not employee_has_active_position(responsible_id):
        return MySqlResponse("Only users with an active position can delete tasks",
                             response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM task_tracking.Task WHERE task_id = %s"
        cursor.execute(query, (task_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return MySqlResponse("Task deleted successfully", MySqlResponse.OK)
        else:
            return MySqlResponse("Task not found", MySqlResponse.NOT_FOUND)
    except Exception as error:
        print("Error deleting task:", error)
        return MySqlResponse("Error deleting task", MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def delete_all_employee_tasks():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # Delete all employee tasks where task_id > 0
        query = "DELETE FROM task_tracking.employee_task WHERE task_id > 0"
        cursor.execute(query)
        connection.commit()

        return MySqlResponse("All employee tasks deleted successfully", response_code=MySqlResponse.OK)
    except Exception as error:
        return MySqlResponse(f"Error deleting employee tasks: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_max_task_id() -> int:
    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()

        query = "SELECT MAX(task_id) FROM Task"
        cursor.execute(query)
        result = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if result is not None:
            return int(result)
        else:
            return -1
    except Exception as error:
        print("Error while connecting to MySQL:", error)
        return -1


def task_exists(task_id: int) -> bool:
    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()

        query = "SELECT task_id FROM Task WHERE task_id = %s"
        cursor.execute(query, (task_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result is not None:
            return True
        else:
            return False
    except Exception as error:
        print("Error while connecting to MySQL:", error)
        return False


delete_all_employee_tasks.__unittest_skip__ = True