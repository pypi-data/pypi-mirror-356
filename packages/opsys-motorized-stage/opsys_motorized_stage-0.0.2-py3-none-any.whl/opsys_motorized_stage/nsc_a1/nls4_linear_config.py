"""
Configuration for NLS4-8-11 Linear Stage
Optimized settings and parameters for the Newmark Systems NLS4-8-11 vacuum compatible linear stage
"""

class NLS4_8_11_Config:
    """Configuration class for NLS4-8-11 linear stage"""
    
    # Linear stage specifications
    MOTOR_MODEL = "NLS4-8-11"
    STAGE_TYPE = "Linear Stage"
    TRAVEL_RANGE_MM = 200  # 8 inch travel = ~203.2mm
    TRAVEL_RANGE_INCHES = 8.0
    
    # Motor specifications (NEMA 17 vacuum compatible)
    STEPS_PER_REV = 200  # 1.8 degrees per step
    MICROSTEPPING = 256  # Typical microstepping setting for precision
    TOTAL_STEPS_PER_REV = STEPS_PER_REV * MICROSTEPPING  # 51,200 steps/rev
    
    # Leadscrew specifications (two common options available)
    # Using fine resolution leadscrew by default
    LEADSCREW_PITCH_MM = 1.5875  # mm per revolution (fine resolution option)
    # Alternative: 6.35 mm/rev for faster motion
    
    # Linear resolution calculation
    MICRONS_PER_STEP = (LEADSCREW_PITCH_MM * 1000) / TOTAL_STEPS_PER_REV  # ~0.031 µm/step
    MM_PER_STEP = LEADSCREW_PITCH_MM / TOTAL_STEPS_PER_REV  # ~0.000031 mm/step
    INCHES_PER_STEP = MM_PER_STEP / 25.4  # Convert to inches
    
    # Speed parameters based on hardware specifications
    # Max speed: 10 mm/sec for fine leadscrew (from spec sheet)
    MAX_SPEED_MM_SEC = 10.0  # mm/second (hardware limit)
    MAX_SPEED_STEPS_SEC = int(MAX_SPEED_MM_SEC / MM_PER_STEP)  # ~322,560 steps/sec
    
    # Conservative speed settings for reliable operation
    DEFAULT_SPEED = 50000  # steps/sec (~1.55 mm/sec)
    MIN_SPEED = 1000       # Minimum reliable speed
    MAX_SPEED = min(100000, MAX_SPEED_STEPS_SEC)  # Conservative maximum
    
    # Acceleration parameters
    DEFAULT_ACCELERATION = 50000   # steps/sec²
    MIN_ACCELERATION = 10000       # Minimum acceleration
    MAX_ACCELERATION = 200000      # Maximum acceleration
    
    # Position limits based on travel range
    # Convert travel range to steps
    MAX_TRAVEL_STEPS = int(TRAVEL_RANGE_MM / MM_PER_STEP)  # ~6.4M steps for 200mm
    
    # Safety margins (10% of travel range)
    SAFETY_MARGIN_STEPS = int(MAX_TRAVEL_STEPS * 0.1)
      # Position limits with safety margins
    MIN_POSITION = -SAFETY_MARGIN_STEPS
    MAX_POSITION = MAX_TRAVEL_STEPS + SAFETY_MARGIN_STEPS
    MAX_POSITION_STEPS = MAX_POSITION  # Alias for backward compatibility
    
    # Physical parameters
    REPEATABILITY_UM = 10  # ±10 µm bidirectional repeatability
    ACCURACY_MM_PER_MM = 0.0006  # 0.0006 mm/mm accuracy
    MAX_LOAD_KG = 22.6  # 50 lb max load
    
    # Safety parameters
    ENABLE_SOFT_LIMITS = True
    ENABLE_POSITION_TRACKING = True
    
    # Timing parameters
    MOTION_TIMEOUT = 60      # Timeout for motion completion (seconds)
    COMMAND_TIMEOUT = 5      # Timeout for command response (seconds)
    
    @classmethod
    def steps_to_mm(cls, steps):
        """Convert steps to millimeters"""
        return steps * cls.MM_PER_STEP
    
    @classmethod
    def mm_to_steps(cls, mm):
        """Convert millimeters to steps"""
        return int(mm / cls.MM_PER_STEP)
    
    @classmethod
    def steps_to_inches(cls, steps):
        """Convert steps to inches"""
        return steps * cls.INCHES_PER_STEP
    
    @classmethod
    def inches_to_steps(cls, inches):
        """Convert inches to steps"""
        return int(inches / cls.INCHES_PER_STEP)
    
    @classmethod
    def steps_to_microns(cls, steps):
        """Convert steps to microns"""
        return steps * cls.MICRONS_PER_STEP
    
    @classmethod
    def microns_to_steps(cls, microns):
        """Convert microns to steps"""
        return int(microns / cls.MICRONS_PER_STEP)
    
    @classmethod
    def get_travel_range_steps(cls):
        """Get travel range in steps"""
        return cls.MAX_TRAVEL_STEPS
    
    @classmethod
    def validate_speed(cls, speed):
        """Validate and clamp speed to safe range"""
        return max(cls.MIN_SPEED, min(speed, cls.MAX_SPEED))
    
    @classmethod
    def validate_acceleration(cls, acceleration):
        """Validate and clamp acceleration to safe range"""
        return max(cls.MIN_ACCELERATION, min(acceleration, cls.MAX_ACCELERATION))
    
    @classmethod
    def validate_position(cls, position):
        """Validate position against soft limits"""
        if cls.ENABLE_SOFT_LIMITS:
            return max(cls.MIN_POSITION, min(position, cls.MAX_POSITION))
        return position
    
    @classmethod
    def validate_position_mm(cls, position_mm):
        """Validate position in mm and return clamped value"""
        max_mm = cls.steps_to_mm(cls.MAX_POSITION)
        min_mm = cls.steps_to_mm(cls.MIN_POSITION)
        return max(min_mm, min(position_mm, max_mm))

