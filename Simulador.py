'''
----------------------------------------------------------
    @file: Simulador.py
    @date: Oct 2022
    @date_modif: Wed, Nov 2, 2022
    @author: Rogelio Salais
    @e-mail: rogelio.salais@hotmail.com
    @brief: Implementation of a ARX formula simulator, which can be modified within the program
    @Note: 
    Open source
----------------------------------------------------------
'''

import numpy as np
import time 
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

ventana = tkinter.Tk()
ventana.geometry("1200x700")


class simulador:

    listcoefa = [1]
    listcoefb = [0, 1]
    result = []
    coefd = 0
    coefPert = 0
    UnitLadderNo = 0
    maxSteps = 1000
    stepAmplitude = 1
    maxOutDelay = 0
    maxInpDelay = 0
    inpType = 0
    hasDeclaredCoefA = False
    hasDeclaredCoefB = False
    hasDeclaredPert = False
    hasDeclaredCoefD = False
    hasDeclaredEntry = False
    hasInitializedInput = False
    hasInitializedOutput = False
    canSimulate = False
    #First Order Model
    gainK = 0
    Tau = 0
    thetaPrime = 0
    T = 0


    inputMemory = []  # a
    outputMemory = []  # b
    # perturbation

    def printEquation(self):
        print("Ecuacion de diferencias:")
        strEquation='c(k) = '
        for x in range (len(self.listcoefa)):
            strEquation+=str(self.listcoefa[x])+'c(k - '+str((x+1))+') + '
        strEquation+=str(str(self.listcoefb[0])+'m(k - '+ str(self.coefd) +') + ')
        for x in range (1,len(self.listcoefb),1):
            strEquation+=str(str(self.listcoefb[x])+'m(k - '+str((x+1))+' - '+ str(self.coefd) +') + ')
        strEquation+=str(self.coefPert)
        print(strEquation)
        

    # Funcion que a partir de la lista de coeficientes a, calcula el valor maximo que se tiene que guardar del input para calcular el siguiente valor

    def calculateMaxOutDelay(self):
        '''
        @name: calculateMaxOutDelay
        @brief: This script takes the length of the a coefficient list and uses it to calculate a maximum
        @param: 
        @return: --
        '''
        self.maxOutDelay = len(self.listcoefa)
        for i in range(self.maxOutDelay):
            self.outputMemory.append(0)
        self.hasInitializedOutput = True

     # Funcion que a partir de la lista de coeficientes a, calcula el valor maximo que se tiene que guardar del input para calcular el siguiente valor

    def calculateMaxInpDelay(self):
        '''
        @name: calculateMaxInpDelay
        @brief: 
        @param: 
        @return: --
        '''

        self.maxInpDelay = len(self.listcoefb) + self.coefd

        # Ingresa a la memoria las primeras unidades necesarias para la entrada
        for i in range(int(self.maxInpDelay)):
            if self.inpType == 1:  # Escalon unitario
                if(i < self.coefd):
                    self.inputMemory.append(1)
                else:
                    self.inputMemory.append(0)
            elif self.inpType == 2:  # Escalon definido
                if(i < self.coefd):
                    self.inputMemory.append(self.stepAmplitude)
                else:
                    self.inputMemory.append(0)
            elif self.inpType == 3:  # Rampa
                if(i < self.coefd):
                    self.stepAmplitude = 1
                    self.inputMemory.append(1)
                else:
                    self.inputMemory.append(0)
            elif self.inpType == 4:  # Lectura de archivo
                pass  # Pendiente: Primera lectura de entrada
        self.hasInitializedInput = True

        '''
        @name: returnStepResult
        @brief: Calcula la salida en el siguiente step
        @param:
        @return: --
        '''
    def returnStepResult(self):
        self.updatesIfCanSimulate()
        if (self.canSimulate):
            accum = 0
            for i in range(len(self.outputMemory)):
                accum += self.outputMemory[i]*self.listcoefa[i]

            for i in range(len(self.inputMemory)-int(self.coefd)):
                accum += self.inputMemory[i+int(self.coefd)] * self.listcoefb[i]
                
            self.outputMemory.pop()
            self.outputMemory.insert(0, accum)

            if self.inpType == 1:       #UNITARIO
                self.inputMemory.pop()
                self.inputMemory.insert(0, 1)
            elif self.inpType == 2:     #DEFINIDO
                self.inputMemory.pop()
                self.inputMemory.insert(0, self.stepAmplitude)
            elif self.inpType == 3:     #RAMPA
                self.inputMemory.pop()
                self.inputMemory.insert(0, self.returnNextRamp())
                pass
            elif self.inpType == 4:     #ARCHIVA
                pass
            else:
                pass

            accum += self.coefPert

            return accum
        else:
            print("Cannot simulate! Parameters are missing")
            return 0

    def returnNextRamp(self):
        self.stepAmplitude += 1
        return self.stepAmplitude

    def updatesIfCanSimulate(self): #Updates and informs if everything necessary to simulate is ready
        self.canSimulate = self.hasDeclaredCoefD & self.hasDeclaredCoefA & self.hasDeclaredCoefB & self.hasDeclaredEntry & self.hasDeclaredPert & self.hasInitializedOutput & self.hasInitializedInput

    def firstOrderModelValues(self): #Calculates a's and b's values for the first order model
        d = math.trunc(self.thetaPrime / self.T)
        theta = self.thetaPrime - (d * self.T)
        m = 1- (theta / self.T)
        a1 = math.e ** ((-1 * self.T) / self.Tau)
        b1 = self.gainK * (1 - math.e ** ((-1 * m * self.T) / self.Tau))
        b2 = self.gainK * (math.e ** ((-1 * m * self.T) / self.Tau) - math.e ** ((-1 * self.T) / self.Tau))
        self.listcoefa = [a1]
        self.listcoefb = [b1, b2]
        

