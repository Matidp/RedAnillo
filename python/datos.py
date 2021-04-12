import matplotlib.pylab as plt
import numpy as np
import matplotlib as mpl
import pandas
import seaborn
import csv
import scipy.interpolate as intp
import copy
import mparser

t_conns = ["time_conn0","time_conn1","time_conn2","time_conn3","time_conn4","time_conn6","time_conn7"]

connections = ["conn0","conn1","conn2","conn3","conn4","conn6","conn7"]

colors = ["tab:blue", "tab:green", "tab:brown", "tab:orange", "tab:red", "tab:purple", "peru"]

modelos = ["base", "menorcam", "alter"]

casos = ["caso1", "caso2"]

flatui = ["#9b59b6", "#3498db","#f4a80b", "#95a5a6", "#e74c3c", "#14398e", "#2ecc71", "#4f4f4f"]

escenarios2 = [ "1", "2", "3.5", "7"]

escenarios = ["1", "2", "3.5", "7"]

paletas = ["rocket", "vlag", "deep", "Blues_d", "salmon"]

nodos = ["nodo0", "nodo1", "nodo2", "nodo3", "nodo4", "nodo5", "nodo6", "nodo7"]

metricas = ["buf0",	"buf1",	"pktp",	"gdelay", "hopc", "source"]
other_met = ["hopc", "source"]
metr_raw = ["buf0",	"buf1",	"gdelay", "pktp"]
metr_pkt = ["buf0",	"buf1",	"pktp"]

maxvemi = {"1": 100, "2": 65, "3.5": 64, "7": 35}
maxvhop = {"1": 192, "2": 127, "3.5": 109, "7": 60}

titulos = {
	"base": "Caso Base",
	"menorcam": "algo menorcamino",
	"alter": "algoritmo alternante",
	"source": "Nodo Emisor",
	"hopc": "Cantidad de Saltos",
	"buf0": "Buffer Izquierdo",
	"buf1": "Buffer Derecho",
	"delay": "Tiempo de Retardo",
	"pktp": "Paquetes Procesados",
	"nodo0": "Nodo 0",
	"nodo1": "Nodo 1",
	"nodo2": "Nodo 2",
	"nodo3": "Nodo 3",
	"nodo4": "Nodo 4",
	"nodo5": "Nodo 5",
	"nodo6": "Nodo 6",
	"nodo7": "Nodo 7",
	"conn0": "Conexión 0",
	"conn1": "Conexión 1",
	"conn2": "Conexión 2",
	"conn3": "Conexión 3",
	"conn4": "Conexión 4",
	"conn6": "Conexión 6",
	"conn7": "Conexión 7",
	"0.1": "ArrivalTime 0.1", 
	"1": "ArrivalTime 1", 
	"3.5": "ArrivalTime 3.5", 
	"2": "ArrivalTime 2", 
	"7": "ArrivalTime 7", 
	"caso1": "Caso 1",
	"caso2": "Caso 2"
}



vectores = mparser.parsear_todo()

def ocurrencias(mod,caso,esc,nodo,metr):
	target = vectores[mod][caso][esc][nodo][metr]
	ans = {}

	if metr == "hopc":
		for i in range(1,9):
			if mod in ["menorcam"]:
				ans[i] = target.count(i-1)
			else:
				ans[i] = target.count(i)
	else:
		for i in range(8):
			ans[i] = target.count(i)
	return ans


def valores_finales():

	ans = copy.deepcopy(vectores)
	for mod in vectores.keys():
		for caso in vectores[mod].keys():
			for esc in vectores[mod][caso].keys():
				for nodo in vectores[mod][caso][esc].keys():
					for met in metr_raw:
						ans[mod][caso][esc][nodo][met] = vectores[mod][caso][esc][nodo][met][-1]
	return ans

def valores_maximos(): 
	ans = copy.deepcopy(vectores)
	
	for mod in vectores.keys():
		for caso in vectores[mod].keys():
			for esc in vectores[mod][caso].keys():
				for nodo in vectores[mod][caso][esc].keys():
					for met in metr_raw:
						ans[mod][caso][esc][nodo][met] = max(vectores[mod][caso][esc][nodo][met])
	return ans

def valores_promedio():
	ans = copy.deepcopy(vectores)

	for mod in vectores.keys():
		for caso in vectores[mod].keys():
			for esc in vectores[mod][caso].keys():
				for nodo in vectores[mod][caso][esc].keys():
					for met in metr_raw:
						ans[mod][caso][esc][nodo][met] = sum(vectores[mod][caso][esc][nodo][met]) / len(vectores[mod][caso][esc][nodo][met])

	return ans