# Preset movement profiles optimized for linear stage operations
class MovementProfiles:
    """Predefined movement profiles for different linear stage operations"""
      # Ultra-precision profile for critical positioning
    ULTRA_PRECISION = {
        'speed': 5000,      # ~0.16 mm/sec
        'low_speed': 1000,  # Starting speed
        'acceleration_ms': 2000,  # Slow acceleration (2 seconds)
        'deceleration_ms': 2000,  # Slow deceleration  
        'description': 'Ultra-precision for critical measurements'
    }
    
    # High precision profile for fine positioning
    PRECISION = {
        'speed': 15000,     # ~0.47 mm/sec
        'low_speed': 2000,  # Starting speed
        'acceleration_ms': 1000,  # 1 second acceleration
        'deceleration_ms': 1000,  # 1 second deceleration
        'description': 'High precision positioning'
    }
    
    # Normal operation profile for general use
    NORMAL = {
        'speed': 50000,     # ~1.55 mm/sec
        'low_speed': 5000,  # Starting speed
        'acceleration_ms': 500,   # 0.5 second acceleration
        'deceleration_ms': 500,   # 0.5 second deceleration
        'description': 'Normal speed operation'
    }
    
    # Fast movement profile for rapid positioning
    FAST = {
        'speed': 400000,  # ~12.4 mm/sec
        'low_speed': 2000, # Starting speed
        'acceleration_ms': 1000,   # 1 second acceleration
        'deceleration_ms': 1000,   # 1 second deceleration
        'description': 'Fast movement for rapid positioning'
    }
    
    # Homing profile for initial positioning
    HOMING = {
        'speed': 1000000,  # ~31 mm/sec
        'low_speed': 2000,  # Starting speed
        'acceleration_ms': 1000,  # 1 second acceleration
        'deceleration_ms': 1000,  # 1 second deceleration
        'description': 'Safe speed for homing operations'
    }
    
    @classmethod
    def get_profile(cls, profile_name):
        """Get movement profile by name"""
        profiles = {
            'ultra_precision': cls.ULTRA_PRECISION,
            'precision': cls.PRECISION,
            'normal': cls.NORMAL,
            'fast': cls.FAST,
            'homing': cls.HOMING
        }
        return profiles.get(profile_name.lower(), cls.NORMAL)

