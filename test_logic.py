#!/usr/bin/env python3

"""
File containing unit and integration tests for logic that does not require the robot hardware
and can therefore be run on a computer.
"""

from logic import get_angle_for_color, determine_color, configure_model

import pytest


def test_pytest_is_working():
    """
    Trivial test to ensure pytest is installed and configured correctly. This test should be
    detected by the pytest framework and it should pass.
    """
    assert True


def test_get_angle_for_color():
    """
    Test that the correct bin is returned for a given color.
    """
    # success cases (valid input)
    assert get_angle_for_color("red") == 20
    assert get_angle_for_color("purple") == -65
    assert get_angle_for_color("blue") == -40
    assert get_angle_for_color("green") == -100
    assert get_angle_for_color("yellow") == -145
    assert get_angle_for_color("orange") == -185


    # failure cases (invalid input), check that exception of the correct type is raised
    for bad_color in ["Black", "Unknown", None]:
        with pytest.raises(ValueError):
            get_angle_for_color(bad_color)

    
def test_determine_color():
    """
    Test that the correct color is returned for a given input.
    """
    # success cases (valid input)
    assert determine_color([[0.983, 0.133, 0.12]]) == "red"
    assert determine_color([[0.297, 0.569, 0.766]]) == "blue"
    assert determine_color([[0.184, 0.946, 0.265]]) == "green"
    assert determine_color([[0.794, 0.597, 0.117]]) == "yellow"
    assert determine_color([[0.934, 0.299, 0.195]]) == "orange"
    assert determine_color([[0.575, 0.46, 0.676]]) == "purple"
    
    # failure cases (invalid input), check that exception of the correct type is raised
    for bad_input in [0, "Unknown", [[0,0,0]]]:
        with pytest.raises(ValueError):
           determine_color(bad_input)
            
def test_configure_model():
    """
    Test that the model is correctly returned.
    """
    
    assert "red" in configure_model()
    assert "blue" in configure_model()
    assert "purple" in configure_model()
    assert "orange" in configure_model()
    assert "yellow" in configure_model()
    assert "green" in configure_model()
    
    assert configure_model()["red"] == [0.9833396964651359, 0.13341222395888788, 0.12000060007573042]
    assert configure_model()["blue"] == [0.29696525566385273, 0.5685819968198188, 0.7657114169202253]
    assert configure_model()["green"] == [0.1839364012705053, 0.9456485415668089, 0.2651701238929021]
    assert configure_model()["yellow"] ==[0.7937084131236172, 0.5967384723569865, 0.116948151680524]
    assert configure_model()["orange"] == [0.9341408680863833, 0.29881121066181904, 0.194598320892472]
    assert configure_model()["purple"] == [0.5750997899250333, 0.4601728450160798, 0.6758299396530505]
           
if __name__ == "__main__":
    print("To run the tests, first run `pipenv` with the project's virtual environment activated. "
          "This can be done automatically in Visual Studio Code by running the relevant task "
          "accessed from the Command Palette (Ctrl+Shift+P). "
          "Then, run `pytest` on the command line or use the testing option () in Visual Studio Code.")
