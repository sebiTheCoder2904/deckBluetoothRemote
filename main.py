from nicegui import ui, events
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
import json


UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
macAddress = "34:85:18:03:21:0A"

selected_Pin = None
firstCard = True
Card = ""

''' 
modes:  digital input/output,
        analog input/output,
        uart tx/rx,
        i2c sda/sdl,
        SPI mosi/miso/sck

'''

esp32_configuration = {
    "name": "Esp32c3",
    "mac": "34:85:18:03:21:0A",
    "UART_SERVICE_UUID": "6E400001-B5A3-F393-E0A9-E50E24DCCA9E",
    "UART_RX_CHAR_UUID": "6E400002-B5A3-F393-E0A9-E50E24DCCA9E",
    "UART_TX_CHAR_UUID": "6E400003-B5A3-F393-E0A9-E50E24DCCA9E",
    "pins": {
        "D0":  {"pinmode": "output", "mode": "pwm", "map2": "Left Trigger"},
        "D1":  {"pinmode": "output", "mode": "", "map2": ""},
        "D2":  {"pinmode": "output", "mode": "", "map2": ""},
        "D3":  {"pinmode": "output", "mode": "", "map2": ""},
        "D4":  {"pinmode": "output", "mode": "", "map2": ""},
        "D5":  {"pinmode": "output", "mode": "", "map2": ""},
        "D6":  {"pinmode": "output", "mode": "", "map2": ""},
        "D7":  {"pinmode": "output", "mode": "", "map2": ""},
        "D8":  {"pinmode": "output", "mode": "", "map2": ""},
        "D9":  {"pinmode": "output", "mode": "", "map2": ""},
        "D10": {"pinmode": "output", "mode": "", "map2": ""},
        "V3": {},
        "GND": {},
        "V5":  {},
    }
}

pins = {
    # pin: (x1, y1, x2, y2),
    "D0": (0, 72, 44, 103),
    "D1": (0, 121, 45, 152),
    "D2": (1, 171, 45, 201),
    "D3": (0, 220, 45, 250),
    "D4": (0, 269, 45, 298),
    "D5": (0, 317, 45, 348),
    "D6": (0, 368, 45, 399),
    "V5": (295, 73, 340, 102),
    "GND": (295, 122, 340, 152),
    "V3": (295, 171, 340, 200),
    "D10": (295, 219, 340, 250),
    "D9": (295, 268, 340, 299),
    "D8": (295, 317, 340, 347),
    "D7": (295, 366, 340, 396)
}

def point_in_rectangle(point, rectangle):
    x, y = point
    x1, y1, x2, y2 = rectangle
    return x1 <= x <= x2 and y1 <= y <= y2

@ui.refreshable
def confCard() -> None:
    Card = ui.card().style("width: 340px; height: 435px")
    with Card:
        pinlable = ui.label(f"Selected Pin: {selected_Pin}").classes("mx-auto")
        ui.separator()
        if selected_Pin is not None:
            pin_info = esp32_configuration["pins"][selected_Pin]
            for pin_key, pin_value in pin_info.items():
                ui.label(f"{pin_key}: {pin_value}")

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

def mouse_handler(e: events.MouseEventArguments):
    global selected_Pin
    coordinates = (int(e.image_x), int(e.image_y))
    #print(coordinates)

    for pin in pins:
        if point_in_rectangle(coordinates, pins[pin]):
            selected_Pin = pin
            print(selected_Pin)
            confCard.refresh()



start_run_button = ui.button("start run()", on_click=run)
testbutton = ui.button("send a byte to esp32c3", color="red", on_click=lambda: sendData("test"))
bluetoothLog = ui.log(max_lines=10).classes('w-full h-20')
ui.separator()
with ui.card().style("width: 695px;"):
    with ui.row().classes("w-full"):
        ui.button("load json")
        ui.space()
        ui.button("save json")
ui.separator()
with ui.row():
    ii = ui.interactive_image("/home/deck/Documents/Projects/deckBluetoothRemote/resources/cut_esp32.png",
                        on_mouse=mouse_handler, 
                        events=['mousedown'])
    confCard()
    



ui.run(port=2009,
       dark=True,
       title="deckremote",
       show=False)