# Correct NSC-A1 commands based on actual manual
class NLS4_Commands:
    """Correct NSC-A1 command templates based on the actual manual"""
    
    # Movement mode commands
    SET_ABSOLUTE_MODE = "ABS"
    SET_INCREMENTAL_MODE = "INC"
    
    # Basic movement commands
    MOVE_ABSOLUTE = "X{position}"    # Move to absolute position
    
    # Speed and acceleration (from manual)
    SET_HIGH_SPEED = "HSPD={speed}"      # High speed setting
    SET_LOW_SPEED = "LSPD={speed}"       # Low speed setting  
    SET_ACCELERATION = "ACC={acceleration}"  # Acceleration in milliseconds
    SET_DECELERATION = "DEC={acceleration}"  # Deceleration in milliseconds
    GET_HIGH_SPEED = "HSPD"
    GET_LOW_SPEED = "LSPD"
    GET_ACCELERATION = "ACC"
    GET_DECELERATION = "DEC"
    
    # Position and status
    GET_POSITION = "PX"              # Get current position
    SET_POSITION = "PX={position}"   # Set current position value
    GET_PULSE_SPEED = "PS"           # Get current pulse speed
    
    # Motor control
    ENABLE_MOTOR = "EO=1"            # Enable motor power
    DISABLE_MOTOR = "EO=0"           # Disable motor power
    GET_MOTOR_ENABLE = "EO"          # Get motor enable status
    
    # Motion control
    JOG_POSITIVE = "J+"              # Jog in positive direction
    JOG_NEGATIVE = "J-"              # Jog in negative direction
    STOP_MOTION = "STOP"             # Stop with deceleration
    ABORT_MOTION = "ABORT"           # Immediate stop
    
    # Homing commands
    HOME_POSITIVE = "H+"             # Home in positive direction
    HOME_NEGATIVE = "H-"             # Home in negative direction
    HOME_LOW_POSITIVE = "HL+"        # Home positive with low speed
    HOME_LOW_NEGATIVE = "HL-"        # Home negative with low speed
    LIMIT_HOME_POSITIVE = "L+"       # Limit homing positive
    LIMIT_HOME_NEGATIVE = "L-"       # Limit homing negative
    
    # Status and information
    GET_MOTOR_STATUS = "MST"         # Get motor status
    GET_MOVE_MODE = "MM"             # Get move mode (0=abs, 1=inc)
    GET_DEVICE_NAME = "DN"           # Get device name
    GET_FIRMWARE_VERSION = "VER"     # Get firmware version
    GET_PRODUCT_ID = "ID"            # Get product ID
    
    # Digital I/O
    GET_DIGITAL_INPUTS = "DI"        # Get digital input status
    GET_DIGITAL_OUTPUTS = "DO"       # Get digital output status
    SET_DIGITAL_OUTPUTS = "DO={value}"  # Set digital outputs
    
    # Advanced features
    CLEAR_ERRORS = "CLR"             # Clear limit and StepNLoop errors
    STORE_SETTINGS = "STORE"         # Store settings to flash
    
    # Driver settings (require RR to read, RW to write)
    SET_MICROSTEPS = "DRVMS={value}" # Set driver microstepping
    SET_RUN_CURRENT = "DRVRC={value}"  # Set driver run current
    SET_IDLE_CURRENT = "DRVIC={value}" # Set driver idle current
    SET_IDLE_TIME = "DRVIT={value}"    # Set driver idle time
    READ_DRIVER_PARAMS = "RR"          # Read driver parameters
    WRITE_DRIVER_PARAMS = "RW"         # Write driver parameters
    
    # Encoder functions
    GET_ENCODER_POSITION = "EX"      # Get encoder counter value
    SET_ENCODER_POSITION = "EX={value}"  # Set encoder counter value
    
    # Temperature monitoring (if supported)
    GET_TEMPERATURE = "TEMP"         # Get driver temperature
    
    # Communication settings
    SET_BAUDRATE = "BAUD={rate}"     # Set communication baud rate
    GET_BAUDRATE = "BAUD"            # Get current baud rate
    
    # Pulse output settings
    SET_PULSE_WIDTH = "PW={width}"   # Set pulse width
    GET_PULSE_WIDTH = "PW"           # Get pulse width
    
    # Step resolution settings
    SET_STEP_RESOLUTION = "SR={res}" # Set step resolution
    GET_STEP_RESOLUTION = "SR"       # Get step resolution
    
    # Backlash compensation (if supported)
    SET_BACKLASH = "BL={steps}"      # Set backlash compensation
    GET_BACKLASH = "BL"              # Get backlash setting
    
    # Soft limits
    SET_POSITIVE_LIMIT = "PL={pos}"  # Set positive software limit
    SET_NEGATIVE_LIMIT = "NL={pos}"  # Set negative software limit
    GET_POSITIVE_LIMIT = "PL"        # Get positive limit
    GET_NEGATIVE_LIMIT = "NL"        # Get negative limit
    
    # Error handling
    GET_ERROR_STATUS = "ERR"         # Get error status
    GET_LAST_ERROR = "LE"            # Get last error code
    
    # Calibration and testing
    SELF_TEST = "TEST"               # Run self-test
    CALIBRATE = "CAL"                # Run calibration routine
    
    # Advanced motion profiles
    SET_S_CURVE = "SC={enable}"      # Enable/disable S-curve acceleration
    GET_S_CURVE = "SC"               # Get S-curve status
    
    # Position feedback and closed-loop control (if encoder present)
    ENABLE_CLOSED_LOOP = "CL=1"      # Enable closed-loop control
    DISABLE_CLOSED_LOOP = "CL=0"     # Disable closed-loop control
    GET_CLOSED_LOOP = "CL"           # Get closed-loop status
    
    # Motor holding settings
    SET_HOLD_CURRENT = "HC={current}" # Set holding current percentage
    GET_HOLD_CURRENT = "HC"          # Get holding current
    
    # Motion timing
    SET_SETTLE_TIME = "ST={time}"    # Set settle time after motion
    GET_SETTLE_TIME = "ST"           # Get settle time
    
    @classmethod
    def format_command(cls, template, **kwargs):
        """Format command template with parameters"""
        return template.format(**kwargs)
    
    @classmethod
    def get_all_commands(cls):
        """Get dictionary of all available commands"""
        commands = {}
        for attr_name in dir(cls):
            if not attr_name.startswith('_') and not callable(getattr(cls, attr_name)):
                attr_value = getattr(cls, attr_name)
                if isinstance(attr_value, str):
                    commands[attr_name] = attr_value
        return commands
    
    @classmethod
    def validate_command_parameters(cls, command_template, **kwargs):
        """Validate that all required parameters are provided for a command"""
        import re
        # Find all parameter placeholders in the template
        placeholders = re.findall(r'\{(\w+)\}', command_template)
        missing_params = []
        for param in placeholders:
            if param not in kwargs:
                missing_params.append(param)
        
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")
        
        return True

