# -*- coding: utf-8 -*-
import visa
import numpy as np
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

    def init(self, s):
		self.s = s
      	for n, v in s.iteritems():
			setattr(self, n, v)
        
	def test(self):
        print "Test (ID):", self.hp.query("ID")

	def _get_data(self, command, start, stop, step):
        print "Getting data:",
        data = self.hp.query(command)
        print "OK"
		print "Parsing data:",
		filtered = re.findall("\w\s([eE.\d+-]+)", data)

		ys = [float(f) for f in filtered]
		xs = np.arange(start, stop+step, step)

		print "OK"
		#print "ys:", len(ys), "xs:", len(xs)
		return zip(xs, ys)

class Transfer(Analyzer):

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
                raise Exception("Error - Too small V_GS_STEP! (Max. 1001 steps)")
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
    def get_data(self):
        return self._get_data("DO 'IDS';", self.V_GS_START, self.V_GS_STOP, self.V_GS_STEP)

