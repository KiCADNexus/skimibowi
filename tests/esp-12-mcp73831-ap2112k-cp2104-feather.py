# Generated by Swimibowi - SKiDL Microcontroller Board Wizard
#
# MIT license
#
# Skimibowi - SKiDL Microcontroller Board Wizard
# Copyright (C) 2019  Jussi Vestman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Creates Kicad netlist file for a microcontroller board"""

from skidl import subcircuit
from skidl import show
import itertools
from skidl import generate_netlist
from skidl import Net
from skidl import Part


def subcircuit_label(name):
    """Creates subcircuit label footprint"""
    Part('./library/Skimibowi.lib', 'Label', ref=" ", value=name, footprint=f"Skimibowi:label{len(name)}")


def R(value):
    """Creates default resistor footprint"""
    return Part('Device', 'R', value=value, footprint='Resistor_SMD:R_1206_3216Metric')


def C(value):
    """Creates default capacitor footprint"""
    return Part('Device', 'C', value=value, footprint='Capacitor_SMD:C_1206_3216Metric')


def Device(library, name, value=""):
    """Make part lookup and return the part with footprint set"""
    footprint = show(library, name).F2
    if not value:
        value=name
    return Part(library, name, value=value, footprint=footprint)


def D(name,value=""):
    """Creates diode"""
    return Device('Diode', name, value=value)


def connect_parts(a, b):
    """Connect pins with same name of two parts"""
    flatten = itertools.chain.from_iterable

    a_pins = list(flatten([pin.name.split("/") for pin in a.get_pins()]))
    b_pins = list(flatten([pin.name.split("/") for pin in b.get_pins()]))
    common_pins = [value for value in a_pins if value in b_pins]

    for pin_name in common_pins:
        a[pin_name] += Net.fetch(pin_name)
        b[pin_name] += Net.fetch(pin_name)


@subcircuit
def generate_esp():
    """Generate ESP-module code to circuit"""
    subcircuit_label('esp')
    global U1
    U1 = Part('RF_Module', 'ESP-12E', footprint='RF_Module:ESP-12E')

    U1['VCC'] += Net.fetch('+3V3')
    U1['GND'] += Net.fetch('GND')
    U1['EN'] & R('10k') & Net.fetch('+3V3')
    U1['GPIO15'] & R('4k7') & Net.fetch('GND')


    @subcircuit
    def generate_power_led():
        """Generate led connected to ESP GPI0 that is on after boot"""
        subcircuit_label('power_led')
        led = Part('Device', 'LED', footprint='LED_SMD:LED_1206_3216Metric')
        U1['GPIO0'] & (R('1k') & led & Net.fetch('+3V3'))


    generate_power_led()

    # Generate button for pulling ESP RST pin to low (e.g. reset)

    sw_reset = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
    sw_reset[1] += Net.fetch('RST')
    sw_reset[2] += Net.fetch('GND')

    # Generate ESP serial networks

    U1['TX'] += Net.fetch('tx')
    U1['RX'] += Net.fetch('rx')


generate_esp()


BATTERY = Part('Connector', 'Conn_01x02_Female', footprint='JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal')
BATTERY[1] += Net.fetch('+VBatt')
BATTERY[2] += Net.fetch('GND')


@subcircuit
def generate_mcp73831():
    """Generate MCP73831 battery management IC"""
    subcircuit_label('mcp73831')
    BATTERYMANAGER = Part('Battery_Management', 'MCP73831-2-OT', footprint='Package_TO_SOT_SMD:SOT-23-5')

    BM_LED = Part('Device', 'LED', footprint='LED_SMD:LED_1206_3216Metric')
    BATTERYMANAGER['STAT'] & R('1k') & BM_LED & Net.fetch('+VBus')

    BATTERYMANAGER['VSS'] += Net.fetch('GND')
    Net.fetch('GND') & R('2k') & BATTERYMANAGER['PROG']
    Net.fetch('+VLipo') & C('10uF') & Net.fetch('GND')


generate_mcp73831()


