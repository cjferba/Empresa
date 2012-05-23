#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  empre.py
#  
#  Copyright 2012 Carlos Jesus Fernandez Basso <cjferba@gmail.com>

from gi.repository import Gtk
import shutil
from PIL import Image
import MySQLdb

def buscar(X):
	for i in range(len(X)):
		if X[i]==",":
			return int(X[i+1:len(X)][:])

class Handler:
	
	
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
	
	#  Manejador de seleccionar una imagen.
	  
	def aceptFile(self, boton):
		global archivo
		archivo = boton.get_filename()
		# Abrir imagen
		img = Image.open(archivo)
		# Comprobamos su tamaño
		w,h = img.size
		if (w>450 or h>450):
			# Notificacion al usuario
			texto = builder.get_object("label25")
			texto.set_label("Error! La imagen debe tener un tamaño máximo de 450x450.\n(Ideal: 300x360)")
			dialog = builder.get_object("messagedialog1")
			dialog.show_all()
			boton.set_filename('(Ninguno)')
	
	#  Mostrar diálogo Acerca de...
	
	def moreInfo(self, entry):
		info = builder.get_object("aboutdialog1")
		info.show_all()
	
	# Ocultar diálogo Acerca de...
	#  
	def lessInfo(self, dialog, arg):
		dialog.hide()
	
	#  Manejador de  selección de menú Crear
	#  
	def menuCrear(self, entry):
		global padre_old, padre_menu
		menu = builder.get_object("grid3")
		menu.reparent(padre_menu)
		panel = builder.get_object("box2")
		padre_old = panel.get_parent()
		contenedor = builder.get_object("aspectframe1")
		titulo = builder.get_object("label2")
		titulo.set_label("Introducir datos del empleado")
		boton = builder.get_object("button1")
		boton.set_label("Crear")
		panel.reparent(contenedor)
	
	#  Manejador de  selección de menú Actualizar
	#  
	def menuActualizar(self, entry):
		global padre_menu
		menu = builder.get_object("grid3")
		menu.reparent(padre_menu)
		# Realizamos consulta 
		query = "SELECT NOMBRE,DNI,ID FROM EMPLEADOS WHERE 1;"
		micursor.execute(query)
		num = micursor.fetchall()
		# Insertar los valores del comboboxtext
		comboBox = builder.get_object("comboboxtext2")
		comboBox.remove_all()
		for i in num:
			comboBox.insert(-1,None,str(i['NOMBRE'])+" "+str(i['DNI'])+","+str(i['ID']))#str(i['DNI'])+","+
		dialog = builder.get_object("dialog1")
		boton = builder.get_object("button3")
		boton.set_label("Seleccionar")
		dialog.show_all()
	
	#  Manejador selección de menú Obtener.
	#  
 	def menuObtener(self, entry):
		global padre_menu
		menu = builder.get_object("grid3")
		menu.reparent(padre_menu)
		# Realizamos la consulta
		query = "SELECT NOMBRE,DNI,ID FROM EMPLEADOS WHERE 1;"
		micursor.execute(query)
		num = micursor.fetchall()
		#Isertamos los valores del comboboxtext
		comboBox = builder.get_object("comboboxtext2")
		comboBox.remove_all()
		for i in num:
			comboBox.insert(-1,None,str(i['NOMBRE'])+" "+str(i['DNI'])+","+str(i['ID']))#str(i['DNI'])+","+

		dialog = builder.get_object("dialog1")
		boton = builder.get_object("button3")
		boton.set_label("Consultar")
		dialog.show_all()
	
	#  Manejador selección del menú Borrar
	#  
	def menuBorrar(self, entry):
		global padre_menu
		menu = builder.get_object("grid3")
		menu.reparent(padre_menu)
		# Realizamos la consulta de ids
		query = "SELECT NOMBRE,DNI,ID FROM EMPLEADOS WHERE 1 ORDER BY ID;"
		micursor.execute(query)
		num = micursor.fetchall()
		# Establecemos los valores del comboboxtext
		comboBox = builder.get_object("comboboxtext2")
		comboBox.remove_all()
		for i in num:
			comboBox.insert(-1,None,str(i['NOMBRE'])+" "+str(i['DNI'])+","+str(i['ID']))#str(i['DNI'])+","+
		dialog = builder.get_object("dialog1")
		boton = builder.get_object("button3")
		boton.set_label("Borrar")
		dialog.show_all()

	#  Manejador de la excepción click en un botón.
	#
	def onButtonClick(self, button):
		global padre_old, padre_menu, micursor, Conexion
		
		if (button.get_label() == "Ok"):
			# Ocultamos los diálogos.
			dialog = builder.get_object("messagedialog1")
			dialog.hide()
			
		if (button.get_label() == "Actualizar"):
			global id_update
			# Realizamos la actualización
			doUpdate(id_update)
			Conexion.commit()
			cleanWidgets()
			
		if (button.get_label() == "Crear"):
			# Realizamos la inserción
			doInsert()
			Conexion.commit()
			cleanWidgets()
			
		if (button.get_label() == "Consultar"):
			# Ocultamos el diálogo.
			comboBox = builder.get_object("comboboxtext2")
			Id = comboBox.get_active_text()
			# Comprobamos que ha escogido un id
			if (Id==None):
				# Notificamos al usuario
				texto = builder.get_object("label25")
				texto.set_label("Error! Debe seleccionar un ID.")
				dialog = builder.get_object("messagedialog1")
				dialog.show_all()
			else:
				dialog = builder.get_object("dialog1")
				dialog.hide()
				# Realizamos la consulta
				x=buscar(Id)
				doQuery(x)
			
		if (button.get_label() == "Cancelar"):
			dialog = builder.get_object("dialog1")
			dialog.hide()
			reMenu()
			
		if (button.get_label() == "Hecho"):
			panel = builder.get_object("vbox2")
			panel.reparent(padre_old)
			reMenu()
			
		if (button.get_label() == "Rechazar"):
			cleanWidgets()
		
		if (button.get_label() == "Seleccionar"):
			comboBox = builder.get_object("comboboxtext2")
			Id = comboBox.get_active_text()
			if (Id==None):
				texto = builder.get_object("label25")
				texto.set_label("Error! Debe seleccionar un ID.")
				dialog = builder.get_object("messagedialog1")
				dialog.show_all()
			else:
				x=str(buscar(Id))
				doQueryUpdate(x)
				dialog = builder.get_object("dialog1")
				dialog.hide()
				panel = builder.get_object("box2")
				padre_old = panel.get_parent()
				contenedor = builder.get_object("aspectframe1")
				panel.reparent(contenedor)
		
		if (button.get_label() == "Borrar"):
			comboBox = builder.get_object("comboboxtext2")
			Id = comboBox.get_active_text()
			if (Id==None):
				texto = builder.get_object("label25")
				texto.set_label("Error! Debe seleccionar un ID.")
				dialog = builder.get_object("messagedialog1")
				dialog.show_all()
			else:
				x=str(buscar(Id))
				query = "DELETE FROM EMPLEADOS WHERE ID="+x+";"
				micursor.execute(query)
				texto = builder.get_object("label25")
				texto.set_label("La entrada ha sido borrada con éxito")
				dialog = builder.get_object("messagedialog1")
				dialog.show_all()
				dialog = builder.get_object("dialog1")
				dialog.hide()
				reMenu()