def graph():
    house_prices = np.random.normal(200000, 25000, 5000)
    plt.hist(house_prices, 50)
    plt.show()

def printVentana():
    # Para mandar parametros con boton:
    #  def saludo(nombre):
    #        print("hola "+ nombre)
    # boton1 = tkinter.button(ventana, text="Presiona",command=lambda: saludo("string"))

    # Para cajas de texto:
    # cajaTexto = tkinter.Entry(ventana,font = "Helvetica 20")
    # cajaTexto.pack()

    # Para mandar caja de textos a una funcion con un boton:
    #
    # def textoDeLaCaja():
    #   text20 = cajaTexto.get()
    #   print(text20)
    # boton1 = tkinter.button(ventana, text="Presiona",command=lambda: textoDeLaCaja)
    # boton1.pack()
    etiqueta = tkinter.Label(ventana, text="   Entradas:",
                             font="Helvetica 15").grid(row=0, column=0, columnspan=2)
    # Estas son las as
    etiquetaA1 = tkinter.Label(
        ventana, text="a1", font="Helvetica 15").grid(row=1, column=0)
    cajaTextoEntradasA1 = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=1, column=1)
    etiquetaA2 = tkinter.Label(
        ventana, text="a2", font="Helvetica 15").grid(row=2, column=0)
    cajaTextoEntradasA2 = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=2, column=1)
    etiquetaA3 = tkinter.Label(
        ventana, text="a3", font="Helvetica 15").grid(row=3, column=0)
    cajaTextoEntradasA3 = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=3, column=1)
    etiquetaA4 = tkinter.Label(
        ventana, text="a4", font="Helvetica 15").grid(row=4, column=0)
    cajaTextoEntradasA4 = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=4, column=1)
    # bs
    etiquetaB1 = tkinter.Label(
        ventana, text="b1", font="Helvetica 15").grid(row=5, column=0)

    cajaTextoEntradasB1 = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=5, column=1)

    etiquetaB2 = tkinter.Label(
        ventana, text="b2", font="Helvetica 15").grid(row=6, column=0)

    cajaTextoEntradasB2 = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=6, column=1)

    etiquetaB3 = tkinter.Label(
        ventana, text="b3", font="Helvetica 15").grid(row=7, column=0)

    cajaTextoEntradasB3 = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=7, column=1)

    etiquetaB4 = tkinter.Label(
        ventana, text="b4", font="Helvetica 15").grid(row=8, column=0)

    cajaTextoEntradasB4 = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=8, column=1)

    # ds
    etiquetaD = tkinter.Label(
        ventana, text="d", font="Helvetica 15").grid(row=9, column=0)

    cajaTextoEntradasD = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=9, column=1)

    boton1 = tkinter.Button(ventana, text="Ingresar",
                            width=35, height=2, command=graph).grid(row=10, column=0, columnspan=2)

    # Plots grids columns 2 a 7
    etiquetaYK = tkinter.Label(ventana, text="y(k)", font="Helvetica 15").grid(
        row=0, column=3, columnspan=5)
    # 'y' y 't' son los arreglos con los datos ahi cambiaria a las C's y M's
    y = []
    t = []
    for x in list(range(0, 101)):
        t.append(x/15.87)
    for x in t:
        y.append(x+1)
    figure = plt.figure(figsize=(5, 4), dpi=100)
    figure.add_subplot(111).plot(t, y)
    # ventana es el objeto que contiene todo lo que se quiere desplegar y figure es la figura de la tabla.
    chart = FigureCanvasTkAgg(figure, ventana)
    chart.get_tk_widget().grid(row=2, column=3, columnspan=5, rowspan=10)

    # Perturbaciones
    etiquetaPert = tkinter.Label(
        ventana, text="Perturbaciones", font="Helvetica 15").grid(row=0, column=9, columnspan=2)
    etiquetaEscalon = tkinter.Label(
        ventana, text="Esc", font="Helvetica 15").grid(row=1, column=9)
    cajaTextoEscalon = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=1, column=10)
    etiquetaRandom = tkinter.Label(
        ventana, text="Rand", font="Helvetica 15").grid(row=2, column=9)
    cajaTextoRandom = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=2, column=10)

    # u(k)
    etiquetaU = tkinter.Label(
        ventana, text="u(k)", font="Helvetica 15").grid(row=3, column=9, columnspan=2)
    etiquetaEscalon = tkinter.Label(
        ventana, text="Esc", font="Helvetica 15").grid(row=4, column=9)
    cajaTextoEscalon = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=4, column=10)

    ventana.mainloop()


