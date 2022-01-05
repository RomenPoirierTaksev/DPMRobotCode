#!/usr/bin/env python3

"""
Sort foam cubes by color.
The user loads the cube in a chminey, and then presses the touch sensor.
This will start the code where continously, cubes will be scanned, their color will be determined,
a motor will activate the piston to push the cube on a conveyor bell. This conveyor bell will rotate

"""

# Adjust these imports based on your implementation
from logic import determine_color, get_angle_for_color
from utils.brick import Color, configure_ports
import brickpi3
from utils.brick import TouchSensor, EV3ColorSensor, EV3UltrasonicSensor, configure_ports, Motor
from time import sleep, time
from threading import Thread

print("Program start.\nPlease wait for sensors to turn on...")

# Initialize BrickPi
brick_pi = brickpi3.BrickPi3()

# Setup motors
MOTOR_CONVEYER_BELT = brick_pi.PORT_B
MOTOR_PISTON = brick_pi.PORT_A
MOTOR_ROTATION = brick_pi.PORT_C

# Setup motor information
brick_pi.offset_motor_encoder(MOTOR_ROTATION, brick_pi.get_motor_encoder(MOTOR_ROTATION))
brick_pi.set_motor_limits(MOTOR_ROTATION, 50, 100)
brick_pi.set_motor_position(MOTOR_ROTATION, 0)

# Setup sensors
COLOR_SENSOR, TOUCH_SENSOR = configure_ports(PORT_1=EV3ColorSensor, PORT_2=TouchSensor)

print("Done waiting.")


def turn_and_drop_cube(angle):
    """
    Orients the conveyor belt towards the angle specified as an argument,
    actions it so that the cube is droped, and moves back to its initial position.
    """
    
    # If the angle is not an int, raise an error
    if not isinstance(angle, int):
        raise ValueError("The input angle is invalid")
    
    # Turn the conveyor belt towards the indicated angle
    brick_pi.set_motor_position(MOTOR_ROTATION, angle)
    sleep(1.5) 
    forward_speed = -60
    # Start the conveyor belt to drop the cube
    brick_pi.set_motor_power(MOTOR_CONVEYER_BELT, forward_speed)
    sleep(1)
    # Stop the conveyor belt to drop the cube
    brick_pi.set_motor_power(MOTOR_CONVEYER_BELT, 0)
    sleep(0.1)
    # Turn the conveyor belt back to the initial position
    brick_pi.set_motor_position_relative(MOTOR_ROTATION, -angle)
    sleep(1.5)
    
def get_cube_color():
    """
    Actions the color sensor and scans RGB values for 1.5 seconds and returns its color as a string.
    """

    measurements_list = []
    start_time = time()
    
    # Add measured RGB values to a list for 1.5 seconds
    while time() < start_time + 1.5:
            cs_data = COLOR_SENSOR.get_value()
            cs_data.pop() #removing the last value of the list, we only want RGB 
            measurements_list.append(cs_data)
            print(cs_data)
            
    # Return the deduced color based on the taken measurements
    return determine_color(measurements_list)

def push_cube_with_piston():
    """
    Actions the piston motor to push the cube onto the conveyor belt.
    """
    # Move piston forward
    forward_speed = -15
    brick_pi.set_motor_power(MOTOR_PISTON, forward_speed)
    sleep(0.8)
    brick_pi.set_motor_power(MOTOR_PISTON, 0)
    # Move piston backwards
    brick_pi.set_motor_power(MOTOR_PISTON, -forward_speed)
    sleep(0.8)
    brick_pi.set_motor_power(MOTOR_PISTON, 0)
    sleep(0.1)
        
if __name__ == "__main__":
    try:
        # Start the system when the touch sensor is pressed
        pressed = False
        while True:
            print(TOUCH_SENSOR.is_pressed())
            if TOUCH_SENSOR.is_pressed():
                pressed = True
                sleep(1)
            # Stop the piston when the touch sensor is pressed again.
            if pressed and TOUCH_SENSOR.is_pressed():
                break
            if pressed:
                # Determine the cube color
                detected_color = get_cube_color()
                print(detected_color)
                sleep(1)
                # Push cube onto the conveyor belt
                push_cube_with_piston()
                
                # Determine angle for that color
                angle = get_angle_for_color(detected_color)
                # Turn conveyor belt and drop cube while next color is getting scanned
                Thread(target=turn_and_drop_cube, args=(angle,)).start()
        

    except BaseException as e:
         print(e)
    finally:
        sleep(3)
        brick_pi.set_motor_power(MOTOR_ROTATION, 0)
        exit()

