import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from dao.EmployeePositionDao import create_employee_position, delete_all_employee_positions
from dao.TaskDao import get_max_task_id
from model.EmployeePosition import EmployeePosition
from dao import TaskDao
from model.MySqlResponse import MySqlResponse
from model.Task import Task

dao = TaskDao


class EmployeeTaskDaoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        employee_position = EmployeePosition(
            1,
            "2",
            1,
            datetime(2025, 1, 1),
            datetime(2028, 1, 1),
            datetime.now(),
            1
        )
        create_employee_position(employee_position=employee_position, responsible_id="1")

    def test_1_create_task_success(self):
        updated_or_assigned_by = "2"
        task = Task(
            task_id=1,
            name="Task 1",
            description="Description 1",
            date_active=datetime.now(),
            created_at=datetime.now(),
            status="Active"
        )
        with patch("dao.Authorization.employee_has_active_position", return_value=True):
            response = dao.create_task(task, updated_or_assigned_by)
        self.assertEqual(response.response_code, MySqlResponse.CREATED)
        self.assertEqual(response.response, "Task created successfully")

    def test_2_create_task_unauthorized(self):
        updated_or_assigned_by = "0"
        task = Task(
            task_id=1,
            name="Task 1",
            description="Description 1",
            date_active=datetime.now(),
            created_at=datetime.now(),
            status="Active"
        )
        with patch("dao.Authorization.employee_has_active_position", return_value=False):
            response = dao.create_task(task, updated_or_assigned_by)
        self.assertEqual(response.response_code, MySqlResponse.UNAUTHORIZED)
        self.assertEqual(response.response, "Only users with an active position can create tasks")

    def test_3_fetch_tasks_success(self):
        response = dao.fetch_tasks()
        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertTrue(isinstance(response.response, list))

    def test_4_get_task_by_id_success(self):
        task_id = get_max_task_id()
        response = dao.get_task_by_id(task_id)
        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertTrue(isinstance(response.response, Task))

    def test_5_get_task_by_id_not_found(self):
        task_id = 100
        response = dao.get_task_by_id(task_id)
        self.assertEqual(response.response_code, MySqlResponse.NOT_FOUND)
        self.assertEqual(response.response, "Task not found")

    def test_6_update_task_success(self):
        updated_or_assigned_by = "2"
        task = Task(
            task_id=get_max_task_id() or -1,
            name="Updated Task",
            description="Updated Description",
            date_active=datetime.now() + timedelta(days=365 * 4),
            created_at=datetime.now(),
            status="Updated Status"
        )
        with patch("dao.Authorization.employee_has_active_position", return_value=True):
            response = dao.update_task(task, updated_or_assigned_by)
        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertEqual(response.response, "Task updated successfully")

    def test_7_update_task_not_found(self):
        updated_or_assigned_by = "2"
        task = Task(
            task_id=100,
            name="Updated Task",
            description="Updated Description",
            date_active=datetime.now(),
            created_at=datetime.now(),
            status="Updated Status"
        )
        with patch("dao.Authorization.employee_has_active_position", return_value=True):
            response = dao.update_task(task, updated_or_assigned_by)
        self.assertEqual(response.response_code, MySqlResponse.NOT_FOUND)
        self.assertEqual(response.response, "Task not found")

    def test_8_assign_task_success(self):
        task_id = get_max_task_id() or -1
        with patch("dao.Authorization.employee_has_active_position", return_value=True):
            response = dao.assign_task(
                task_id=task_id,
                assigned_to_id="2",
                assigned_by_id="2",
                assigned_date=datetime.now()
            )
        self.assertEqual(response.response_code, MySqlResponse.CREATED)
        self.assertEqual(response.response, "Task assigned successfully")

    def test_9_assign_task_not_found(self):
        task_id = 10234
        updated_or_assigned_by = "2"
        assigned_by_id = "2"
        assigned_date = datetime.now()
        with patch("dao.Authorization.employee_has_active_position", return_value=True):
            response = dao.assign_task(task_id, updated_or_assigned_by, assigned_by_id, assigned_date)
        self.assertEqual(response.response_code, MySqlResponse.NOT_FOUND)
        self.assertEqual(response.response, "Task not found")

    def test_10_unassigned_task_not_found(self):
        task_id = 100
        unassigned_from = "2"
        unassigned_by = "2"
        with patch("dao.Authorization.employee_has_active_position", return_value=True):
            response = dao.unassigned_task(task_id, unassigned_from, unassigned_by)
        self.assertEqual(response.response_code, MySqlResponse.NOT_FOUND)
        self.assertEqual(response.response, "Task not found")

    def test_11_delete_task_not_found(self):
        task_id = 100
        updated_or_assigned_by = "2"
        with patch("dao.Authorization.employee_has_active_position", return_value=True):
            response = dao.delete_task(task_id, updated_or_assigned_by)
        self.assertEqual(response.response_code, MySqlResponse.NOT_FOUND)
        self.assertEqual(response.response, "Task not found")

    @classmethod
    def tearDownClass(cls):
        dao.delete_all_employee_tasks()
        delete_all_employee_positions()


if __name__ == '__main__':
    unittest.main()
