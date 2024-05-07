#this method is just use for loop to connect device and sent data to api one by one
#From last method we use threading to connect device and sent data to api at the same time but it got bug about way to write error data with json syntax that quite imposible to process data
#to improve with out threading we can use asyncio to connect device and sent data to api at the same time and we can write error data with json syntax that can be process data(I think)
#or using threading and rearrange(when writed json and we open it and just rearrange it) the way to write error data with json syntax that can be process data
import asyncio
from bleak import BleakClient
import json
import datetime
import requests

# Define a list of device addresses and their corresponding names
DEVICES = [
    {"address": "A09B0D4B-99D4-F68B-183E-09C3F1819D0D", "tag_no": 1},
    {"address": "B09B0D41-99D4-F68B-183E-09C3F1819D0D", "tag_no": 2},
    # Add more devices as needed
]

def send_to_api(filename):
    url = 'replace with API URL'

    with open(filename, 'r') as file:
        data = json.load(file)  # load the file as a JSON object

    response = requests.post(url, json=data)  # send the JSON object

    if response.status_code == 200:
        print('Data successfully sent to API')
    else:
        print(f'Failed to send data to API. Status code: {response.status_code}')

# UUIDs for the different features
UUID_ACCELERATION = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UUID_ANGULAR_VELOCITY = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UUID_MAGNETIC_VALUE = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
UUID_AIR_PRESSURE = "6E400004-B5A3-F393-E0A9-E50E24DCCA9E"
UUID_HUMIDITY = "6E400005-B5A3-F393-E0A9-E50E24DCCA9E"
UUID_TEMPERATURE = "6E400006-B5A3-F393-E0A9-E50E24DCCA9E"
UUID_QUATERNION = "6E400007-B5A3-F393-E0A9-E50E24DCCA9E"

def notification_handler(sender: int, data: bytearray, tag_no: int):
    # This function will be called when a notification is received
    # Extract the UUID from the sender
    uuid = str(sender).split()[0].lower()

    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23]

    # Open the JSON file in append mode
    with open('sensor_data.json', 'a') as file:

        # Check if the data is from the accelerometer
        if  uuid == UUID_ACCELERATION.lower():
            # Parse the accelerometer data
            x = int.from_bytes(data[3:5], byteorder='little', signed=True) / 16384.0  # Convert to g
            y = int.from_bytes(data[5:7], byteorder='little', signed=True) / 16384.0  # Convert to g
            z = int.from_bytes(data[7:9], byteorder='little', signed=True) / 16384.0  # Convert to g
            # return the data to the JSON file
            return {'timestamp': timestamp, 'sensor': 'Accelerometer', 'xg': x, 'yg': y, 'zg': z, 'tag_no': tag_no}


        # Check if the data is from the gyroscope
        elif uuid == UUID_ANGULAR_VELOCITY.lower():
            # Parse the gyroscope data
            x = int.from_bytes(data[3:5], byteorder='little', signed=True) * (1000 / 16384.0)  # Convert to deg/s
            y = int.from_bytes(data[5:7], byteorder='little', signed=True) * (1000 / 16384.0)  # Convert to deg/s
            z = int.from_bytes(data[7:9], byteorder='little', signed=True) * (1000 / 16384.0)  # Convert to deg/s
            return {'timestamp': timestamp, 'sensor': 'Gyroscope', 'xdeg_per_s': x, 'ydeg_per_s': y, 'zdeg_per_s': z, 'tag_no': tag_no}


        # Check if the data is from the magnetometer
        elif uuid == UUID_MAGNETIC_VALUE.lower():
            # Parse the magnetometer data
            x = int.from_bytes(data[3:5], byteorder='little', signed=True) * (4912 / 32752.0)  # Convert to uT
            y = int.from_bytes(data[5:7], byteorder='little', signed=True) * (4912 / 32752.0)  # Convert to uT
            z = int.from_bytes(data[7:9], byteorder='little', signed=True) * (4912 / 32752.0)  # Convert to uT
            return {'timestamp': timestamp, 'sensor': 'Magnetometer', 'xuT': x, 'yuT': y, 'zuT': z, 'tag_no': tag_no}

        # Check if the data is from the barometer
        elif uuid == UUID_AIR_PRESSURE.lower():
            # Parse the barometer data
            pressure = int.from_bytes(data[3:7], byteorder='little', signed=True)  # Convert to Pa
            return {'timestamp': timestamp, 'sensor': 'Barometer', 'pa': pressure, 'tag_no': tag_no}

        # Check if the data is from the humidity sensor
        elif uuid == UUID_HUMIDITY.lower():
            # Parse the humidity data
            humidity = int.from_bytes(data[3:7], byteorder='little', signed=True) /1000  # Convert to %
            return {'timestamp': timestamp, 'sensor': 'Humidity', 'percen': humidity, 'tag_no': tag_no}

        # Check if the data is from the temperature sensor
        elif uuid == UUID_TEMPERATURE.lower():
            # Parse the temperature data
            temperature = int.from_bytes(data[3:7], byteorder='little', signed=True) / 100  # Convert to °C
            return {'timestamp': timestamp, 'sensor': 'Temperature', 'celsius': temperature, 'tag_no': tag_no}

        # Check if the data is from the Quaternion sensor
        elif uuid == UUID_QUATERNION.lower():
            # Parse the Quaternion data
            q0 = int.from_bytes(data[3:5], byteorder='little', signed=True)  # Convert to Quaternion value
            q1 = int.from_bytes(data[5:7], byteorder='little', signed=True)  # Convert to Quaternion value
            q2 = int.from_bytes(data[7:9], byteorder='little', signed=True)  # Convert to Quaternion value
            q3 = int.from_bytes(data[9:11], byteorder='little', signed=True)  # Convert to Quaternion value
            return {'timestamp': timestamp, 'sensor': 'Quaternion', 'q0': q0, 'q1': q1, 'q2': q2, 'q3': q3, 'tag_no': tag_no}