def reMenu():
	menu = builder.get_object("grid3")
	contenedor = builder.get_object("aspectframe1")
	menu.reparent(contenedor)

#  Función que vacía los contenidos de los widgets editables
#    
def cleanWidgets():
	global archivo
	entrada = builder.get_object("entry1")
	entrada.set_text("")
	
	entrada = builder.get_object("entry2")
	entrada.set_text("")
	
	entrada = builder.get_object("entry3")
	entrada.set_text("")
	
	entrada = builder.get_object("entry4")
	entrada.set_text("")
	
	entrada = builder.get_object("comboboxtext4")
	entrada.set_active(-1)
	
	entrada = builder.get_object("entry5")
	entrada.set_text("")
	
	entrada = builder.get_object("comboboxtext5")
	entrada.set_active(-1)
	
	entrada = builder.get_object("filechooserbutton1")
	entrada.set_filename('(Ninguno)')
	
	archivo = None
	
	panel = builder.get_object("box2")
	panel.reparent(padre_old)
	reMenu()

#  Función que recoge la información de los widgets en pantalla  
#  
def doUpdate(Id):
	global archivo
	
	entrada = builder.get_object("entry1")
	nom = entrada.get_text()
	
	entrada = builder.get_object("entry2")
	DNI = entrada.get_text()
		
	entrada = builder.get_object("entry3")
	DIRECCION = entrada.get_text()
			
	entrada = builder.get_object("entry4")
	SALARIO = entrada.get_text()
		
	entrada = builder.get_object("comboboxtext4")
	PUESTO = entrada.get_active_text()
			
	entrada = builder.get_object("entry5")
	TELEFONO = entrada.get_text()
		
	entrada = builder.get_object("comboboxtext5")
	CIUDAD = entrada.get_active_text()
	
	# Comprobación de elementos nulos
	if (nom == '' or SALARIO == '' or TELEFONO == '' or CIUDAD == None or DIRECCION=='' or PUESTO==None):
		texto = builder.get_object("label25")
		texto.set_label("Error! Se ha introducido un campo nulo o no válido.\nAviso: No se ha realizado la operación de inserción.")
		dialog = builder.get_object("messagedialog1")
		dialog.show_all()
	else:
		if archivo != None and archivo != "(Ninguno)":
			
			try:
				shutil.copyfile(archivo,'./resources/'+nom+'.jpg')
			except:
				texto = builder.get_object("label25")
				texto.set_label("Error! No se pudo copiar la imagen seleccionada.\nAviso: No se ha realizado la operación de inserción")
				dialog = builder.get_object("messagedialog1")
				dialog.show_all()
			else:
				query = "UPDATE EMPLEADOS SET NOMBRE=\""+nom+"\",  DNI=\""+DNI+"\", DIRECCION=\""+DIRECCION+"\",SALARIO=\""+SALARIO+"\", PUESTO=\""+PUESTO+"\", TELEFONO=\""+TELEFONO+"\", CIUDAD=\""+CIUDAD+"\", FOTO=\""+nom+".jpg\" WHERE ID="+Id+";"
		else:
			query = "UPDATE EMPLEADOS SET NOMBRE=\""+nom+"\",  DNI=\""+DNI+"\", DIRECCION=\""+DIRECCION+"\",SALARIO=\""+SALARIO+"\", PUESTO=\""+PUESTO+"\", TELEFONO=\""+TELEFONO+"\", CIUDAD=\""+CIUDAD+"\" WHERE ID="+Id+";"
		micursor.execute(query)

 
