"""Generates microcontroller board descriptions in SKiDL"""

def generate(args, wizard):
    """ Generates microcontroller board descriptions in SKiDL """

    code = '''#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Bus, Part, Net, generate_netlist
'''.format(**args)

    if args['mcu'] in ['ESP-12E', 'ESP-07']:
        code += generate_esp(args)

    if args['powersource'] not in ['No battery', 'JST PH S2B']:
        code += generate_battery(args)

    if args['powersource'] == 'JST PH S2B':
        code += generate_power_connector(args)

    if wizard.field('fuse'):
        code += generate_fuse(args)

    if wizard.field('switch'):
        code += generate_power_switch(args)

    if wizard.field('battery_management') == 'MCP73871-2AA':
        code += generate_battery_management(args)

    if 'regulator' in args and args['regulator'] is not None:
        code += generate_regulator(args)

    if wizard.field('reset'):
        code += generate_reset_line(args)

    if wizard.field('Reset button'):
        code += generate_reset_button(args)

    if wizard.field('Flash button'):
        code += generate_flash_button(args)

    if wizard.field("led"):
        code += generate_power_led(args)

    if wizard.field('DS18B20') or wizard.field('DS18B20U') or wizard.field('onewire_connector'):
        code += generate_onewire_bus(args)

    if wizard.field('DS18B20'):
        code += generate_18b20(args)

    if wizard.field('DS18B20U'):
        code += generate_18b20u(args)

    if wizard.field('onewire_connector') != "No Onewire connector":
        code += generate_onewire_connector(args)

    if wizard.field('ina219'):
        code += generate_ina219(args)

    if wizard.field('FTDI header'):
        code += generate_ftdi_header(args)

    if wizard.field('powersource') != 'No battery':
        code += connect_power_network(wizard)

    if wizard.field('usb_connector') != 'No USB connector':
        code += generate_usb_connector(args)

    if wizard.field('usb_uart') == 'FT231':
        code += generate_ftdi230(args)

    if wizard.field('board_footprint') == 'Arduino Uno R3':
        code += generate_arduino_uno_r3_board_footprint(args)

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
    """Generate power switch"""
    return '''
FUSE = Part('Device', 'Fuse', footprint='Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open')
'''.format(**args)

def generate_power_connector(args):
    """Generate power connector"""
    return '''
BATTERY = Part('Connector', 'Conn_01x02_Female', footprint='{powersource_footprint}')
BATTERY[1] += Net.fetch('+VLipo')
BATTERY[2] += Net.fetch('GND')
'''.format(**args)

def connect_power_network(wizard):
    """Connect components that connect mcu/regulator throuh optional power switch, fuse and ina219 to battery"""
    if wizard.field('regulator') not in ['No regulator', True, False]:
        components = ['REGULATOR[\'VI\']']
    else:
        components = ['Net.fetch(\'+VBatt\')']

    elements = {
        'ina219': 'INA219_R_SHUNT',
        'switch': 'SWITCH[1,2]',
        'fuse': 'FUSE'
    }

    for element in elements:
        if wizard.field(element):
            components.append(elements[element])

    components.append('BATTERY')

    line = " & ".join(components)
    return '\n' + line + '\n'

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
    """Generate 18b20 part and cconnect it to onewire bus"""
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
FTDI_HEADER = Part('Connector', 'Conn_01x06_Female', footprint='Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical')
FTDI_HEADER[1] += Net.fetch('GND')
FTDI_HEADER[2] += NC
FTDI_HEADER[3] += Net.fetch('{mcurail}')
FTDI_HEADER[4] += U1['RX']
FTDI_HEADER[5] += U1['TX']
FTDI_HEADER[6] += NC
'''.format(**args)

def generate_ftdi230(args):
    """Generate FTDI uart circuitry"""
    return '''
FTDI230 = Part('Interface_USB', 'FT231XS', footprint="Package_SO:SSOP-20_3.9x8.7mm_P0.635mm")
FTDI230['VCC'] += Net.fetch('{mcurail}')
FTDI230['GND'] += Net.fetch('GND')
FTDI230['TXD'] += U1['RX']
FTDI230['RXD'] += U1['TX']
FTDI230['USBDM'] += USBMICRO['D-']
FTDI230['USBDP'] += USBMICRO['D+']

Q1 = Part('Transistor_BJT', 'PZT2222A', footprint='Package_TO_SOT_SMD:SOT-223')
Q2 = Part('Transistor_BJT', 'PZT2222A', footprint='Package_TO_SOT_SMD:SOT-223')
QR1 = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
QR2 = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
Q1['B'] += QR1[1]
QR1[2] += FTDI230['DTR']
Q2['B'] += QR2[1]
QR2[2] += FTDI230['RTS']
Q1['E'] += U1['GPIO0']
Q2['E'] += U1['RST']
Q1['C'] += Q2['C']
Q2['C'] += FTDI230['DTR']
Q1['C'] += FTDI230['RTS']
'''.format(**args)

def generate_usb_connector(args):
    """Generate USB connector"""
    return '''
USBMICRO = Part('Connector', 'USB_B_Micro', footprint='{usb_connector_footprint}')
USBMICRO['VBUS'] += Net.fetch('+VBus')
USBMICRO['GND'] += Net.fetch('GND')
'''.format(**args)

def generate_regulator(args):
    """Generate regulator that regulates battery voltage to corresponding voltage rail"""

    return '''
REGULATOR = Part('{module}', '{part}', value='{part}', footprint='{footprint}')
#REGULATOR['VI'] += Net.fetch('+VBatt')
REGULATOR['VO'] += Net.fetch('{output}')
REGULATOR['GND'] += Net.fetch('GND')
'''.format(**(args['regulator']))

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

def generate_arduino_uno_r3_board_footprint(args):
    """Generate Arduino Uno R3 board layout footprint"""
    return '''
BOARD = Part('MCU_Module', 'Arduino_Uno_R3', footprint='Module:Arduino_UNO_R3_WithMountingHoles')
BOARD['RESET'] += U1['RST']
BOARD['+5V'] += Net.fetch('+5V')
BOARD['3V3'] += Net.fetch('+3V3')
BOARD['GND'] += Net.fetch('GND')
BOARD['Vin'] += Net.fetch('+VBus')

BOARD['TX'] += U1['TX']
BOARD['RX'] += U1['RX']
'''.format(args)
