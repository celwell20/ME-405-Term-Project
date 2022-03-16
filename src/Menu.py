# -*- coding: utf-8 -*-
"""@file Menu.py
@brief ME 405 RC Drawing Car Term Project Software
@mainpage

\section documentation Documentation
            Link to our term project firmware documentation: https://celwell20.github.io/ME-405-Term-Project/Documentation
            

\section software_design Software Design
            This section describes our software design, and outlines our finite state machine and task diagrams
            used to control the remote control drawing vehicle.

\subsection task_diagram Nucleo/Microcontroller Task Diagram
            Task diagram for our remote control car's microcontroller.
            \image html task_diagram.png "RC Car MCU Task Diagram"

We utilized a closed-loop proportional controller with feedback from the Pittman motor encoders to command the
car to travel to the desired angle. A co-task program was then used to control both motors semi synchronously. A parsing
task and interpreter task are then used to parse the code file and send the encoder values needed to reach the desired position.

\subsection comm_fsm Communication Finite State Machine
            Finite state machine for our MCU communication.
            \image html comm_fsm.PNG "Communication FSM"

The communication FSM is relatively simple with the task waiting for a signal from each motor that the desired position has
been reached, once this is achieved, the next command is sent. 

\subsection hard_fsm Hardware (motor and encoder) Finite State Machine
            Finite state machine for our various hardware components.
            \image html hardware_fsm.PNG "Hardware FSM"

The hardware FSM is more involved with the task having three
main areas, a rotation, translation, and pen stage. Depending on the value given to this task, the motors will initiate a
rotation, translation, or lift/lower the pen. After the command has been executed the state always returns to wait.

Our software consisted of several programs and drivers shown below:

main.py - Main program that instantiates all harware objects such as the motors, encoders, and controllers.

cotask.py - Task scheduling driver provided by Dr.Ridgley.

Closed_Loop.py - Controller driver that provides closed loop control to a system.

motor_elwell_mccue.py - Driver that controls a motor with PWM.

encoder_elwell_mccue.py - Driver that controls an encoder to record position.

chassis_driver.py - Driver that controls chassis measurements and converts position commands to encoder values.

servo_driver.py - Driver that controls a servo motor between two set positions (Level and Raised).

task_share.py - Program that allows for data to be shared across two tasks.

code.txt - Text file that contains all commands for the plotter to do.

@author  Clayton Elwell
@author  Tyler McCue



"""

