import unittest
from unittest import mock
from dao import TaskDao
from model.MySqlResponse import MySqlResponse

dao = TaskDao


class EmployeeTaskMock(unittest.TestCase):
    def test_fetch_employee_tasks(self):
        mock_cursor = mock.Mock()
        mock_connection = mock.Mock()
        mock_connection.cursor.return_value = mock_cursor

        tasks_employee = [
            (1, "assigned_to_id1", 1, "assigned_by_id_1", "2023-01-01 10:00:00"),
            (2, "assigned_to_id2", 2, "assigned_by_id_2", "2023-01-02 12:00:00")
        ]
        mock_cursor.fetchall.return_value = tasks_employee
        dao.connect_to_mysql = mock.Mock(return_value=mock_connection)

        response = dao.fetch_employee_tasks(1)

        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertEqual(len(response.response), 2)

        employee_tasks = response.response
        self.assertEqual(employee_tasks[0].task_id, 1)
        self.assertEqual(employee_tasks[0].assigned_to_id, "assigned_to_id1")
        self.assertEqual(employee_tasks[1].task_id, 2)
        self.assertEqual(employee_tasks[1].assigned_to_id, "assigned_to_id2")

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM employee_task WHERE task_id = %s",
            (1,)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