def doInsert():
	global archivo
	
	entrada = builder.get_object("entry1")
	nom = entrada.get_text()
	
	entrada = builder.get_object("entry2")
	DNI = entrada.get_text()
		
	entrada = builder.get_object("entry3")
	DIRECCION = entrada.get_text()
			
	entrada = builder.get_object("entry4")
	SALARIO = entrada.get_text()
		
	entrada = builder.get_object("entry5")
	TELEFONO = entrada.get_text()
			
	entrada = builder.get_object("comboboxtext4")
	PUESTO = entrada.get_active_text()
	
	entrada = builder.get_object("comboboxtext5")
	CIUDAD = entrada.get_active_text()
	
	query = "SELECT count(ID) FROM EMPLEADOS WHERE 1;"
	micursor.execute(query)
	reg = micursor.fetchone()
	query = "SELECT max(ID) FROM EMPLEADOS;"
	micursor.execute(query)
	reg2 = micursor.fetchone()
	
	index = "0"
	if (reg['count(ID)'] != reg2['max(ID)']):
		query = "SELECT ID FROM EMPLEADOS WHERE 1 ORDER BY ID;"
		micursor.execute(query)
		lista = micursor.fetchall()
		
		flag = True
		for i in range(len(lista)):
			if ((int(lista[i]['ID']) != (i+1)) and flag):
				index = str(i+1)
				flag = False
	else:
		index = str(int(reg2['max(ID)'])+1)
	
	# Comprobación de elementos nulos
	if (nom == '' or DNI=='' or SALARIO=='' or CIUDAD==None or PUESTO == None or index=="0" or SALARIO=='' or DIRECCION=='' or TELEFONO==''):

		texto = builder.get_object("label25")
		texto.set_label("Error! Se ha introducido un campo nulo o no válido.\nAviso: No se ha realizado la operación de inserción.")
		dialog = builder.get_object("messagedialog1")
		dialog.show_all()
	else:
		# Consultamos alguna aparición por Nombre
		query = "SELECT * FROM EMPLEADOS WHERE NOMBRE=\""+nom+"\";"
		micursor.execute(query)
		# Si no obtenemos resultados, insertamos el registro
		if (micursor.fetchone()==None):
			if archivo != None or archivo != '(Ninguno)':
				# Copiamos la imagen seleccionada
				try:
					shutil.copyfile(archivo,'./resources/'+nom+'.jpg')
				except:
					# En caso de error, notificamos al usuario
					texto = builder.get_object("label25")
					texto.set_label("Error! No se pudo copiar la imagen seleccionada.\nAviso: No se ha realizado la operación de inserción")
					dialog = builder.get_object("messagedialog1")
					dialog.show_all()
				else:
					# Realizamos la inserción con imagen seleccionada
					query = "INSERT INTO EMPLEADOS (ID, NOMBRE,  DNI, DIRECCION,SALARIO, PUESTO, TELEFONO, CIUDAD, FOTO) VALUES ("+index+", \""+nom+"\", \""+DNI+"\", \""+DIRECCION+"\", \""+SALARIO+"\", \""+PUESTO+"\", \""+TELEFONO+"\", \""+CIUDAD+"\", \""+nom+".jpg\");"
			else:
				# Realizamos la inserción con imagen predeterminada
				query = "INSERT INTO EMPLEADOS (ID, NOMBRE,  DNI, DIRECCION,SALARIO, PUESTO, TELEFONO, CIUDAD, FOTO) VALUES ("+index+", \""+nom+"\", \""+DNI+"\", \""+DIRECCION+"\", \""+SALARIO+"\", \""+PUESTO+"\", \""+TELEFONO+"\", \""+CIUDAD+"\", \"empleado.jpg\");"

			# EJECUCIÓN DE LA INSERCIÓN
			micursor.execute(query)
		else:
			# En caso contrario, notificamos al usuario
			texto = builder.get_object("label25")
			texto.set_label("Error! Ya existe una entrada con nombre "+nom+" .\nAviso: No se ha realizado la operación de inserción")
			dialog = builder.get_object("messagedialog1")
			dialog.show_all()

