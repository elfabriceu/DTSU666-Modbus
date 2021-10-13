#!/usr/bin/env python
"""
Chint DTSU666-Modbus 80A 3P4W Smart Meter Three Phase Electrical System. The Python plugin for Domoticz
Author: elfabric.eu
Requirements: 
    1.python module minimalmodbus -> http://minimalmodbus.readthedocs.io/en/master/
        (pi@raspberrypi:~$ sudo pip3 install minimalmodbus)
    2.Communication module Modbus USB to RS485 converter module
"""
"""
<plugin key="DTSU666" name="Chint DTSU666-Modbus" version="1.0.0" author="elfabric.eu">
    <params>
        <param field="SerialPort" label="Modbus Port" width="200px" required="true" default="/dev/ttyUSB0" />
        <param field="Mode1" label="Baud rate" width="40px" required="true" default="9600"  />
        <param field="Mode2" label="Device ID" width="40px" required="true" default="1" />
        <param field="Mode3" label="Reading Interval min." width="40px" required="true" default="1" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>

"""

import minimalmodbus
import serial
import Domoticz


class BasePlugin:
    def __init__(self):
        self.runInterval = 1
        self.rs485 = "" 
        return

    def onStart(self):
        self.rs485 = minimalmodbus.Instrument(Parameters["SerialPort"], int(Parameters["Mode2"]))
        self.rs485.serial.baudrate = Parameters["Mode1"]
        self.rs485.serial.bytesize = 8
        self.rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.rs485.serial.stopbits = 1
        self.rs485.serial.timeout = 1
        self.rs485.debug = False

        self.rs485.mode = minimalmodbus.MODE_RTU
        devicecreated = []
        Domoticz.Log("Chint DTSU666 Modbus plugin start")
        self.runInterval = int(Parameters["Mode3"]) * 1 
        if 1 not in Devices:
            Domoticz.Device(Name="Voltage L1-L2", Unit=1,TypeName="Voltage",Used=0).Create()
        if 2 not in Devices:
            Domoticz.Device(Name="Voltage L2-L3", Unit=2,TypeName="Voltage",Used=0).Create()
        if 3 not in Devices:
            Domoticz.Device(Name="Voltage L3-L1", Unit=3,TypeName="Voltage",Used=0).Create()
        if 4 not in Devices:
            Domoticz.Device(Name="Voltage L1", Unit=4,TypeName="Voltage",Used=0).Create()
        if 5 not in Devices:
            Domoticz.Device(Name="Voltage L2", Unit=5,TypeName="Voltage",Used=0).Create()
        if 6 not in Devices:
            Domoticz.Device(Name="Voltage L3", Unit=6,TypeName="Voltage",Used=0).Create()
        if 7 not in Devices:
            Domoticz.Device(Name="Current L1,L2,L3", Unit=7,TypeName="Current/Ampere",Used=0).Create()
        if 8 not in Devices:
            Domoticz.Device(Name="Sum of Line Currents", Unit=8,TypeName="Current (Single)",Used=0).Create()
        if 9 not in Devices:
            Domoticz.Device(Name="Active Power L1", Unit=9,TypeName="Usage",Used=0).Create()
        if 10 not in Devices:
            Domoticz.Device(Name="Active Power L2", Unit=10,TypeName="Usage",Used=0).Create()
        if 11 not in Devices:
            Domoticz.Device(Name="Active Power L3", Unit=11,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VAr"} 
        if 12 not in Devices:
            Domoticz.Device(Name="Reactive Power L1", Unit=12,TypeName="Custom",Used=0,Options=Options).Create()
        if 13 not in Devices:
            Domoticz.Device(Name="Reactive Power L2", Unit=13,TypeName="Custom",Used=0,Options=Options).Create()
        if 14 not in Devices:
            Domoticz.Device(Name="Reactive Power L3", Unit=14,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;PF"} 
        if 15 not in Devices:
            Domoticz.Device(Name="Power Factor L1", Unit=15,TypeName="Custom",Used=0,Options=Options).Create()
        if 16 not in Devices:
            Domoticz.Device(Name="Power Factor L2", Unit=16,TypeName="Custom",Used=0,Options=Options).Create()
        if 17 not in Devices:
            Domoticz.Device(Name="Power Factor L3", Unit=17,TypeName="Custom",Used=0,Options=Options).Create()
        if 18 not in Devices:
            Domoticz.Device(Name="Total System Active Power", Unit=18,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VAr"} 
        if 19 not in Devices:
            Domoticz.Device(Name="Total System Reactive Power", Unit=19,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;PF"} 
        if 20 not in Devices:
            Domoticz.Device(Name="Total System Power Factor", Unit=20,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;Hz"} 
        if 21 not in Devices:
            Domoticz.Device(Name="Frequency of supply voltages", Unit=21,TypeName="Custom",Used=0,Options=Options).Create()
        if 22 not in Devices:
            Domoticz.Device(Name="Import kWh Meter", Unit=22,TypeName="General",Subtype=0x1D,Used=0).Create()
        if 23 not in Devices:
            Domoticz.Device(Name="Export kWh Meter", Unit=23,TypeName="General",Subtype=0x1D,Used=0).Create()			
        if 24 not in Devices:
            Domoticz.Device(Name="Import kWh", Unit=24,Type=0x71,Subtype=0x0,Used=0).Create()
        if 25 not in Devices:
            Domoticz.Device(Name="Export kWh", Unit=25,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 26 not in Devices:
            Domoticz.Device(Name="EQ+ Import reactive kVArh", Unit=26,Type=0x71,Subtype=0x0,Used=0,Options=Options).Create()
        if 27 not in Devices:
            Domoticz.Device(Name="EQ- Export reactive kVArh", Unit=27,Type=0x71,Subtype=0x0,Used=0,Options=Options).Create()
        if 28 not in Devices:
            Domoticz.Device(Name="Q1 kVArh", Unit=28,Type=0x71,Subtype=0x0,Used=0,Options=Options).Create()
        if 29 not in Devices:
            Domoticz.Device(Name="Q2 kVArh", Unit=29,Type=0x71,Subtype=0x0,Used=0,Options=Options).Create()
        if 30 not in Devices:
            Domoticz.Device(Name="Q3 kVArh", Unit=30,Type=0x71,Subtype=0x0,Used=0,Options=Options).Create()
        if 31 not in Devices:
            Domoticz.Device(Name="Q4 kVArh", Unit=31,Type=0x71,Subtype=0x0,Used=0,Options=Options).Create()

    def onStop(self):
        Domoticz.Log("Chint DTSU666 Modbus plugin stop")

    def onHeartbeat(self):
        self.runInterval -=1;
        if self.runInterval <= 0:
            # Get data from DTSU666
            try:
                Volts_AB = self.rs485.read_float(0x2000, functioncode=4, numberOfRegisters=2)/10
                Volts_BC = self.rs485.read_float(0x2002, functioncode=4, numberOfRegisters=2)/10
                Volts_CA = self.rs485.read_float(0x2004, functioncode=4, numberOfRegisters=2)/10
                Volts_L1 = self.rs485.read_float(0x2006, functioncode=4, numberOfRegisters=2)/10
                Volts_L2 = self.rs485.read_float(0x2008, functioncode=4, numberOfRegisters=2)/10
                Volts_L3 = self.rs485.read_float(0x200A, functioncode=4, numberOfRegisters=2)/10
                Current_L1 = self.rs485.read_float(0x200C, functioncode=4, numberOfRegisters=2)/1000
                Current_L2 = self.rs485.read_float(0x200E, functioncode=4, numberOfRegisters=2)/1000
                Current_L3 = self.rs485.read_float(0x2010, functioncode=4, numberOfRegisters=2)/1000
                Active_Power_L1 = self.rs485.read_float(0x2014, functioncode=4, numberOfRegisters=2)/10
                Active_Power_L2 = self.rs485.read_float(0x2016, functioncode=4, numberOfRegisters=2)/10
                Active_Power_L3 = self.rs485.read_float(0x2018, functioncode=4, numberOfRegisters=2)/10
                Reactive_Power_L1 = self.rs485.read_float(0x201C, functioncode=4, numberOfRegisters=2)/10
                Reactive_Power_L2 = self.rs485.read_float(0x201E, functioncode=4, numberOfRegisters=2)/10
                Reactive_Power_L3 = self.rs485.read_float(0x2020, functioncode=4, numberOfRegisters=2)/10
                Power_Factor_L1 = self.rs485.read_float(0x202C, functioncode=4, numberOfRegisters=2)/1000
                Power_Factor_L2 = self.rs485.read_float(0x202E, functioncode=4, numberOfRegisters=2)/1000
                Power_Factor_L3 = self.rs485.read_float(0x2030, functioncode=4, numberOfRegisters=2)/1000
                Total_System_Active_Power = self.rs485.read_float(0x2012, functioncode=4,numberOfRegisters=2)/10
                Total_System_Reactive_Power = self.rs485.read_float(0x201A, functioncode=4,numberOfRegisters=2)/10
                Total_System_Power_Factor = self.rs485.read_float(0x202A, functioncode=4,numberOfRegisters=2)/1000
                Frequency_Of_Supply_Voltages = self.rs485.read_float(0x2044, functioncode=4, numberOfRegisters=2)/100
                Total_import_kwh = self.rs485.read_float(0x401E, functioncode=4, numberOfRegisters=2)*1000
                Total_export_kwh = self.rs485.read_float(0x4028, functioncode=4, numberOfRegisters=2)*1000
                Total_Q1_kvarh = self.rs485.read_float(0x4028, functioncode=4, numberOfRegisters=2)*1000
                Total_Q2_kvarh = self.rs485.read_float(0x403C, functioncode=4, numberOfRegisters=2)*1000
                Total_Q3_kvarh = self.rs485.read_float(0x4046, functioncode=4, numberOfRegisters=2)*1000
                Total_Q4_kvarh = self.rs485.read_float(0x4050, functioncode=4, numberOfRegisters=2)*1000
                Total_import_Power = 0
                if Active_Power_L1>0: Total_import_Power += Active_Power_L1
                if Active_Power_L2>0: Total_import_Power += Active_Power_L2
                if Active_Power_L3>0: Total_import_Power += Active_Power_L3
                Total_export_Power = 0
                if Active_Power_L1<0: Total_export_Power -= Active_Power_L1
                if Active_Power_L2<0: Total_export_Power -= Active_Power_L2
                if Active_Power_L3<0: Total_export_Power -= Active_Power_L3
            except:
                Domoticz.Log("Connection problem");
            else:
                #Update devices
                Devices[1].Update(0,str(Volts_AB))
                Devices[2].Update(0,str(Volts_BC))
                Devices[3].Update(0,str(Volts_CA))
                Devices[4].Update(0,str(Volts_L1))
                Devices[5].Update(0,str(Volts_L2))
                Devices[6].Update(0,str(Volts_L3))
                Devices[7].Update(0,str(Current_L1)+";"+str(Current_L2)+";"+str(Current_L3))
                Devices[8].Update(0,str(abs(Current_L1)+abs(Current_L2)+abs(Current_L3)))
                Devices[9].Update(0,str(Active_Power_L1))
                Devices[10].Update(0,str(Active_Power_L2))
                Devices[11].Update(0,str(Active_Power_L3))
                Devices[12].Update(0,str(Reactive_Power_L1))
                Devices[13].Update(0,str(Reactive_Power_L2))
                Devices[14].Update(0,str(Reactive_Power_L3))
                Devices[15].Update(0,str(Power_Factor_L1))
                Devices[16].Update(0,str(Power_Factor_L2))
                Devices[17].Update(0,str(Power_Factor_L3))
                Devices[18].Update(0,str(Total_System_Active_Power))
                Devices[19].Update(0,str(Total_System_Reactive_Power))
                Devices[20].Update(0,str(Total_System_Power_Factor))
                Devices[21].Update(0,str(Frequency_Of_Supply_Voltages))
                Devices[22].Update(0,str(Total_import_Power)+";"+str(Total_import_kwh))
                Devices[23].Update(0,str(Total_export_Power)+";"+str(Total_export_kwh))				
                Devices[24].Update(0,str(Total_import_kwh))
                Devices[25].Update(0,str(Total_export_kwh))
                Devices[26].Update(0,str((Total_Q1_kvarh+Total_Q2_kvarh)))
                Devices[27].Update(0,str((Total_Q3_kvarh+Total_Q4_kvarh)))
                Devices[28].Update(0,str(Total_Q1_kvarh))
                Devices[29].Update(0,str(Total_Q2_kvarh))
                Devices[30].Update(0,str(Total_Q3_kvarh))
                Devices[31].Update(0,str(Total_Q4_kvarh))

            if Parameters["Mode6"] == 'Debug':
                Domoticz.Log("Chint DTSU666 Modbus Data")
                Domoticz.Log('Voltage L1-L2: {0:.3f} V'.format(Volts_AB))
                Domoticz.Log('Voltage L2-L3: {0:.3f} V'.format(Volts_BC))
                Domoticz.Log('Voltage L3-L1: {0:.3f} V'.format(Volts_CA))
                Domoticz.Log('Voltage L1: {0:.3f} V'.format(Volts_L1))
                Domoticz.Log('Voltage L2: {0:.3f} V'.format(Volts_L2))
                Domoticz.Log('Voltage L3: {0:.3f} V'.format(Volts_L3))
                Domoticz.Log('Current L1: {0:.3f} A'.format(Current_L1))
                Domoticz.Log('Current L2: {0:.3f} A'.format(Current_L2))
                Domoticz.Log('Current L3: {0:.3f} A'.format(Current_L3))
                Domoticz.Log('Active power L1: {0:.3f} W'.format(Active_Power_L1))
                Domoticz.Log('Active power L2: {0:.3f} W'.format(Active_Power_L2))
                Domoticz.Log('Active power L3: {0:.3f} W'.format(Active_Power_L3))
                Domoticz.Log('Total Import Power: {0:.3f} W'.format(Total_import_Power))
                Domoticz.Log('Total Export Power: {0:.3f} W'.format(Total_export_Power))
                Domoticz.Log('Reactive power L1: {0:.3f} VAr'.format(Reactive_Power_L1))
                Domoticz.Log('Reactive power L2: {0:.3f} VAr'.format(Reactive_Power_L2))
                Domoticz.Log('Reactive power L3: {0:.3f} VAr'.format(Reactive_Power_L3))
                Domoticz.Log('Power factor L1: {0:.3f}'.format(Power_Factor_L1))
                Domoticz.Log('Power factor L2: {0:.3f}'.format(Power_Factor_L2))
                Domoticz.Log('Power factor L3: {0:.3f}'.format(Power_Factor_L3))
                Domoticz.Log('Total system active power: {0:.3f} W'.format(Total_System_Active_Power))
                Domoticz.Log('Total system reactive  power: {0:.3f} VA'.format(Total_System_Reactive_Power))
                Domoticz.Log('Total system power factor: {0:.3f} PF'.format(Total_System_Power_Factor))
                Domoticz.Log('Frequency of supply voltages: {0:.3f} Hz'.format(Frequency_Of_Supply_Voltages))
                Domoticz.Log('Total import kWh: {0:.3f} kWh'.format(Total_import_kwh/1000))
                Domoticz.Log('Total export kWh: {0:.3f} kWh'.format(Total_export_kwh/1000))
                Domoticz.Log('Q1 kVArh: {0:.3f} kVArh'.format(Total_Q1_kvarh/1000))
                Domoticz.Log('Q2 kVArh: {0:.3f} kVArh'.format(Total_Q2_kvarh/1000))
                Domoticz.Log('Q3 kVArh: {0:.3f} kVArh'.format(Total_Q3_kvarh/1000))
                Domoticz.Log('Q1 kVArh: {0:.3f} kVArh'.format(Total_Q4_kvarh/1000))

            self.runInterval = int(Parameters["Mode3"]) * 6


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
