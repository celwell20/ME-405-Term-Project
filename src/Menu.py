# -*- coding: utf-8 -*-
"""@file Menu.py
@brief ME 405 RC Drawing Car Term Project Software
@mainpage
      
\section software_design Software Design
            This section describes our software design, and outlines our finite state machine and task diagrams
            used to control the remote control drawing vehicle.

\subsection task_diagram Nucleo/Microcontroller Task Diagram
            Task diagram for our remote control car's microcontroller.
            \image html task_diagram.png "RC Car MCU Task Diagram"

\subsection user_fsm User Interface Finite State Machine
            Finite state machine for our user interface.
            \image html user_fsm.png "User Interface FSM"
            
\subsection comm_fsm Communication Finite State Machine
            Finite state machine for our MCU communication.
            \image html comm_fsm.PNG "Communication FSM"
            
\subsection hard_fsm Hardware (motor and encoder) Finite State Machine
            Finite state machine for our various hardware components.
            \image html hardware_fsm.PNG "Hardware FSM"
                      

@author  Clayton Elwell
@author  Tyler McCue



"""