#finales = valores_finales()
maximos = valores_maximos()
promedios = valores_promedio()


## Graficos


def gdelay_por_escenario(modo, caso, log=False, interp=0, title=""):

	fig, axs = plt.subplots(figsize=(10,10)) #creo una figura y divido en pares para dibujar

	plt.axis('equal')
	axs.set_ylim(bottom=0, top=200)
	
	plt.title("Retardo General. "+titulos[modo]+", "+titulos[caso])
	for i in range(len(escenarios)):
		fx = vectores[modo][caso][escenarios[i]]["nodo5"]["time_gdelay"]
		fy = vectores[modo][caso][escenarios[i]]["nodo5"]["gdelay"]
		if interp != 0:
			linsp = np.linspace(1, 200, interp)
			yinterp = np.interp(linsp, fx, fy)
			axs.plot(linsp,yinterp, color=colors[i], label=titulos[escenarios[i]])
		else:
			axs.plot(fx,fy, color=colors[i], label=titulos[escenarios[i]])
	if log:
		plt.yscale('log')
	plt.xlabel("Tiempo de simulacion (seg)")
	plt.ylabel("Retardo (segundos)")
	plt.legend()
	
	plt.show

def delay_por_conexion(modo, caso, esc, log=False, interp=0, title=""):

	fig, axs = plt.subplots(figsize=(10,10)) #creo una figura y divido en pares para dibujar
	plt.axis('equal')
	axs.set_ylim(bottom=0, top=200)
	
	plt.title("Retardo de cada Conexion. "+titulos[modo]+", "+titulos[caso]+", "+titulos[esc])
	for i in range(len(connections)):
		fx = vectores[modo][caso][esc]["nodo5"][t_conns[i]]
		fy = vectores[modo][caso][esc]["nodo5"][connections[i]]
		if interp != 0:
			linsp = np.linspace(1, 200, interp)
			yinterp = np.interp(linsp, fx, fy)
			axs.plot(linsp,yinterp, color=colors[i], label=titulos[connections[i]])
		else:
			axs.plot(fx,fy, color=colors[i], label=titulos[connections[i]])
	if log:
		plt.yscale('log')
	plt.xlabel("Tiempo de simulacion (seg)")
	plt.ylabel("Retardo (segundos)")
	plt.legend()
	
	plt.show

def comp_delay_por_conexion(modo, caso, log=False, interp=0, title=""):
	fig, axs = plt.subplots(1, len(escenarios2), figsize=(8*len(escenarios2),8)) #creo una figura y divido en pares para dibujar
	plt.axis('equal')
	
	fig.suptitle("Retardo de cada Conexion. "+titulos[modo]+", "+titulos[caso], fontsize=24)

	for j in range(len(escenarios2)):
		axs[j].set_ylim(bottom=0, top=200)

		for i in range(len(connections)):
			fx = vectores[modo][caso][escenarios2[j]]["nodo5"][t_conns[i]]
			fy = vectores[modo][caso][escenarios2[j]]["nodo5"][connections[i]]
			if interp != 0:
				linsp = np.linspace(1, 200, interp)
				yinterp = np.interp(linsp, fx, fy)
				axs[j].plot(linsp,yinterp, color=colors[i], label=titulos[connections[i]])
			else:
				axs[j].plot(fx,fy, color=colors[i], label=titulos[connections[i]])
		axs[j].set_title(titulos[escenarios2[j]])
		plt.xlabel("Tiempo de simulacion (seg)")
		plt.ylabel("Retardo (segundos)")
	
	if log:
		plt.yscale('log')
	plt.legend()
	
	plt.show


def algorithm_ocurs(mod, caso, esc, metr):
	fig, ax = plt.subplots( figsize=(6, 6))


	tar =  ocurrencias(mod,caso,esc,"nodo5",metr)
	lists = sorted(tar.items()) # sorted by key, return a list of tuples
	x, y = zip(*lists) # unpack a list of pairs into two tuples

	df = pandas.DataFrame({
		titulos[metr]: x,
		"Ocurrencias": y
	})

	graph = seaborn.barplot(x=titulos[metr], y="Ocurrencias", data = df, ax=ax)

	if metr == "hopc":
		for k in range(8):
			graph.text(x[k]-1,max(y[k], 0),y[k], ha='center')
	else:
		for k in range(8):
			graph.text(x[k],max(y[k], 0),y[k], ha='center')


	fig.suptitle(titulos[mod]+", "+titulos[caso]+", "+titulos[esc])
	fig.tight_layout(rect=[0, 0.03, 1, 0.95])
	seaborn.despine(top=True)

