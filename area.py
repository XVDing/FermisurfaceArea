# 分类圈的个数
import numpy as np
import matplotlib as mpl 
from matplotlib import pyplot as plt
import scipy as sp
from scipy import interpolate
import os
from matplotlib import font_manager

mpl.use('Agg')

fontpath='/lustre/home/sztu_ep_huanglili/wangrui/dingxy/vasp/kd/font/times.ttf'
#fontpath="D:\\JianGuoYun\\others\\keda\\old\\fermi\\font\\times.ttf"
# ------------------ font setup ----------------------#
font_family = font_manager.FontProperties(fname=fontpath)
styles = ['normal', 'italic', 'oblique']
weights = ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']
font = {'fontproperties': font_family,  # 'family': 'Liberation Sans'
		'style': styles[0],
		'color': 'black',
		'weight': weights[1],
		'size': 20.0, }

char_system = "/"
##################### 按x从小到大对数据进行重新分类。 ########################
def x_judge(data=np.array([]), sec=20):
	data = data[np.argsort(data[:, 0])]
	pre_x = data[0, 0]
	index = 1
	length = (data[-1, 0] - data[0, 0]) * 1/sec
	length_judge = 10 * abs(data[1, 0]-data[0, 0]) + length
	for i in range(1, len(data[:, 0])):
		if data[i, 0] - pre_x > length_judge:
			index = index + 1
		length_judge = abs(data[i, 0] - pre_x) * 5 + length
		pre_x = data[i, 0]
	data_all_x = [[] for i in range(0, index)]
	data_all_y = [[] for i in range(0, index)]
	index_j = 1
	pre_x = data[0, 0]
	length_judge = 10 * abs(data[1, 0]-data[0, 0]) + length
	for j in range(0, len(data[:, 0])):
		if data[j, 0] - pre_x > length_judge:
			index_j = index_j + 1
		length_judge = abs(data[j, 0] - pre_x) * 5 + length
		data_all_x[index_j-1].append(data[j, 0])
		data_all_y[index_j-1].append(data[j, 1])
		pre_x = data[j, 0]
	data_all = [[] for i in range(0, index)]
	for k in range(0, index):
		data_all_1 = [[] for i in range(0, 2)]
		for h in range(0, len(data_all_x[k])):
			data_all_1[0].append(data_all_x[k][h])
			data_all_1[1].append(data_all_y[k][h])
		data_all[k].append(data_all_1)
	return index, data_all

#################### x之后，按y从小到大对数据进行进一步的分类 ####################
def y_judge(data0=[], sec=20):
	data1 = np.zeros((len(data0[0]), 2))
	for i in range(0, len(data0[0])):
		data1[i, 0] = data0[0][i]
		data1[i, 1] = data0[1][i]
	data = data1[np.argsort(data1[:, 1])]
	pre_y = data[0, 1]
	index = 1
	length = (data[-1, 1] - data[0, 1]) * 1/sec
	length_judge = 10 * abs(data[1, 1]-data[0, 1]) + length
	for i in range(1, len(data[:, 1])):
		if data[i, 1] - pre_y > length_judge:
			index = index + 1
		length_judge = abs(data[i, 1] - pre_y) * 5 + length
		pre_y = data[i, 1]
	data_all_x = [[] for i in range(0, index)]
	data_all_y = [[] for i in range(0, index)]
	index_j = 1
	pre_y = data[0, 1]
	length_judge = 10 * abs(data[1, 1]-data[0, 1]) + length
	for j in range(0, len(data[:, 1])):
		if data[j, 1] - pre_y > length_judge:
			index_j = index_j + 1
		length_judge = abs(data[j, 1] - pre_y) * 5 + length
		data_all_x[index_j-1].append(data[j, 0])
		data_all_y[index_j-1].append(data[j, 1])
		pre_y = data[j, 1]
	data_all = [[] for i in range(0, index)]
	for k in range(0, index):
		data_all_1 = [[] for i in range(0, 2)]
		for h in range(0, len(data_all_x[k])):
			data_all_1[0].append(data_all_x[k][h])
			data_all_1[1].append(data_all_y[k][h])
		data_all[k].append(data_all_1)
	return index, data_all

