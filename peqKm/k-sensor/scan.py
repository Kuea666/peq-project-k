import asyncio
from bleak import BleakScanner

async def scan_for_devices():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    for device in devices:
        print(f"Device found: {device.name}, MAC Address: {device.address}")

    if not devices:
        print("No BLE devices found.")

asyncio.run(scan_for_devices())