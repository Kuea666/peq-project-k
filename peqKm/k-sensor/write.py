import asyncio
from bleak import BleakClient
import csv
import datetime

DEVICE_ADDRESS = "A09B0D4B-99D4-F68B-183E-09C3F1819D0D"

# UUID for the Accelerometer
UUID_ACCELERATION = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UUID_TEMPERATURE = "6E400006-B5A3-F393-E0A9-E50E24DCCA9E"
def clear_csv_file(file_path):
    open(file_path, 'w').close()

def notification_handler(sender: int, data: bytearray):
    # This function will be called when a notification is received

    # Extract the UUID from the sender
    uuid = str(sender).split()[0].lower()

    # Get the current timestamp
    timestamp = datetime.datetime.now()

    # Open the CSV file in append mode
    with open('sensor_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        # Check if the data is from the accelerometer
        if uuid == UUID_ACCELERATION.lower():
            # Parse the accelerometer data
            x = int.from_bytes(data[3:5], byteorder='little', signed=True) / 16384.0  # Convert to g
            y = int.from_bytes(data[5:7], byteorder='little', signed=True) / 16384.0  # Convert to g
            z = int.from_bytes(data[7:9], byteorder='little', signed=True) / 16384.0  # Convert to g

            # Write the data to the CSV file
            writer.writerow([timestamp, 'Accelerometer', x, y, z])

        # Check if the data is from the temperature sensor
        elif uuid == UUID_TEMPERATURE.lower():
            # Parse the temperature data
            temperature = int.from_bytes(data[3:7], byteorder='little', signed=True)/100  # Convert to °C

            # print(f"Temperature data: {temperature}°C")

            # Write the data to the CSV file
            for i in range(5):  # Change this number to write more entries
                writer.writerow([timestamp, 'Temperature', temperature])

async def main():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print(f"Connected: {client.is_connected}")
        clear_csv_file('sensor_data.csv')
        # Write the header to the CSV file
        with open('sensor_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Sensor', 'X', 'Y', 'Z'])
        # Subscribe to the notifications for the Accelerometer
        await client.start_notify(UUID_ACCELERATION, notification_handler)
        # Subscribe to the notifications for the Temperature
        await client.start_notify(UUID_TEMPERATURE, notification_handler)

        await asyncio.sleep(1.0)  # Keep the connection alive for 1 seconds

        # Unsubscribe from the notifications
        await client.stop_notify(UUID_ACCELERATION)

asyncio.run(main())