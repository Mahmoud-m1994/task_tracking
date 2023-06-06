import unittest

from utilities.UuIdGenrator import generate_text_uuid


class UuidGenerator(unittest.TestCase):

    def test_generate_uuid_for_employee(self):
        employee_id = generate_text_uuid("employee-id")
        self.assertTrue(str(employee_id).__contains__("employee"))
        self.assertEqual(employee_id,employee_id)

    def test_generate_two_different_uuid_for_employee(self):
        employee_id = generate_text_uuid("employee-id")
        employee_id2 = generate_text_uuid("employee-id")
        self.assertNotEqual(employee_id, employee_id2)


if __name__ == '__main__':
    unittest.main()
