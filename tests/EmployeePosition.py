import unittest
from datetime import datetime
from unittest.mock import patch

from model.EmployeePosition import EmployeePosition
from dao.EmployeePositionDao import create_employee_position, delete_all_employee_positions
from model.MySqlResponse import MySqlResponse


class EmployeePositionTest(unittest.TestCase):
    employee_position = EmployeePosition(
        1,
        "2",
        1,
        datetime(2025, 1, 1),
        datetime(2028, 1, 1),
        datetime.now(),
        1
    )

    def test_1_create_employee_position_success(self):
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_employee_position(self.employee_position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.CREATED)
        self.assertEqual(response.response, "Employee position created successfully")

    def test_2_create_employee_position_unauthorized(self):
        responsible_id = "0"
        with patch("dao.Authorization.is_admin", return_value=False):
            response = create_employee_position(self.employee_position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.UNAUTHORIZED)
        self.assertEqual(response.response, "Only admins can create employee positions")

    def test_3_create_employee_position_invalid_dates(self):
        self.employee_position.end_date = datetime(2024, 1, 1)
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_employee_position(self.employee_position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.BAD_REQUEST)
        self.assertEqual(response.response, "Start-date cannot be after the end-date")

    def test_4_create_employee_position_in_past(self):
        self.employee_position.start_date = datetime(2020, 1, 1)
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_employee_position(self.employee_position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.BAD_REQUEST)
        self.assertEqual(response.response, "Start or end-date cannot be in the past")

    def test_5_create_employee_position_already_existing_active_one(self):
        employee_position_new = EmployeePosition(
            1,
            "2",
            1,
            datetime(2024, 6, 1),
            datetime(2025, 12, 31),
            datetime.now(),
            1
        )
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_employee_position(employee_position_new, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.ALREADY_EXISTING)
        self.assertEqual(
            response.response,
            "Already has active position, do you want to set this one to active anyway ?"
        )

    def test_6_create_employee_position_success_not_overlapping_non_active(self):
        employee_position_new = EmployeePosition(
            1,
            "2",
            1,
            datetime(2030, 6, 1),
            datetime(2033, 12, 31),
            datetime.now(),
            0
        )
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_employee_position(employee_position_new, responsible_id)
            self.assertEqual(response.response_code, MySqlResponse.CREATED)
            self.assertEqual(response.response, "Employee position created successfully")

    def test_7_create_employee_position_failure_no_overlapping_but_active(self):
        employee_position_new = EmployeePosition(
            1,
            "2",
            1,
            datetime(2043, 6, 2),
            datetime(2053, 12, 31),
            datetime.now(),
            1
        )
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_employee_position(employee_position_new, responsible_id)
            self.assertEqual(response.response_code, MySqlResponse.ALREADY_EXISTING)

    @classmethod
    def tearDownClass(cls):
        delete_all_employee_positions()


if __name__ == '__main__':
    unittest.main()
