from dao.Authorization import user_has_active_position
from database.DatabaseConnector import disconnect_from_mysql, connect_to_mysql
from model.MySqlResponse import MySqlResponse
from model.Task import Task


def create_task(task: Task, responsible_id: str) -> MySqlResponse:
    if not user_has_active_position(responsible_id):
        return MySqlResponse("Only users with an active position can create tasks", response_code=MySqlResponse.UNAUTHORIZED)

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
            task = Task(task_id, name, description, date_active, created_at, status)
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
            task = Task(task_id, name, description, date_active, created_at, status)
            return MySqlResponse(response=task, response_code=MySqlResponse.OK)
        else:
            return MySqlResponse(response="Task not found", response_code=MySqlResponse.NOT_FOUND)
    except Exception as error:
        return MySqlResponse(response=f"Error retrieving task by ID: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def update_task(task: Task, responsible_id: str) -> MySqlResponse:
    if not user_has_active_position(responsible_id):
        return MySqlResponse("Only users with an active position can update tasks", response_code=MySqlResponse.UNAUTHORIZED)

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


def delete_task(task_id: int, responsible_id: str) -> MySqlResponse:
    if not user_has_active_position(responsible_id):
        return MySqlResponse("Only users with an active position can delete tasks", response_code=MySqlResponse.UNAUTHORIZED)

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