REGULATOR = Part('Regulator_Linear', 'AP2112K-3.3', value='AP2112K-3.3', footprint='Package_TO_SOT_SMD:SOT-23-5')
REGULATOR['VO'] += Net.fetch('+3V3')
REGULATOR['GND'] += Net.fetch('GND')
REGULATOR['EN'] & R('10k') & REGULATOR['VIN']
Net.fetch('GND') & C('10uF') & REGULATOR['VI']
Net.fetch('GND') & C('10uF') & REGULATOR['VO']

USBMICRO = Part('Connector', 'USB_B_Micro', footprint='USB_Micro-B_Amphenol_10103594-0001LF_Horizontal')
USBMICRO['VBUS'] += Net.fetch('+VBus')
USBMICRO['GND'] += Net.fetch('GND')
USBMICRO['D-'] += Net.fetch('USBD-')
USBMICRO['D+'] += Net.fetch('USBD+')

REGULATOR['VI'] & D("MBR0520LT") & BATTERY


@subcircuit
def generate_cp2104():
    """Generate CP2104 usb uart circuitry"""
    subcircuit_label('cp2104')
    cp2104 = Part('Interface_USB', 'CP2104', footprint="Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm")
    cp2104['VIO'] += Net.fetch('+3V3')
    cp2104['VDD'] += Net.fetch('+3V3')
    cp2104['REGIN'] += Net.fetch('+3V3')

    Net.fetch('GND') & C('10uF') & (cp2104['VIO'] | cp2104['VDD'] | cp2104['REGIN'])

    cp2104['GND'] += Net.fetch('GND')
    cp2104['VBUS'] += Net.fetch('+VBus')
    cp2104['D+'] += Net.fetch('USBD+')
    cp2104['D-'] += Net.fetch('USBD-')
    cp2104['TXD'] & R('470') & Net.fetch('rx')
    cp2104['RXD'] & R('470') & Net.fetch('tx')
    cp2104['DTR'] += Net.fetch('DTR')
    cp2104['RTS'] += Net.fetch('RTS')

    # Support ROM programming
    cp2104['VPP'] & C('4.7uF') & Net.fetch('GND')

    # Optional, improves stability
    cp2104['RST'] & R('4k7') & Net.fetch('+3V3')


generate_cp2104()



@subcircuit
def generate_esp_uart_reset():
    """Generate reset circuitry for ESP"""
    subcircuit_label('esp_uart_reset')
    Q1 = Part('Device', 'Q_NPN_BEC', value='mmbt2222', footprint='Package_TO_SOT_SMD:SOT-23')
    Q2 = Part('Device', 'Q_NPN_BEC', value='mmbt2222', footprint='Package_TO_SOT_SMD:SOT-23')
    Net.fetch('DTR') & R('10k') & Q1['B']
    Net.fetch('RTS') & R('10k') & Q2['B']
    Net.fetch('DTR') & Q2['E']
    Net.fetch('RTS') & Q1['E']
    Q1['C'] & Net.fetch('RST')
    Q2['C'] & Net.fetch('GPIO0')


generate_esp_uart_reset()


BOARD = Part('./library/feather.lib', 'Adafruit_Feather', footprint='Skimibowi:Adafruit_Feather')

connect_parts(BOARD, U1)

BOARD['RST'] += Net.fetch('RST')
BOARD['3V3'] += Net.fetch('+3V3')
BOARD['A0'] += Net.fetch('ADC')
BOARD['RX'] += Net.fetch('rx')
BOARD['TX'] += Net.fetch('tx')
BOARD['BAT'] += Net.fetch('+VBatt')
#BOARD['EN'] += NC # noqa: F821
BOARD['USB'] += Net.fetch('+VBus')
U1['ADC'] += Net.fetch('ADC')

BOARD['SCL'] += Net.fetch('SCL')
BOARD['SDA'] += Net.fetch('SDA')
U1['GPIO5'] += Net.fetch('SCL')
U1['GPIO4'] += Net.fetch('SDA')



generate_netlist()
