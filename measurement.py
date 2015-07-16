#-*- coding: utf-8 -*-
from modes import *
import data

# SMU2 - Drain
# SMU3 - Source
# SMU4 - Gate

settings = {
    #compliance
    'I_DS_MAX'      :   10e-2,
    'I_GS_MAX'      :   1e-4,
    
    # measurement
    'V_DS'          :   9,
    'V_GS_START'    :   1.5,
    'V_GS_STOP'     :   3.5,
    'V_GS_STEP'     :   0.004,
}
    
tr = Transfer()

for V_DS in [10,9,8]:
	try:
		settings['V_DS'] = V_DS
		tr.init(settings)
		tr.setup()
		tr.meas()
		data.save(tr.get_data(), tr.get_settings(), "2N7000_VDS" + str(V_DS))
		data.plot_tr("2N7000_VDS" + str(V_DS), "Ch-ka przejsciowa 2N7000", preview=False)
	except e:
		print e

