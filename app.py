#--------------------------------------Importamos librerias--------------------------------------------

from tkinter import *
import os
from turtle import color
import cv2
import numpy as np
from matplotlib import pyplot
from mtcnn_cv2 import MTCNN
import errno

#------------------------ Crearemos una funcion que se encargara de registrar el usuario ---------------------


def registrar_usuario():
    usuario_info = usuario.get() #Obetnemos la informacion alamcenada en usuario
    contra_info = contra.get() #Obtenemos la informacion almacenada en contra
    
    #Para prevenir en caso exista el usuario, remplace sus valores sin dar error
    try:
        os.mkdir(usuario_info)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    archivo = open("./"+usuario_info+"/usuario.txt", "w") #Abriremos la informacion en modo escritura
    archivo.write(usuario_info + "\n")   #escribimos la info
    archivo.write(contra_info)
    archivo.close()
    registro_facial()

#--------------------------- Funcion para almacenar el registro facial --------------------------------------
  
def registro_facial():
     #Llamamos a la funcion registro usuario para guardar usuario y contraseña
    #Vamos a capturar el rostro
    cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Leemos el video
        cv2.imshow('Registro Facial',frame)         #Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
            break
    usuario_img = usuario.get()
    cv2.imwrite("./"+usuario_img+"/photo.jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)   #Limpiamos los text variables
    contra_entrada.delete(0, END)
    Label(pantalla1, text = "Registro Facial Exitoso", fg = "green", font = ("Calibri",11)).grid(padx=6, pady = 10, row=10, column=3)

    #----------------- Detectamos el rostro y exportamos los pixeles --------------------------
    
    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tamaño de 150x200
            cv2.imwrite("./"+usuario_img+"/photo.jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        # pyplot.show()  #Mostrar la cara detectada en pantalla

    img = "./"+usuario_img+"/photo.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)    

#------------------------Crearemos una funcion para asignar al boton registro --------------------------------
def registro():
    global usuario
    global contra  #Globalizamos las variables para usarlas en otras funciones
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
    pantalla1.title("Registro")
    pantalla1.geometry("300x250")  #Asignamos el tamaño de la ventana
    pantalla1.configure(bg='black') #Asignamos la configuracion de la ventana
    
    #--------- Empezaremos a crear las entradas ----------------------------------------
    
    usuario = StringVar()
    contra = StringVar()
    
    Label(pantalla1, text = ":::Formulario de Registro:::",bg='black', fg = "white").grid(padx=6, pady = 10, row=0, column=3)
    # Label(pantalla1, text = "", bg='black')  #Dejamos un poco de espacio
    # Label(pantalla1, text = "", bg='black')  #Dejamos un poco de espacio
    Label(pantalla1, text = "Usuario * ", bg='black', fg = "white").grid(padx=6, pady = 10, row=4, column=2)  #Mostramos en la pantalla 1 el usuario
    usuario_entrada = Entry(pantalla1, textvariable = usuario) #Creamos un text variable para que el usuario ingrese la info
    usuario_entrada.grid(padx=6, pady = 10, row=4, column=3)
    Label(pantalla1, text = "Contraseña * ",bg='black', fg = "white").grid(padx=6, pady = 10, row=5, column=2) #Mostramos en la pantalla 1 la contraseña
    contra_entrada = Entry(pantalla1, textvariable = contra) #Creamos un text variable para que el usuario ingrese la contra
    contra_entrada.grid(padx=6, pady = 10, row=5, column=3)
    # Label(pantalla1, text = "", bg='black')  #Dejamos un espacio para la creacion del boton
    Button(pantalla1, text = "Siguiente", bg='black', fg= "white", width = 15, height = 1, command = registrar_usuario).grid(padx=6, pady = 10, row=7, column=3)  #Creamos el boton
    Button(pantalla1, text = "Atras", bg='black', fg= "white", width = 15, height = 1, command = pantalla_principal).grid(padx=6, pady = 10, row=9, column=3)
#------------------------------------------- Funcion para verificar los datos ingresados al login ------------------------------------
def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada3.delete(0, END)
    contra_entrada3.delete(0, END)

    lista_archivos = os.listdir()   #Vamos a importar la lista de archivos con la libreria os
    if log_usuario in lista_archivos:   #Comparamos los archivos con el que nos interesa
        archivo2 = open("./"+log_usuario+"/usuario.txt", "r")  #Abrimos el archivo en modo lectura
        verificacion = archivo2.read().splitlines()  #leera las lineas dentro del archivo ignorando el resto
        if log_contra in verificacion:
            print("Inicio de sesion exitoso")
            Label(pantalla3, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).grid(padx=6, pady = 10, row=9, column=3)
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(pantalla3, text = "Contraseña Incorrecta", fg = "red", font = ("Calibri",11)).grid(padx=6, pady = 10, row=9, column=3)
    else:
        print("Usuario no encontrado")
        Label(pantalla3, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).grid(padx=6, pady = 10, row=9, column=3)
    
#--------------------------Funcion para el Login Facial --------------------------------------------------------
def verificacion_login_facial():
#------------------------------Vamos a capturar el rostro-----------------------------------------------------
    cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Leemos el video
        cv2.imshow('Login Facial',frame)         #Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
            print("Usuario no encontrado")
            cap.release()                               #Cerramos
            cv2.destroyAllWindows()
            Label(pantalla4, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).grid(padx=6, pady = 10, row=9, column=3)
            break
            
    
    usuario_login = verificacion_usuario.get() #Con esta variable vamos a guardar la foto pero con otro nombre para no sobreescribir
    cv2.imwrite("./"+usuario_login+"/photoLOG.jpg",frame) #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada4.delete(0, END)   #Limpiamos los text variables

    #----------------- Funcion para guardar el rostro --------------------------
    
    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen 150x200
            cv2.imwrite("./"+usuario_login+"/photoLOG.jpg",cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])

    #-------------------------- Detectamos el rostro-------------------------------------------------------
    
    img = "./"+usuario_login+"/photoLOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    #-------------------------- Funcion para comparar los rostros --------------------------------------------
    def orb_sim(img1,img2):
        orb = cv2.ORB_create()  #Creamos el objeto de comparacion
 
        kpa, descr_a = orb.detectAndCompute(img1, None)  #Creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None)  #Creamos descriptor 2 y extraemos puntos claves

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza

        matches = comp.match(descr_a, descr_b)  #Aplicamos el comparador a los descriptores

        regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos claves
        if len(matches) == 0:
            return 0
        return len(regiones_similares)/len(matches)  #Exportamos el porcentaje de similitud
        
    #---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------
    
    im_archivos = os.listdir(path="./"+usuario_login)   #Vamos a importar la lista de archivos con la libreria os
    if "photoLOG.jpg" in im_archivos:   #Comparamos los archivos con el que nos interesa
        rostro_reg = cv2.imread("./"+usuario_login+"/photo.jpg",0)     #Importamos el rostro del registro
        rostro_log = cv2.imread("./"+usuario_login+"/photoLOG.jpg",0)  #Importamos el rostro del inicio de sesion
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.98:
            Label(pantalla4, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).grid(padx=6, pady = 10, row=9, column=3)
            print("Bienvenido al sistema usuario: ",usuario_login)
            print("Compatibilidad con la foto del registro: ",similitud)
        else:
            print("Rostro incorrecto, Cerifique su usuario")
            print("Compatibilidad con la foto del registro: ",similitud)
            Label(pantalla4, text = "Incompatibilidad de rostros", fg = "red", font = ("Calibri",11)).grid(padx=6, pady = 10, row=9, column=3)
    else:
        print("Usuario no encontrado")
        Label(pantalla4, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).grid(padx=6, pady = 10, row=9, column=3)
#------------------------Funcion que asignaremos al boton login -------------------------------------------------
        
def login():
    global pantalla2
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("300x280")   #Creamos la ventana
    pantalla2.configure(bg='black') #Asignamos la configuracion de la ventan
    Label(pantalla2, text = "Login facial: debe de asignar un usuario:",  fg = "white", bg = "black").pack()
    Label(pantalla2, text = "Login tradicional: debe asignar usuario y contraseña:",  fg = "white", bg = "black").pack()
    Label(pantalla2, text = "", bg = "black").pack()  #Dejamos un poco de espacio
    
    Label(pantalla2, text = "", bg = "black").pack()
    Button(pantalla2, text = "Inicio de Sesion Tradicional",  fg = "white", bg = "black", width = 20, height = 1, command = login_traditional).pack()

    #------------ Vamos a crear el boton para hacer el login facial --------------------
    Label(pantalla2, text = "", bg = "black").pack()
    Button(pantalla2, text = "Inicio de Sesion Facial", fg = "white", bg = "black", width = 20, height = 1, command = login_facial).pack()

#------------------------Funcion que muestra el login de forma tradicional (user-password) -------------------------------------------------
        
def login_traditional():
    pantalla2.destroy()
    global pantalla3
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada3
    global contra_entrada3
    
    pantalla3 = Toplevel(pantalla)
    pantalla3.title("Login traditional")
    pantalla3.geometry("300x250")   #Creamos la ventana
    pantalla3.configure(bg='black') #Asignamos la configuracion de la ventan    
    
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()

    Label(pantalla3, text = ":::Login:::",bg='black', fg = "white").grid(padx=6, pady = 10, row=0, column=3)
    # Label(pantalla1, text = "", bg='black')  #Dejamos un poco de espacio
    # Label(pantalla1, text = "", bg='black')  #Dejamos un poco de espacio
    Label(pantalla3, text = "Usuario * ", bg='black', fg = "white").grid(padx=6, pady = 10, row=4, column=2)  #Mostramos en la pantalla 1 el usuario
    usuario_entrada3 = Entry(pantalla3, textvariable = verificacion_usuario) #Creamos un text variable para que el usuario ingrese la info
    usuario_entrada3.grid(padx=6, pady = 10, row=4, column=3)
    Label(pantalla3, text = "Contraseña * ",bg='black', fg = "white").grid(padx=6, pady = 10, row=5, column=2) #Mostramos en la pantalla 1 la contraseña
    contra_entrada3 = Entry(pantalla3, textvariable = verificacion_contra) #Creamos un text variable para que el usuario ingrese la contra
    contra_entrada3.grid(padx=6, pady = 10, row=5, column=3)
    # Label(pantalla1, text = "", bg='black')  #Dejamos un espacio para la creacion del boton
    Button(pantalla3, text = "Ingresar", bg='black', fg= "white", width = 15, height = 1, command = verificacion_login).grid(padx=6, pady = 10, row=7, column=3)  #Creamos el boton
#------------------------Funcion que muestra el login de reconocimiento facial -------------------------------------------------
        
def login_facial():
    pantalla2.destroy()
    global pantalla4
    global verificacion_usuario
    global usuario_entrada4
    global contra_entrada4

    
    pantalla4 = Toplevel(pantalla)
    pantalla4.title("Login Facial")
    pantalla4.geometry("300x250")   #Creamos la ventana
    pantalla4.configure(bg='black') #Asignamos la configuracion de la ventan    
    
    verificacion_usuario = StringVar()

    Label(pantalla4, text = ":::Login:::",bg='black', fg = "white").grid(padx=6, pady = 10, row=0, column=3)
    Label(pantalla4, text = "Usuario * ", bg='black', fg = "white").grid(padx=6, pady = 10, row=4, column=2)  #Mostramos en la pantalla 1 el usuario
    usuario_entrada4 = Entry(pantalla4, textvariable = verificacion_usuario) #Creamos un text variable para que el usuario ingrese la info
    usuario_entrada4.grid(padx=6, pady = 10, row=4, column=3)

    # Label(pantalla1, text = "", bg='black')  #Dejamos un espacio para la creacion del boton
    Button(pantalla4, text = "Ingresar", bg='black', fg= "white", width = 15, height = 1, command = verificacion_login_facial).grid(padx=6, pady = 10, row=7, column=3)
#------------------------- Funcion de muestra pantalla principal ------------------------------------------------
    
def pantalla_principal():
    global pantalla          #Globalizamos la variable para usarla en otras funciones
    pantalla = Tk()
    pantalla.geometry("300x280")  #Asignamos el tamaño de la ventana 
    pantalla.title("Aprende e Ingenia") #Asignamos el titulo de la pantalla
    pantalla.configure(bg='black') #Asignamos la configuracion de la ventana
    Label(text = "Login Inteligente", bg = "black",  fg = "white" , width = "300", height = "2", font = ("Verdana", 13)).pack() #Asignamos caracteristicas de la ventana
    
#------------------------- Vamos a Crear los Botones ------------------------------------------------------
    
    Label(text = "",bg = "black").pack()  #Creamos el espacio entre el titulo y el primer boton
    Button(text = "Iniciar Sesion", bg = "black",  fg = "white", height = "2", width = "30", command = login).pack()
    Label(text = "",bg = "black").pack() #Creamos el espacio entre el primer boton y el segundo boton
    Button(text = "Registro", bg = "black",  fg = "white", height = "2", width = "30", command = registro).pack()
    pantalla.mainloop()
    # cv2.destroyAllWindows()                            #Cerramos

pantalla_principal()