import unittest
from unittest.mock import MagicMock, patch
from opsys_motorized_stage.nls4_controller import NLS4_MotorController


class TestNLS4MotorController(unittest.TestCase):

    def setUp(self):
        self.controller = NLS4_MotorController()
        self.controller.is_connected = True  # Pretend it's connected
        self.controller.config.validate_position = MagicMock(return_value=True)
        self.controller.config.steps_to_mm = MagicMock(side_effect=lambda steps: steps * 0.001)

    @patch.object(NLS4_MotorController, 'enable_motor')
    @patch.object(NLS4_MotorController, 'send_command')
    @patch.object(NLS4_MotorController, 'get_position', return_value=1000)
    @patch.object(NLS4_MotorController, 'set_movement_profile')
    def test_setup_motor_defaults_success(self, mock_profile, mock_get_pos, mock_send_cmd, mock_enable):
        mock_send_cmd.side_effect = ["OK"]  # Simulate ABS command success
        result = self.controller.setup_motor_defaults()
        self.assertTrue(result)
        mock_enable.assert_called_once()
        mock_profile.assert_called_once_with('fast')
        self.assertEqual(self.controller.last_position, 1000)

    @patch('opsys_motorized_stage.nls4_controller.MovementProfiles.get_profile')
    @patch.object(NLS4_MotorController, 'set_speed')
    @patch.object(NLS4_MotorController, 'set_low_speed')
    @patch.object(NLS4_MotorController, 'set_acceleration')
    @patch.object(NLS4_MotorController, 'set_deceleration')
    def test_set_movement_profile_valid(self, mock_dec, mock_acc, mock_low, mock_speed, mock_get_profile):
        mock_get_profile.return_value = {
            'speed': 1000,
            'low_speed': 100,
            'acceleration_ms': 50,
            'deceleration_ms': 50
        }
        result = self.controller.set_movement_profile('normal')
        self.assertTrue(result)
        mock_get_profile.assert_called_once_with('normal')
        mock_speed.assert_called_with(1000)

    @patch.object(NLS4_MotorController, 'move_absolute', return_value=True)
    def test_move_absolute_safe_valid(self, mock_move_abs):
        self.controller.config.validate_position.return_value = True
        result = self.controller.move_absolute_safe(5000)
        self.assertTrue(result)
        mock_move_abs.assert_called_once_with(5000)
        self.assertEqual(self.controller.last_position, 5000)

    @patch.object(NLS4_MotorController, 'get_position', return_value=1000)
    @patch.object(NLS4_MotorController, 'move_relative', return_value=True)
    def test_move_relative_safe_valid(self, mock_move_rel, mock_get_pos):
        result = self.controller.move_relative_safe(500)
        self.assertTrue(result)
        mock_move_rel.assert_called_once_with(500)
        self.assertEqual(self.controller.last_position, 1500)

    def test_move_absolute_safe_invalid_position(self):
        self.controller.config.validate_position.return_value = False
        result = self.controller.move_absolute_safe(9999999)
        self.assertFalse(result)

    def test_move_relative_safe_invalid_position(self):
        self.controller.get_position = MagicMock(return_value=100)
        self.controller.config.validate_position.return_value = False
        result = self.controller.move_relative_safe(999999)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