################### 判定圈的个数并对数据进行整合 #################################
def xy_judge(data=np.array([]), sec=20):
	index, data_all_x = x_judge(data, sec)
	index_all = 0
	for i in range(0, index):
		index_2, data_all_temp1 = y_judge(data_all_x[i][0], sec)
		index_all = index_all + index_2
	data_all = [[] for i in range(0, index_all)]
	index_use = 0
	for j in range(0, index):
		index_1, data_all_1 = y_judge(data_all_x[j][0], sec)
		for k in range(0, index_1):
			data_all_temp = [[] for i in range(0, 2)]
			for h in range(0, len(data_all_1[k][0][0])):
				data_all_temp[0].append(data_all_1[k][0][0][h])
				data_all_temp[1].append(data_all_1[k][0][1][h])
			data_all[k+index_use].append(data_all_temp)
		index_use = index_1 + index_use
	return index_all, data_all

################# 积分 ####################################
def interpolate_data(x, y, numbers=10001):
	x1 = np.linspace(min(x), max(x), numbers)
	func = interpolate.interp1d(x[:], y[:], kind='linear')
	y1 = func(x1)
	y2 = np.linspace(min(y1), max(y1), numbers * 2)
	func2 = interpolate.interp1d(y1[:], x1[:], kind='linear')
	x2 = func2(y2)
	x3 = np.linspace(min(x2), max(x2), numbers * 3)
	func3 = interpolate.interp1d(x2[:], y2[:], kind='linear')
	y3 = func3(x3)
	y4 = np.linspace(min(y3), max(y3), numbers * 4)
	func4 = interpolate.interp1d(y3[:], x3[:], kind='linear')
	x4 = func4(y4)
	x_min = min(x4)
	x_max = max(x4)
	y_min = min(y4)
	y_max = max(y4)
	x4 = list(x4)
	y4 = list(y4)
	for i in range(0, len(x)):
		x4.append(x[i])
		y4.append(y[i])
	length_l = np.sqrt((x_max - x_min) ** 2 + (y_max - y_min) ** 2)/np.sqrt(numbers * 4)
	return x4, y4, length_l

def integrals_mtkg(x, y, numbers=100):
	x1, y1, ll = interpolate_data(x, y, numbers)
	x_min = min(x1)
	y_min = min(y1)
	x_max = max(x1)
	y_max = max(y1)
	x2 = np.random.random(numbers) * (x_max - x_min) + x_min
	y2 = np.random.random(numbers) * (y_max - y_min) + y_min
	Area_s = (x_max - x_min) * (y_max - y_min)
	count = 0
	for i in range(0, len(x2)):
		marker_count = 0
		for j in range(0, len(x1)):
			if np.sqrt((x2[i]-x1[j]) ** 2 + (y2[i] - y1[j]) ** 2) <= ll:
				marker_count = 1
				break
		if marker_count == 1:
			count = count + 1
	integrals = Area_s * count / (numbers)
	return Area_s, integrals

def zhi_xin(x=[], y=[]):
	x1 = 1/2 * (max(x) - min(x)) + min(x)
	y1 = 1/2 * (max(y) - min(y)) + min(y)
	return x1, y1

################### the entrance for all the calculations ##############################################################
def get_filepath(filepath="./"):
	curPath = filepath
	# dirs = [dirs for dirs, file, name in os.walk(filepath)]
	dirs = [name for name in os.listdir(curPath) if os.path.isdir(os.path.join(curPath, name))]
	dir_file = []
	for flag_file in dirs:
		if flag_file != './idea' and flag_file != './__pycache__':
			dir_file.append(curPath + char_system + flag_file + char_system)
	return dir_file
def plot_bz(fontsize=16):
	import fermi as fe
	bz_name, fermi_name = fe.get_filename()
	fe.plot_band("fermi_surface", 400, fontpath, fontsize)
	return bz_name, fermi_name
