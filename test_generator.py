"""Tests for SKiDL generator functions"""
import unittest
from unittest.mock import Mock
from generator import generate
from generator import generate_ftdi_header
from generator import generate_ftdi230
import sys
from io import StringIO

class TestGenerator(unittest.TestCase):
    """Tests for SKiDL generator functions"""
    def test_esp12e_basic(self):
        """Test basic generation case with ESP-12E"""
        wizard = Mock()
        wizard.field.return_value = False
        self.assertEqual(
            generate({'mcu':'ESP-12E',
                      'mcu_footprint':'RF_Module:ESP-12E',
                      'mcurail':'+VBatt',
                      'powersource':'No battery'}, wizard),
            '''
#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Bus, Part, Net, generate_netlist

U1 = Part('RF_Module', 'ESP-12E', footprint='RF_Module:ESP-12E')

NETS = {}
NETS['+VBatt'] = Net('+VBatt')
NETS['+VBus'] = Net('+VBus')
NETS['+3V'] = Net('+3V')
NETS['+3V3'] = Net('+3V3')
NETS['+5V'] = Net('+5V')
NETS['GND'] = Net('GND')

U1['VCC'] += NETS['+VBatt']
U1['GND'] += NETS['GND']
U1['EN'] += NETS['+VBatt']
U1['GPIO15'] += NETS['GND']

generate_netlist()
'''
        )
    def test_esp12e_all_options(self):
        """Test ESP-12E with reset line, reset button and 18b20"""
        self.maxDiff = 10000
        wizard = Mock()
        wizard.field.return_value = True
        self.assertEqual(
            generate({'mcu':'ESP-12E',
                      'mcu_footprint':'RF_Module:ESP-12E',
                      'mcurail':'+VBatt',
                      'powersource':'No battery',
                      'resistor_footprint':'Resistor_SMD:R_1206_3216Metric'}, wizard),
            '''
#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Bus, Part, Net, generate_netlist

U1 = Part('RF_Module', 'ESP-12E', footprint='RF_Module:ESP-12E')

NETS = {}
NETS['+VBatt'] = Net('+VBatt')
NETS['+VBus'] = Net('+VBus')
NETS['+3V'] = Net('+3V')
NETS['+3V3'] = Net('+3V3')
NETS['+5V'] = Net('+5V')
NETS['GND'] = Net('GND')

U1['VCC'] += NETS['+VBatt']
U1['GND'] += NETS['GND']
U1['EN'] += NETS['+VBatt']
U1['GPIO15'] += NETS['GND']

NETS['RST'] = Net('RST')
U1['RST'] += NETS['RST']
U1['GPIO16'] += NETS['RST']

SW1 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW1[1] += NETS['RST']
SW1[2] += NETS['GND']

SW2 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW2[1] += U1['GPIO15']
SW2[2] += NETS['GND']

NETS['VDD'] = Net('VDD')
NETS['VDD'] += NETS['+VBatt']
NETS['DQ'] = Net('DQ')

U3R1 = Part('Device', 'R', value='4k7', footprint='Resistor_SMD:R_1206_3216Metric')
U3R1[1] += NETS['VDD']
U3R1[2] += NETS['DQ']

U2 = Part('Sensor_Temperature', 'DS18B20', footprint="Package_TO_SOT_THT:TO-92_Inline")
U2['VDD'] += NETS['VDD']
U2['GND'] += NETS['GND']
U2['DQ'] += NETS['DQ']
U1['GPIO2'] += NETS['DQ']

U3 = Part('Sensor_Temperature', 'DS18B20U', footprint="Package_SO:MSOP-8_3x3mm_P0.65mm")
U3['VDD'] += NETS['VDD']
U3['GND'] += NETS['GND']
U3['DQ'] += NETS['DQ']
U1['GPIO2'] += NETS['DQ']

FTDI_HEADER = Part('Connector', 'Conn_01x06_Female', footprint='Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical')
FTDI_HEADER[1] += NETS['GND']
FTDI_HEADER[2] += NC
FTDI_HEADER[3] += NETS['VDD']
FTDI_HEADER[4] += U1['TX']
FTDI_HEADER[5] += U1['RX']
FTDI_HEADER[6] += NC

generate_netlist()
'''
        )

    def test_ftdi_header(self):
        """Test FTDI header generation"""
        self.assertEqual(generate_ftdi_header(),
        '''
FTDI_HEADER = Part('Connector', 'Conn_01x06_Female', footprint='Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical')
FTDI_HEADER[1] += NETS['GND']
FTDI_HEADER[2] += NC
FTDI_HEADER[3] += NETS['VDD']
FTDI_HEADER[4] += U1['TX']
FTDI_HEADER[5] += U1['RX']
FTDI_HEADER[6] += NC
''')

    def test_ftdi230(self):
        """Test generation of FTDI230"""
        self.assertEqual(generate_ftdi230({'resistor_footprint':'Resistor_SMD:R_1206_3216Metric'}),
        '''
FTDI230 = Part('Interface_USB', 'FT231XS', footprint="Package_SO:SSOP-20_3.9x8.7mm_P0.635mm")
USBMICRO = Part('Connector', 'USB_B_Micro', footprint='USB_Micro-B_Molex-105017-0001')
FTDI230['VCC'] += NETS['VDD']
FTDI230['GND'] += NETS['GND']
FTDI230['TXD'] += U1['RX']
FTDI230['RXD'] += U1['TX']
FTDI230['USBDM'] += USBMICRO['D-']
FTDI230['USBDP'] += USBMICRO['D+']
USBMICRO['VBUS'] += NETS['+VBus']
USBMICRO['GND'] += NETS['GND']

Q1 = Part('Transistor_BJT', 'PZT2222A', footprint='Package_TO_SOT_SMD:SOT-223')
Q2 = Part('Transistor_BJT', 'PZT2222A', footprint='Package_TO_SOT_SMD:SOT-223')
QR1 = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_1206_3216Metric')
QR2 = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_1206_3216Metric')
Q1['B'] += QR1[1]
QR1[2] += FTDI230['DTR']
Q2['B'] += QR2[1]
QR2[2] += FTDI230['RTS']
Q1['E'] += U1['GPIO0']
Q2['E'] += U1['RST']
Q1['C'] += Q2['C']
Q2['C'] += FTDI230['DTR']
Q1['C'] += FTDI230['RTS']
''')

    def test_esp12e_all_options_execution(self):
        """Test execution of generated skidl code with all options true"""

        codeOut = StringIO()
        codeErr = StringIO()
        sys.stdout = codeOut
        sys.stderr = codeErr

        wizard = Mock()
        wizard.field.return_value = True

        exec( generate({'mcu':'ESP-12E',
                        'mcu_footprint':'RF_Module:ESP-12E',
                        'mcurail':'+VBatt',
                        'powersource':'No battery',
                        'resistor_footprint':'Resistor_SMD:R_1206_3216Metric'}, wizard))

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        self.assertTrue(codeErr.getvalue().endswith('No errors or warnings found during netlist generation.\n\n'))
        self.assertEqual('', codeOut.getvalue())

        codeOut.close()
        codeErr.close()


if __name__ == '__main__':
    unittest.main()
