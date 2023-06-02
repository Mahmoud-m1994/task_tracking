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
