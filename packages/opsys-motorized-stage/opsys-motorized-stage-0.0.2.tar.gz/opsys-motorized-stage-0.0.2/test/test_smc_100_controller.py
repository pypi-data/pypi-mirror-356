import unittest
from unittest.mock import patch, MagicMock
from opsys_motorized_stage.smc_100_controller import Smc100Controller


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(Smc100Controller, 'connect_stage')
    def test_connect_stage(self, smc100_mock: MagicMock):
        smc100_conn = Smc100Controller()
        smc100_conn.connect_stage()
        smc100_mock.assert_called_once_with()

    @ patch.object(Smc100Controller, 'disconnect_stage')
    def test_disconnect_stage(self, smc100_mock: MagicMock):
        smc100_conn = Smc100Controller()
        smc100_conn.disconnect_stage()
        smc100_mock.assert_called_once_with()

    @ patch.object(Smc100Controller, 'set_stage_home')
    def test_set_stage_home(self, smc100_mock: MagicMock):
        smc100_conn = Smc100Controller()
        smc100_conn.set_stage_home()
        smc100_mock.assert_called_once_with()

    @ patch.object(Smc100Controller, 'get_position')
    def test_get_position(self, smc100_mock: MagicMock):
        smc100_conn = Smc100Controller()
        smc100_conn.get_position()
        smc100_mock.assert_called_once_with()

    @ patch.object(Smc100Controller, 'move_rel')
    def test_move_rel(self, smc100_mock: MagicMock):
        smc100_conn = Smc100Controller()
        smc100_conn.move_rel(15, 'mm', True)
        smc100_mock.assert_called_once_with(15, 'mm', True)

    @ patch.object(Smc100Controller, 'move_abs')
    def test_move_abs(self, smc100_mock: MagicMock):
        smc100_conn = Smc100Controller()
        smc100_conn.move_abs('10', 'um', True)
        smc100_mock.assert_called_once_with('10', 'um', True)

    @ patch.object(Smc100Controller, 'stop_movement')
    def test_stop_movement(self, smc100_mock: MagicMock):
        smc100_conn = Smc100Controller()
        smc100_conn.stop_movement()
        smc100_mock.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
