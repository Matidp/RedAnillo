import matplotlib.pylab as plt
import numpy as np
import matplotlib as mpl
import pandas
import seaborn
import csv
import scipy.interpolate as intp
import copy

# Funciones de Parseo
def parsear_todo():

	data = {
		"base" : parsear_caso("base"),
		"menorcam" : parsear_caso("menorcam"),
		"alter" : parsear_caso("alter")
	}
	
	return data

def parsear_caso(modo):

	data = {
		"caso1" : parsear_escenario(modo, "caso1"),
		"caso2" : parsear_escenario(modo, "caso2")
	}
	return data

def parsear_escenario(modo, caso):

	data = {
		"0.1": parsear_archivo(caso,"nuevas/"+modo+"/"+caso+"/"+"0,1.csv"),
		"3.5": parsear_archivo(caso,"nuevas/"+modo+"/"+caso+"/"+"3,5.csv"),
		"1": parsear_archivo(caso,"nuevas/"+modo+"/"+caso+"/"+"1.csv"),
		"2": parsear_archivo(caso,"nuevas/"+modo+"/"+caso+"/"+"2.csv"),
		"7": parsear_archivo(caso,"nuevas/"+modo+"/"+caso+"/"+"7.csv")
	}
	

	return data

def parsear_archivo(caso, file, tres=False):

	def parsear_nodo(nodo, file):
		data = pandas.read_csv(file, encoding = 'utf8')

		base = 20
		if caso is "caso2":
			base = 35		

		if nodo in [5]:

			time_gdelay = data['vectime'].loc[[(base + nodo*6)]].tolist()
			gdelay = data['vecvalue'].loc[[(base + nodo*6)]].tolist()

			time_conn0 = data['vectime'].loc[[(base + nodo*6)+1]].tolist()
			conn0 = data['vecvalue'].loc[[(base + nodo*6)+1]].tolist()

			time_conn1 = data['vectime'].loc[[(base + nodo*6)+2]].tolist()
			conn1 = data['vecvalue'].loc[[(base + nodo*6)+2]].tolist()

			time_conn2 = data['vectime'].loc[[(base + nodo*6)+3]].tolist()
			conn2 = data['vecvalue'].loc[[(base + nodo*6)+3]].tolist()

			time_conn3 = data['vectime'].loc[[(base + nodo*6)+4]].tolist()
			conn3 = data['vecvalue'].loc[[(base + nodo*6)+4]].tolist()

			time_conn4 = data['vectime'].loc[[(base + nodo*6)+5]].tolist()
			conn4 = data['vecvalue'].loc[[(base + nodo*6)+5]].tolist()

			time_conn6 = data['vectime'].loc[[(base + nodo*6)+6]].tolist()
			conn6 = data['vecvalue'].loc[[(base + nodo*6)+6]].tolist()

			time_conn7 = data['vectime'].loc[[(base + nodo*6)+7]].tolist()
			conn7 = data['vecvalue'].loc[[(base + nodo*6)+7]].tolist()
					
			time_hopc = data['vectime'].loc[[(base + nodo*6)+8]].tolist()
			hopc = data['vecvalue'].loc[[(base + nodo*6)+8]].tolist()

			time_source = data['vectime'].loc[[(base + nodo*6)+9]].tolist()
			source = data['vecvalue'].loc[[(base + nodo*6)+9]].tolist()

			time_pktp = data['vectime'].loc[[(base + nodo*6)+10]].tolist()
			pktp = data['vecvalue'].loc[[(base + nodo*6)+10]].tolist()


			time_buf0 = data['vectime'].loc[[(base + nodo*6)+11]].tolist()
			buf0 = data['vecvalue'].loc[[(base + nodo*6)+11]].tolist()

			time_buf1 = data['vectime'].loc[[(base + nodo*6)+12]].tolist()
			buf1 = data['vecvalue'].loc[[(base + nodo*6)+12]].tolist()

			time_hopc = list(map(float,time_hopc[0].split()))
			time_source = list(map(float,time_source[0].split()))
			time_gdelay = list(map(float,time_gdelay[0].split()))
			time_buf0 = list(map(float,time_buf0[0].split()))
			time_buf1 = list(map(float,time_buf1[0].split()))
			time_pktp = list(map(float,time_pktp[0].split()))
			
			hopc = list(map(float,hopc[0].split()))
			source = list(map(float,source[0].split()))
			gdelay = list(map(float,gdelay[0].split()))
			buf0 = list(map(float,buf0[0].split()))
			buf1 = list(map(float,buf1[0].split()))
			pktp = list(map(float,pktp[0].split()))

			time_conn0 = list(map(float,time_conn0[0].split()))
			time_conn1 = list(map(float,time_conn1[0].split()))
			time_conn2 = list(map(float,time_conn2[0].split()))
			time_conn3 = list(map(float,time_conn3[0].split()))
			time_conn4 = list(map(float,time_conn4[0].split()))
			time_conn6 = list(map(float,time_conn6[0].split()))
			time_conn7 = list(map(float,time_conn7[0].split()))
			
			conn0 = list(map(float,conn0[0].split()))
			conn1 = list(map(float,conn1[0].split()))
			conn2 = list(map(float,conn2[0].split()))
			conn3 = list(map(float,conn3[0].split()))
			conn4 = list(map(float,conn4[0].split()))
			conn6 = list(map(float,conn6[0].split()))
			conn7 = list(map(float,conn7[0].split()))
			
			return {
				"time_buf0" : time_buf0,
				"time_buf1" : time_buf1,
				"time_pktp" : time_pktp,
				"time_gdelay" : time_gdelay,
				"time_hopc" : time_hopc,
				"time_source" : time_source,
				"time_conn0": time_conn0,
				"time_conn1": time_conn1,
				"time_conn2": time_conn2,
				"time_conn3": time_conn3,
				"time_conn4": time_conn4,
				"time_conn6": time_conn6,
				"time_conn7": time_conn7,
				"conn0": conn0,
				"conn1": conn1,
				"conn2": conn2,
				"conn3": conn3,
				"conn4": conn4,
				"conn6": conn6,
				"conn7": conn7,
				"buf0" : buf0,
				"buf1" : buf1,
				"pktp" : pktp,
				"gdelay" : gdelay,
				"hopc" : hopc,
				"source" : source
			}

	
		elif nodo in [6, 7]:

			time_gdelay = data['vectime'].loc[[(base + nodo*6)+7]].tolist()
			gdelay = data['vecvalue'].loc[[(base + nodo*6)+7]].tolist()

			time_hopc = data['vectime'].loc[[(base + nodo*6)+8]].tolist()
			hopc = data['vecvalue'].loc[[(base + nodo*6)+8]].tolist()

			time_source = data['vectime'].loc[[(base + nodo*6)+9]].tolist()
			source = data['vecvalue'].loc[[(base + nodo*6)+9]].tolist()

			time_pktp = data['vectime'].loc[[(base + nodo*6)+10]].tolist()
			pktp = data['vecvalue'].loc[[(base + nodo*6)+10]].tolist()


			time_buf0 = data['vectime'].loc[[(base + nodo*6)+11]].tolist()
			buf0 = data['vecvalue'].loc[[(base + nodo*6)+11]].tolist()

			time_buf1 = data['vectime'].loc[[(base + nodo*6)+12]].tolist()
			buf1 = data['vecvalue'].loc[[(base + nodo*6)+12]].tolist()

		else:

			time_gdelay = data['vectime'].loc[[(base + nodo*6)]].tolist()
			gdelay = data['vecvalue'].loc[[(base + nodo*6)]].tolist()

			time_hopc = data['vectime'].loc[[(base + nodo*6)+1]].tolist()
			hopc = data['vecvalue'].loc[[(base + nodo*6)+1]].tolist()

			time_source = data['vectime'].loc[[(base + nodo*6)+2]].tolist()
			source = data['vecvalue'].loc[[(base + nodo*6)+2]].tolist()

			time_pktp = data['vectime'].loc[[(base + nodo*6)+3]].tolist()
			pktp = data['vecvalue'].loc[[(base + nodo*6)+3]].tolist()

			time_buf0 = data['vectime'].loc[[(base + nodo*6)+4]].tolist()
			buf0 = data['vecvalue'].loc[[(base + nodo*6)+4]].tolist()

			time_buf1 = data['vectime'].loc[[(base + nodo*6)+5]].tolist()
			buf1 = data['vecvalue'].loc[[(base + nodo*6)+5]].tolist()


		time_hopc = list(map(float,time_hopc[0].split()))
		time_source = list(map(float,time_source[0].split()))
		time_gdelay = list(map(float,time_gdelay[0].split()))
		time_buf0 = list(map(float,time_buf0[0].split()))
		time_buf1 = list(map(float,time_buf1[0].split()))
		time_pktp = list(map(float,time_pktp[0].split()))
		
		hopc = list(map(float,hopc[0].split()))
		source = list(map(float,source[0].split()))
		gdelay = list(map(float,gdelay[0].split()))
		buf0 = list(map(float,buf0[0].split()))
		buf1 = list(map(float,buf1[0].split()))
		pktp = list(map(float,pktp[0].split()))
		
		return {
			"time_buf0" : time_buf0,
			"time_buf1" : time_buf1,
			"time_pktp" : time_pktp,
			"time_gdelay" : time_gdelay,
			"time_hopc" : time_hopc,
			"time_source" : time_source,
			"buf0" : buf0,
			"buf1" : buf1,
			"pktp" : pktp,
			"gdelay" : gdelay,
			"hopc" : hopc,
			"source" : source
		}
	
	data = {}
	for i in range(8):
		data["nodo"+str(i)] = parsear_nodo(i, file)
	
	return data



