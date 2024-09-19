import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
from matplotlib import font_manager

char_system = "\\"
def write_yrange(Emin=-5, Emax=5, step=2):
    if step >= 1:
        yticks = [float('{:d}'.format(yticks)) for yticks in np.arange(Emin, Emax + step, step)]
        yticksname = ['{:d}'.format(yticks) for yticks in np.arange(Emin, Emax + step, step)]
    else:
        yticks = [float('{:3.2f}'.format(yticks)) for yticks in np.arange(Emin, Emax + step, step)]
        yticksname = ['{:3.2f}'.format(yticks) for yticks in np.arange(Emin, Emax + step, step)]
    return yticks, yticksname

#################### get all the data  ############################################
def get_filename():
    file_list = os.listdir()
    list_file = []
    legend_name = []
    for file in file_list:
        if file.split('.')[-1]=="dat":
            list_file.append(file)
            legend_name.append(file.split('.')[0])
        else:
            print("This is not a .dat file !")
    bz_name = ""
    fermi_name = ""
    for i in range(0, 2):
        if "bz" in list_file[i]:
            bz_name = list_file[i]
        elif "fermi" in list_file[i]:
            fermi_name = list_file[i]
    return bz_name, fermi_name

def plot_band(figname='fermi_surface', dpi=400, fontpath="", fontsize=16):
    plt.rcParams["mathtext.default"] = "regular"
    plt.rcParams['xtick.direction'] = "in"
    plt.rcParams['ytick.direction'] = "in"
    # ------------------ font setup ----------------------#
    font_family = font_manager.FontProperties(fname=fontpath)
    styles = ['normal', 'italic', 'oblique']
    weights = ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']
    font = {'fontproperties': font_family,  # 'family': 'Liberation Sans'
            'style': styles[0],
            'color': 'black',
            'weight': weights[1],
            'size': fontsize+4, }
    color_list = ['#B71C1C', '#C62828', '#D32F2F', '#E53935', '#F44336', '#EF5350', '#E57373', '#EF9A9A', '#FFCDD2',
                  '#FFEBEE']
    line_width = 2
    bz_name, fermi_name = get_filename()
    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot(111)
    data = np.loadtxt(fermi_name)
    fermi_h_x = data[:, 0]
    fermi_h_y = data[:, 1]
    data = np.loadtxt(bz_name)
    bz_x = data[:, 0]
    bz_y = data[:, 1]
    len_y = max(bz_y) - min(bz_y)
    len_x = max(bz_x) - min(bz_x)
    print(min(bz_x), max(bz_x), min(bz_y), min(bz_y))
    ax.scatter(fermi_h_x, fermi_h_y, linestyle='-', linewidth=line_width, marker='o', color='blue', s=0.1)
    ax.plot(bz_x, bz_y, linestyle='--', linewidth=line_width, color='k')
    sp = plt.gca()
    sp_lists = ['top', 'right', 'bottom', 'left']
    for sp_list in sp_lists:
        sp.spines[sp_list].set_visible(False)
    xticks, xticksname = write_yrange(Emin=min(bz_x), Emax=max(bz_x), step=len_x/4)
    yticks, yticksname = write_yrange(Emin=min(bz_y), Emax=max(bz_y), step=len_y/4)
    sec = 0.05           # a section
    ax.axvline(x=0, ymin=0.5, ymax=0.5 + max(bz_y) / len_y - sec, linestyle='--', linewidth=line_width, color='k')
    ax.axhline(y=0, xmin=0.5, xmax=0.5 + max(bz_x) / len_x - sec, linestyle='--', linewidth=line_width, color='k')
    s_x = [0, max(bz_x), 0]
    s_y = [0, 0, max(bz_y)]
    ax.text(0 - 0.02, 0 - 0.10, r"$\Gamma$", fontdict=font, fontsize=fontsize+3)
    ax.text(max(bz_x), 0 - 0.03, r"$N$", fontdict=font, fontsize=fontsize+3)
    ax.text(0 - 0.035, max(bz_y) + 0.02, r"$X$", fontdict=font, fontsize=fontsize+3)
    ax.scatter(s_x, s_y, marker='o', color="red", s=5)
    ax.set_xlim(min(bz_x)-sec*len_x, max(bz_x)+len_x*sec)
    ax.set_xlabel(r'$k_x (\AA^{-1})$', labelpad=-1.0, fontdict=font, fontsize=font['size'] + 5, fontweight=weights[4])
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticksname, fontdict=font, fontsize=fontsize+3)
    ax.set_ylabel(r'$k_y (\AA^{-1})$', labelpad=-1.0, fontdict=font, fontsize=font['size'] + 5, fontweight=weights[4])
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticksname, fontdict=font, fontsize=fontsize+3)
    ax.set_ylim([min(bz_y)-sec*len_y, max(bz_y)+sec*len_y])
    plt.savefig(figname + '.png', dpi=dpi, bbox_inches='tight', facecolor='w')
    #plt.show()
    plt.close('all')
    print("All --> Finished OK")

if __name__=='__main__':
    # plot_band(Emin=-0.75, Emax=0.75, step=0.75, figsize=(12, 8), text_label='(a)',
    #          figname='fermi_surface', title='11-1', dpi=400)
    #print(get_filename())
    file_type = "hole"
    manipulat_plot_file(file_type, 0)