#  Función que obtiene la información de una tupla seleccionada.

def doQuery(Id):
	global micursor, padre_old
	
	# Realizamos la consulta
	query = "SELECT * FROM EMPLEADOS WHERE ID="+str(Id)+";"
	micursor.execute(query)
	registro = micursor.fetchone()
	
	texto = builder.get_object("label15")
	texto.set_label(registro['NOMBRE'])
	
	texto = builder.get_object("label16")
	texto.set_label(registro['DNI'])
	
	texto = builder.get_object("label17")
	texto.set_label(registro['DIRECCION'])
	
	texto = builder.get_object("label18")
	texto.set_label(str(registro['SALARIO']))
	
	texto = builder.get_object("label21")
	texto.set_label(registro['PUESTO'])
	
	texto = builder.get_object("label22")
	texto.set_label(str(registro['TELEFONO']))
	
	texto = builder.get_object("label24")
	texto.set_label(registro['CIUDAD'])
	
	imagen = builder.get_object("image2")
	imagen.clear()
	if (registro['FOTO']!=None):
		imagen.set_from_file("./resources/"+registro['FOTO'])
		
	panel = builder.get_object("vbox2")
	padre_old = panel.get_parent()
	contenedor = builder.get_object("aspectframe1")
	panel.reparent(contenedor)

