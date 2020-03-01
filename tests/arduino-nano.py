# Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""

from skidl import show
from skidl import generate_netlist
from skidl import Net
from skidl import Part


def Device(library, name):
    """Make part lookup and return the part with footprint set"""
    footprint = show(library, name).F2
    return Part(library, name, value=name, footprint=footprint)


def D(name):
    """Creates diode"""
    return Device('Diode', name)


def C(value):
    """Creates default capacitor footprint"""
    return Part('Device', 'C', value=value, footprint='Capacitor_SMD:C_1206_3216Metric')

U1 = Part('MCU_Microchip_ATmega', 'ATmega328P-AU', footprint='Package_QFP:TQFP-32_7x7mm_P0.8mm')

# Power networks
U1['VCC'] += Net.fetch('+5V')
U1['AVCC'] += Net.fetch('+5V')
U1['GND'] += Net.fetch('GND')

# Crystal
ATMEGA_XTAL = Part('Device','Resonator', footprint='Resonator_SMD_muRata_CSTxExxV-3Pin_3.0x1.1mm')
U1['XTAL1'] += ATMEGA_XTAL[1]
U1['XTAL2'] += ATMEGA_XTAL[3]
ATMEGA_XTAL[2] += Net.fetch('GND')

ATMEGA_XTAL_R = Part('Device', 'R', value='1M', footprint='Resistor_SMD:R_1206_3216Metric')
U1['XTAL1'] += ATMEGA_XTAL_R[1]
U1['XTAL2'] += ATMEGA_XTAL_R[2]

# Serial communications
U1['PD1'] += Net.fetch('tx')
U1['PD0'] += Net.fetch('rx')

# I2C
U1['PC4'] += Net.fetch('SDA')
U1['PC5'] += Net.fetch('SCL')

ICSP_CONN = Part('Connector_Generic', 'Conn_02x03_Odd_Even', footprint='Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical')
ICSP_CONN[1] += U1['PB4']
ICSP_CONN[2] += Net.fetch('+5V')
ICSP_CONN[3] += U1['PB5']
ICSP_CONN[4] += U1['PB3']
ICSP_CONN[5] += U1['RESET']
ICSP_CONN[6] += Net.fetch('GND')

FUSE = Part('Device', 'Fuse', footprint='Fuse_1812_4532Metric')

REGULATOR = Part('Regulator_Linear', 'LD1117S50TR_SOT223', value='LD1117S50TR_SOT223', footprint='Package_TO_SOT_SMD:SOT-223-3_TabPin2')
REGULATOR['VO'] += Net.fetch('+5V')
REGULATOR['GND'] += Net.fetch('GND')

AUTOSELECTOR = Part('Device', 'D', footprint='Diode_SMD:D_SMA')
Net.fetch('+5V') & AUTOSELECTOR & Net.fetch('+VBus')

USBMICRO = Part('Connector', 'USB_B_Mini', footprint='USB_Mini-B_Lumberg_2486_01_Horizontal')
USBMICRO['VBUS'] += Net.fetch('+VBus')
USBMICRO['GND'] += Net.fetch('GND')
USBMICRO['D-'] += Net.fetch('USBD-')
USBMICRO['D+'] += Net.fetch('USBD+')

REGULATOR['VI'] & D("MBR0520LT") & FUSE & Net.fetch('+VBus')

FTDI230 = Part('Interface_USB', 'FT231XS', footprint="Package_SO:SSOP-20_3.9x8.7mm_P0.635mm")
FTDI230['VCC'] += Net.fetch('+5V')
FTDI230['GND'] += Net.fetch('GND')
FTDI230['TXD'] += Net.fetch('rx')
FTDI230['RXD'] += Net.fetch('tx')
FTDI230['3V3OUT'] += Net.fetch('+3V3')
FTDI230['USBDM'] += Net.fetch('USBD-')
FTDI230['USBDP'] += Net.fetch('USBD+')
FTDI230['DTR'] += Net.fetch('DTR')
FTDI230['RTS'] += Net.fetch('RTS')
Net.fetch('GND') & C('100nF') & FTDI230['3V3OUT']

BOARD = Part('MCU_Module', 'Arduino_Nano_v3.x', footprint='Module:Arduino_Nano')
BOARD['RESET'] += U1['RESET']
BOARD['+5V'] += Net.fetch('+5V')
BOARD['3V3'] += Net.fetch('+3V3')
BOARD['GND'] += Net.fetch('GND')
BOARD['Vin'] += Net.fetch('Vin')

BOARD['A4'] += Net.fetch('SDA')
BOARD['A5'] += Net.fetch('SCL')

BOARD['RX'] += Net.fetch('rx')
BOARD['TX'] += Net.fetch('tx')

BOARD['D2'] += U1['PD2']
BOARD['D3'] += U1['PD3']
BOARD['D4'] += U1['PD4']
BOARD['D5'] += U1['PD5']
BOARD['D6'] += U1['PD6']
BOARD['D7'] += U1['PD7']

BOARD['A0'] += U1['PC0']
BOARD['A1'] += U1['PC1']
BOARD['A2'] += U1['PC2']
BOARD['A3'] += U1['PC3']
BOARD['A4'] += U1['PC4']
BOARD['A5'] += U1['PC5']

BOARD['D8'] += U1['PB0']
BOARD['D9'] += U1['PB1']
BOARD['D10'] += U1['PB2']
BOARD['D11'] += U1['PB3']
BOARD['D12'] += U1['PB4']
BOARD['D13'] += U1['PB5']

BOARD['AREF'] += U1['AREF']

generate_netlist()