def parsear_archivo2(caso, file, tres=False):

	def parsear_nodo(nodo, file):
		data = pandas.read_csv(file, encoding = 'utf8')

		base = 20
		params = 5
		if caso is "caso2":
			base = 35		

		if nodo in [5]:

			time_gdelay = data['vectime'].loc[[(base + nodo*params)]].tolist()
			gdelay = data['vecvalue'].loc[[(base + nodo*params)]].tolist()

			time_conn0 = data['vectime'].loc[[(base + nodo*params)+1]].tolist()
			conn0 = data['vecvalue'].loc[[(base + nodo*params)+1]].tolist()

			time_conn1 = data['vectime'].loc[[(base + nodo*params)+2]].tolist()
			conn1 = data['vecvalue'].loc[[(base + nodo*params)+2]].tolist()

			time_conn2 = data['vectime'].loc[[(base + nodo*params)+3]].tolist()
			conn2 = data['vecvalue'].loc[[(base + nodo*params)+3]].tolist()

			time_conn3 = data['vectime'].loc[[(base + nodo*params)+4]].tolist()
			conn3 = data['vecvalue'].loc[[(base + nodo*params)+4]].tolist()

			time_conn4 = data['vectime'].loc[[(base + nodo*params)+5]].tolist()
			conn4 = data['vecvalue'].loc[[(base + nodo*params)+5]].tolist()

			time_conn6 = data['vectime'].loc[[(base + nodo*params)+6]].tolist()
			conn6 = data['vecvalue'].loc[[(base + nodo*params)+6]].tolist()

			time_conn7 = data['vectime'].loc[[(base + nodo*params)+7]].tolist()
			conn7 = data['vecvalue'].loc[[(base + nodo*params)+7]].tolist()
					
			time_hopc = data['vectime'].loc[[(base + nodo*params)+8]].tolist()
			hopc = data['vecvalue'].loc[[(base + nodo*params)+8]].tolist()

			time_source = data['vectime'].loc[[(base + nodo*params)+9]].tolist()
			source = data['vecvalue'].loc[[(base + nodo*params)+9]].tolist()

			time_buf0 = data['vectime'].loc[[(base + nodo*params)+10]].tolist()
			buf0 = data['vecvalue'].loc[[(base + nodo*params)+10]].tolist()

			time_buf1 = data['vectime'].loc[[(base + nodo*params)+11]].tolist()
			buf1 = data['vecvalue'].loc[[(base + nodo*params)+11]].tolist()

			time_hopc = list(map(float,time_hopc[0].split()))
			time_source = list(map(float,time_source[0].split()))
			time_gdelay = list(map(float,time_gdelay[0].split()))
			time_buf0 = list(map(float,time_buf0[0].split()))
			time_buf1 = list(map(float,time_buf1[0].split()))
			
			hopc = list(map(float,hopc[0].split()))
			source = list(map(float,source[0].split()))
			gdelay = list(map(float,gdelay[0].split()))
			buf0 = list(map(float,buf0[0].split()))
			buf1 = list(map(float,buf1[0].split()))

			time_conn0 = list(map(float,time_conn0[0].split()))
			time_conn1 = list(map(float,time_conn1[0].split()))
			time_conn2 = list(map(float,time_conn2[0].split()))
			time_conn3 = list(map(float,time_conn3[0].split()))
			time_conn4 = list(map(float,time_conn4[0].split()))
			time_conn6 = list(map(float,time_conn6[0].split()))
			time_conn7 = list(map(float,time_conn7[0].split()))
			
			conn0 = list(map(float,conn0[0].split()))
			conn1 = list(map(float,conn1[0].split()))
			conn2 = list(map(float,conn2[0].split()))
			conn3 = list(map(float,conn3[0].split()))
			conn4 = list(map(float,conn4[0].split()))
			conn6 = list(map(float,conn6[0].split()))
			conn7 = list(map(float,conn7[0].split()))
			
			return {
				"time_buf0" : time_buf0,
				"time_buf1" : time_buf1,
				"time_gdelay" : time_gdelay,
				"time_hopc" : time_hopc,
				"time_source" : time_source,
				"time_conn0": time_conn0,
				"time_conn1": time_conn1,
				"time_conn2": time_conn2,
				"time_conn3": time_conn3,
				"time_conn4": time_conn4,
				"time_conn6": time_conn6,
				"time_conn7": time_conn7,
				"conn0": conn0,
				"conn1": conn1,
				"conn2": conn2,
				"conn3": conn3,
				"conn4": conn4,
				"conn6": conn6,
				"conn7": conn7,
				"buf0" : buf0,
				"buf1" : buf1,
				"gdelay" : gdelay,
				"hopc" : hopc,
				"source" : source
			}

	
		elif nodo in [6, 7]:

			time_gdelay = data['vectime'].loc[[(base + nodo*params)+7]].tolist()
			gdelay = data['vecvalue'].loc[[(base + nodo*params)+7]].tolist()

			time_hopc = data['vectime'].loc[[(base + nodo*params)+8]].tolist()
			hopc = data['vecvalue'].loc[[(base + nodo*params)+8]].tolist()

			time_source = data['vectime'].loc[[(base + nodo*params)+9]].tolist()
			source = data['vecvalue'].loc[[(base + nodo*params)+9]].tolist()

			time_buf0 = data['vectime'].loc[[(base + nodo*params)+10]].tolist()
			buf0 = data['vecvalue'].loc[[(base + nodo*params)+10]].tolist()

			time_buf1 = data['vectime'].loc[[(base + nodo*params)+11]].tolist()
			buf1 = data['vecvalue'].loc[[(base + nodo*params)+11]].tolist()

		else:

			time_gdelay = data['vectime'].loc[[(base + nodo*params)]].tolist()
			gdelay = data['vecvalue'].loc[[(base + nodo*params)]].tolist()

			time_hopc = data['vectime'].loc[[(base + nodo*params)+1]].tolist()
			hopc = data['vecvalue'].loc[[(base + nodo*params)+1]].tolist()

			time_source = data['vectime'].loc[[(base + nodo*params)+2]].tolist()
			source = data['vecvalue'].loc[[(base + nodo*params)+2]].tolist()

			time_buf0 = data['vectime'].loc[[(base + nodo*params)+3]].tolist()
			buf0 = data['vecvalue'].loc[[(base + nodo*params)+3]].tolist()

			time_buf1 = data['vectime'].loc[[(base + nodo*params)+4]].tolist()
			buf1 = data['vecvalue'].loc[[(base + nodo*params)+4]].tolist()


		time_hopc = list(map(float,time_hopc[0].split()))
		time_source = list(map(float,time_source[0].split()))
		time_gdelay = list(map(float,time_gdelay[0].split()))
		time_buf0 = list(map(float,time_buf0[0].split()))
		time_buf1 = list(map(float,time_buf1[0].split()))
		
		hopc = list(map(float,hopc[0].split()))
		source = list(map(float,source[0].split()))
		gdelay = list(map(float,gdelay[0].split()))
		buf0 = list(map(float,buf0[0].split()))
		buf1 = list(map(float,buf1[0].split()))
		
		return {
			"time_buf0" : time_buf0,
			"time_buf1" : time_buf1,
			"time_gdelay" : time_gdelay,
			"time_hopc" : time_hopc,
			"time_source" : time_source,
			"buf0" : buf0,
			"buf1" : buf1,
			"gdelay" : gdelay,
			"hopc" : hopc,
			"source" : source
		}
	
	data = {}
	for i in range(8):
		data["nodo"+str(i)] = parsear_nodo(i, file)
	
	return data
