import csv

def check_limits(limits):
    #Check if the provided limits are valid.
    return limits[0] < limits[1]

def read_temperatures_from_csv(file_path):
    #Read temperature data from a CSV file for multiple sensors.
    sensor_data = {}
    try:
        with open(file_path, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sensor_id = int(row['sensor_id'])
                time = row['time']
                temperature = float(row['temperature'])

                if sensor_id not in sensor_data:
                    sensor_data[sensor_id] = []

                sensor_data[sensor_id].append((time, temperature))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")
    
    return sensor_data

def main():
    import sys
    if len(sys.argv) != 2:
        print("Error: Incorrect command line arguments.")
        return
    
    # Example usage of reading temperatures
    csv_file_path = sys.argv[1]  # Get CSV file path from command line
    sensor_data = read_temperatures_from_csv(csv_file_path)
    print("Retrieved sensor data:", sensor_data)

if __name__ == '__main__':
    main()