# Command validation and safety functions
class CommandValidator:
    """Validates commands and parameters for safety"""
    
    @staticmethod
    def validate_position(position, config=None):
        """Validate position is within safe limits"""
        if config is None:
            config = NLS4_8_11_Config
        
        if config.ENABLE_SOFT_LIMITS:
            if position < config.MIN_POSITION or position > config.MAX_POSITION:
                raise ValueError(f"Position {position} is outside safe limits "
                               f"({config.MIN_POSITION} to {config.MAX_POSITION})")
        return True
    
    @staticmethod
    def validate_speed(speed, config=None):
        """Validate speed is within safe limits"""
        if config is None:
            config = NLS4_8_11_Config
        
        validated_speed = config.validate_speed(speed)
        if validated_speed != speed:
            print(f"Warning: Speed {speed} clamped to {validated_speed}")
        return validated_speed
    
    @staticmethod
    def validate_acceleration(acceleration, config=None):
        """Validate acceleration is within safe limits"""
        if config is None:
            config = NLS4_8_11_Config
        
        validated_acc = config.validate_acceleration(acceleration)
        if validated_acc != acceleration:
            print(f"Warning: Acceleration {acceleration} clamped to {validated_acc}")
        return validated_acc
    
    @staticmethod
    def estimate_move_time(start_pos, end_pos, speed, acceleration):
        """Estimate time required for a move"""
        distance = abs(end_pos - start_pos)
        if distance == 0:
            return 0
        
        # Simple trapezoidal motion profile estimation
        # Time to accelerate to full speed
        accel_time = speed / acceleration
        accel_distance = 0.5 * acceleration * accel_time**2
        
        if distance <= 2 * accel_distance:
            # Triangular profile (no constant speed phase)
            total_time = 2 * (distance / acceleration)**0.5
        else:
            # Trapezoidal profile
            const_speed_distance = distance - 2 * accel_distance
            const_speed_time = const_speed_distance / speed
            total_time = 2 * accel_time + const_speed_time
        
        return total_time

# Status parsing utilities
class StatusParser:
    """Parse and interpret NSC-A1 status responses"""
    
    @staticmethod
    def parse_motor_status(status_response):
        """Parse MST command response"""
        try:
            status_bits = int(status_response.strip())
            return {
                'moving': bool(status_bits & 0x01),
                'stopped': bool(status_bits & 0x02),
                'motor_enabled': bool(status_bits & 0x04),
                'positive_limit': bool(status_bits & 0x08),
                'negative_limit': bool(status_bits & 0x10),
                'home_switch': bool(status_bits & 0x20),
                'error': bool(status_bits & 0x40),
                'busy': bool(status_bits & 0x80),
            }
        except (ValueError, AttributeError):
            return None
    
    @staticmethod
    def parse_digital_io(di_response):
        """Parse digital input status"""
        try:
            input_bits = int(di_response.strip())
            return {
                'input_1': bool(input_bits & 0x01),
                'input_2': bool(input_bits & 0x02),
                'input_3': bool(input_bits & 0x04),
                'input_4': bool(input_bits & 0x08),
            }
        except (ValueError, AttributeError):
            return None
    
    @staticmethod
    def format_position_report(position_steps, config=None):
        """Format position in multiple units"""
        if config is None:
            config = NLS4_8_11_Config
        
        return {
            'steps': position_steps,
            'mm': config.steps_to_mm(position_steps),
            'inches': config.steps_to_inches(position_steps),
            'microns': config.steps_to_microns(position_steps),
        }