def comp_esc_ocurs(mod, caso, metr):
	fig, ax = plt.subplots(1,len(escenarios2), figsize=(6*len(escenarios2), 6))

	fig.suptitle(titulos[metr]+". "+titulos[mod]+", "+titulos[caso], fontsize=24)
	maxv = 0

	for j in range(len(escenarios2)):
		tar =  ocurrencias(mod,caso,escenarios2[j],"nodo5",metr)
		lists = sorted(tar.items()) # sorted by key, return a list of tuples
		x, y = zip(*lists) # unpack a list of pairs into two tuples
		maxv = max(maxv, max(y))
		df = pandas.DataFrame({
			titulos[metr]: x,
			"Ocurrencias": y
		})

		graph = seaborn.barplot(x=titulos[metr], y="Ocurrencias", data = df, ax=ax[j])
		ax[j].set_title(titulos[escenarios2[j]])
		ax[j].set_ylim(bottom=0, top=maxv)
		if metr == "hopc":
			for k in range(8):
				graph.text(x[k]-1,max(y[k], 0),y[k], ha='center')
		else:
			for k in range(8):
				graph.text(x[k],max(y[k], 0),y[k], ha='center')

	fig.tight_layout(rect=[0, 0.03, 1, 0.95])
	seaborn.despine(top=True)


def compare_algorithms_ocurs(caso, esc, metr):
	fig, ax = plt.subplots(1,3, figsize=(20, 6))

	for i,mod in enumerate(modelos):
		tar =  ocurrencias(mod,caso,esc,"nodo5",metr)
		lists = sorted(tar.items()) # sorted by key, return a list of tuples
		x, y = zip(*lists) # unpack a list of pairs into two tuples

		df = pandas.DataFrame({
			titulos[metr]: x,
			"Ocurrencias": y
		})

		graph = seaborn.barplot(x=titulos[metr], y="Ocurrencias", data = df, ax=ax[i], palette=seaborn.color_palette("Set2"))

		if metr == "hopc":
			for k in range(8):
				graph.text(x[k]-1,max(y[k], 0),y[k], ha='center')
		else:
			for k in range(8):
				graph.text(x[k],max(y[k], 0),y[k], ha='center')
		ax[i].set_title(titulos[mod])
		if metr == "source":
			ax[i].set_ylim(bottom=0, top=maxvemi[esc])
		else:
			ax[i].set_ylim(bottom=0, top=maxvhop[esc])


	fig.suptitle("Caso: "+titulos[caso]+", Escenario: "+titulos[esc]+", nodo: "+titulos["nodo5"], fontsize=30)
	fig.tight_layout(rect=[0, 0.03, 1, 0.95])
	seaborn.despine(top=True)



def test_jointplot():
	
	x = vectores["base"]["caso1"]["1"]["nodo5"]["time_gdelay"]
	y = vectores["base"]["caso1"]["1"]["nodo5"]["gdelay"]
	df = pandas.DataFrame({
			"x": x,
			"y": y
		})


	seaborn.jointplot("x", "y", data=df, kind="hex")

def ocupacion_buffers(model, caso, esc):
	
	fig, ax = plt.subplots(figsize=(7, 7))

	values = []
	lmetr = []
	lnodes = []

	#for nodo in nodos:
	#	values.append(maximos[model][caso][esc][nodo]["pktp"])
	#	lmetr.append("pktp")
	#	lnodes.append(nodo)

	for i in range(len(nodos)):
		values.append(maximos[model][caso][esc][nodos[i]]["buf0"])
		lmetr.append(titulos["buf0"])
		lnodes.append(i)

	for i in range(len(nodos)):
		values.append(maximos[model][caso][esc][nodos[i]]["buf1"])
		lmetr.append(titulos["buf1"])
		lnodes.append(i)



	df = pandas.DataFrame({
		"Nodo": lnodes,
		"Cant. Paquetes": values,
		"metricas": lmetr
	})
	
	seaborn.barplot(x = 'Nodo', y = 'Cant. Paquetes', hue = 'metricas', data = df)
	fig.tight_layout(rect=[0, 0.03, 1, 0.95])
	seaborn.despine(top=True)



