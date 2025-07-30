"""
Enhanced Motor Controller for NLS4-8-11 Linear Stage
"""
import os
import sys
module_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the module file
sys.path.append(module_dir) # Add the module directory to the system path

from .nsc_a1.performax_interface import PerformaxMotorController
from .nsc_a1.nls4_linear_config import NLS4_8_11_Config, MovementProfiles
import time


class NLS4_MotorController(PerformaxMotorController):
    """Enhanced motor controller specifically for NLS4-8-11 linear stage"""
    
    def __init__(self, dll_path=None):
        """Initialize NLS4-8-11 linear stage controller"""
        super().__init__(dll_path)
        self.config = NLS4_8_11_Config()
        self.current_profile = 'normal'
        self.last_position = 0
        self.position_tracking_enabled = True
        
        print(f"NLS4-8-11 Linear Stage Controller initialized")
        print(f"Stage model: {self.config.MOTOR_MODEL}")
        print(f"Stage type: {self.config.STAGE_TYPE}")
        print(f"Travel range: {self.config.TRAVEL_RANGE_MM}mm ({self.config.TRAVEL_RANGE_INCHES}\")")
        print(f"Resolution: {self.config.MICRONS_PER_STEP:.3f} µm/step")
        
    def setup_motor_defaults(self):
        """Setup linear stage with safe default parameters for NLS4-8-11"""
        if not self.is_connected:
            print("Linear stage not connected. Connect first.")
            return False
        
        print("Setting up NLS4-8-11 linear stage with default parameters...")
        
        try:
            # Critical initialization sequence for NLS4-8-11 linear stage
            print("  Initializing stage communication...")
            
            # First, ensure motor is enabled - this is crucial for position commands
            print("  Enabling motor...")
            self.enable_motor()            
            time.sleep(0.3)  # Extended delay for motor to stabilize
            
            # Set position tracking mode - use NSC-A1 commands
            print("  Setting position mode...")
            # Try absolute mode first
            abs_response = self.send_command("ABS")
            time.sleep(0.2)
            
            # If absolute mode doesn't work, try incremental mode
            if abs_response and ("ERROR" in abs_response.upper() or "?" in abs_response):
                print("Absolute mode failed, trying incremental mode...")
                inc_response = self.send_command("INC")
                time.sleep(0.2)
                
                if inc_response and ("ERROR" in inc_response.upper() or "?" in inc_response):
                    print("Warning: Position mode setting uncertain")
                else:
                    print("Incremental mode set successfully")
            else:
                print("    Absolute mode set successfully")
            
            # Set safe default movement profile (normal speed, smooth acceleration)
            print("Setting movement profile...")
            self.set_movement_profile('fast')
            
            # Verify communication with position query
            print("Verifying communication...")
            initial_pos = self.get_position()
            if initial_pos is not None:
                print(f"Initial position: {initial_pos} steps")
                print(f"Position in mm: {self.config.steps_to_mm(initial_pos):.3f}")
                self.last_position = initial_pos
            else:
                print("Warning: Could not read initial position")
            
            print("NLS4-8-11 linear stage setup completed successfully!")
            return True
            
        except Exception as e:
            print(f"Linear stage setup failed: {e}")
            return False
    
    def set_movement_profile(self, profile_name):
        """Set movement profile optimized for NLS4-8-11 linear stage"""
        # Get profile using the correct method
        profile = MovementProfiles.get_profile(profile_name)
        if not profile:
            print(f"Invalid profile: {profile_name}")
            available_profiles = ['ultra_precision', 'precision', 'normal', 'fast', 'homing']
            print(f"Available profiles: {available_profiles}")
            return False
        
        if not self.is_connected:
            print("Linear stage not connected.")
            return False
        
        self.current_profile = profile_name
        
        print(f"Setting movement profile: {profile_name}")
        try:
            # Apply profile settings using parent class methods (no axis parameters)
            self.set_speed(profile['speed'])
            self.set_low_speed(profile['low_speed'])
            self.set_acceleration(profile['acceleration_ms'])
            self.set_deceleration(profile['deceleration_ms'])
            
            print(f"Profile '{profile_name}' applied successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to set profile '{profile_name}': {e}")
            return False
    
    def move_absolute_safe(self, position_steps):
        """Move to absolute position with safety checks for NLS4-8-11"""
        if not self.is_connected:
            print("Linear stage not connected.")
            return False
          # Validate position is within travel limits
        if not self.config.validate_position(position_steps):
            print(f"Position {position_steps} steps is outside safe travel range!")
            print(f"Safe range: 0 to {self.config.MAX_POSITION_STEPS} steps")
            print(f"({0:.1f} to {self.config.steps_to_mm(self.config.MAX_POSITION_STEPS):.1f} mm)")
            return False
        
        print(f"Moving to position: {position_steps} steps ({self.config.steps_to_mm(position_steps):.3f} mm)")
        
        try:
            # Use direct NSC-A1 command for absolute movement
            success = self.move_absolute(position_steps)
            
            if success and self.position_tracking_enabled:
                self.last_position = position_steps
                
            return success
            
        except Exception as e:
            print(f"Absolute move failed: {e}")
            return False
    
    def move_relative_safe(self, steps):
        """Move relative distance with safety checks"""
        if not self.is_connected:
            print("Linear stage not connected.")
            return False
        
        # Calculate target position
        current_pos = self.get_position()
        if current_pos is None:
            print("Cannot read current position for safety check")
            return False
        
        target_pos = current_pos + steps
        
        # Validate target position
        if not self.config.validate_position(target_pos):
            print(f"Target position {target_pos} steps would be outside safe range!")
            print(f"Current: {current_pos} steps, Move: {steps} steps")
            print(f"Safe range: 0 to {self.config.MAX_POSITION_STEPS} steps")
            return False
        
        distance_mm = self.config.steps_to_mm(abs(steps))
        direction = "forward" if steps > 0 else "backward"
        print(f"Moving {direction}: {abs(steps)} steps ({distance_mm:.3f} mm)")
        
        try:
            success = self.move_relative(steps)
            
            if success and self.position_tracking_enabled:
                self.last_position = target_pos
                
            return success
            
        except Exception as e:
            print(f"Relative move failed: {e}")
            return False
    
    def get_position_mm(self):
        """Get current position in millimeters"""
        position = self.get_position()
        if position is not None:
            return self.config.steps_to_mm(position)
        return None
    
    def get_position_inches(self):
        """Get current position in inches"""
        position = self.get_position()
        if position is not None:
            return self.config.steps_to_inches(position)
        return None
    
    def get_position_microns(self):
        """Get current position in microns"""
        position = self.get_position()
        if position is not None:
            return self.config.steps_to_microns(position)
        return None
        
    def home_stage_safe(self):
        """Safely home the linear stage with enhanced status monitoring"""
        if not self.is_connected:
            print("Linear stage not connected.")
            return False
        
        print("Homing linear stage...")
        print("Note: Homing can take 30-60 seconds depending on stage position")
        
        try:
            # Set homing profile for safe, controlled movement
            print("Setting homing movement profile...")
            self.set_movement_profile('homing')
            
            # Record start time and position
            start_time = time.time()
            start_position = self.get_position()
            print(f"Starting position: {start_position} steps")
            
            # Execute home command
            print("  Executing home command...")
            response = self.home_motor()
            
            if response and ("ERROR" in response.upper() or "?" in response):
                print("Standard home command failed, trying alternative sequence...")
                # Alternative: Move to negative limit slowly then set zero
                self.set_movement_profile('precision')
                # Additional implementation would be hardware-specific
                print("Alternative homing not fully implemented - please manually home")
                return False
                        
            return True
            
        except Exception as e:
            print(f"Homing failed: {e}")
            return False
    
    def _get_axis_letter(self):
        """Convert axis number to letter - NLS4-8-11 linear stage only has X axis"""
        # NLS4-8-11 linear stage only has one axis of motion (X)
        # Always return 'X' regardless of axis number input
        return 'X'
            
    def jog_stage(self, direction='positive', duration=1.0):
        """Jog the linear stage in specified direction"""
        if not self.is_connected:
            print("Linear stage not connected.")
            return None
        
        # Calculate jog distance based on current speed and duration
        current_speed = 5000  # Default jog speed steps/sec
        jog_steps = int(current_speed * duration)
        
        if direction.lower() in ['negative', 'neg', '-', 'left', 'backward']:
            jog_steps = -jog_steps
        
        print(f"Jogging stage {direction} for {duration}s...")
        return self.move_relative_safe(jog_steps)
        
    def emergency_stop(self):
        """Emergency stop for linear stage"""
        if not self.is_connected:
            print("Linear stage not connected.")
            return False
        
        print("EMERGENCY STOP - Stopping linear stage immediately!")
        try:
            # Use NSC-A1 ABORT command for immediate stop
            self.abort_motor()
            print("Linear stage stopped successfully!")
            return True
            
        except Exception as e:
            print(f"Emergency stop failed: {e}")
            return False
    
    def get_motor_status_detailed(self):
        """Get detailed linear stage status information"""
        if not self.is_connected:
            return None
        
        status = {}
        
        # Get basic status using NSC-A1 command
        axis_letter = self._get_axis_letter()
        raw_status = self.send_command("STATUS")
        status['raw_status'] = raw_status
        
        # Get position
        position = self.get_position()
        status['position_steps'] = position
        status['position_mm'] = self.config.steps_to_mm(position) if position is not None else None
        status['position_inches'] = self.config.steps_to_inches(position) if position is not None else None
        status['position_microns'] = self.config.steps_to_microns(position) if position is not None else None
        
        # Get motion status
        status['is_moving'] = self.is_moving()
        status['current_profile'] = self.current_profile
        
        # Get travel limits status
        if position is not None:
            status['within_limits'] = self.config.validate_position(position)
            status['distance_from_home'] = position
            status['distance_from_end'] = self.config.MAX_POSITION_STEPS - position
        else:
            status['within_limits'] = False
            status['distance_from_home'] = None
            status['distance_from_end'] = None
        
        return status
    
    def print_stage_info(self):
        """Print comprehensive information about the linear stage"""
        print(f"\n{'='*50}")
        print(f"NLS4-8-11 Linear Stage Information")
        print(f"{'='*50}")
        print(f"Stage Model: {self.config.MOTOR_MODEL}")
        print(f"Stage Type: {self.config.STAGE_TYPE}")
        print(f"Travel Range: {self.config.TRAVEL_RANGE_MM}mm ({self.config.TRAVEL_RANGE_INCHES}\")")
        print(f"Resolution: {self.config.MICRONS_PER_STEP:.3f} µm/step")
        print(f"Max Position: {self.config.MAX_POSITION_STEPS:,} steps")
        print(f"Current Profile: {self.current_profile}")
        
        if self.is_connected:
            print(f"\nConnection Status: Connected")
            status = self.get_motor_status_detailed()
            if status:
                print(f"Current Position: {status['position_steps']} steps")
                pos_mm = status['position_mm']
                pos_inches = status['position_inches']
                if pos_mm is not None:
                    print(f"Position (mm): {pos_mm:.3f} mm")
                else:
                    print(f"Position (mm): Unknown")
                if pos_inches is not None:
                    print(f"Position (inches): {pos_inches:.6f}\"")
                else:
                    print(f"Position (inches): Unknown")
                print(f"Moving: {'Yes' if status['is_moving'] else 'No'}")
                print(f"Within Limits: {'Yes' if status['within_limits'] else 'No'}")
        else:
            print(f"\nConnection Status: Not Connected")
        
        print(f"{'='*50}\n")
        
    def print_motor_info(self):
        """Alias for print_stage_info for backward compatibility"""
        self.print_stage_info()
    
    def move_mm(self, distance_mm, relative=False):
        """Move by distance in millimeters"""
        steps = self.config.mm_to_steps(distance_mm)
        
        # Handle zero distance moves
        if abs(steps) < 1:
            print(f"Move distance too small: {distance_mm:.3f} mm ({steps} steps)")
            return True
        
        if relative:
            return self.move_relative_safe(steps)
        else:
            # Convert to absolute position
            if relative == False and distance_mm <= 0:
                # Absolute move to position
                return self.move_absolute_safe(steps)
            else:
                # Relative move
                return self.move_relative_safe(steps)
    
    def move_inches(self, distance_inches, relative=False):
        """Move by distance in inches"""
        distance_mm = distance_inches * 25.4  # Convert inches to mm
        return self.move_mm(distance_mm, relative)
    
    def move_microns(self, distance_microns, relative=False):
        """Move by distance in microns"""
        distance_mm = distance_microns / 1000.0  # Convert microns to mm
        return self.move_mm(distance_mm, relative)
    
    def is_motion_complete(self):
        """Check if current motion is complete (inverse of is_moving)"""
        return not self.is_moving()
    
    def wait_for_motion_complete_with_status(self, timeout=60, check_interval=0.2, verbose=False):
        """
        Enhanced wait for motion completion with detailed status reporting
        
        Args:
            timeout (float): Maximum time to wait in seconds
            check_interval (float): Time between status checks in seconds  
            verbose (bool): Print status updates during wait
            
        Returns:
            bool: True if motion completed, False if timeout
        """
        if not self.is_connected:
            print("Linear stage not connected.")
            return False
        
        start_time = time.time()
        last_position = None
        position_stable_count = 0
        
        if verbose:
            print(f"Waiting for motion to complete (timeout: {timeout}s)...")
        
        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Check timeout
            if elapsed > timeout:
                print(f"Timeout after {timeout}s waiting for motion to complete")
                return False
            
            # Check if still moving
            is_moving = self.is_moving()
            current_position = self.get_position()
            
            if verbose:
                print(f"{elapsed:.1f}s: Moving={is_moving}, Position={current_position} steps")
            
            # Motion is complete when:
            # 1. is_moving() returns False, AND
            # 2. Position is stable for a few checks
            if not is_moving:
                if last_position is not None and current_position == last_position:
                    position_stable_count += 1
                    if position_stable_count >= 3:  # Stable for 3 consecutive checks
                        if verbose:
                            print(f"Motion completed after {elapsed:.1f}s")
                        return True
                else:
                    position_stable_count = 0
            else:
                position_stable_count = 0
            
            last_position = current_position
            time.sleep(check_interval)
    
    def get_motion_status(self):
        """
        Get detailed motion status information
        
        Returns:
            dict: Motion status including position, moving state, and timing
        """
        if not self.is_connected:
            return None
        
        status = {
            'is_moving': self.is_moving(),
            'position_steps': self.get_position(),
            'timestamp': time.time()
        }
        
        # Add position in different units
        if status['position_steps'] is not None:
            status['position_mm'] = self.config.steps_to_mm(status['position_steps'])
            status['position_inches'] = self.config.steps_to_inches(status['position_steps'])
            status['position_microns'] = self.config.steps_to_microns(status['position_steps'])
        
        # Add profile information
        status['current_profile'] = self.current_profile
        
        return status
    
    def monitor_motion(self, duration=10, interval=0.5):
        """
        Monitor motion for a specified duration and print status updates
        
        Args:
            duration (float): How long to monitor in seconds
            interval (float): Time between status updates in seconds
        """
        if not self.is_connected:
            print("Linear stage not connected.")
            return
        
        print(f"Monitoring motion for {duration}s (updates every {interval}s):")
        print("Time(s) | Moving | Position(steps) | Position(mm)")
        print("-" * 50)
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            status = self.get_motion_status()
            
            if status:
                moving_str = "YES" if status['is_moving'] else "NO "
                pos_steps = status['position_steps'] or 0
                pos_mm = status['position_mm'] or 0.0
                
                print(f"{elapsed:6.1f}  | {moving_str:6} | {pos_steps:12} | {pos_mm:10.3f}")
            
            time.sleep(interval)
        
        print("-" * 50)
        print("Motion monitoring complete")
    
    def move_absolute_safe_with_monitoring(self, position_steps, timeout=60):
        """Move to absolute position with safety checks and detailed monitoring"""
        if not self.is_connected:
            print("Linear stage not connected.")
            return False
        
        # Validate position is within travel limits
        if not self.config.validate_position(position_steps):
            print(f"Position {position_steps} steps is outside safe travel range!")
            print(f"Safe range: 0 to {self.config.MAX_POSITION_STEPS} steps")
            print(f"({0:.1f} to {self.config.steps_to_mm(self.config.MAX_POSITION_STEPS):.1f} mm)")
            return False
        
        distance_mm = self.config.steps_to_mm(position_steps)
        current_pos = self.get_position()
        
        print(f"Moving to absolute position: {position_steps} steps ({distance_mm:.3f} mm)")
        if current_pos is not None:
            move_distance = abs(position_steps - current_pos)
            move_distance_mm = self.config.steps_to_mm(move_distance)
            print(f"Move distance: {move_distance} steps ({move_distance_mm:.3f} mm)")
        
        try:
            # Execute the move
            success = self.move_absolute(position_steps)
            if not success:
                print("Move command failed")
                return False
            
            # Wait for motion to complete with monitoring
            print("Waiting for motion to complete...")
            motion_complete = self.wait_for_motion_complete_with_status(
                timeout=timeout,
                check_interval=0.5,
                verbose=True
            )
            
            if motion_complete:
                final_pos = self.get_position()
                final_mm = self.config.steps_to_mm(final_pos) if final_pos else 0
                print(f"Move completed! Final position: {final_pos} steps ({final_mm:.3f} mm)")
                
                if self.position_tracking_enabled:
                    self.last_position = final_pos
                return True
            else:
                print("Motion timed out or failed")
                return False
                
        except Exception as e:
            print(f"Absolute move failed: {e}")
            return False
    
    def move_relative_safe_with_monitoring(self, steps, timeout=60):
        """Move relative distance with safety checks and detailed monitoring"""
        if not self.is_connected:
            print("Linear stage not connected.")
            return False
        
        # Calculate target position
        current_pos = self.get_position()
        if current_pos is None:
            print("Cannot read current position for safety check")
            return False
        
        target_pos = current_pos + steps
        
        # Validate target position
        if not self.config.validate_position(target_pos):
            print(f"Target position {target_pos} steps would be outside safe range!")
            print(f"Current: {current_pos} steps, Move: {steps} steps")
            print(f"Safe range: 0 to {self.config.MAX_POSITION_STEPS} steps")
            return False
        
        distance_mm = self.config.steps_to_mm(abs(steps))
        direction = "forward" if steps > 0 else "backward"
        print(f"Moving {direction}: {abs(steps)} steps ({distance_mm:.3f} mm)")
        print(f"From {current_pos} to {target_pos} steps")
        
        try:
            # Execute the move
            success = self.move_relative(steps)
            if not success:
                print("Move command failed")
                return False
            
            # Wait for motion to complete with monitoring
            print("Waiting for motion to complete...")
            motion_complete = self.wait_for_motion_complete_with_status(
                timeout=timeout,
                check_interval=0.5,
                verbose=True
            )
            
            if motion_complete:
                final_pos = self.get_position()
                final_mm = self.config.steps_to_mm(final_pos) if final_pos else 0
                print(f"Move completed! Final position: {final_pos} steps ({final_mm:.3f} mm)")
                
                if self.position_tracking_enabled:
                    self.last_position = final_pos
                return True
            else:
                print("Motion timed out or failed")
                return False
                
        except Exception as e:
            print(f"Relative move failed: {e}")
            return False
