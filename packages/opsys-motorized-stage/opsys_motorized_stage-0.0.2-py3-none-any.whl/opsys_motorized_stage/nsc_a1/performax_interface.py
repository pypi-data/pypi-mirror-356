"""
Python Motor Control for Arcus Performax Motor Controller
Based on NSC-A1 Manual and Sample Code

This script provides a Python interface to control Arcus Performax motor controllers
using the PerformaxCom.dll library through ctypes.

Requirements:
- PerformaxCom.dll and SiUSBXp.dll in the same directory
- pyserial library (pip install pyserial)
"""

import sys
import os
module_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the module file
sys.path.append(module_dir) # Add the module directory to the system path

import ctypes
from ctypes import wintypes, byref, c_char_p, c_void_p, c_uint32, c_int32, POINTER
import time

class PerformaxMotorController:
    """Class to interface with Arcus Performax motor controllers"""
    
    # Constants from the header file
    PERFORMAX_RETURN_SERIAL_NUMBER = 0x00
    PERFORMAX_RETURN_DESCRIPTION = 0x01
    PERFORMAX_MAX_DEVICE_STRLEN = 255
    PERFORMAX_CMD_RESPONSE_LENGTH = 64
    
    def __init__(self, dll_path=None):
        """Initialize the motor controller interface"""
        self.dll_path_SiUSBXp = os.path.join(module_dir, 'SiUSBXp.dll') if dll_path==None else dll_path
        self.dll_path_PerformaxCom = os.path.join(module_dir, 'PerformaxCom.dll') if dll_path==None else dll_path
        self.device_handle = None
        self.is_connected = False
        
        # Load the DLL
        try:
            self.dll = ctypes.windll.LoadLibrary(self.dll_path_SiUSBXp)
            self.dll = ctypes.windll.LoadLibrary(self.dll_path_PerformaxCom)
            self._setup_function_prototypes()
        except OSError as e:
            print(f"Warning: Could not load DLL {self.dll_path_SiUSBXp}: {e}")
            print("DLL will be loaded when needed")
            self.dll = None
    
    def _setup_function_prototypes(self):
        """Setup ctypes function prototypes for DLL functions"""
        if not self.dll:
            return
        
        # fnPerformaxComGetNumDevices
        self.dll.fnPerformaxComGetNumDevices.argtypes = [POINTER(wintypes.DWORD)]
        self.dll.fnPerformaxComGetNumDevices.restype = wintypes.BOOL
        
        # fnPerformaxComGetProductString
        self.dll.fnPerformaxComGetProductString.argtypes = [
            wintypes.DWORD,  # device number
            ctypes.POINTER(ctypes.c_char),  # device string buffer
            wintypes.DWORD   # options
        ]
        self.dll.fnPerformaxComGetProductString.restype = wintypes.BOOL
        
        # fnPerformaxComOpen
        self.dll.fnPerformaxComOpen.argtypes = [
            wintypes.DWORD,  # device number
            POINTER(wintypes.HANDLE)  # handle pointer
        ]
        self.dll.fnPerformaxComOpen.restype = wintypes.BOOL
        
        # fnPerformaxComClose
        self.dll.fnPerformaxComClose.argtypes = [wintypes.HANDLE]
        self.dll.fnPerformaxComClose.restype = wintypes.BOOL
        
        # fnPerformaxComSetTimeouts
        self.dll.fnPerformaxComSetTimeouts.argtypes = [wintypes.DWORD, wintypes.DWORD]
        self.dll.fnPerformaxComSetTimeouts.restype = wintypes.BOOL
        
        # fnPerformaxComSendRecv
        self.dll.fnPerformaxComSendRecv.argtypes = [
            wintypes.HANDLE,  # device handle
            ctypes.POINTER(ctypes.c_char),  # send buffer
            wintypes.DWORD,   # bytes to write
            wintypes.DWORD,   # bytes to read
            ctypes.POINTER(ctypes.c_char)   # receive buffer
        ]
        self.dll.fnPerformaxComSendRecv.restype = wintypes.BOOL
    
    def _ensure_dll_loaded(self):
        """Ensure DLL is loaded before use"""
        if not self.dll:
            try:
                self.dll = ctypes.windll.LoadLibrary(self.dll_path)
                self._setup_function_prototypes()
                return True
            except OSError as e:
                print(f"Error loading DLL {self.dll_path}: {e}")
                print("Make sure PerformaxCom.dll and SiUSBXp.dll are in the current directory")
                return False
        return True
    
    def get_device_list(self):
        """Get list of connected Performax devices"""
        if not self._ensure_dll_loaded():
            return []
        
        device_count = wintypes.DWORD()
        
        # Get number of devices
        if not self.dll.fnPerformaxComGetNumDevices(byref(device_count)):
            print("Failed to get number of devices")
            return []
        
        if device_count.value == 0:
            print("No Performax devices found")
            return []
        
        devices = []
        for i in range(device_count.value):
            # Create buffer for device string
            device_string = (ctypes.c_char * self.PERFORMAX_MAX_DEVICE_STRLEN)()
            
            # Get device serial number
            if self.dll.fnPerformaxComGetProductString(
                i, 
                ctypes.cast(device_string, ctypes.POINTER(ctypes.c_char)),
                self.PERFORMAX_RETURN_SERIAL_NUMBER
            ):
                # Convert to string
                serial = ctypes.string_at(device_string).decode('ascii', errors='ignore')
                devices.append({
                    'index': i,
                    'serial': serial,
                    'description': f"Device {i}: {serial}"
                })
        
        return devices
    
    def connect_device(self, device_index=0):
        """Connect to a specific device by index"""
        if not self._ensure_dll_loaded():
            return False
        
        if self.is_connected:
            print("Already connected to a device. Disconnect first.")
            return False
        
        device_handle = wintypes.HANDLE()
        
        # Set timeouts
        self.dll.fnPerformaxComSetTimeouts(1000, 1000)
        
        # Open device
        if self.dll.fnPerformaxComOpen(device_index, byref(device_handle)):
            self.device_handle = device_handle
            self.is_connected = True
            print(f"Successfully connected to device {device_index}")
            return True
        else:
            print(f"Failed to connect to device {device_index}")
            return False
    
    def connect(self):
        """Connect to first available device"""
        devices = self.get_device_list()
        if devices:
            return self.connect_device(0)
        return False
    
    def disconnect_device(self):
        """Disconnect from the current device"""
        if not self.is_connected:
            print("No device connected")
            return True
        
        if self.dll and self.dll.fnPerformaxComClose(self.device_handle):
            self.device_handle = None
            self.is_connected = False
            print("Device disconnected successfully")
            return True
        else:
            print("Failed to disconnect device")
            return False
    
    def disconnect(self):
        """Disconnect from the current device (alias)"""
        return self.disconnect_device()
    
    def send_command(self, command):
        """Send a command to the motor controller and get reply"""
        if not self.is_connected:
            print("No device connected")
            return None
        
        if not self._ensure_dll_loaded():
            return None
        
        # Prepare command string
        if len(command) > self.PERFORMAX_CMD_RESPONSE_LENGTH:
            print(f"Command too long. Max length: {self.PERFORMAX_CMD_RESPONSE_LENGTH}")
            return None
        
        # Create send buffer
        send_buffer = (ctypes.c_char * self.PERFORMAX_CMD_RESPONSE_LENGTH)()
        for i, char in enumerate(command.encode('ascii')):
            send_buffer[i] = char
        
        # Create receive buffer
        recv_buffer = (ctypes.c_char * self.PERFORMAX_CMD_RESPONSE_LENGTH)()
        
        # Send command
        if self.dll.fnPerformaxComSendRecv(
            self.device_handle,
            ctypes.cast(send_buffer, ctypes.POINTER(ctypes.c_char)),
            self.PERFORMAX_CMD_RESPONSE_LENGTH,
            self.PERFORMAX_CMD_RESPONSE_LENGTH,
            ctypes.cast(recv_buffer, ctypes.POINTER(ctypes.c_char))
        ):
            # Convert response to string
            response = ctypes.string_at(recv_buffer).decode('ascii', errors='ignore').rstrip('\x00')
            return response
        else:
            print("Failed to send command")
            return None
    
    # Motor control functions using NSC-A1 command syntax
    def set_absolute_mode(self):
        """Set absolute move mode"""
        return self.send_command("ABS")
    
    def set_incremental_mode(self):
        """Set incremental move mode"""
        return self.send_command("INC")
    
    def move_relative(self, steps=1000):
        """Move motor relative to current position using correct NSC-A1 commands"""
        # Set incremental mode first, then move
        self.set_incremental_mode()
        # In incremental mode, use X command with the step value
        command = f"X{steps}"
        return self.send_command(command)
    
    def move_absolute(self, position=0):
        """Move motor to absolute position using correct NSC-A1 commands"""
        # Set absolute mode first, then move
        self.set_absolute_mode()
        # In absolute mode, use X command with the position value
        command = f"X{position}"
        return self.send_command(command)
    
    def set_speed(self, speed=1000):
        """Set motor high speed using correct NSC-A1 command"""
        command = f"HSPD={speed}"
        return self.send_command(command)
    
    def set_low_speed(self, speed=100):
        """Set motor low speed using correct NSC-A1 command"""
        command = f"LSPD={speed}"
        return self.send_command(command)
    
    def set_acceleration(self, acceleration=300):
        """Set motor acceleration in milliseconds (NSC-A1 format)"""
        command = f"ACC={acceleration}"
        return self.send_command(command)
    
    def set_deceleration(self, deceleration=300):
        """Set motor deceleration in milliseconds (NSC-A1 format)"""
        command = f"DEC={deceleration}"
        return self.send_command(command)
    
    def stop_motor(self):
        """Stop motor with deceleration"""
        return self.send_command("STOP")
    
    def abort_motor(self):
        """Stop motor immediately without deceleration"""
        return self.send_command("ABORT")
    
    def home_motor(self, direction='positive'):
        """Home the motor using correct NSC-A1 commands"""
        if direction.lower() in ['positive', 'pos', '+']:
            return self.send_command("L+")
        else:
            return self.send_command("L-")
    
    def jog_motor(self, direction='positive'):
        """Jog the motor using correct NSC-A1 commands"""
        if direction.lower() in ['positive', 'pos', '+']:
            return self.send_command("J+")
        else:
            return self.send_command("J-")
    
    def enable_motor(self):
        """Enable motor power"""
        return self.send_command("EO=1")
    
    def disable_motor(self):
        """Disable motor power"""
        return self.send_command("EO=0")
    
    def get_position(self):
        """Get current motor position using correct NSC-A1 command"""
        # Use the correct NSC-A1 command from the manual
        response = self.send_command("PX")
        if response:
            try:
                # The PX command returns a 28-bit number directly
                position = int(response.strip())
                return position
            except ValueError:
                print(f"Error parsing position response: {response}")
                return None
        return None
    
    def is_moving(self):
        """Check if motor is currently moving using MST command"""
        # Use MST (Motor Status) command to check if motor is moving
        response = self.send_command("MST")
        if response:
            try:
                # MST returns status bits, check for moving status
                status = int(response.strip())
                # Bit 0 typically indicates if motor is moving
                return (status & 1) == 1
            except ValueError:
                print(f"Error parsing motor status: {response}")
                return False
        return False
    
    def wait_for_motion_complete(self, timeout=30):
        """Wait for motor motion to complete"""
        start_time = time.time()
        while self.is_moving():
            if time.time() - start_time > timeout:
                print(f"Timeout waiting for motion to complete")
                return False
            time.sleep(0.1)
        return True
    
    def get_status(self):
        """Get general motor status using MST command"""
        response = self.send_command("MST")
        return response