def comp_ocupacion_buffers(model, caso):
	fig, ax = plt.subplots(1,len(escenarios2), figsize=(9*len(escenarios2), 7))

	fig.suptitle("Ocupación de los Buffers. "+titulos[model]+", "+titulos[caso], fontsize=24)

	vmax = 0

	for j,esc in enumerate(escenarios2):

		maxs = []
		proms = []
		lmetr = []
		lmetr2 = []
		lnodes = []

		for i in range(len(nodos)):
			vmax = max(vmax, maximos[model][caso][esc][nodos[i]]["buf0"])
			maxs.append(maximos[model][caso][esc][nodos[i]]["buf0"])
			proms.append(promedios[model][caso][esc][nodos[i]]["buf0"])
			lmetr.append("Buf 0, Máximo")
			lmetr2.append("Buf 0, Promedio")

			lnodes.append(i)

		for i in range(len(nodos)):
			vmax = max(vmax, maximos[model][caso][esc][nodos[i]]["buf1"])
			maxs.append(maximos[model][caso][esc][nodos[i]]["buf1"])
			proms.append(promedios[model][caso][esc][nodos[i]]["buf1"])
			lmetr.append("Buf 1, Máximo")
			lmetr2.append("Buf 1, Promedio")

			lnodes.append(i)

		df = pandas.DataFrame({
			"Nodo": lnodes,
			"Cant. Paquetes": proms,
			"maxs": maxs,
			"metricas1": lmetr,
			"metricas2": lmetr2
		})	
		graph =seaborn.barplot(x = 'Nodo', y = 'maxs', hue = 'metricas1', data = df,  ax=ax[j], palette="pastel")
		seaborn.barplot(x = 'Nodo', y = 'Cant. Paquetes', hue = 'metricas2', data = df,  ax=ax[j])
		ax[j].set_ylim(bottom=0, top=vmax)
		ax[j].set_title(titulos[esc])
		for p in graph.patches:
			height = p.get_height()
			if(height>1):
				graph.text(p.get_x()+p.get_width()/2., height + 0.1,"%.0f" %height ,ha="center")
		total = float(len(df))


	#fig.tight_layout(rect=[0, 0.03, 1, 0.95])
	seaborn.despine(top=True)

def comp_pkts_proc(model, caso):
	fig, ax = plt.subplots(1,len(escenarios2), figsize=(9*len(escenarios2), 7))

	fig.suptitle("Paquetes Procesados por Nodo. "+titulos[model]+", "+titulos[caso], fontsize=24)

	vmax = 0

	for j,esc in enumerate(escenarios2):

		pktp = []
		lnodes = []

		for i in range(len(nodos)):
			vmax = max(vmax, maximos[model][caso][esc][nodos[i]]["pktp"])
			pktp.append(maximos[model][caso][esc][nodos[i]]["pktp"])
			lnodes.append(i)

		df = pandas.DataFrame({
			"Nodo": lnodes,
			"Paquetes": pktp,
		})	

		graph =seaborn.barplot(x = 'Nodo', y = 'Paquetes', data = df,  ax=ax[j], palette=seaborn.color_palette("Set3"))
		ax[j].set_ylim(bottom=0, top=vmax)
		ax[j].set_title(titulos[esc])
		for p in graph.patches:
			height = p.get_height()
			if(height>1):
				graph.text(p.get_x()+p.get_width()/2., height + 0.1,"%.0f" %height ,ha="center")
		total = float(len(df))


	#fig.tight_layout(rect=[0, 0.03, 1, 0.95])
	seaborn.despine(top=True)




def comp_mod_caso_ocurrencia(esc,nodo,metr):


	#barras -> nodos
	#x -> modelos
	#y -> casos

	fig, ax = plt.subplots(2,3, figsize=(20, 12))


	for i,mod in enumerate(modelos):
		for j,caso in enumerate(casos):
			tar =  ocurrencias(mod,caso,esc,nodo,metr)
			lists = sorted(tar.items()) # sorted by key, return a list of tuples
			x, y = zip(*lists) # unpack a list of pairs into two tuples

			df = pandas.DataFrame({
				titulos[metr]: x,
				"Ocurrencias": y
			})

			graph = seaborn.barplot(x=titulos[metr], y="Ocurrencias", data = df, ax=ax[j][i])

			for k in range(8):
				graph.text(x[k],max(y[k], 0),y[k], ha='center')
			ax[j][i].set_title(titulos[mod]+", "+titulos[caso])


	fig.suptitle("Escenario: "+titulos[esc]+", nodo: "+titulos[nodo]+", metrica: "+titulos[metr], fontsize=30)
	fig.tight_layout(rect=[0, 0.03, 1, 0.95])
	seaborn.despine(top=True)

