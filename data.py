from os.path import join
import re
import numpy as np
import matplotlib.pyplot as plt
import json

data_dir = 'data'
results_dir = 'results'

def save_tr(filename, tr_obj):
    v = tr_obj.V_GS_START
    v_stop = tr_obj.V_GS_STOP
    v_step = tr_obj.V_GS_STEP
    
    data = tr_obj.get_data_tr()
    print "Pharsing data:",
    filtered = re.findall("\w\s([eE.\d+-]+)", data)
    V_GS = []
    I_DS = [float(f) for f in filtered]
 
    while v <= v_stop:
        V_GS.append(v)
        v += v_step

    pharsed_data = zip(V_GS, I_DS)
    print "OK"
    save(filename, pharsed_data, tr_obj.s)
    
    #print "IDS length: ", len(I_DS)
    #print "V_GS length: ", len(V_GS)
def save(filename, data, settings):
    print "Saving file (" + data_dir + "/" + filename + ".dat):",
    file = open(join(data_dir, filename + ".dat"), 'w')
    for point in data:
        file.write(str(point[0]) + "\t" + str(point[1]) + "\n")
    file.close()
    print "OK"
    print "Saving settings file (" + data_dir + "/" + filename + ".json):",
    file = open(join(data_dir, filename + ".json"), 'w')
    file.write(json.dumps(settings, indent=4))
    file.close()
    print "OK"

def plot_tr(filename, title, save=True, preview=True):
    file = open(join(data_dir, filename + ".dat"))
    data = np.loadtxt(file)
    file.close()
    plt.plot(data[:,0], data[:,1])
    plt.title(title)
    plt.xlabel(r'$V_{GS} [V]$')
    plt.ylabel(r'$I_{DS}$ [A]')
    plt.grid()
    if save == True:
        print "Plotting to file (" + data_dir + "/" + results_dir + ".png):",
        plt.savefig(join(results_dir, filename + ".png"))
        print "OK"
    if preview == True:
        plt.show()
