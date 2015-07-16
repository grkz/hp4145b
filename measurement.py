#-*- coding: utf-8 -*-
from modes import *
import data
import numpy as np

# SMU2 - Drain
# SMU3 - Source
# SMU4 - Gate

settings = {
    #compliance
    'I_DS_MAX'      :   10e-2,
    'I_GS_MAX'      :   1e-4,
    
    # measurement
    'V_DS'          :   9,
    'V_GS_START'    :   1.6,
    'V_GS_STOP'     :   3.2,
    'V_GS_STEP'     :   0.004,
}
  
tr = Transfer()
"""
filename = "2N7000_TR"
parameter = 'V_DS'
#param_list = [2, 3, 4, 5, 6]
param_list = np.linspace(1,10,4)

for value in param_list:
    try:
        settings['V_DS'] = value
        tr.init(settings)
        tr.setup()
        tr.meas()
        data.save(filename + "_" + parameter + str(value), tr.get_data(), tr.get_settings())
        data.plot_tr(filename +"_" + parameter + str(value), "Ch-ka przejsciowa 2N7000", preview=False, legend_loc=2)
    except Exception as e:
        print e
        
data.plots_tr(filename, "Ch-ki przejsciowe 2N7000", preview=True, legend_loc=2)

"""
### OUTPUT


settings2 = {
    #compliance
    'I_DS_MAX'      :   10e-2,
    'I_GS_MAX'      :   1e-4,
    
    # measurement
    'V_GS'          :   3,
    'V_DS_START'    :   0,
    'V_DS_STOP'     :   3,
    'V_DS_STEP'     :   0.01,
}

otp = Output()

filename = "2N7000_OT"
parameter = 'V_GS'
param_list = np.linspace(2,3,6)

for value in param_list:
    try:
        settings2[parameter] = value
        otp.init(settings2)
        otp.setup()
        otp.meas()
        data.save(filename + "_" + parameter + str(value), otp.get_data(), otp.get_settings())
        data.plot_op(filename +"_" + parameter + str(value), "Ch-ka wyjsciowa 2N7000", preview=False, legend_loc=2)
    except Exception as e:
        print e
    
data.plots_op(filename, "Ch-ki wyjsciowe 2N7000", preview=True, legend_loc=4)
