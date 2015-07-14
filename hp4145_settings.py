# -*- coding: utf-8 -*-
import visa
import numpy as np
import matplotlib.pyplot as plt
import re
rm = visa.ResourceManager()
hp = rm.open_resource("GPIB0::15::INSTR") # hp4145 address
hp.timeout = 50000

warning = """
# SMU2 - Drain
# SMU3 - Source
# SMU4 - Gate
"""

def test():
        print "Test (ID):", hp.query("ID")
def channel_setup(mode):
    """ set channels for:
        T - transfer DC characteristics
        O - output DC characteristics

        mode - string parameter
        # SMU2 - Drain
        # SMU3 - Source
        # SMU4 - Gate
    """
    hp.write("IT2;")
    if mode == "T":
        print("setting MOSFET transfer characteristics...")
        print(warning)
        print "Setting channels:",
        # MOSFET transfer characteristics

        # VD: SMU2: VDS / IDS, V / CONST
        hp.write("DE,CH2,'VDS','IDS',1,3;")

        # VS: SMU3: V3 / I3, COM / CONST
        hp.write("DE,CH3,'V3','I3',3,3;")

        # VG: SMU4: VGS / IG / V / VAR1
        hp.write("DE,CH4,'VGS','IG',1,1;")
        
        print("OK")
        
    elif mode == "O":
        print("MOSFET output characteristics")
        
def const_setup_transfer(V_DS, I_DS_MAX):
    """VD: SMU2: VDS / IDS, / V / CONST"""
    print "Setting constants: ",
    hp.write("SS VC 2," + str(V_DS) + "," + str(I_DS_MAX) + ";")
    print "OK"
def var1_setup_transfer(V_GS_START, V_GS_STOP, V_GS_STEP, I_GS_MAX=1E-3, log=False):
    """VG: SMU4: VGS / IG / V / VAR1"""
    print "Setting variables: ",
    if (abs(V_GS_STOP - V_GS_START) / V_GS_STEP) > 1001:
            print "Error - Too small V_GS_STEP! (Max. 1001 steps)"
            return
    hp.write("SS VR 1," + str(V_GS_START) + "," + str(V_GS_STOP) + "," + str(V_GS_STEP) + "," + str(I_GS_MAX) + ";")
    print "OK"
def display_setup_transfer(V_GS_min, V_GS_max, I_DS_min, I_DS_max, log=False):
        hp.write("SM;DM1;XN 'VGS',1," + str(V_GS_min) + "," + str(V_GS_max) + ";YB;YA 'IDS',1," + str(I_DS_min) + "," + str(I_DS_max) + ";")
def single_measurement():
        print "Measuring:",
        hp.write("BC;")
        hp.write("DR1;")
        hp.write("MD ME1;")
        hp.wait_for_srq()
        hp.write("DR0;")
        print "DONE."
def get_data_transfer(V_GS_START, V_GS_STOP, V_GS_STEP, output_file):
        print "Getting data and plotting:",
        file = open(output_file, 'w')
        data = hp.query("DO 'IDS';")
        filtered = re.findall("\w\s([+-eE.\d]+),", data)
        V_GS = []
        I_DS = [float(f) for f in filtered]
        
        
        while V_GS_START <= V_GS_STOP:
                V_GS += [V_GS_START]
                V_GS_START += V_GS_STEP
        
        #print "IDS length: ", len(I_DS)
        #print "V_GS length: ", len(V_GS)
        
        for point in zip(V_GS, I_DS):
                file.write(str(point[0]) + "\t" + str(point[1]) + "\n")
        file.close()
        figure_transfer(output_file)
        print "DONE."
def figure_transfer(data_file):
	file = open(data_file)
	data = np.loadtxt(file)
	file.close()
	plt.plot(data[:,0], data[:,1])
	plt.title(u"Ch-ka przejsciowa")
	plt.xlabel(r'$V_{GS} [V]$')
	plt.ylabel(r'$I_{DS}$ [A]')
	plt.grid()
	plt.savefig(data_file + '.png')
	plt.show()
         
