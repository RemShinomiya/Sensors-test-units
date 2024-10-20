import sensors_main
import unittest
import sys
import csv
import os
from unittest.mock import patch

class TemperatureData:
    """Class to store temperature and time information."""
    def __init__(self, time: str, temperature: float):
        self.time = time
        self.temperature = temperature


class TemperatureSensor:
    """Temperature sensor class."""
    def __init__(self, sensorId: int):
        self.sensorId = sensorId
        self.sensorData = []  # List to store temperature data

    def getTemperature(self) -> float:
        """Return the most recent temperature from sensorData or None if no data."""
        if self.sensorData:
            return self.sensorData[-1].temperature  # Return last recorded temperature
        return None  # No data

    def recordTemperature(self, time: str, temperature: float) -> None:
        """Record time and temperature."""
        new_data = TemperatureData(time, temperature)  # Create new TemperatureData object
        self.sensorData.append(new_data)  # Add to data list


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
        testargs = ["sensors_main.py", "sensor_data.csv"]
        with patch.object(sys, 'argv', testargs):
            sensors_main.main()
            mock_print.assert_not_called()  # Should not print an error message

    @patch('builtins.print')
    def test_check_limits_integration2(self, mock_print):
        testargs = ["sensors_main.py"]
        with patch.object(sys, 'argv', testargs):
            sensors_main.main()
            mock_print.assert_called_with("Error: Incorrect command line arguments.")

    ######################
    # Unit tests for TemperatureSensor #
    ######################

    def setUp(self):
        """Set up the environment for tests."""
        self.sensor = TemperatureSensor(sensorId=1)

    def test_initial_sensorData(self):
        """Test that initial sensorData is empty."""
        self.assertEqual(len(self.sensor.sensorData), 0, "Initial sensorData should be empty")

    def test_getTemperature_initial(self):
        """Test getTemperature returns None when no data is present."""
        self.assertIsNone(self.sensor.getTemperature(), "Initial temperature should be None")

    def test_recordTemperature(self):
        """Test recording temperature and time."""
        self.sensor.recordTemperature("12:30", 25.0)

        # Check that sensorData has one record
        self.assertEqual(len(self.sensor.sensorData), 1, "sensorData should have one record")

        # Check the temperature and time values
        recorded_data = self.sensor.sensorData[0]
        self.assertEqual(recorded_data.temperature, 25.0, "Temperature value does not match")
        self.assertEqual(recorded_data.time, "12:30", "Time value does not match")

    def test_getTemperature_after_recording(self):
        """Test getTemperature after recording temperature."""
        self.sensor.recordTemperature("14:00", 28.5)
        self.assertEqual(self.sensor.getTemperature(), 28.5, "Most recent temperature does not match after recording")

    def test_multiple_records(self):
        """Record multiple times and check the accuracy of records."""
        self.sensor.recordTemperature("09:00", 20.0)
        self.sensor.recordTemperature("10:00", 22.0)
        self.sensor.recordTemperature("11:00", 24.0)

        # Check the total number of records
        self.assertEqual(len(self.sensor.sensorData), 3, "Number of records does not match")

        # Check each record value
        expected_temperatures = [20.0, 22.0, 24.0]
        for i, expected_temp in enumerate(expected_temperatures):
            self.assertEqual(self.sensor.sensorData[i].temperature, expected_temp, "Temperature value does not match at index {}".format(i))

        # Check the most recent temperature
        self.assertEqual(self.sensor.getTemperature(), 24.0, "Most recent temperature does not match")

    ######################
    # Test for reading from CSV #
    ######################

    def test_read_temperatures_from_csv(self):
        """Test reading temperature data from a CSV file for multiple sensors."""
        # Create a temporary CSV file
        csv_file_path = "test_sensor_data.csv"
        with open(csv_file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["sensor_id", "time", "temperature"])  # Write header
            writer.writerow([1, "12:00", 21.0])
            writer.writerow([1, "12:30", 22.5])
            writer.writerow([2, "12:00", 20.0])
            writer.writerow([2, "12:30", 23.5])

        # Read temperatures from the CSV file
        sensor_data = sensors_main.read_temperatures_from_csv(csv_file_path)

        # Check if data is read correctly
        expected_data = {
            1: [("12:00", 21.0), ("12:30", 22.5)],
            2: [("12:00", 20.0), ("12:30", 23.5)]
        }
        self.assertEqual(len(sensor_data), len(expected_data), "Number of records read from CSV does not match")
        
        for sensor_id in expected_data:
            self.assertIn(sensor_id, sensor_data, "Sensor ID {} not found in data".format(sensor_id))
            self.assertEqual(sensor_data[sensor_id], expected_data[sensor_id], "Data read from CSV does not match expected values for sensor {}".format(sensor_id))

        # Clean up the temporary CSV file
        os.remove(csv_file_path)


if __name__ == '__main__':
    unittest.main()