#  Función que recopila la información actual de la tupla que se desea 
#  modificar y la asigna a los widgets correspondientes.

def doQueryUpdate(Id):
	global id_update
	id_update = Id
	titulo = builder.get_object("label2")
	titulo.set_label("Actualizar la semilla "+str(Id))
	
	boton = builder.get_object("button1")
	boton.set_label("Actualizar")
	
	# Consultamos la información actual del registro
	query = "SELECT * FROM EMPLEADOS WHERE ID="+Id+";"
	micursor.execute(query)
	registro = micursor.fetchone()
	
	entrada = builder.get_object("entry1")
	entrada.set_text(str(registro['NOMBRE']))
	
	entrada = builder.get_object("entry2")
	entrada.set_text(str(registro['DNI']))
	
	entrada = builder.get_object("entry3")
	entrada.set_text(str(registro['DIRECCION']))
	
	entrada = builder.get_object("entry4")
	entrada.set_text(str(registro['SALARIO']))
	
	entrada = builder.get_object("comboboxtext4")
	if (str(registro['PUESTO'])=="Director/a"):
		index = 0
	elif (str(registro['PUESTO'])=="Empleado/a"):
		index = 1
	elif (str(registro['PUESTO'])=="Secretario/a"):
		index = 2
	else:
		index = 3
	entrada.set_active(index)
	
	entrada = builder.get_object("entry5")
	entrada.set_text(str(registro['TELEFONO']))

	entrada = builder.get_object("comboboxtext5")
	if (str(registro['CIUDAD'])=="Granada"):
		index = 0
	elif (str(registro['CIUDAD'])=="Madrid"):
		index = 1
	elif (str(registro['CIUDAD'])=="Barcelona"):
		index = 2
	elif (str(registro['CIUDAD'])=="Valencia"):
		index = 3
	else:
		index = 4
	entrada.set_active(index)

#  Función que conecta la Base de Datos y ejecuta el create.sql
def iniciaDB():
	global Conexion,micursor
	
	# Realizamos la Conexion
	try:
		Conexion = MySQLdb.connect(host='localhost', user='conan',passwd='crom', db='DBdeConan')
	except:
		print "No se ha podido conectar a la Base de Datos DBdeConan."
		raise SystemExit
	else:
		micursor = Conexion.cursor(MySQLdb.cursors.DictCursor)
		# Abrimos el fichero .sql
		try:
			fichero = open('resources/create.sql','r')
		except:
			print "Ha ocurrido un error. No se puede abrir el fichero .sql ."
			raise SystemExit
		else:
			listaQuery = fichero.readlines()
			fichero.close()
	try:
		micursor.execute(listaQuery[0])
	except:
		pass
	else:
	 	# Ejecutamos las sentencias
	 	for i in range(1,len(listaQuery)):
			try:
				micursor.execute(listaQuery[i])
			except:
				print "Error al editar la Base de Datos."
				raise SystemExit
		
		Conexion.commit()

#  Función que desconecta la Base de Datos
#  
def destroyDB():
	global micursor,Conexion
	micursor.execute("DROP TABLE EMPLEADOS;")
	Conexion.commit()
	micursor.close()
	Conexion.close()
	
# Variables Globales
Conexion = None
micursor = None
padre_old = None
id_update = None
padre_menu = None
archivo = None

# Iniciamos la BD
iniciaDB()
# Obtenemos la interfaz
builder = Gtk.Builder()
builder.add_from_file("interfaz.glade")

# Conectamos las señales
builder.connect_signals(Handler())

# Mostramos la ventana principal con el menú
window = builder.get_object("window1")
menu = builder.get_object("grid3")
padre_menu = menu.get_parent()
contenedor = builder.get_object("aspectframe1")
menu.reparent(contenedor)
window.show_all()

# Entramos en el bucle principal
Gtk.main()
# Destruimos la BD
destroyDB()
