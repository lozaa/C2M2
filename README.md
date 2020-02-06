# C2M2
This is Aidan Loza's repository for work and documentation done while researching at the Center for Computational Mathematics and Modeling at Temple.

The Aidan_Steering file is an (in-progress) implementation of a PD controller for Dr. Seibold's new four-wheel independently steered robot model. The long-term goal of this project is to create a system of robots which dynamically follow one another along a line and model real-life vehicles on the road, and use them to create a model which can be used to imitate traffic flow scenarios.

The goal of the software side of this project is for the code to be modular and provide a clear set of variables which can be adjusted so the controller works for different sizes and models of robot. The user should be able to command a speed to model, and the code should be able to command that for whichever model of robot it is running on without changing more than a single variable.

## Scaling
The robot models we use in the lab are meant to imitate a mid-size car at a 1:20 scale. This means that they are designed to travel at 1/20 the speed of a real car as well. The code we use to control the vehicles takes this into account and employs a conversion factor so that the programmer (and eventually user) can command an equivalent speed to model and the code will convert that speed to the appropriate motor speed. The essential variables in this scaling equation are the radius of the wheels on the robot and the gear ratio between the driving axle and motors that command speed.

## Mechanical Design
todo

## Specifications: 
Brickman v0.8.1

Kernel 4.4.87-22-ev3dev-ev3

Board: LEGO MINDSTORMS EV3 Programmable Brick

Revision: 0006

Image: ev3dev-jessie-ev3-generic-2017-09-14

The image file is important -- though it might be tempting to update the robot's operating system, SOME CODE RUNS DIFFERENTLY BETWEEN VERSIONS. The version history of ev3dev can be found at https://github.com/ev3dev/ev3dev/releases.

### TODO
- Add information on mechanical design, transmission difficulty etc
