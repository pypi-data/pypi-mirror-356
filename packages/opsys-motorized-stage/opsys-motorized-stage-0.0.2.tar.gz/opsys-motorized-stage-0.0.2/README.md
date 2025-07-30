# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is motorized stage controllers implementation for motorized stage devices

### How do I get set up? ###

* pip install opsys-motorized-stage

### Unit Testing

* python -m unittest -v

### Reference Links

* https://github.com/freespace/pySMC100
* https://www.newport.com/mam/celum/celum_assets/resources/SMC100CC_and_SMC100PP_-_User_Manual.pdf?3
* https://www.newport.com/mam/celum/celum_assets/resources/SMC100_-_Command_Interface_Manual.pdf?3
* https://www.newmarksystems.com/downloads/software/NSC-A/NSC-A1/NSC-A1_Manual_Rev_1.3.0.pd

### Usage Example
```
SMC_100
-------
from opsys_motorized_stage.smc_100_controller import Smc100Controller

motor_stage_conn = Smc100Controller()

motor_stage_conn.connect_stage()
motor_stage_conn.set_stage_home()
motor_stage_conn.move_abs(15, 'mm')
motor_stage_conn.disconnect_stage()

NLS4
----
from opsys_motorized_stage.nls4_controller import NLS4_MotorController

motor_stage_conn = NLS4_MotorController()
motor_stage_conn.connect()
motor_stage_conn.home_stage_safe()
motor_stage_conn.setup_motor_defaults()
motor_stage_conn.wait_for_motion_complete_with_status()
motor_stage_conn.move_mm(15)
motor_stage_conn.wait_for_motion_complete_with_status()
motor_stage_conn.disconnect_stage()
```