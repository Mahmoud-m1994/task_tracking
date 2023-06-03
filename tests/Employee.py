import unittest
from unittest.mock import patch

from model.Employee import Employee
from dao.EmployeeDao import create_employee, delete_employee
from model.MySqlResponse import MySqlResponse


class EmployeeTest(unittest.TestCase):
    def test_1_create_employee_success(self):
        print(1)
        employee = Employee("123456", "UNIT TEST EMPLOYEE")
        responsible_id = "1"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=True):
            response = create_employee(employee, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.CREATED)
        self.assertEqual(response.response, "Employee created successfully")

    def test_2_create_employee_unauthorized(self):
        print(2)
        employee = Employee("123456", "UNIT TEST EMPLOYEE")
        responsible_id = "0"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=False):
            response = create_employee(employee, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.UNAUTHORIZED)
        self.assertEqual(response.response, "Only admins can create employees")

    def test_3_create_employee_already_existing(self):
        print(3)
        employee = Employee("123456", "UNIT TEST EMPLOYEE")
        responsible_id = "1"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=True):
            response = create_employee(employee, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.ALREADY_EXISTING)
        self.assertEqual(response.response, "Employee with the same employee_id already exists")

    def test_4_delete_employee_not_authorized(self):
        employee_id = "123456"
        responsible_id = "0"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=False):
            response = delete_employee(employee_id, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.UNAUTHORIZED)
        self.assertEqual(response.response, "Only admins can delete employees")

    def test_5_delete_employee_success(self):
        employee_id = "123456"
        responsible_id = "1"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=True):
            response = delete_employee(employee_id, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertEqual(response.response, "Employee deleted successfully")


if __name__ == '__main__':
    unittest.main()
