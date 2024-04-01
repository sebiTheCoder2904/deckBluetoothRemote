from nicegui import ui
import asyncio
import sys
from itertools import count, takewhile
from typing import Iterator
import time
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
macAddress = "34:85:18:03:21:0A"


async def sendData(data):
    print(data)
    await client.write_gatt_char(char.uuid, b'\x01') # this send data to device
    await asyncio.sleep(5.0)
    await client.write_gatt_char(char.uuid, b'\x00') # this send data to device



async def discover_esp32():
    # Create a scanner
    scanner = BleakScanner()

    try:
        # Start scanning
        await scanner.start()

        # Keep scanning until ESP32 is found
        while True:
            devices = await scanner.get_discovered_devices()
            for device in devices:
                if device.address == macAddress:
                    print("ESP32 found!")
                    await interact_with_esp32(device)
                    return

            # Sleep for a short duration before scanning again
            await asyncio.sleep(1)
    finally:
        # Stop scanning
        await scanner.stop()

async def interact_with_esp32(device):
    async with BleakClient(device.address) as client:
        # Discover services
        services = await client.get_services()
        print("Services:", services)

        # Access the service and characteristic you want to interact with
        # For example:
        # service_uuid = "0000180f-0000-1000-8000-00805f9b34fb"
        # characteristic_uuid = "00002a19-0000-1000-8000-00805f9b34fb"
        # value = await client.read_gatt_char(characteristic_uuid)

        # Perform read/write operations on characteristics as needed

async def main():
    await discover_esp32()

asyncio.run(main())

#testbutton = ui.button("send a byte to esp32c3", color="red", on_click=lambda: sendData("test"))

'''
ui.run(port=2009,
       dark=True,
       title="deckremote",
       show=False)'''