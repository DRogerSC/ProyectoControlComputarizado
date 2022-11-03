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
import tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
ventana = tkinter.Tk()
ventana.geometry("1000x700")


class simulador:

    listcoefa = [1]
    listcoefb = [0, 1]
    result = []
    coefd = 0
    coefPert = 0
    UnitLadderNo = 0
    maxSteps = 1000
    stepSize = 0
    maxOutDelay = 0
    maxInpDelay = 0
    inpType = 0

    inputMemory = []  # a
    outputMemory = []  # b
    # perturbation

    def printEquation(self):
        print("Ecuacion de diferencias:\n\n")
        print("")

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
            self.inputMemory.append(0)

     # Funcion que a partir de la lista de coeficientes a, calcula el valor maximo que se tiene que guardar del input para calcular el siguiente valor

    def calculateMaxInpDelay(self):
        '''
        @name: calculateMaxInpDelay
        @brief: 
        @param: 
        @return: --
        '''

        self.maxInpDelay = len(self.listcoefb) + self.coefd[0]

        # Ingresa a la memoria las primeras unidades necesarias para la entrada
        for i in range(int(self.maxInpDelay)):
            if self.inpType == 1:  # Escalon unitario
                self.outputMemory.append(1)
            elif self.inpType == 2:  # Escalon definido
                self.outputMemory.append(self.stepSize)
            elif self.inpType == 3:  # Rampa
                self.outputMemory.append(self.stepSize)
            elif self.inpType == 4:  # Lectura de archivo
                pass  # Pendiente: Primera lectura de entrada

    def returnStepResult(self):
        '''
        @name: returnStepResult
        @brief: Calcula la salida en el siguiente step
        @param:
        @return: --
        '''
        accum = 0
        for i in range(len(self.outputMemory)-1):
            accum += self.outputMemory[i]*self.listcoefa[i]

        for i in range(len(self.inputMemory)-int(self.coefd[0])):
            accum += self.inputMemory[i+int(self.coefd[0])] * self.listcoefb[i]
        self.outputMemory.pop()
        self.outputMemory.insert(1, accum)

        return accum


def plot():

    # the figure that will contain the plot
    fig = Figure(figsize=(5, 5),
                 dpi=100)

    # list of squares
    y = [i**2 for i in range(101)]

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(y)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


def printVentana():

    etiqueta = tkinter.Label(ventana, text="Hola Mundo")
    # Para mandar parametros con boton:
    #  def saludo(nombre):
    #        print("hola "+ nombre)
    # boton1 = tkinter.button(ventana, text="Presiona",command=lambda: saludo("string"))
    # Para cajas de texto:
    #cajaTexto = tkinter.Entry(ventana,font = "Helvetica 20")
    # cajaTexto.pack()
    # Para mandar caja de textos a una funcion con un boton:
    # def textoDeLaCaja():
    #   text20 = cajaTexto.get()
    #   print(text20)
    #
    #boton1 = tkinter.button(ventana, text="Presiona",command=lambda: textoDeLaCaja)
    # boton1.pack()
    # Para ordenar de una mejor forma
    #
    etiqueta = tkinter.Label(ventana, text="   Entradas:",
                             font="Helvetica 15").grid(row=0, column=0, columnspan=2)
    # Estas son las as
    etiquetaA1 = tkinter.Label(
        ventana, text="a1", font="Helvetica 15").grid(row=1, column=0)
    cajaTextoEntradas = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=1, column=1)
    etiquetaA2 = tkinter.Label(
        ventana, text="a2", font="Helvetica 15").grid(row=2, column=0)
    cajaTextoEntradas = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=2, column=1)
    etiquetaA3 = tkinter.Label(
        ventana, text="a3", font="Helvetica 15").grid(row=3, column=0)
    cajaTextoEntradas = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=3, column=1)
    etiquetaA4 = tkinter.Label(
        ventana, text="a4", font="Helvetica 15").grid(row=4, column=0)
    cajaTextoEntradas = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=4, column=1)
    # bs
    etiquetaB1 = tkinter.Label(
        ventana, text="b1", font="Helvetica 15").grid(row=5, column=0)

    cajaTextoEntradas = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=5, column=1)

    etiquetaB2 = tkinter.Label(
        ventana, text="b2", font="Helvetica 15").grid(row=6, column=0)

    cajaTextoEntradas = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=6, column=1)

    etiquetaB3 = tkinter.Label(
        ventana, text="b3", font="Helvetica 15").grid(row=7, column=0)

    cajaTextoEntradas = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=7, column=1)

    etiquetaB4 = tkinter.Label(
        ventana, text="b4", font="Helvetica 15").grid(row=8, column=0)

    cajaTextoEntradas = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=8, column=1)

    # ds
    etiquetaD = tkinter.Label(
        ventana, text="d", font="Helvetica 15").grid(row=9, column=0)

    cajaTextoEntradas = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=9, column=1)

    boton1 = tkinter.Button(ventana, text="Ingresar",
                            width=35, height=2, command=plot).grid(row=10, column=0, columnspan=2)

    # Plots grids 2 a 7

    # Perturbaciones
    etiquetaPert = tkinter.Label(
        ventana, text="Perturbaciones", font="Helvetica 15").grid(row=0, column=7, columnspan=2)
    etiquetaEscalon = tkinter.Label(
        ventana, text="Esc", font="Helvetica 15").grid(row=1, column=7)
    cajaTextoEscalon = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=1, column=8)
    etiquetaRandom = tkinter.Label(
        ventana, text="Rand", font="Helvetica 15").grid(row=2, column=7)
    cajaTextoRandom = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=2, column=8)

    # u(k)
    etiquetaU = tkinter.Label(
        ventana, text="u(k)", font="Helvetica 15").grid(row=3, column=7, columnspan=2)
    etiquetaEscalon = tkinter.Label(
        ventana, text="Esc", font="Helvetica 15").grid(row=4, column=7)
    cajaTextoEscalon = tkinter.Entry(
        ventana, font="Helvetica 15").grid(row=4, column=8)

    ventana.mainloop()


