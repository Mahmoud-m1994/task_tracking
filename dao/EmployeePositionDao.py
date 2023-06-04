from dao.Authorization import is_admin
from database.DatabaseConnector import disconnect_from_mysql, connect_to_mysql
from model.EmployeePosition import EmployeePosition
from model.MySqlResponse import MySqlResponse
from utilities.DateValidator import (
    is_start_date_after_end_date_or_equal,
    is_date_in_past,
    is_existing_end_date_after_start_date,
    is_existing_end_date_after_end_date,
    is_existing_start_date_after_end_date
)


def create_employee_position(employee_position: EmployeePosition, responsible_id: str) -> MySqlResponse:
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can create employee positions", response_code=MySqlResponse.UNAUTHORIZED)

    # Check if the start date is after the end date
    if is_start_date_after_end_date_or_equal(employee_position.start_date, employee_position.end_date):
        return MySqlResponse("Start-date cannot be after the end-date", response_code=MySqlResponse.BAD_REQUEST)

    # Check if the start or end date is in the past
    if is_date_in_past(str(employee_position.start_date)) or is_date_in_past(str(employee_position.end_date)):
        return MySqlResponse("Start or end-date cannot be in the past", response_code=MySqlResponse.BAD_REQUEST)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # Check if the targeted employee has any active position
        query = "SELECT end_date FROM task_tracking.employee_position " \
                "WHERE employee_id = %s AND is_active = 1 " \
                "ORDER BY created_at DESC LIMIT 1"
        cursor.execute(query, (employee_position.employee_id,))
        row = cursor.fetchone()

        if row:
            print('meh')
            print(str(row[0]))
            if employee_position.is_active == 1:
                return MySqlResponse("Already has active position, do you want to set this one to active anyway ?",
                                     response_code=MySqlResponse.ALREADY_EXISTING)
            existing_end_date = row[0]
            # Check if the new position starts before the existing position ends
            if is_existing_end_date_after_start_date(str(existing_end_date), str(employee_position.start_date)):
                return MySqlResponse("Cannot start a new position before the existing one ends",
                                     response_code=MySqlResponse.BAD_REQUEST)

            # Check if the new position ends before or at the same time as the existing position ends
            if is_existing_end_date_after_end_date(str(existing_end_date), str(employee_position.end_date)):
                return MySqlResponse("Cannot end a new position before or at the same time as the existing one ends",
                                     response_code=MySqlResponse.BAD_REQUEST)

            # Check if the existing position starts before the new position ends
            if is_existing_start_date_after_end_date(str(existing_end_date), str(employee_position.end_date)):
                return MySqlResponse("Cannot end a new position before the existing one starts",
                                     response_code=MySqlResponse.BAD_REQUEST)

        # Create the new position
        create_position_query = "INSERT INTO task_tracking.employee_position " \
                                "(employee_id, position_id, start_date, end_date, created_at, is_active) " \
                                "VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(create_position_query, (
            employee_position.employee_id,
            employee_position.position_id,
            employee_position.start_date,
            employee_position.end_date,
            datetime.now(),
            employee_position.is_active
        ))
        connection.commit()

        return MySqlResponse("Employee position created successfully", response_code=MySqlResponse.CREATED)
    except Exception as e:
        return MySqlResponse(str(e), response_code=MySqlResponse.ERROR)

    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_positions_for_employee(employee_id: str) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM task_tracking.employee_position " \
                "WHERE employee_id = %s ORDER BY created_at DESC"
        cursor.execute(query, (employee_id,))
        rows = cursor.fetchall()

        positions = []
        for row in rows:
            id = row[0]
            employee_id = row[1]
            position_id = row[2]
            start_date = row[3]
            end_date = row[4]
            created_at = row[5]
            is_active = row[6]

            position = EmployeePosition(id, employee_id, position_id, start_date, end_date, created_at, is_active)

            positions.append(position)

        if len(positions) == 0:
            return MySqlResponse("No positions found for the given employee ID",
                                 response_code=MySqlResponse.NOT_FOUND)

        return MySqlResponse(positions, response_code=MySqlResponse.OK)
    except Exception as err:
        print(f"Error retrieving positions: {err}")
        return MySqlResponse("Error retrieving positions",
                             response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_active_position(employee_id: str) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM task_tracking.employee_position " \
                "WHERE employee_id = %s AND is_active = 1"
        cursor.execute(query, (employee_id,))
        row = cursor.fetchone()

        if row:
            id = row[0]
            employee_id = row[1]
            position_id = row[2]
            start_date = row[3]
            end_date = row[4]
            created_at = row[5]
            is_active = row[6]

            position = EmployeePosition(id, employee_id, position_id, start_date, end_date, created_at, is_active)

            return MySqlResponse(response=position, response_code=MySqlResponse.OK)
        else:
            return MySqlResponse("No active position found", response_code=MySqlResponse.NOT_FOUND)
    except Exception as error:
        return MySqlResponse(f"Error fetching active position: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


from datetime import datetime


def change_position_status(employee_id: str, employee_positions_id: int, responsible_id: str, is_active: int) -> MySqlResponse:
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can create employee positions", response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM task_tracking.employee_position WHERE employee_id = %s AND id = %s"
        cursor.execute(query, (employee_id, employee_positions_id))
        row_to_be_updated = cursor.fetchone()

        if not row_to_be_updated:
            return MySqlResponse("Position not found or does not belong to the employee",
                                 response_code=MySqlResponse.NOT_FOUND)

        if is_active == 0:
            end_date = datetime.now()
        else:
            end_date = row_to_be_updated[4]

        active_query = "SELECT * FROM task_tracking.employee_position WHERE employee_id = %s AND is_active = 1"
        cursor.execute(active_query, (employee_id,))
        existing_row = cursor.fetchone()

        if existing_row and is_active == 1:
            return MySqlResponse("There is already an active position for the employee",
                                 response_code=MySqlResponse.ALREADY_EXISTING)

        update_query = "UPDATE task_tracking.employee_position SET is_active = %s, end_date = %s " \
                       "WHERE employee_id = %s AND id = %s"
        cursor.execute(update_query, (is_active, end_date, employee_id, employee_positions_id))
        connection.commit()

        return MySqlResponse("Position status updated successfully", response_code=MySqlResponse.OK)
    except Exception as error:
        return MySqlResponse(f"Error changing position status: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def change_position_dates(
        employee_id: str,
        position_id: int,
        responsible_id: str,
        start_date: datetime = None,
        end_date: datetime = None
) -> MySqlResponse:
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can create employee positions", response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # Check if the position exists and belongs to the employee
        query = "SELECT * FROM task_tracking.employee_position " \
                "WHERE employee_id = %s AND position_id = %s"
        cursor.execute(query, (employee_id, position_id))
        row = cursor.fetchone()

        if not row:
            return MySqlResponse("Position not found or does not belong to the employee",
                                 response_code=MySqlResponse.NOT_FOUND)

        # Update the start and/or end date
        query = "UPDATE task_tracking.employee_position SET start_date = %s, end_date = %s " \
                "WHERE employee_id = %s AND position_id = %s"
        cursor.execute(query, (start_date, end_date, employee_id, position_id))
        connection.commit()

        return MySqlResponse("Position dates updated successfully", response_code=MySqlResponse.OK)
    except Exception as error:
        return MySqlResponse(f"Error changing position dates: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def delete_employee_position(employee_id: str, position_id: int, responsible_id: str):
    if not is_admin(responsible_id):
        return MySqlResponse("Only admins can delete employee positions", response_code=MySqlResponse.UNAUTHORIZED)

    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # Check if the position exists and belongs to the employee
        query = "SELECT * FROM task_tracking.employee_position WHERE employee_id = %s AND id = %s"
        cursor.execute(query, (employee_id, position_id))
        row = cursor.fetchone()

        if not row:
            return MySqlResponse("Position not found or does not belong to the employee",
                                 response_code=MySqlResponse.NOT_FOUND)

        # Delete the position
        query = "DELETE FROM task_tracking.employee_position WHERE employee_id = %s AND id = %s"
        cursor.execute(query, (employee_id, position_id))
        connection.commit()

        return MySqlResponse("Position deleted successfully", response_code=MySqlResponse.OK)
    except Exception as error:
        return MySqlResponse(f"Error deleting position: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)

