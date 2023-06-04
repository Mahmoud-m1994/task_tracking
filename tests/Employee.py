import unittest
from unittest.mock import patch

from model.Employee import Employee
from dao.EmployeeDao import create_employee, delete_employee, get_employee_by_id
from model.MySqlResponse import MySqlResponse


class EmployeeTest(unittest.TestCase):
    def test_1_create_employee_success(self):
        employee = Employee("123456", "UNIT TEST EMPLOYEE")
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_employee(employee, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.CREATED)
        self.assertEqual(response.response, "Employee created successfully")

    def test_2_create_employee_unauthorized(self):
        employee = Employee("123456", "UNIT TEST EMPLOYEE")
        responsible_id = "0"
        with patch("dao.Authorization.is_admin", return_value=False):
            response = create_employee(employee, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.UNAUTHORIZED)
        self.assertEqual(response.response, "Only admins can create employees")

    def test_3_create_employee_already_existing(self):
        employee = Employee("123456", "UNIT TEST EMPLOYEE")
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_employee(employee, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.ALREADY_EXISTING)
        self.assertEqual(response.response, "Employee with the same employee_id already exists")

    def test_5_get_employee_by_id_found(self):
        employee_id = "123456"
        employee_name = "UNIT TEST EMPLOYEE"
        response = get_employee_by_id(employee_id)
        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertEqual(response.response.name, employee_name)

    def test_6_get_employee_by_id_not_found(self):
        employee_id = "654321"
        response = get_employee_by_id(employee_id)
        self.assertEqual(response.response_code, MySqlResponse.NOT_FOUND)
        self.assertEqual(response.response, "Employee not found")

    def test_7_delete_employee_success(self):
        employee_id = "123456"
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = delete_employee(employee_id, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertEqual(response.response, "Employee deleted successfully")


if __name__ == '__main__':
    unittest.main()
