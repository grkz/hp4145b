# -*- coding: utf-8 -*-
import visa
import numpy as np
import matplotlib.pyplot as plt
import re

info = """
# SMU2 - Drain
# SMU3 - Source
# SMU4 - Gate
"""

address = "GPIB0::15::INSTR" # hp4145 address

class Analyzer:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.hp = self.rm.open_resource(address)
        self.hp.timeout = 50000
        self.test()
        self.s = None
        
    def test(self):
        print "Test (ID):", self.hp.query("ID")
        
    def set_compliance(self, I_DS_MAX, I_GS_MAX):
        self.I_DS_MAX = I_DS_MAX
        self.I_GS_MAX = I_GS_MAX

class Transfer(Analyzer):
    def init(self, s):
	self.s = s
        self.set_compliance(s['I_DS_MAX'], s['I_GS_MAX'])
        
        self.V_DS = s['V_DS']
        self.V_GS_START = s['V_GS_START']
        self.V_GS_STOP = s['V_GS_STOP']
        self.V_GS_STEP = s['V_GS_STEP']

    def setup(self):
        self.channels_setup()
        self.const_setup()
        self.var1_setup()
        self.display_setup(0)   # I_DS_MIN - display setting
    def channels_setup(self):
        """ set channels for:
        transfer DC characteristics
        # SMU2 - Drain
        # SMU3 - Source
        # SMU4 - Gate
        """
        
        print("setting MOSFET transfer characteristics...")
        print info
        print "Setting channels:",
        
        # integration time
        self.hp.write("IT2;")
        # MOSFET transfer characteristics

        # VD: SMU2: VDS / IDS, V / CONST
        self.hp.write("DE,CH2,'VDS','IDS',1,3;")

        # VS: SMU3: V3 / I3, COM / CONST
        self.hp.write("DE,CH3,'V3','I3',3,3;")

        # VG: SMU4: VGS / IG / V / VAR1
        self.hp.write("DE,CH4,'VGS','IG',1,1;")

        print("OK")
    
    def const_setup(self):
        """VD: SMU2: VDS / IDS, / V / CONST"""
        print "Setting constants: ",
        self.hp.write("SS VC 2," + str(self.V_DS) + "," + str(self.I_DS_MAX) + ";")
        print "OK"
    def var1_setup(self):
        """VG: SMU4: VGS / IG / V / VAR1"""
        print "Setting variables: ",
        if (abs(self.V_GS_STOP - self.V_GS_START) / self.V_GS_STEP) > 1001:
                print "Error - Too small V_GS_STEP! (Max. 1001 steps)"
                return
        self.hp.write("SS VR 1," + str(self.V_GS_START) + "," + str(self.V_GS_STOP) + "," + str(self.V_GS_STEP) + "," + str(self.I_GS_MAX) + ";")
        print "OK"
    def display_setup(self, I_DS_MIN):
            self.hp.write("SM;DM1;XN 'VGS',1," + str(self.V_GS_START) + "," + str(self.V_GS_STOP) + ";YB;YA 'IDS',1," + str(I_DS_MIN) + "," + str(self.I_DS_MAX) + ";")
    def meas(self):
            print "Measuring:",
            self.hp.write("BC;")
            self.hp.write("DR1;")
            self.hp.write("MD ME1;")
            self.hp.wait_for_srq()
            self.hp.write("DR0;")
            print "OK"
    def get_data_tr(self):
        print "Getting data:",
        data = self.hp.query("DO 'IDS';")
        print "OK"
        return data

