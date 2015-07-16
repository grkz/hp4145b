from os.path import join, basename, splitext
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import json

data_dir = 'data'
results_dir = 'results'


def save(filename, data, settings):
    path_data = join(data_dir, filename + ".dat")
    path_settings = join(data_dir, filename + ".json")
    
    print "Saving file (" + path_data +"):",
    with open(path_data, 'w') as file:
        for point in data:
            file.write(str(point[0]) + "\t" + str(point[1]) + "\n")
    print "OK"
    
    print "Saving settings file (" + path_settings + "):",
    with open(path_settings, 'w') as file:
        file.write(json.dumps(settings, indent=4))
    print "OK"

def plot_tr(filename, title, save=True, preview=True, clear=True, legend_loc=0):
    plot(filename, title, "$V_{GS}$", "$V_{DS}$", 'V_DS', save, preview, clear, legend_loc)
def plot_op(filename, title, save=True, preview=True, clear=True, legend_loc=0):
    plot(filename, title, "$V_{DS}$", "$V_{GS}$", 'V_GS', save, preview, clear, legend_loc)
def plots_tr(filename, title, save=True, preview=True, clear=True, legend_loc=0):
    plots(filename, title, "$V_{GS}$", "$V_{DS}$", 'V_DS', save, preview, clear, legend_loc)
def plots_op(filename, title, save=True, preview=True, clear=True, legend_loc=0):
    plots(filename, title, "$V_{DS}$", "$V_{GS}$", 'V_GS', save, preview, clear, legend_loc)

def plots(filename, title, xlabel, label, parameter, save=True, preview=True, clear=True, legend_loc=0):
    """plots all filename* files"""
    for path in glob.glob(data_dir + "/" + filename + "*.dat"):
        plot(splitext(basename(path))[0], title, xlabel, label, parameter, save=False, preview=False, clear=False, legend_loc=legend_loc)
    
    if save == True:
        save_plot(filename)
    if preview == True:
        plt.show()
    if clear == True:
        plt.clf()
    
def save_plot(filename):
    path = join(results_dir, filename + ".png")
    print "Plotting to file (" + path + "):",
    plt.savefig(path)
    print "OK"


def plot(filename, title, xlabel, label, parameter, save=True, preview=True, clear=True, legend_loc=0):
    path_data = join(data_dir, filename + ".dat")
    path_settings = join(data_dir, filename + ".json")
    
    with open(path_data) as file:
        data = np.loadtxt(file)
   
    with open(path_settings) as file:
        settings = json.load(file)
    
    plt.plot(data[:,0], data[:,1], label=label + ' = ' + str(settings[parameter]) + ' V')
    plt.title(title)
    plt.legend(loc=legend_loc)
    plt.xlabel(xlabel + r' [V]')
    plt.ylabel(r'$I_{DS}$ [A]')
    plt.grid(True)

    if save == True:
        save_plot(filename)
    if preview == True:
        plt.show()
    if clear == True:
        plt.clf()