def printMenu():
    '''
        @name: PrintMenu
        @brief: Prints the menu of options and returns what the user chooses as a string
    '''
    print("1. Declarar coeficientes a\n")
    print("2. Declarar coeficientes b\n")
    print("3. Declarar coeficiente d\n")
    print("4. Declarar coeficiente perturbacion\n")
    print("5. Visualizar ecuacion de diferencias\n")
    print("6. Elegir tipo de señal de entrada\n")
    print("7. Iniciar simulador\n")
    inp = input("Elige tu opcion:\n")
    return inp


def printMenuEntrada():
    '''
        @name: PrintMenu
        @brief: Prints the menu of input options and returns what the user chooses as a string

    '''
    print("1. Escalon Unitario\n")
    print("2. Escalon definido \n")
    print("3. Rampa\n")
    print("4. Archivo\n")
    inp = input("Elige tu opcion:\n")
    return inp

###################
# CODIGO PRINCIPAL
###################


def main():
    printVentana()
    print("First print")

    # Se lee un archivo con los atributos de la clase; ya declarados y se vuelve a declarar la clase con estos atributos

    # MockCode
    #sim = simulador(listcoefa, listcoefb, coefd, coefPert, stepTime)

    sim = simulador()

    # Primer entrada:
    print("Bienvenido al simulador: ¿Que quieres hacer?\n")
    choice = printMenu()

    while (choice != 0):

        if choice == '1':
            print("Declara tus coeficientes con el siguiente formato:\n ")
            stringACoef = input("Ejemplo: 2.31 0.23 0 2 etc.\n")
            sim.listcoefa = [float(x) for x in stringACoef.split(" ")]
            # sim.listcoefa = list(map(float, stringACoef))

        elif choice == '2':
            print("Declara tus coeficientes con el siguiente formato:\n ")
            stringBCoef = input("Ejemplo: 2.31 0.23 0 2 etc. \n")
            sim.listcoefb = [float(x) for x in stringBCoef.split(" ")]
            # sim.listcoefb = list(map(float, stringBCoef))

        elif choice == '3':
            print("Declara un delay entero (d):\n ")
            stringDCoef = input("Ejemplo: 2 \n")
            sim.coefd = [float(x) for x in stringDCoef.split(" ")]
            #sim.coefd = list(map(int, stringDCoef))

        elif choice == '4':
            print("Declara una perturbacion constante (pert):\n ")
            stringDCoefPert = input("Ejemplo: 2 \n")
            sim.coefPert = [float(x) for x in stringDCoefPert.split(" ")]
            #sim.coefd = list(map(int, stringDCoef))

        elif choice == '5':
            sim.printEquation()

        elif choice == '6':
            print("Elige el tipo de señal de entrada:\n")
            choiceInp = printMenuEntrada()
            sim.inpType = int(choiceInp)

        elif choice == '7':
            sim.calculateMaxInpDelay()
            sim.calculateMaxOutDelay()

            while (1):
                print(sim.returnStepResult())

        else:
            print("Invalid command!")

        print("What do you want to do?")
        choice = printMenu()

    return 1
    # Numero de parametros, step time

    # Segunda entrada:

    # Iteracion de parametros A & B

    # Tercera entrada

    # Tipo de senal: Escalon, senoidal, leer de .txt

    # Cuarta entrada

    # Numero de pasos a simular, opcion indefinida para simulacion a tiempo real


main()