def comp_nodo_metricas(mod, caso):

	
	#barras -> nodos
	#x -> escenarios
	#y -> metricas	
	fig, ax = plt.subplots(3,4, figsize=(25, 20))

	for i,esc in enumerate(escenarios):
		for j,metr in enumerate(metr_pkt):
			x = []
			for k,nodo in enumerate(nodos):
				x.append(maximos[mod][caso][esc][nodo][metr])
			y = np.arange(len(nodos))

			df = pandas.DataFrame({
				titulos[metr]: x,
				"Nodo": y
			})

			graph = seaborn.barplot(x="Nodo", y=titulos[metr], data = df, ax=ax[j][i])
			
			for k in range(8):
				graph.text(y[k],x[k],int(x[k]), ha='center')
			ax[j][i].set_title(titulos[esc])


	fig.suptitle("modelo: "+titulos[mod]+", caso: "+titulos[caso], fontsize=30)
	fig.tight_layout(rect=[0, 0.03, 1, 0.95])



"""
#HORIZONTAL
#Hay 2 metricas, las de los nodos, y las de los paquetes
def comp_nodo_metricas(mod, caso):

	
	#barras -> nodos
	#x -> escenarios
	#y -> metricas	
	fig, ax = plt.subplots(4,4, figsize=(25, 20))

	for i,esc in enumerate(escenarios):
		for j,metr in enumerate(metr_raw):
			x = []
			for k,nodo in enumerate(nodos):
				x.append(maximos[mod][caso][esc][nodo][metr])
			y = np.arange(len(nodos))

			df = pandas.DataFrame({
				titulos[metr]: x,
				"Nodo": y
			})

			graph = seaborn.barplot(y="Nodo", x=titulos[metr], data = df, ax=ax[j][i], orient="h")
			
			for k in range(8):
				graph.text(x[k],max(y[k], 0),int(x[k]), ha='left')
			ax[j][i].set_title(titulos[esc]+", "+titulos[metr])


	fig.suptitle("modelo: "+titulos[mod]+", caso: "+titulos[caso], fontsize=30)
	fig.tight_layout(rect=[0, 0.03, 1, 0.95])

def nodes_barplot(model, caso, esc):
	fig, ax = plt.subplots(figsize=(20, 10))

	y_pos = np.arange(len(nodos))
	
	width = 0.2
	buf0_xpos = []
	for nodo in nodos:
		buf0_xpos.append(maximos[model][caso][esc][nodo]["buf0"])

	buf1_xpos = []
	for nodo in nodos:
		buf1_xpos.append(maximos[model][caso][esc][nodo]["buf1"])

	pktp_xpos = []
	for nodo in nodos:
		pktp_xpos.append(maximos[model][caso][esc][nodo]["pktp"])

	rect1 = ax.barh(y_pos, buf0_xpos, width, align='center', color='gold')
	rect2 = ax.barh(y_pos + width, buf1_xpos, width, align='center', color='lime')
	rect3 = ax.barh(y_pos + 2*width, pktp_xpos, width, align='center', color='pink')

	width = 0.2
	buf0_prom_xpos = []
	for nodo in nodos:
		buf0_prom_xpos.append(promedios[model][caso][esc][nodo]["buf0"])

	buf1_prom_xpos = []
	for nodo in nodos:
		buf1_prom_xpos.append(promedios[model][caso][esc][nodo]["buf1"])

	pktp_prom_xpos = []
	for nodo in nodos:
		pktp_prom_xpos.append(promedios[model][caso][esc][nodo]["pktp"])

	rect4 = ax.barh(y_pos, buf0_prom_xpos, width, align='center', color='orange')
	rect5 = ax.barh(y_pos + width, buf1_prom_xpos, width, align='center', color='green')
	rect6 = ax.barh(y_pos + 2*width, pktp_prom_xpos, width, align='center', color='palevioletred')



	def autolabel(rects):
		for rect in rects:
			width = rect.get_width()
			if width < 10:
				continue
			ax.annotate('{}'.format(int(width)),
						xy=(width, rect.get_y() + rect.get_height() / 2),
						xytext=(-11, -5),  # 3 points vertical offset
						textcoords="offset points",
						ha='center', va='bottom')

	autolabel(rect1)
	autolabel(rect2)
	autolabel(rect3)

	autolabel(rect4)
	autolabel(rect5)
	autolabel(rect6)

	ax.set_yticks(y_pos)
	ax.set_yticklabels(nodos)
	ax.invert_yaxis()  # labels read top-to-bottom
	ax.legend(labels=['maximo Buffer 0', "maximo Buffer 1", "Paquetes Procesados",'promedio Buffer 0', "promedio Buffer 1", "Paquetes Procesados promedio"])

	ax.set_xlabel('Valor Promedio/Máximo por campo')
	ax.set_title('Información sobre nodos, modelo: '+model+', caso: '+caso+', escenario: '+esc)

	plt.show()


"""	
