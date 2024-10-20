import sensors_main
import unittest
import sys
from unittest.mock import patch

# Define the TemperatureData class
class TemperatureData:
    #Class to store temperature and time information.
    def __init__(self, time: str, temperature: float):
        self.time = time
        self.temperature = temperature


class TemperatureSensor:
    #Temperature sensor class.
    def __init__(self, sensorId: int):
        self.sensorId = sensorId
        self.sensorData = []  # List to store temperature data

    def getTemperature(self) -> float:
        #Return the latest temperature from the sensorData list, or None if there is no data.
        if self.sensorData:
            return self.sensorData[-1].temperature  # Return the last recorded temperature
        return None  # No data

    def recordTemperature(self, time: str, temperature: float) -> None:
        #Record time and temperature.
        new_data = TemperatureData(time, temperature)  # Create a new TemperatureData object
        self.sensorData.append(new_data)  # Add to the data list


# Unit test class for the sensors_main module.
class TestSensors(unittest.TestCase):

    ###################
    # Unit test cases #
    ###################

    # Test case for check_limits with correct inputs (UT1)
    def test_check_limits1(self):
        limits = [18, 22]
        result = sensors_main.check_limits(limits)
        self.assertTrue(result, "Expected True for valid limits")

    # Test case for check_limits with incorrect inputs (UT2)
    def test_check_limits2(self):
        limits = [22, 18]
        result = sensors_main.check_limits(limits)
        self.assertFalse(result, "Expected False for invalid limits")

    # Test case for check_limits with equal limits (UT3)
    def test_check_limits3(self):
        limits = [22, 22]
        result = sensors_main.check_limits(limits)
        self.assertFalse(result, "Expected False when limits are equal")

    ##########################
    # Integration test cases #
    ##########################

    @patch('builtins.print')
    def test_check_limits_integration1(self, mock_print):
        # Set the command line arguments (min and max temperature)
        testargs = ["sensors_main.py", "18", "22"]
        with patch.object(sys, 'argv', testargs):
            sensors_main.main()
            mock_print.assert_not_called()  # Should not print an error message

    @patch('builtins.print')
    def test_check_limits_integration2(self, mock_print):
        # Set invalid command line arguments (min > max)
        testargs = ["sensors_main.py", "22", "18"]
        with patch.object(sys, 'argv', testargs):
            sensors_main.main()
            mock_print.assert_called_with("Error: Incorrect command line arguments.")

    ######################
    # Unit tests for TemperatureSensor #
    ######################

    def setUp(self):
        #Set up the environment for tests.
        self.sensor = TemperatureSensor(sensorId=1)

    def test_initial_sensorData(self):
        #Check that the initial sensorData is empty.
        self.assertEqual(len(self.sensor.sensorData), 0, "Initial sensorData should be empty")

    def test_getTemperature_initial(self):
        #Check getTemperature returns None when there is no data.
        self.assertIsNone(self.sensor.getTemperature(), "Initial temperature should be None")

    def test_recordTemperature(self):
        #Check recording temperature and time.
        self.sensor.recordTemperature("12:30", 25.0)

        # Check that sensorData has one entry
        self.assertEqual(len(self.sensor.sensorData), 1, "sensorData should have one entry")

        # Check the recorded temperature and time
        recorded_data = self.sensor.sensorData[0]
        self.assertEqual(recorded_data.temperature, 25.0, "Recorded temperature does not match")
        self.assertEqual(recorded_data.time, "12:30", "Recorded time does not match")

    def test_getTemperature_after_recording(self):
        #Check getTemperature after recording temperature.
        self.sensor.recordTemperature("14:00", 28.5)
        self.assertEqual(self.sensor.getTemperature(), 28.5, "Latest temperature does not match after recording")

    def test_multiple_records(self):
        #Record multiple times and check the accuracy of the entries.
        self.sensor.recordTemperature("09:00", 20.0)
        self.sensor.recordTemperature("10:00", 22.0)
        self.sensor.recordTemperature("11:00", 24.0)

        # Check the total number of records
        self.assertEqual(len(self.sensor.sensorData), 3, "Number of records does not match")

        # Check the value of each record
        expected_temperatures = [20.0, 22.0, 24.0]
        for i, expected_temp in enumerate(expected_temperatures):
            self.assertEqual(self.sensor.sensorData[i].temperature, expected_temp, "Temperature value does not match at position {}".format(i))

        # Check the latest temperature
        self.assertEqual(self.sensor.getTemperature(), 24.0, "Latest temperature does not match")


if __name__ == '__main__':
    unittest.main()
