from os.path import join
import re
import numpy as np
import matplotlib.pyplot as plt
import json

data_dir = 'data'
results_dir = 'results'

    
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
    with open(join(data_dir, filename + ".json")) as file:
        settings = json.load(file)
    plt.plot(data[:,0], data[:,1], label='$V_{DS} = ' + str(settings['V_DS']) + '\ V$')
    plt.title(title)
    plt.legend()
    plt.xlabel(r'$V_{GS}$ [V]')
    plt.ylabel(r'$I_{DS}$ [A]')
    plt.grid()
    if save == True:
        print "Plotting to file (" + results_dir + "/" + results_dir + ".png):",
        plt.savefig(join(results_dir, filename + ".png"))
        print "OK"
    if preview == True:
        plt.show()
