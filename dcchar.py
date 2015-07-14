from hp4145_settings import *

# SMU2 - Drain
# SMU3 - Source
# SMU4 - Gate

#test()

#T - transfer DC characteristics
#O - output DC characteristics
channel_setup("T")
filename = "2N7000_2"
V_DS = 10
I_DS_MAX = 100e-3

V_GS_START = 1.5
V_GS_STOP = 3.1
V_GS_STEP = 0.005

I_GS_MAX= 1e-3

const_setup_transfer(V_DS, I_DS_MAX)
var1_setup_transfer(V_GS_START, V_GS_STOP, V_GS_STEP, I_GS_MAX, log=False)

print "V_DS", V_DS, 
print "I_DS_MAX", I_DS_MAX
print "V_GS_START", V_GS_START,
print "V_GS_STOP", V_GS_STOP,
print "V_GS_STEP", V_GS_STEP
print "I_GS_MAX", I_GS_MAX

display_setup_transfer(V_GS_START, V_GS_STOP, 0, I_DS_MAX, log=False)
single_measurement()
get_data_transfer(V_GS_START, V_GS_STOP, V_GS_STEP, filename)