def printMenu():
    '''
        @name: PrintMenu
        @brief: Prints the menu of options and returns what the user chooses as a string
    '''
    print("0. Declarar ecuacion tipo modelo de primer orden ")
    print("1. Declarar coeficientes de la entrada (an)")
    print("2. Declarar coeficientes de la salida (bn)")
    print("3. Declarar delay (d)")
    print("4. Declarar coeficiente perturbacion (p(n))")
    print("5. Elegir tipo de señal de entrada")
    print("6. Visualizar ecuacion de diferencias")
    print("7. Iniciar simulador")
    inp = input("Elige tu opcion:")
    return inp


def printMenuEntrada():
    '''
        @name: PrintMenu
        @brief: Prints the menu of input options and returns what the user chooses as a string

    '''
    print("1. Escalon Unitario")
    print("2. Escalon definido ")
    print("3. Rampa")
    print("4. Archivo")
    inp = input("Elige tu opcion:")
    return inp


def submitFunction(sim: simulador):
    #Get data of a1 store in a1
    #Get data of a2 store in a2
    #Get data of a3 store in a3
    #Get data of a4 store in a4

    #Get data of b0 
    #Get data of b1
    #Get data of b2
    #Get data of b3

    #Get data of d

    #Get data of type of entry 

    # sim.listcoefa = [a1, a2, a3, a4]
    # sim.hasDeclaredCoefA = True

    # sim.listcoefb = [b0, b1, b2, b3]
    # sim.hasDeclaredCoefB = True

    # sim.coefd = d
    # sim.hasDeclaredCoefD = True
    pass



def pauseFunction():
    global start
    start = False

def startFunction():
    global start
    start = True

def resetFunction():
    ##Sets everything to cero, including memory
    pass

    

###################
# CODIGO PRINCIPAL
###################


## Variables/Funciones llevadas a cabo por la interfaz graficas



def main():
    global start
    
    start = False 


    plotOutput = []
    plotInput = []
    plotTime = []
  
    print("First print")

    # Se lee un archivo con los atributos de la clase; ya declarados y se vuelve a declarar la clase con estos atributos


    sim = simulador()

    # Primer entrada:
    print("Bienvenido al simulador: ¿Que quieres hacer?\n")
    choice = printMenu()

    while (choice != 9):

        if choice == '0':   #Declarar modelo de primer orden
            printVentana()                                                                                                                   


        if choice == '1':
            print("Declara tus coeficientes (a1, a2, ...) con el siguiente formato:")
            stringACoef = input("Ejemplo: -0.3 -0.2 0.1 etc.\n")
            sim.listcoefa = [float(x) for x in stringACoef.split(" ")]
            sim.hasDeclaredCoefA = True
    

        elif choice == '2':
            print("Declara tus coeficientes (b0, b1, ...) con el siguiente formato:")
            stringBCoef = input("Ejemplo: 1 0 1 etc.\n")
            sim.listcoefb = [float(x) for x in stringBCoef.split(" ")]
            sim.hasDeclaredCoefB = True
            
           

        elif choice == '3':
            print("Declara un delay entero (d):")
            stringDCoef = input("Ejemplo: 2\n")
            sim.coefd = int(stringDCoef)
            sim.hasDeclaredCoefD = True
           

        elif choice == '4':
            print("Declara una perturbacion constante (pert):")
            stringDCoefPert = input("Ejemplo: 2 \n")
            sim.coefPert = int(stringDCoefPert)
            sim.hasDeclaredPert = True
        

        elif choice == '5':

            print("Elige el tipo de señal de entrada:")
            choiceInp = printMenuEntrada()
            if choiceInp == '2':        ##En caso de que el tipo de entrada sea escalon definido
                inputSize = input("Cual es el tamaño del escalon deseado?:")
                sim.stepAmplitude = float(inputSize)
            sim.inpType = int(choiceInp)
            sim.hasDeclaredEntry = True

        elif choice == '6':
             sim.printEquation()            

        elif choice == '7':
            sim.calculateMaxInpDelay()
            sim.calculateMaxOutDelay()
            print("Input memory:")
            print(sim.inputMemory)
            print("Output memory:")
            print(sim.outputMemory)
            start = True
            while (start):

               
                result = float(sim.returnStepResult())
                print(result)
                plotOutput.append(result)
                plotInput.append(sim.inputMemory[0])
                plotTime = range(len(plotOutput))
                arrPlotOutput = np.array(plotOutput)
                arrPlotInput = np.array(plotInput)
                arrPlotTime = np.array(plotTime) 
                plt.plot(arrPlotTime, arrPlotOutput)
                plt.plot(arrPlotTime, arrPlotInput)
                plt.pause(0.5)
                # print("Input memory:")
                # print(sim.inputMemory)
                # print("Output memory:")
                # print(sim.outputMemory)
             


        else:
            print("Invalid command!")

        print("What do you want to do?")
        choice = printMenu()

    return 1



main()