def data_solve_single(sec=20, numbers=100, fontsize=16, kz=""):
	bz_name, fermi_name = plot_bz(fontsize)
	# kz = get_kz()
	data = np.loadtxt(fermi_name, dtype=np.float64)
	index, data2 = xy_judge(data, sec)
	color = ["red", "blue", "black", "pink", "cyan", "gray", "orange", "green", "purple", "navy", "teal", "lime", "yellow", "indigo", "olive", "Gold", "cornislk", "wheat", "peru", "linen", "chocolate", "brown", "tomato", "tan", "maroon", "coral"]
	integral = []
	Area_s = []
	#import re
	#p = re.compile(r'([\d].[\d]+)\.dat')
	ax = plt.subplot(121)
	for i1 in range(0, index):
		ax.scatter(data2[i1][0][0], data2[i1][0][1], s=0.5)
	ax.set_title("k$_z$ = " + kz, fontsize=fontsize, color="red", fontdict=font)
	ax2 = plt.subplot(122)
	for i2 in range(0, index):
		x1, y1, length_l = interpolate_data(data2[i2][0][0], data2[i2][0][1])
		ax2.scatter(x1, y1, s=0.5)
	ax2.set_title("k$_z$ = " + kz, fontsize=fontsize, color="red", fontdict=font)
	plt.savefig("test.png", dpi=300)
	ax3 = plt.subplot(111)
	for i in range(0, index):
		ax3.scatter(data2[i][0][0], data2[i][0][1], color=color[i], s=0.5)
		area, integra = integrals_mtkg(data2[i][0][0], data2[i][0][1], numbers)
		integral.append(integra)
		Area_s.append(area)
		# Area_o.append(areao)
		x1, y1 = zhi_xin(data2[i][0][0], data2[i][0][1])
		ax3.text(x1, y1, round(integra, 5), color="k", fontdict=font)
	ax3.set_title("k$_z$ = " + kz, color="red", fontdict=font)
	ax3.set_xlabel("Sum_Integrals = " + str(round(sum(integral), 5)), color="blue", fontdict=font)
	ax3.set_ylabel("ky", color="blue", fontdict=font)
	print(Area_s)
	print(integral)
	plt.savefig("Integral.png", dpi=300)
	return integral

def manipulate_single(filename="001FM", band_index=0, kz=0, sec=20, numbers=100, fontsize=16):
	filepath0 = os.getcwd()
	path = filepath0 + char_system + filename + char_system + str(band_index) + char_system + "kz=" + str(kz)
	os.chdir(path)
	print(path)
	intergal = data_solve_single(sec, numbers, fontsize, kz)
	os.chdir(filepath0)
def manipulate_part(filename="001FM", band_index=0, sec=20, numbers=100, fontsize=16):
	filepath0 = os.getcwd()
	path = filepath0 + char_system + filename + char_system + str(band_index)
	filepath_kz = get_filepath(path)
	for kz_path in filepath_kz:
		os.chdir(kz_path)
		print(kz_path)
		kz = kz_path.split(char_system)[-2].split("=")[-1]
		intergal = data_solve_single(sec, numbers, fontsize, kz)
	os.chdir(filepath0)
def manipulate_all(sec=20, numbers=100, fontsize=16):
	filepath0 = os.getcwd()
	filepath = get_filepath(filepath0)
	for path in filepath:
		filepath_band = get_filepath(path)
		for band_path in filepath_band:
			filepath_kz = get_filepath(band_path)
			for kz_path in filepath_kz:
				os.chdir(kz_path)
				print(kz_path)
				kz = kz_path.split(char_system)[-2].split("=")[-1]
				intergal = data_solve_single(sec, numbers, fontsize, kz)
	os.chdir(filepath0)

if __name__=='__main__':
	fontsize = 16
	# index = 10          ###### 文件指标
	sec = 10            ###### sec for judge
	numbers = 9001     ###### 定义插点密度
	########## plot single ###############
	filetype = ["mag0.0", "mag0.5", "mag1.0", "mag1.5"]
	filetype = ["mag2.0", "mag2.5"]
	band_index = 0
	band_index_all = [1, 2, 3]
	kz_0 = ["0.44"]
	kz_1 = ["0.08"]
	kz_2 = ["0.28"]
	#kz_3 = ["0.36"]
	######################################
	#print(get_kz())
	#for ll in kz_0:
	#	manipulate_single(filetype, 0, ll, 3, numbers, fontsize)
	#manipulate_part(filetype, 1, 15, numbers, fontsize)
	#for ls in kz_1:
	#	manipulate_single(filetype, 1, ls, 6.5, numbers, fontsize)
	#for lll in kz_2:
	#	manipulate_single(filetype, 2, lll, 3, numbers, fontsize)
	#for lls in kz_3:
	#	manipulate_single(filetype, 3, lls, 12, numbers, fontsize)
	#manipulate_single(filetype, band_index, "0.00001", sec, numbers, fontsize)
	for file in filetype:
		for band_index in range(2):
			manipulate_part(file, band_index, sec, numbers, fontsize)
	for file1 in filetype1:
		manipulate_part(file1, 1, 8, numbers, fontsize)
	# for f in band_index_all:
	# 	manipulate_part(filetype, f, sec, numbers, fontsize)
	############ plot all ################
	#manipulate_all(sec, numbers, fontsize)
