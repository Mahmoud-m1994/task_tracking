from dao.IsEmployeeAdmin import is_admin
from database.DatabaseConnector import disconnect_from_mysql, connect_to_mysql
from model.Position import Position
from model.MySqlResponse import MySqlResponse


def create_position(position: Position, responsible_id: str) -> MySqlResponse:
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can create positions", response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "INSERT INTO task_tracking.Position (name) VALUES (%s)"
        cursor.execute(query, (position.name,))
        connection.commit()

        return MySqlResponse("Position created successfully", response_code=MySqlResponse.CREATED)
    except Exception as err:
        return MySqlResponse(f"Error creating position: {err}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def fetch_positions() -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM task_tracking.Position ORDER BY position_id DESC"
        cursor.execute(query)
        rows = cursor.fetchall()

        positions = []
        for row in rows:
            position_id = row[0]
            name = row[1]
            position = Position(position_id, name)
            positions.append(position)

        return MySqlResponse(positions, response_code=MySqlResponse.OK)
    except Exception as err:
        return MySqlResponse(f"Error retrieving positions: {err}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_position_by_id(position_id: int) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM task_tracking.Position WHERE position_id = %s"
        cursor.execute(query, (position_id,))
        row = cursor.fetchone()

        if row:
            position = Position(row[0], row[1])
            return MySqlResponse(position, response_code=MySqlResponse.OK)
        else:
            return MySqlResponse("Position not found", response_code=MySqlResponse.NOT_FOUND)
    except Exception as error:
        return MySqlResponse(f"Error retrieving position by ID: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def update_position(position: Position, responsible_id: str) -> MySqlResponse:
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can update positions", response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "UPDATE task_tracking.Position SET name = %s WHERE position_id = %s"
        cursor.execute(query, (position.name, position.position_id))
        connection.commit()

        if cursor.rowcount > 0:
            return MySqlResponse("Position updated successfully", MySqlResponse.OK)
        else:
            return MySqlResponse("Position not found", MySqlResponse.NOT_FOUND)
    except Exception as error:
        print("Error updating position:", error)
        return MySqlResponse("Error updating position", MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def delete_position(position_id: int, responsible_id: str) -> MySqlResponse:
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can delete positions", response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM task_tracking.Position WHERE position_id = %s"
        cursor.execute(query, (position_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return MySqlResponse("Position deleted successfully", MySqlResponse.OK)
        else:
            return MySqlResponse("Position not found", MySqlResponse.NOT_FOUND)
    except Exception as error:
        print("Error deleting position:", error)
        return MySqlResponse("Error deleting position", MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)
