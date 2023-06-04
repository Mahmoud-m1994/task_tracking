from database.DatabaseConnector import connect_to_mysql, disconnect_from_mysql


def is_admin(responsible_id: str) -> bool:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT is_admin FROM task_tracking.Employee WHERE employee_id = %s"
        cursor.execute(query, (responsible_id,))
        result = cursor.fetchone()

        if result and result[0] == 1:
            return True
        else:
            return False

    except Exception as err:
        print(f"Error checking admin status: {err}")
        return False
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def employee_has_active_position(employee_id: str) -> bool:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT COUNT(*) FROM task_tracking.employee_position WHERE employee_id = %s AND is_active = 1"
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()

        if result and result[0] > 0:
            return True
        else:
            return False
    except Exception as error:
        print(f"Error checking user active position: {error}")
        return False
    finally:
        cursor.close()
        disconnect_from_mysql(connection)
