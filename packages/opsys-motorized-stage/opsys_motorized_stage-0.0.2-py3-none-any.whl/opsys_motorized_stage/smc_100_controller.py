import time
import serial
from .smc_100.smc_100 import SMC100

# import wrapper
try:
    import serial.tools.list_ports
except Exception as e:
    print(e)


class Smc100Controller:
    """
    SMC100 Single-Axis Stepper Motion Controller
    Interface
    """
    _device_address = 1
    _max_timeout = 65  # in seconds

    def __init__(self, is_log=True):
        """
        initialize parameters

        Args:
            is_log (bool, optional): Log printings flag. Defaults to True.
        """
        self.stage_controller = None
        self._is_log = is_log

    def connect_stage(self):
        """
        Connect to motorized stage serial port -
        Scan COM ports to find ATEN related

        Returns:
            bool/str: connection to Motorized stage status/COM port
        """
        try:
            ports = serial.tools.list_ports.comports()
            for port, description, hwid in sorted(ports):
                print("{}: {} [{}]".format(port, description, hwid))
                if ("ATEN USB to Serial Bridge" in description):
                    try:
                        self.stage_controller = SMC100(
                            self._device_address, port)
                        stage_id = self.stage_controller.sendcmd(
                            'ID', '?', True)

                        if stage_id is not None:
                            print('Serial connection established')
                            self.stage_controller.reset_and_configure()
                            return True
                    except Exception as error:
                        print(error)
        except:
            print(
                "Fail to connect!\nPlease make sure you have ATEN driver installed\nhttps://www.aten.com/global/en/supportcenter/info/downloads/?action=display_product&pid=575"
            )
        return False
    
    def setup_configs(self,
                      low_speed,
                      high_speed,
                      acceleration):
        """
        Initialize parameters before stage connection
        """
        print('Not Implemented')

    def disconnect_stage(self):
        """
        Disconnect from stage motor
        """
        self.stage_controller.close()

    def set_stage_home(self):
        """
        Motorized stage homing
        """
        self.stage_controller.home()

        # wait for homing completion
        self._position_polling('mm', 0)

    def stop_movement(self):
        """
        Stop stage motor movement
        """
        self.stage_controller.stop()

    def _position_polling(self, units, target_position):
        """
        Poll motor current position

        Args:
            units (str): mm/um
            target_position (int): target mototr position
        """
        start_timepoint = time.time()
        position = abs(self.get_position(units))

        while position != target_position:
            current_timepoint = time.time()
            # reached maximum timeout
            if (current_timepoint - start_timepoint) >= self._max_timeout:
                break
            
            raw_position = self.get_position(units)  # direction indicator
            position = abs(raw_position)

            if self._is_log:
                print(f'Current position: {raw_position}')

    def get_position(self, units='mm'):
        """
        Get current stage position

        Args:
            units (str, optional): Position units (um/mm). Defaults to 'mm'.

        Returns:
            float: current stage position
        """
        if units == 'mm':
            return self.stage_controller.get_position_mm()
        elif units == 'um':
            return self.stage_controller.get_position_um()

        print('Error - Wrong units provided!')
        return 'Error'

    def move_abs(self, position, units, is_poll=True):
        """
        Move stage motor absolute

        Args:
            position (float): Position value
            units (str): Position units (um/mm)
            is_poll (bool, optional): Wait for arrival to target position.
                                      Defaults to True.
        """
        if units == 'mm':
            self.stage_controller.move_absolute_mm(position)
        elif units == 'um':
            self.stage_controller.move_absolute_um(position)

        if is_poll:
            self._position_polling(units, position)
            print(f'Moving stage absolute {position}{units} finished')

    def move_rel(self, distance, units, is_poll=True):
        """
        Move stage motor relative

        Args:
            distance (float): Distance value
            units (str): Distance units (um/mm)
            is_poll (bool, optional): Wait for arrival to target position.
                                      Defaults to True.
        """
        current_position = self.get_position(units)
        target_position = current_position + distance

        if units == 'mm':
            self.stage_controller.move_relative_mm(distance)
        elif units == 'um':
            self.stage_controller.move_relative_um(distance)

        if is_poll:
            self._position_polling(units, target_position)
            print(f'Moving stage relative {distance}{units} finished')
