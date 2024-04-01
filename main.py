from nicegui import ui
import asyncio
import sys
from itertools import count, takewhile
from typing import Iterator
import time
import bleak
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




async def run():
    async with BleakClient(macAddress) as client:
        while 1:
            try:
                # Read the value of a characteristic
                value = await client.read_gatt_char("b1ec5ab1-f818-4398-b3d3-b9fe79391b34")
                bluetoothLog.push(f"Received: {value.decode()}")
                #print("Received:", value.decode())
            except bleak.exc.BleakDBusError:
                bluetoothLog.push("device disconndected")
                #print("device disconnected")

# Run the asyncio event loop
#loop = asyncio.get_event_loop()
#loop.run_until_complete(run())

start_run_button = ui.button("start run()", on_click=run)
testbutton = ui.button("send a byte to esp32c3", color="red", on_click=lambda: sendData("test"))
bluetoothLog = ui.log(max_lines=10).classes('w-full h-20')


ui.run(port=2009,
       dark=True,
       title="deckremote",
       show=False)