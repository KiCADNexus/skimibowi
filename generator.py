#    Skimibowi - SKiDL Microcontroller Board Wizard
#    Copyright (C) 2019  Jussi Vestman
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Generates microcontroller board descriptions in SKiDL"""

def generate(args):
    """Generates microcontroller board descriptions in SKiDL """

    code = '''#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Bus, Part, Net, generate_netlist
'''.format(**args)

    if args['mcu'] in ['ESP-12E', 'ESP-07']:
        code += generate_esp(args)
        if (args.get('usb_uart', 'No USB') != 'No USB') or args.get('FTDI header', False):
            code += generate_esp_serial(args)

    if args['mcu'] in ['ATmega328P-PU', "ATmega328P-AU", "ATmega328P-MU"]:
        code += generate_atmega328p(args)
        if args['icsp']:
            code += generate_icsp(args)

    if args['mcu'] in ['ATtiny85-20PU', 'ATtiny85-20SU', 'ATtiny85-20MU' ]:
        code += generate_attiny85(args)

    if args['powersource'] not in ['No battery', 'JST PH S2B', 'Barrel Jack 2.0/5.5mm']:
        code += generate_battery(args)

    if args['powersource'] in ['JST PH S2B', 'Barrel Jack 2.0/5.5mm']:
        code += generate_power_connector(args)

    if args.get('fuse', 'No fuse') != 'No fuse':
        code += generate_fuse(args)

    if args.get('switch', False):
        code += generate_power_switch(args)

    if args.get('battery_management', False) == 'MCP73871-2AA':
        code += generate_battery_management(args)

    if args.get('battery_management', False) == 'MCP73831':
        code += generate_mcp73831(args)

    if args.get('regulator_data', None):
        code += generate_regulator(args)

    if args.get('autoselect', False):
        code += generate_autoselect(args)

    if args.get('reset', False):
        code += generate_reset_line(args)

    if args.get('Reset button', False):
        code += generate_reset_button(args)

    if args.get('Flash button', False):
        code += generate_flash_button(args)

    if args.get("led", False):
        code += generate_power_led(args)

    if args.get('DS18B20', False) or args.get('DS18B20U', False) or args.get('onewire_connector', False) != 'No Onewire connector':
        code += generate_onewire_bus(args)

    if args.get('DS18B20', False):
        code += generate_18b20(args)

    if args.get('DS18B20U', False):
        code += generate_18b20u(args)

    if args.get('onewire_connector', False) != "No Onewire connector":
        code += generate_onewire_connector(args)

    if args.get('ina219', False):
        code += generate_ina219(args)

    if args.get('FTDI header', False):
        code += generate_ftdi_header(args)

    if args.get('usb_connector', False) != 'No USB connector':
        code += generate_usb_connector(args)

    if args.get('powersource', False) != 'No battery' or args.get('usb_connector', False) != 'No USB connector':
        code += connect_power_network(args)

    if args.get('usb_uart', False) == 'FT231':
        code += generate_ftdi230(args)
        if args['mcu'] in ['ESP-12E', 'ESP-07']:
            code += generate_esp_uart_reset(args)

    if args.get('usb_uart', False) == 'FT232RL':
        code += generate_ftdi232RL(args)
        if args['mcu'] in ['ESP-12E', 'ESP-07']:
            code += generate_esp_uart_reset(args)


    if args.get('usb_uart', False) == 'CP2102N-A01-GQFN24':
        code += generate_cp2102(args)
        if args['mcu'] in ['ESP-12E', 'ESP-07']:
            code += generate_esp_uart_reset(args)

    if args.get('hc12', False):
        code += generate_hc12(args)
        if args['mcu'] in ['ESP-12E', 'ESP-07']:
            code += generate_esp_software_serial(args)

    if args.get('board_footprint', False) == 'Arduino Uno R3':
        code += generate_arduino_uno_r3_board_footprint(args)
        if args['mcu'] in ['ATmega328P', 'ATmega328P-AU', 'ATmega328P-MU']:
            code += generate_atmega_arduino_board_connections(args)

    if args.get('board_footprint', False) == 'Arduino Nano':
        code += generate_arduino_nano_v3_board_footprint(args)
        if args['mcu'] in ['ATmega328P', 'ATmega328P-AU', 'ATmega328P-MU']:
            code += generate_atmega_arduino_board_connections(args)

    if args.get('board_footprint', False) == 'Adafruit Feather':
        code += generate_adafruit_feather(args)

    code += '''
generate_netlist()
'''

    return code

def generate_esp(args):
    """Generate ESP-module code to circuit"""
    return '''
U1 = Part('RF_Module', '{mcu}', footprint='{mcu_footprint}')

U1['VCC'] += Net.fetch('{mcurail}')
U1['GND'] += Net.fetch('GND')
U1R1 = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
U1R2 = Part('Device', 'R', value='4k7', footprint='{resistor_footprint}')
Net.fetch('{mcurail}') & U1R1 & U1['EN']
Net.fetch('GND') & U1R2 & U1['GPIO15']
'''.format(**args)

def generate_esp_serial(args):
    """Generate ESP serial networks"""

    return '''
U1['TX'] += Net.fetch('tx')
U1['RX'] += Net.fetch('rx')
'''.format(**args)

def generate_atmega328p(args):
    """Generate ATmega328P subsystem to circuit"""
    return '''
U1 = Part('MCU_Microchip_ATmega', '{mcu}', footprint='{mcu_footprint}')

#Power networks
U1['VCC'] += Net.fetch('+5V')
U1['AVCC'] += Net.fetch('+5V')
U1['GND'] += Net.fetch('GND')

# Crystal
ATMEGA_XTAL = Part('Device','Resonator', footprint='Resonator_SMD_muRata_CSTxExxV-3Pin_3.0x1.1mm')
U1['XTAL1'] += ATMEGA_XTAL[1]
U1['XTAL2'] += ATMEGA_XTAL[3]
ATMEGA_XTAL[2] += Net.fetch('GND') 

ATMEGA_XTAL_R = Part('Device', 'R', value='1M', footprint='{resistor_footprint}')
U1['XTAL1'] += ATMEGA_XTAL_R[1]
U1['XTAL2'] += ATMEGA_XTAL_R[2]

# Serial communications
U1['PD1'] += Net.fetch('tx')
U1['PD0'] += Net.fetch('rx')

#I2C
U1['PC4'] += Net.fetch('SDA')
U1['PC5'] += Net.fetch('SCL')
'''.format(**args)

def generate_attiny85(args):
    """Genereate ATtiny85"""
    return '''
U1 = Part('MCU_Microchip_ATtiny', '{mcu}', footprint='{mcu_footprint}')

#Power networks
U1['VCC'] += Net.fetch('{mcurail}')
U1['GND'] += Net.fetch('GND')
'''.format(**args)

def generate_icsp(args):
    """Generate In Circuit Serial Programmer header"""
    return '''
ICSP_CONN = Part('Connector_Generic', 'Conn_02x03_Odd_Even', footprint='Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical')
ICSP_CONN[1] += U1['PB4']
ICSP_CONN[2] += Net.fetch('+5V')
ICSP_CONN[3] += U1['PB5']
ICSP_CONN[4] += U1['PB3']
ICSP_CONN[5] += U1['RESET']
ICSP_CONN[6] += Net.fetch('GND')
'''.format(**args)

def generate_reset_line(args):
    """Generate reset line from ESP GPIO16 to RST pin"""
    return '''
U1['RST'] += Net.fetch('RST')
U1['GPIO16'] += Net.fetch('RST')
'''.format(**args)

def generate_reset_button(args):
    """Generate button for pulling ESP RST pin to low (e.g. reset)"""
    return '''
SW1 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW1[1] += Net.fetch('RST')
SW1[2] += Net.fetch('GND')
'''.format(**args)

def generate_flash_button(args):
    """Generate button for pulling pulling ESP GPIO0 low (e.g. flash mode when booting)"""
    return '''
SW2 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW2[1] += U1['GPIO0']
SW2[2] += Net.fetch('GND')
'''.format(**args)

def generate_power_led(args):
    """Generate led connected to ESP GPI0 that is on after boot"""
    return '''
LED = Part('Device', 'LED', footprint='{led_footprint}')
LED_R = Part('Device', 'R', value='1k', footprint='{resistor_footprint}')
U1['GPIO0'] & LED_R & LED & Net.fetch('{mcurail}')
'''.format(**args)

def generate_battery(args):
    """Generate Battery Holder"""
    return '''
BATTERY = Part('Device', 'Battery', footprint='{powersource_footprint}')
BATTERY['+'] += Net.fetch('+VBatt')
BATTERY['-'] += Net.fetch('GND')
'''.format(**args)

def generate_power_switch(args):
    """Generate power switch"""
    return '''
SWITCH = Part('Switch', 'SW_DPDT_x2', footprint='Button_Switch_THT:SW_CuK_JS202011CQN_DPDT_Straight')
'''.format(**args)

def generate_fuse(args):
    """Generate Fuse"""
    return '''
FUSE = Part('Device', 'Fuse', footprint='{fuse_footprint}')
'''.format(**args)

def generate_power_connector(args):
    """Generate power connector"""
    if args.get('Battery management', False) == 'No battery management ic':
        args['battery_connector_pos'] = '+VLipo'
    else:
        args['battery_connector_pos'] = '+VBatt'

    return '''
BATTERY = Part('Connector', 'Conn_01x02_Female', footprint='{powersource_footprint}')
BATTERY[1] += Net.fetch('{battery_connector_pos}')
BATTERY[2] += Net.fetch('GND')
'''.format(**args)

def connect_power_network(args):
    """Connect components that connect mcu/regulator throuh optional power switch, fuse and ina219 to battery"""
    if args.get('regulator_data', False):
        components = ['REGULATOR[\'VI\']']
    else:
        components = ['Net.fetch(\'+VBatt\')']

    elements = {
        'ina219': 'INA219_R_SHUNT',
        'switch': 'SWITCH[1,2]',
        'fuse_footprint': 'FUSE'
    }

    for element in elements:
        if args.get(element, False):
            components.append(elements[element])

    if args['powersource'] != 'No battery':
        components.append('BATTERY')
    elif args.get('regulator_data', False):
        components.append('Net.fetch(\'+VBus\')')

    line = " & ".join(components)
    return '\n' + line + '\n'

def generate_autoselect(args):
    """Generate +5V/USB auto selector"""
    return '''
AUTOSELECTOR = Part('Device', 'D', footprint='Diode_SMD:D_SMA')
Net.fetch('+5V') & AUTOSELECTOR & Net.fetch('+VBus')
'''.format(*args)

def generate_onewire_bus(args):
    """Generate DQ net for onewire bus"""
    return '''
U3R1 = Part('Device', 'R', value='4k7', footprint='{resistor_footprint}')
U3R1[1] += Net.fetch('{mcurail}')
U3R1[2] += Net.fetch('DQ')
'''.format(**args)

def generate_18b20u(args):
    """Generate 18B20U part and connect it to onewire bus"""
    return '''
U3 = Part('Sensor_Temperature', 'DS18B20U', footprint="Package_SO:MSOP-8_3x3mm_P0.65mm")
U3['VDD'] += Net.fetch('{mcurail}')
U3['GND'] += Net.fetch('GND')
U3['DQ'] += Net.fetch('DQ')
U1['GPIO2'] += Net.fetch('DQ')
'''.format(**args)

def generate_18b20(args):
    """Generate 18b20 part and connect it to onewire bus"""
    return '''
U2 = Part('Sensor_Temperature', 'DS18B20', footprint="Package_TO_SOT_THT:TO-92_Inline")
U2['VDD'] += Net.fetch('{mcurail}')
U2['GND'] += Net.fetch('GND')
U2['DQ'] += Net.fetch('DQ')
U1['GPIO2'] += Net.fetch('DQ')
'''.format(**args)

def generate_onewire_connector(args):
    """Generate connector for external onewire devices"""
    return '''
ONEWIRECONN = Part('Connector', 'Conn_01x03_Female', footprint='{onewire_connector_footprint}')
ONEWIRECONN[1] += Net.fetch('{mcurail}')
ONEWIRECONN[2] += Net.fetch('DQ')
ONEWIRECONN[3] += Net.fetch('GND')
'''.format(**args)

def generate_ina219(args):
    """Generate INA219 that measures voltage and current at battery + terminal"""
    return '''
INA219 = Part('Analog_ADC', 'INA219AxD', footprint='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm')
INA219['VS'] += Net.fetch('{mcurail}')
INA219['GND'] += Net.fetch('GND')

#Setup I2C bus
INA219['SDA'] += U1['GPIO4']
INA219['SCL'] += U1['GPIO5']
SDA_PULLUP = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
SCL_PULLUP = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
U1['GPIO4'] & SDA_PULLUP & Net.fetch('{mcurail}')
U1['GPIO5'] & SCL_PULLUP & Net.fetch('{mcurail}')

#Setup shunt resistor that is used to measure current from voltage drop
INA219_R_SHUNT = Part('Device', 'R', value='0.1', footprint='{resistor_footprint}')
INA219['IN+'] += INA219_R_SHUNT[1]
INA219['IN-'] += INA219_R_SHUNT[2]

#Set I2C address
INA219_R_A0_PULLDOWN = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
INA219_R_A1_PULLDOWN = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
Net.fetch('GND') & INA219_R_A0_PULLDOWN & INA219['A0']
Net.fetch('GND') & INA219_R_A1_PULLDOWN & INA219['A1']
'''.format(**args)

def generate_ftdi_header(args):
    """Generate header for connecting FTDI programmer"""

    return '''
FTDI_HEADER = Part('Connector', 'Conn_01x06_Female', footprint='Skimibowi:FTDI_Header')
FTDI_HEADER[1] += Net.fetch('GND')
FTDI_HEADER[2] += Net.fetch('CTS')
FTDI_HEADER[3] += Net.fetch('{mcurail}')
FTDI_HEADER[4] += Net.fetch('rx')
FTDI_HEADER[5] += Net.fetch('tx')
FTDI_HEADER[6] += Net.fetch('RTS')
'''.format(**args)

def generate_ftdi230(args):
    """Generate FTDI uart circuitry"""
    return '''
FTDI230 = Part('Interface_USB', 'FT231XS', footprint="Package_SO:SSOP-20_3.9x8.7mm_P0.635mm")
FTDI230['VCC'] += Net.fetch('{mcurail}')
FTDI230['GND'] += Net.fetch('GND')
FTDI230['TXD'] += Net.fetch('rx')
FTDI230['RXD'] += Net.fetch('tx')
FTDI230['3V3OUT'] += Net.fetch('+3V3')
FTDI230['USBDM'] += USBMICRO['D-']
FTDI230['USBDP'] += USBMICRO['D+']
FTDI230['DTR'] += Net.fetch('DTR')
FTDI230['RTS'] += Net.fetch('RTS')
C_3V3 = Part('Device', 'C', value='100nF', footprint='{capacitor_footprint}')
Net.fetch('GND') & C_3V3 & FTDI230['3V3OUT']
'''.format(**args)

def generate_ftdi232RL(args):
    """Generate FTDI uart circuitry"""
    return '''
FTDI230 = Part('Interface_USB', 'FT232RL', footprint="Package_SO:SSOP-28_5.3x10.2mm_P0.65mm")
FTDI230['VCC'] += Net.fetch('{mcurail}')
FTDI230['VCCIO'] += Net.fetch('{mcurail}')
FTDI230['GND'] += Net.fetch('GND')
FTDI230['TXD'] += Net.fetch('rx')
FTDI230['RXD'] += Net.fetch('tx')
FTDI230['3V3OUT'] += Net.fetch('+3V3')
FTDI230['USBD-'] += USBMICRO['D-']
FTDI230['USBD+'] += USBMICRO['D+']
FTDI230['DTR'] += Net.fetch('DTR')
FTDI230['TEST'] += Net.fetch('GND')
C_3V3 = Part('Device', 'C', value='100nF', footprint='{capacitor_footprint}')
Net.fetch('GND') & C_3V3 & FTDI230['3V3OUT']
'''.format(**args)


def generate_cp2102(args):
    """Generate CP2102 usb uart circuitry"""
    return '''
CP2102 = Part('Interface_USB', 'CP2102N-A01-GQFN24', footprint="Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm")
CP2102['VDD'] += Net.fetch('{mcurail}')
CP2102['GND'] += Net.fetch('GND')
CP2102['VBUS'] += Net.fetch('+VBUS')
CP2102['D+'] += USBMICRO['D+']
CP2102['D-'] += USBMICRO['D-']
CP2102['TXD'] += Net.fetch('rx')
CP2102['RXD'] += Net.fetch('tx')
CP2102['DTR'] += Net.fetch('DTR')
CP2102['RTS'] += Net.fetch('RTS')
'''.format(**args)

def generate_esp_uart_reset(args):
    """Generate reset circuitry for ESP"""

    transistors = {
        'THT': {'part': 'PN2222A', 'footprint': 'Package_TO_SOT_THT:TO-92_Inline'},
        'SOT-223': {'part': 'PZT2222A', 'footprint':'Package_TO_SOT_SMD:SOT-223'},
        'SOT-23': {'part':'BC817', 'footprint': 'Package_TO_SOT_SMD:SOT-23'}
    }

    format_strings = args
    format_strings['transistor'] = "Part('Transistor_BJT', '{part}', footprint='{footprint}')".format(**transistors[args['transistor_footprint']])
    return '''
Q1 = {transistor}
Q2 = {transistor}
QR1 = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
QR2 = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
Q1['B'] += QR1[1]
QR1[2] += Net.fetch('DTR')
Q2['B'] += QR2[1]
QR2[2] += Net.fetch('RTS')
Q1['E'] += U1['GPIO0']
Q2['E'] += U1['RST']
Q1['C'] += Q2['C']
Q2['C'] += Net.fetch('DTR')
Q1['C'] += Net.fetch('RTS')
'''.format(**format_strings)

def generate_usb_connector(args):
    """Generate USB connector"""
    return '''
USBMICRO = Part('Connector', '{part}', footprint='{footprint}')
USBMICRO['VBUS'] += Net.fetch('+VBus')
USBMICRO['GND'] += Net.fetch('GND')
'''.format(**(args['usb_connector_footprint']))

def generate_regulator(args):
    """Generate regulator that regulates battery voltage to corresponding voltage rail"""
    if 'enable_pin' in args['regulator_data']:
        return '''
REGULATOR = Part('{module}', '{part}', value='{part}', footprint='{footprint}')
REGULATOR['VO'] += Net.fetch('{output}')
REGULATOR['GND'] += Net.fetch('GND')
REGULATOR['EN'] += REGULATOR['VIN']
    '''.format(**(args['regulator_data']))

    else:
        return '''
REGULATOR = Part('{module}', '{part}', value='{part}', footprint='{footprint}')
REGULATOR['VO'] += Net.fetch('{output}')
REGULATOR['GND'] += Net.fetch('GND')
'''.format(**(args['regulator_data']))

def generate_battery_management(args):
    """Generate battery management IC"""
    return '''
BATTERYMANAGER = Part('Battery_Management', 'MCP73871-2AA', footprint='Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm')
BATTERYMANAGER['IN'] += Net.fetch('+VBus')
BATTERYMANAGER['SEL'] += Net.fetch('+VBus')
BATTERYMANAGER['PROG2'] += Net.fetch('+VBus')
BATTERYMANAGER['TE'] += Net.fetch('+VBus')
BATTERYMANAGER['CE'] += Net.fetch('+VBus')

BATTERYMANAGER['VSS'] += Net.fetch('GND')

BATTERYMANAGER['OUT'] += Net.fetch('+VBatt')

BATTERYMANAGER['VBAT'] += Net.fetch('+VLipo')
BATTERYMANAGER['Vbat_SENSE'] += Net.fetch('+VLipo')

RPROG1 = Part('Device', 'R', value='2k', footprint='{resistor_footprint}')
Net.fetch('GND') & RPROG1 & BATTERYMANAGER['PROG1']
RPROG2 = Part('Device', 'R', value='100k', footprint='{resistor_footprint}')
Net.fetch('GND') & RPROG2 & BATTERYMANAGER['PROG3']

BM_LED = Part('Device', 'LED', footprint='{led_footprint}')
BM_LED_R = Part('Device', 'R', value='1k', footprint='{resistor_footprint}')
BATTERYMANAGER['STAT1'] & BM_LED_R & BM_LED & Net.fetch('+VBus')

BM_LED2 = Part('Device', 'LED', footprint='{led_footprint}')
BM_LED_R2 = Part('Device', 'R', value='1k', footprint='{resistor_footprint}')
BATTERYMANAGER['STAT2'] & BM_LED_R2 & BM_LED2 & Net.fetch('+VBus')

BM_C = Part('Device', 'C', value='10uF', footprint='{capacitor_footprint}')
Net.fetch('+VLipo') & BM_C & Net.fetch('GND')

BM_VPCC_R1 = Part('Device', 'R', value='100k', footprint='{resistor_footprint}')
BM_VPCC_R2 = Part('Device', 'R', value='270k', footprint='{resistor_footprint}')
Net.fetch('GND') & BM_VPCC_R1 & BM_VPCC_R2 & Net.fetch('+VBus')
BATTERYMANAGER['VPCC'] += BM_VPCC_R2[1]

BM_THERM_R = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
BATTERYMANAGER['THERM'] & BM_THERM_R & Net.fetch('GND')
'''.format(**args)

def generate_mcp73831(args):
    """Generate MCP73831 battery management IC"""

    return '''
BATTERYMANAGER = Part('Battery_Management', 'MCP73831-2-OT', footprint='Package_TO_SOT_SMD:SOT-23-5')

BM_LED = Part('Device', 'LED', footprint='{led_footprint}')
BM_LED_R = Part('Device', 'R', value='1k', footprint='{resistor_footprint}')
BATTERYMANAGER['STAT'] & BM_LED_R & BM_LED & Net.fetch('+VBus')

BATTERYMANAGER['VSS'] += Net.fetch('GND')
RPROG = Part('Device', 'R', value='2k', footprint='{resistor_footprint}')
Net.fetch('GND') & RPROG & BATTERYMANAGER['PROG']

BM_C = Part('Device', 'C', value='10uF', footprint='{capacitor_footprint}')
Net.fetch('+VLipo') & BM_C & Net.fetch('GND')
'''.format(**args)

def generate_arduino_uno_r3_board_footprint(args):
    """Generate Arduino Uno R3 board layout footprint"""
    return '''
BOARD = Part('MCU_Module', 'Arduino_Uno_R3', footprint='Module:Arduino_UNO_R3_WithMountingHoles')
BOARD['RESET'] += U1['RESET']
BOARD['+5V'] += Net.fetch('+5V')
BOARD['3V3'] += Net.fetch('+3V3')
BOARD['GND'] += Net.fetch('GND')
BOARD['Vin'] += Net.fetch('Vin')

BOARD['SDA'] += Net.fetch('SDA')
BOARD['SCL'] += Net.fetch('SCL')

BOARD['RX'] += Net.fetch('rx')
BOARD['TX'] += Net.fetch('tx')

'''.format(args)

def generate_arduino_nano_v3_board_footprint(args):
    """Generate Arduino Nano V3 board layout footprint"""
    return '''
BOARD = Part('MCU_Module', 'Arduino_Nano_v3.x', footprint='Module:Arduino_Nano')
BOARD['RESET'] += U1['RESET']
BOARD['+5V'] += Net.fetch('+5V')
BOARD['3V3'] += Net.fetch('+3V3')
BOARD['GND'] += Net.fetch('GND')
BOARD['Vin'] += Net.fetch('Vin')

BOARD['SDA'] += Net.fetch('SDA')
BOARD['SCL'] += Net.fetch('SCL')

BOARD['RX'] += Net.fetch('rx')
BOARD['TX'] += Net.fetch('tx')
'''.format(args)


def generate_atmega_arduino_board_connections(args):
    """Generate connections from ATmega mcu to Arduino headers"""
    return '''
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
'''.format(args)

def generate_adafruit_feather(args):
    """Generate Adafruit Feather board footprint"""
    return '''
BOARD = Part('Skimibowi', 'Adafruit_Feather', footprint='skimibowi:Adafruit_Feather')
'''.format(args)

def generate_hc12(args):
    """Generate footprint for HC-12 RF-module"""

    return '''
HC12 = Part('Skimibowi', 'HC-12', footprint="Skimibowi:HC-12")
HC12['VCC'] += Net.fetch('{mcurail}')
HC12['GND'] += Net.fetch('GND')
HC12['RXD'] += Net.fetch('TXD2')
HC12['TXD'] += Net.fetch('RXD2')
'''.format(**args)

def generate_esp_software_serial(args):
    """Generate ESP software serial networks"""

    return '''
U1['GPIO13'] += Net.fetch('RXD2')
U1['GPIO15'] += Net.fetch('TXD2')
'''.format(**args)
