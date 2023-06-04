import unittest
from unittest.mock import patch

from model.Position import Position
from dao.PositionDao import create_position, delete_position, get_position_by_id_or_name
from model.MySqlResponse import MySqlResponse


class PositionDaoTest(unittest.TestCase):
    def test_1_create_position_success(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.CREATED)
        self.assertEqual(response.response, "Position created successfully")

    def test_2_create_position_unauthorized(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "0"
        with patch("dao.Authorization.is_admin", return_value=False):
            response = create_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.UNAUTHORIZED)
        self.assertEqual(response.response, "Only admins can create positions")

    def test_3_create_position_already_existing(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = create_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.ALREADY_EXISTING)
        self.assertEqual(response.response, "Position with the same name or position_id already exists")

    def test_4_get_position_by_id_found(self):
        position = Position("0203", "UNIT TEST POSITION")
        response = get_position_by_id_or_name(position.position_id, position.name)
        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertEqual(response.response.name, position.name)

    def test_5_get_position_by_id_not_found(self):
        position = Position("9921", "UNIT TEST NOT FOUND")
        response = get_position_by_id_or_name(position.position_id, position.name)
        self.assertEqual(response.response_code, MySqlResponse.NOT_FOUND)
        self.assertEqual(response.response, "Position not found")

    def test_6_delete_position_not_authorized(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "0"
        with patch("dao.Authorization.is_admin", return_value=False):
            response = delete_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.UNAUTHORIZED)
        self.assertEqual(response.response, "Only admins can delete positions")

    def test_7_delete_position_success(self):
        position = Position("0203", "UNIT TEST POSITION")
        responsible_id = "1"
        with patch("dao.Authorization.is_admin", return_value=True):
            response = delete_position(position, responsible_id)
        self.assertEqual(response.response_code, MySqlResponse.OK)
        self.assertEqual(response.response, "Position deleted successfully")


if __name__ == '__main__':
    unittest.main()
