# modular_test_bench_control
Python script for controlling a test bench consisting of conveyors and a robotic arm. Custom module for basic SureServo2 EtherNet/IP conveyor control included.

# Usage

Video demo with explanation: https://youtu.be/Ev3M4YpQl8c

Short demo of routine created with the test bench:

![short demo](https://user-images.githubusercontent.com/56004971/211133881-f716e649-4394-4f4e-ba23-15e3a2d261c2.gif)

This test bench was designed to automate the testing of new gripper and vacuum designs. Using the test bench, it is possible through the GUI to:
1. Test different gripper designs on different parcels
2. Jog the pick conveyor to save a starting point for the parcel to be picked up from (the system will move the parcel to this exact location each cycle of the routine)
3. Jog the arm to save waypoints and create your own custom routine (with vacuum and blowoff points and delays)
4. Run the routine X number of times to collect statistical data for analysis

![image](https://user-images.githubusercontent.com/56004971/211138910-0a98854a-52cd-4e15-88e2-75f746dd84bf.png)

![image](https://user-images.githubusercontent.com/56004971/211138990-1683f8a4-ce05-4d8a-8ac1-a910f56e0d2d.png)

This process is best seen in the video demo above, the short GIF demonstrates a custom routine running on the test bench after being set up in the GUI.

# Development
Everything below documents some background on the development of this project.

This was my co-op project for my 4-month internship with Kindred Part of Ocado Group. I was part of the INDUCT hardware team, developing solutions for parcel induction automation: https://www.kindred.ai/solutions/induct
The previous co-ops prior to my internship had developed a basic foundation for a modular test bench with two FANUC arms, controlled using the fanucpy python module which they had integrated onto the FANUC mates:
![image](https://user-images.githubusercontent.com/56004971/211134012-be10781e-08bf-4b91-852a-a3079c404dce.png)

This was the starting point for my project.

The idea for my project was to continue the development of the test bench, with the main goal being to integrate a parcel recirculation system using the spare conveyors that were available in the lab. Another idea was to integrate a servo drive with these conveyors to demonstrate a possible use for servos in future workcells (most current conveyors use variable frequency drives which offer limited control on conveyor position).

# Mechanical Design
The main goal for the mechanical design was to create a basic recirculation system that would keep parcels inside, in the case that a loss of seal during an arm swing motion throws a parcel out of the test bench. Additionally, the system would have to mechanically reorient the parcels to a consistent position so that repeated tests are consistent and collected data is valid.

The initial development process involved a lot of brainstorming in CAD:
![image](https://user-images.githubusercontent.com/56004971/211134273-083d4cda-d23b-4931-953d-cf8fc877b5b0.png)

As well as many design iterations and reviews:
![image](https://user-images.githubusercontent.com/56004971/211134431-2338a507-78c6-423e-bc1e-4eadfa73f8a4.png)

To end up with a basic finalized CAD design:
![image](https://user-images.githubusercontent.com/56004971/211134699-a9572772-cda7-48b9-a1c1-42e08a073ea0.png)

Following the design, I built the test bench setup utilizing prototyping parts that were available in the lab:
![image](https://user-images.githubusercontent.com/56004971/211134871-286f2d0f-1987-4d0d-8f0c-7e33413d69f3.png)

There were a few parts that were not readily available, which I was able to fabricate, such as a custom 45 degree surface brackets from sheet metal, or proximity sensor mounts from 3D prints. There are quite a few differences between the final product and the CAD, which were changes implemented during the assembly process where I discovered better or ways of building the system.

Additionally, I had specced a SureServo2 servo drive system to mount to the long "pick-area" conveyor, which allows for the consistantly precise reorientation of packages, as seen in the demo videos. The servo drive torque and power was specced to be able to be directly coupled with the conveyor pulley, and handle the parcel loads that the belt may have to carry. The motor can be seen mounted in the image above.

A basic vacuum system and three-cup gripper model were mounted onto the arm for testing purposes. These systems can both be individually swapped out for any new gripper or vacuum concepts that wish to be tested (up to a limit of 8 individually controlled vacuum cups).

# Electrical Design
Apart from the wiring to power the VFD and servo drive systems and safety E-stop wiring, a ProtosX module was used to connect digital I/O sensors and vacuum generators with the PC using ModbusTCP. Two short distance (~3cm) digital output proximity sensors were mounted at the corner of the parcel funnel to detect when the package is oriented correctly:
![324531311_692997738994520_3194667587813015307_n](https://user-images.githubusercontent.com/56004971/211135465-cdaa74f9-b677-4c36-b6bf-9d3bcf2bc7c0.jpg)
Additionally, a ProtosX digital output module was used to turn on and off the solenoids controlling the vacuum flow and blow-off. The system allows for 8 individual vacuum cups to be turned on and off independantly of each other.

The VFD, servo drive, ProtosX module, FANUC arm, as well as the PC running this python script were all connected to an Ethernet network switch.

# Software Design
To control the servo motor through a python script communicating through EtherNet/IP, I created a custom SureServo2 driver which can be found at: https://github.com/ericzhao625/modular_test_bench_control/blob/main/src/sure_servo_2_control.py
The driver allows for a user to create custom "PATHS" that are saved within the drive. These paths can be either relative position (e.g. number of turns from current position), absolute position (e.g. number of turns from the set ORIGIN), or constant speed control. Examples of using the driver in separate code can be found in the main function in the file itself, or in the automated routine sample: https://github.com/ericzhao625/modular_test_bench_control/blob/main/src/automated_routine.py

Additionally, I created a basic driver for ModbusTCP control of the Yaskawa v1000 VFD which controlled the "place" conveyor. Communication with the FANUC arm was facilited using the previous co-op's work with fanucpy, and communication with the ProtosX module was implemented using pymodbus.

Careful consideration was made to limit the arm's movement while being jogged. There are software limitations on how far the user can move the arm in order to prevent potential collisions between the arm and the conveyors, barriers, and package itself. These can be seen as the limits on the sliders.

More documentation related to the code can be found in the files themselves.
