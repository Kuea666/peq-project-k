from bluepy.btle import Peripheral, DefaultDelegate

# Replace with your sensor's address
DEVICE_ADDR = "A09B0D4B-99D4-F68B-183E-09C3F1819D0D"

# UUID for the Accelerometer service (replace if needed)
ACC_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
# UUID for the Accelerometer characteristic (replace if needed)
ACC_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"


class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.data = []

    def handle_notification(self, conn, handle, data):
        # Process the received accelerometer data (replace with your logic)
        x = int.from_bytes(data[0:2], byteorder='little', signed=True) / 16384.0
        y = int.from_bytes(data[2:4], byteorder='little', signed=True) / 16384.0
        z = int.from_bytes(data[4:6], byteorder='little', signed=True) / 16384.0
        self.data.append((x, y, z))  # Store data for later use


def main():
    # Connect to the sensor
    print("Connecting...")
    try:
        p = Peripheral(DEVICE_ADDR)
        print("Connected!")
    except Exception as e:
        print(f"Connection error: {e}")
        return

    # Get services and characteristics
    services = p.getServices()
    acc_service = None
    for service in services:
        if service.uuid == ACC_SERVICE_UUID:
            acc_service = service
            break

    if not acc_service:
        print("Accelerometer service not found")
        return

    acc_char = acc_service.getCharacteristics(ACC_CHAR_UUID)[0]

    # Set delegate and enable notifications
    delegate = MyDelegate()
    p.setDelegate(delegate)
    p.writeCharacteristic(acc_char.valHandle + 1, b"\x01", True)  # Enable notifications

    # Collect data for a while (replace with your desired logic)
    try:
        print("Collecting data...")
        while True:
            if len(delegate.data) >= 100:  # Collect 100 data points (adjust as needed)
                # Process collected data (e.g., print, store in a file)
                for x, y, z in delegate.data:
                    print(f"X: {x:.4f}, Y: {y:.4f}, Z: {z:.4f}")
                delegate.data = []  # Clear collected data
                break
    except KeyboardInterrupt:
        print("Exiting...")

    # Disconnect
    p.disconnect()


if __name__ == "__main__":
    main()