def calculate_average_velocity():
    import json
    from datetime import datetime

    # Open the JSON file and load the data
    with open('sensor_data.json', 'r') as file:
        data = json.load(file)

    # Filter the data
    filtered_data = [entry for entry in data if entry['sensor'] == 'Accelerometer']

    # Initialize the previous timestamp and the initial velocity
    prev_timestamp = datetime.strptime(filtered_data[0]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    u = 0
    sum_vx, sum_vy, sum_vz = 0, 0, 0
    total_time = 0

    # Loop over the filtered data
    for i in range(1, len(filtered_data)):
        # Parse the current and previous timestamps
        curr_timestamp = datetime.strptime(filtered_data[i]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        prev_timestamp = datetime.strptime(filtered_data[i - 1]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")

        # Calculate the time difference in seconds
        t = (curr_timestamp - prev_timestamp).total_seconds()

        # Calculate the velocity for each axis
        vx = abs(filtered_data[i - 1]['xg'] * t * 1000)
        vy = abs(filtered_data[i - 1]['yg'] * t * 1000)
        vz = abs(((filtered_data[i - 1]['zg']) - 1) * t * 1000)

        # Add the product of the velocity and the time to the sum of velocities for each axis
        sum_vx += vx * t
        sum_vy += vy * t
        sum_vz += vz * t

        # Add the time to the total time
        total_time += t

    # Calculate the average velocity for each axis
    avg_vx = sum_vx / total_time
    avg_vy = sum_vy / total_time
    avg_vz = sum_vz / total_time

    # Prepare the data to be written to the JSON file
    output_data = [{
        'timestamp': filtered_data[-1]['timestamp'],
        'sensor': 'Amplitude_Accelerometer',
        'xmm/s': avg_vx,
        'ymm/s': avg_vy,
        'zmm/s': avg_vz,
        'tag_no': filtered_data[0]['tag_no']
    }]

    # Write the data to the JSON file
    with open('amplitude_data.json', 'w') as file:
        json.dump(output_data, file)

def main(device):
    DEVICE_ADDRESS = device["address"]
    TAG_NO = device["tag_no"]

    async def run():
        try:
            async with BleakClient(DEVICE_ADDRESS) as client:
                print(f"Connected: {client.is_connected}")

                sensor_data = []
                # Subscribe to the notifications for the different features
                await client.start_notify(UUID_ACCELERATION, lambda s, d: sensor_data.append(notification_handler(s, d, TAG_NO)))
                await client.start_notify(UUID_ANGULAR_VELOCITY, lambda s, d: sensor_data.append(notification_handler(s, d, TAG_NO)))
                await client.start_notify(UUID_MAGNETIC_VALUE, lambda s, d: sensor_data.append(notification_handler(s, d, TAG_NO)))
                await client.start_notify(UUID_AIR_PRESSURE, lambda s, d: sensor_data.append(notification_handler(s, d, TAG_NO)))
                await client.start_notify(UUID_HUMIDITY, lambda s, d: sensor_data.append(notification_handler(s, d, TAG_NO)))
                await client.start_notify(UUID_TEMPERATURE, lambda s, d: sensor_data.append(notification_handler(s, d, TAG_NO)))
                await client.start_notify(UUID_QUATERNION, lambda s, d: sensor_data.append(notification_handler(s, d, TAG_NO)))

                await asyncio.sleep(1.0)  # Keep the connection alive for 1 seconds

                # Unsubscribe from the notifications
                await client.stop_notify(UUID_ACCELERATION)
                await client.stop_notify(UUID_ANGULAR_VELOCITY)
                await client.stop_notify(UUID_MAGNETIC_VALUE)
                await client.stop_notify(UUID_AIR_PRESSURE)
                await client.stop_notify(UUID_HUMIDITY)
                await client.stop_notify(UUID_TEMPERATURE)
                await client.stop_notify(UUID_QUATERNION)
                with open('sensor_data.json', 'w') as file:
                    json.dump(sensor_data, file)
                calculate_average_velocity()
                send_to_api('amplitude_data.json')
        except Exception as e:
            # Get the current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23]
            # Open the JSON file in append mode
            with open('sensor_data.json', 'w') as file:
                # Write the error message to the JSON file
                json.dump([{'timestamp': timestamp, 'sensor': 'Error', 'tag_no': TAG_NO, 'error': str(e)}], file)

    asyncio.run(run())

for device in DEVICES:
    main(device)
    send_to_api('sensor_data.json')
