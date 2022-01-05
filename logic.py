"""
Module for computations that do not require robot hardware and can therefore be tested on a computer.

It is often faster to test these computations on a computer than on the robot.
"""

# The brick and sound modules must NOT be imported here, but other imports are allowed
from math import sqrt, e, pi, dist
from statistics import median, mean
from ast import literal_eval
import sys


def configure_model():
    """
    Configures the model the color detection algorithm relies on.
    Uses sample data to find average RGB values for each color.
    Returns a dictionnary with the color as a string as key, and a list of average RGB values as value.
    """
    model_output = {}
    color_sensor_file = {"../data_analysis/red_data.csv": "red", "../data_analysis/blue_data.csv": "blue", "../data_analysis/green_data.csv": "green", "../data_analysis/yellow_data.csv": "yellow", "../data_analysis/orange_data.csv": "orange", "../data_analysis/purple_data.csv": "purple"}
    # For each color, compute the average normalized RGB values
    for file in color_sensor_file.keys():
        with open(file, "r") as f:
            red = []
            green = []
            blue = []
            for line in f.readlines():
                r, g, b = literal_eval(line)  # convert string to 3 floats
                if r == 0 and g ==0 and b ==0:
                    continue      
                denominator = sqrt(r ** 2 + g ** 2 + b ** 2)
                if denominator == 0:
                    continue
                red.append(r / denominator)
                green.append(g / denominator)
                blue.append(b / denominator)
            # Store the average values on a dictionary 
            model_output[color_sensor_file[file]] = [mean(red), mean(green), mean(blue)]
    return model_output # Return the model dictionnary 
        
def get_angle_for_color(color):
    """
    This method associates the input string color with the angle of the location it will be dropped in. 
    """
    if color == "purple":
        return -65
    elif color == "blue":
        return -40
    elif color == "green":
        return -100
    elif color == "yellow":
        return -145
    elif color == "orange":
        return -185
    elif color == "red":
        return 20
    else:
        raise ValueError("The input color is invalid")
        
def determine_color(list_of_measurements):
    """
    Takes a list of lists (RGB values), computes the average and uses the model data to find the color with closest distance.
    Returns the closest color as it should be the color of the object.
    """
    try:
        # Compute the average normalized RGB value from the list of measurements
        red = []
        green = []
        blue = []
        for i in range(len(list_of_measurements)):
            if list_of_measurements[i] == [0,0,0]:
                pass
            r = list_of_measurements[i][0]
            g = list_of_measurements[i][1]
            b = list_of_measurements[i][2]
            denominator = sqrt(r ** 2 + g ** 2 + b ** 2)
            red.append(r / denominator)
            green.append(g / denominator)
            blue.append(b / denominator)

        unknown_color_point = [mean(red), mean(green), mean(blue)]
        model = configure_model()
        smallest_dist = sys.maxsize # Get the maximum int value 
        closest_color = None
        # Determine closest color by comparing their distances to the unknown color point
        for color in model:
            if dist(model[color], unknown_color_point) < smallest_dist:
                closest_color = color
                smallest_dist = dist(model[color], unknown_color_point)
                
        return closest_color
    except:
        raise ValueError("The input list of measurements is invalid")