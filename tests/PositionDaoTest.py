import unittest
from unittest.mock import patch

from model.Position import Position
from dao.PositionDao import create_position, delete_position
from model.MySqlResponse import MySqlResponse


class PositionDaoTest(unittest.TestCase):
    def test_1_create_position_success(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "1"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=True):
            response = create_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.CREATED)
        self.assertEqual(response.response, "Position created successfully")

    def test_2_create_position_unauthorized(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "0"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=False):
            response = create_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.UNAUTHORIZED)
        self.assertEqual(response.response, "Only admins can create positions")

    def test_3_create_position_already_existing(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "1"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=True):
            response = create_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.ALREADY_EXISTING)
        self.assertEqual(response.response, "Position with the same name or position_id already exists")

    def test_4_delete_position_not_authorized(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "0"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=False):
            response = delete_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.UNAUTHORIZED)
        self.assertEqual(response.response, "Only admins can delete positions")

    def test_5_delete_position_success(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "1"
        with patch("dao.IsEmployeeAdmin.is_admin", return_value=True):
            response = delete_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertEqual(response.response, "Position deleted successfully")


if __name__ == '__main__':
    unittest.main()