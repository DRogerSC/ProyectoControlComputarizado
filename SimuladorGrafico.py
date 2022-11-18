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
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

ventana = tkinter.Tk()
ventana.geometry("1200x700")

matplotlib.use("Qt5agg")


class simulador:

    listcoefa = [1]
    listcoefb = [0, 1]
    result = []
    coefd = 0
    coefPert = 0
    UnitLadderNo = 0
    maxSteps = 1000
    stepAmplitude = 0
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
        strEquation = 'c(k) = '
        for x in range(len(self.listcoefa)):
            strEquation += str(self.listcoefa[x])+'c(k - '+str((x+1))+') + '
        strEquation += str(str(self.listcoefb[0]) +
                           'm(k - ' + str(self.coefd) + ') + ')
        for x in range(1, len(self.listcoefb), 1):
            strEquation += str(str(self.listcoefb[x]) +
                               'm(k - '+str((x+1))+' - ' + str(self.coefd) + ') + ')
        strEquation += str(self.coefPert)
        print(strEquation)

    # Funcion que a partir de la lista de coeficientes a, calcula el valor maximo que se tiene que guardar del input para calcular el siguiente valor

    def calculateMaxOutDelay(self):
        '''
        @name: calculateMaxOutDelay
        @brief: This script takes the length of the a coefficient list and uses it to calculate a maximum
        @param: 
        @return: --
        '''
        self.outputMemory.clear()

        self.maxOutDelay = len(self.listcoefa)
       
        if self.maxOutDelay == 0:
            print("Error:Calculated 0 Inp delay using:")
            print("List:" + str(self.listcoefa))

        for i in range(self.maxOutDelay):
            self.outputMemory.append(0)
        self.hasInitializedOutput = True

        print("Initialized Output memory to: ")
        print(self.outputMemory)

     # Funcion que a partir de la lista de coeficientes a, calcula el valor maximo que se tiene que guardar del input para calcular el siguiente valor

    def calculateMaxInpDelay(self):
        '''
        @name: calculateMaxInpDelay
        @brief: 
        @param: 
        @return: --
        '''
        self.inputMemory.clear()

        self.maxInpDelay = len(self.listcoefb) + self.coefd
        print("MaxInpDelay:")
        print(self.maxInpDelay)
        if self.maxInpDelay == 0:
            print("Error:Calculated 0 Inp delay using:")
            print("List:" + str(self.listcoefb))
            print("Coefd:" + str(self.coefd))

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
            else:
                print("Error: EntryType not specified")
        self.hasInitializedInput = True

        print("Initialized input memory to: ")
        print(self.inputMemory)
        return


  
    def returnStepResult(self):
        '''
        @name: returnStepResult
        @brief: Calcula la salida en el siguiente step
        @param:
        @return: --
        '''
        self.updatesIfCanSimulate()
        if (self.canSimulate):
            accum = 0
            for i in range(len(self.outputMemory)):
                accum += self.outputMemory[i]*self.listcoefa[i]

            for i in range(len(self.inputMemory)-int(self.coefd)):
                accum += self.inputMemory[i +
                                          int(self.coefd)] * self.listcoefb[i]

            self.outputMemory.pop()
            self.outputMemory.insert(0, accum)

            if self.inpType == 1:  # UNITARIO
                self.inputMemory.pop()
                self.inputMemory.insert(0, 1)
            elif self.inpType == 2:  # DEFINIDO
                self.inputMemory.pop()
                self.inputMemory.insert(0, self.stepAmplitude)
            elif self.inpType == 3:  # RAMPA
                self.inputMemory.pop()
                self.inputMemory.insert(0, self.returnNextRamp())
                pass
            elif self.inpType == 4:  # ARCHIVA
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

    # Updates and informs if everything necessary to simulate is ready
    def updatesIfCanSimulate(self):
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
    


##Funcion para parsear strings vacios como 0

def parseStringToSim(entryStr: str):
    if entryStr == '':
        return 0
    else:
        return float(entryStr)


####################################################################################################
#####   Funciones que usa la interfaz
####################################################################################################



##Funcion 
def submitFunction(sim: simulador):
    print("Pressed submit!")

    
    # Get data of a1 store in a1
    a1 = parseStringToSim(cajaTextoEntradasA1.get())  
    # Get data of a2 store in a2
    a2 = parseStringToSim(cajaTextoEntradasA2.get())  
    # Get data of a3 store in a3
    a3 = parseStringToSim(cajaTextoEntradasA3.get())  
    # Get data of a4 store in a4
    a4 = parseStringToSim(cajaTextoEntradasA4.get())  

    #Update global simulator object's list of a coeff
    sim.listcoefa = [a1, a2, a3, a4]
    sim.hasDeclaredCoefA = True

    # Get data of b0
    b0 = parseStringToSim(cajaTextoEntradasB0.get())  
    # Get data of b1
    b1 = parseStringToSim(cajaTextoEntradasB1.get())  
    # Get data of b2
    b2 = parseStringToSim(cajaTextoEntradasB2.get())  
    # Get data of b3
    b3 = parseStringToSim(cajaTextoEntradasB3.get())  

    #Update global simulator object's list of b coeff
    sim.listcoefb = [b0, b1, b2, b3]
    sim.hasDeclaredCoefB = True

    # Get data of d
    d = parseStringToSim(cajaTextoEntradasD.get())
    
    ##Update global simulator object's d coeff
    sim.coefd = d
    sim.hasDeclaredCoefD = True

    #Initializes global simulator object's inputMemory
    sim.calculateMaxInpDelay()

    #Initializes global simulator object's outputMemory
    sim.calculateMaxOutDelay()

    ##TEMP PERT DECLARATION
    sim.coefPert = 0
    sim.hasDeclaredPert = True

    ##TEMP ENTRY TYPE DECLARATION
    sim.inpType = 2
    sim.hasDeclaredEntry = True
    return


def pauseFunction():
    global start
    start = False
    return


def startFunction():
    global start
    start = True
    return


def resetFunction(listInput: list, listOutput: list, listTime: list):
    # Resets graph
    listInput.clear()
    listOutput.clear()
    listTime.clear()
    plt.clf()
    pass

def updatePert(sim: simulador):
    pert = parseStringToSim(cajaTextoMagnitudPert.get())
    sim.coefPert = pert
    pass

def updateStep(sim: simulador):
    stepMagnitude = parseStringToSim(cajaTextoEscalon.get())
    sim.stepAmplitude = stepMagnitude
    pass



def updateControllerParams(control: simulador):
    Kc = parseStringToSim(cajaTextoKc.get()) 
    Ti = parseStringToSim(cajaTextoTi.get())
    Td = parseStringToSim(cajaTextoTd.get())
    Tint = parseStringToSim(cajaTextoIntervalo.get())

    b0 =  Kc * (1 + Tint/Ti + Td/Tint)
    b1 =  Kc * (-1-(2*Td/Tint))
    b2 =  Kc * (Td/Tint)

    control.listcoefa = [1]
    control.hasDeclaredCoefA = True
    control.listcoefb = [b0, b1, b2]
    control.hasDeclaredCoefB = True
    control.coefd = 0
    control.hasDeclaredCoefD = True
    control.coefPert = 0
    control.hasDeclaredPert = True
    control.inpType = 2 # Tipo Escalon
    control.hasDeclaredEntry = True

    control.calculateMaxInpDelay()
    control.calculateMaxOutDelay()
    pass

def updateRef(var):
    var = parseStringToSim(cajaTextoRef.get())
    return 

def updateMode():
    choice = choiceMode.get()

    if(choice == 0):        # MANUAL
        cajaTextoEscalon.config(state="normal")
        cajaTextoRef.config(state="disabled")
        pass
    elif (choice == 1):     # AUTO
        cajaTextoEscalon.config(state="disabled")
        cajaTextoRef.config(state="normal")
        pass
    else:
        print("Invalid Input")

def updateDecl():
    choice = choiceDecl.get()

    if(choice == 1):        # PRIMER ORDEN
        cajaTextoEntradasA1.config(state="disabled")
        cajaTextoEntradasA2.config(state="disabled")
        cajaTextoEntradasA3.config(state="disabled")
        cajaTextoEntradasA4.config(state="disabled")
        cajaTextoEntradasB0.config(state="disabled")
        cajaTextoEntradasB1.config(state="disabled")
        cajaTextoEntradasB2.config(state="disabled")
        cajaTextoEntradasB3.config(state="disabled")
        cajaTextoEntradasD.config(state="disabled")
        cajaTextoEntradaK.config(state="normal")
        cajaTextoEntradaTau.config(state="normal")
        cajaTextoEntradaTetaPrima.config(state="normal")
        pass

    elif (choice == 0):     # ARX
        cajaTextoEntradasA1.config(state="normal")
        cajaTextoEntradasA2.config(state="normal")
        cajaTextoEntradasA3.config(state="normal")
        cajaTextoEntradasA4.config(state="normal")
        cajaTextoEntradasB0.config(state="normal")
        cajaTextoEntradasB1.config(state="normal")
        cajaTextoEntradasB2.config(state="normal")
        cajaTextoEntradasB3.config(state="normal")
        cajaTextoEntradasD.config(state="normal")
        cajaTextoEntradaK.config(state="disabled")
        cajaTextoEntradaTau.config(state="disabled")
        cajaTextoEntradaTetaPrima.config(state="disabled")

        pass
    else:
        print("Invalid Input")



####################################################################################################
#####   Fin funciones que usa la interfaz
####################################################################################################


###################
# CODIGO PRINCIPAL
###################


# Variables/Funciones llevadas a cabo por la interfaz graficas

globalSim = simulador()
controlador = simulador()


def main():
    
    global start
    global showInterface
    global plotOutput
    global plotInput
    global plotTime
    global isControlled

    start = False
    isControlled = False
 
    plotOutput = []
    plotInput = []
    plotTime = []

    print("Inicializando ventana!")

    showInterface = True
    plt.ion()
    plt.figure(figsize=(5, 5))
    plt.close(1)
    lastResult = 0
    plt.show(block=False)

    ##Funcion necesaria para que la ventana grafica no agarre focus al inicializarse
    def mypause(interval):
        backend = plt.rcParams['backend']
        if backend in matplotlib.rcsetup.interactive_bk:
            figManager = matplotlib._pylab_helpers.Gcf.get_active()
            if figManager is not None:
                canvas = figManager.canvas
                if canvas.figure.stale:
                    canvas.draw()
                canvas.start_event_loop(interval)
                return

    # Primer entrada:
    while (showInterface):
        ventana.update_idletasks()
        ventana.update()
        updateMode()
        updateDecl()
        updatePert(globalSim)
        if choiceMode.get() == 0: #Manual
            isControlled = False
        else:
            isControlled = True
        while(start):
            ventana.update_idletasks()
            ventana.update()
            referencia = lastResult
           
            ##Debugging lines
            ##globalSim.updatesIfCanSimulate()
            ##print(globalSim.canSimulate)

            if isControlled:
                ##Para manipular el valor de entrada, ponemos el inptype en 2 (Tipo escalon definido)
                ##El valor de entrada directamente correspondera al atributo 'stepAmplitude
                
                #Hace un step de la planta
                result = float(globalSim.returnStepResult())
                
                #Actualiza la referencia en el valor planta
                updateRef(referencia)
                error = referencia - result
                controlador.stepAmplitude = error
                entradaPlanta = float(controlador.returnStepResult())
                globalSim.stepAmplitude = entradaPlanta

                print(result)
                plotOutput.append(result)
                plotInput.append(globalSim.inputMemory[0])
                plotTime = range(len(plotOutput))
                arrPlotOutput = np.array(plotOutput)
                arrPlotInput = np.array(plotInput)
                arrPlotTime = np.array(plotTime)



                pass
            else:
                updateStep(globalSim)
                lastResult = float(globalSim.returnStepResult())
                print(lastResult)
                plotOutput.append(lastResult)
                plotInput.append(globalSim.inputMemory[0])
                plotTime = range(len(plotOutput))
                arrPlotOutput = np.array(plotOutput)
                arrPlotInput = np.array(plotInput)
                arrPlotTime = np.array(plotTime)
         
            plt.plot(arrPlotTime, arrPlotOutput)
            plt.plot(arrPlotTime, arrPlotInput)
            mypause(0.5)
       
    return 0


####################################################################################################
#####   INICIO INTERFAZ
####################################################################################################

choiceDecl = tkinter.IntVar()
cajaOpcionManual = tkinter.Radiobutton(ventana, text="ARX", variable=choiceDecl, value = 0)
cajaOpcionManual.grid(row=0, column=1)
cajaOpcionAuto = tkinter.Radiobutton(ventana, text="Ec. Prim. Ord.", variable=choiceDecl, value = 1)
cajaOpcionAuto.grid(row=0, column=3)

etiqueta = tkinter.Label(ventana, text="Entradas ARX:",
                         font="Helvetica 15")
etiqueta.grid(row=1, column=0, columnspan=2)
# Estas son las as
etiquetaA1 = tkinter.Label(
    ventana, text="a1", font="Helvetica 15")
etiquetaA1.grid(row=2, column=0)
cajaTextoEntradasA1 = tkinter.Entry(
    ventana,  font="Helvetica 15")
cajaTextoEntradasA1.grid(row=2, column=1)
etiquetaA2 = tkinter.Label(
    ventana, text="a2", font="Helvetica 15")
etiquetaA2.grid(row=3, column=0)
cajaTextoEntradasA2 = tkinter.Entry(
    ventana,  font="Helvetica 15")
cajaTextoEntradasA2.grid(row=3, column=1)
etiquetaA3 = tkinter.Label(
    ventana, text="a3", font="Helvetica 15")
etiquetaA3.grid(row=4, column=0)
cajaTextoEntradasA3 = tkinter.Entry(
    ventana,  font="Helvetica 15")
cajaTextoEntradasA3.grid(row=4, column=1)
etiquetaA4 = tkinter.Label(
    ventana, text="a4", font="Helvetica 15")
etiquetaA4.grid(row=5, column=0)
cajaTextoEntradasA4 = tkinter.Entry(
    ventana,  font="Helvetica 15")
cajaTextoEntradasA4.grid(row=5, column=1)
# bs
etiquetaB0 = tkinter.Label(
    ventana, text="b0", font="Helvetica 15")
etiquetaB0.grid(row=6, column=0)

cajaTextoEntradasB0 = tkinter.Entry(
    ventana,  font="Helvetica 15")
cajaTextoEntradasB0.grid(row=6, column=1)

etiquetaB1 = tkinter.Label(
    ventana, text="b1", font="Helvetica 15")
etiquetaB1.grid(row=7, column=0)

cajaTextoEntradasB1 = tkinter.Entry(
    ventana,  font="Helvetica 15")
cajaTextoEntradasB1.grid(row=7, column=1)

etiquetaB2 = tkinter.Label(
    ventana, text="b2", font="Helvetica 15")
etiquetaB2.grid(row=8, column=0)

cajaTextoEntradasB2 = tkinter.Entry(
    ventana,  font="Helvetica 15")
cajaTextoEntradasB2.grid(row=8, column=1)

etiquetaB3 = tkinter.Label(
    ventana, text="b3", font="Helvetica 15")
etiquetaB3.grid(row=9, column=0)

cajaTextoEntradasB3 = tkinter.Entry(
    ventana,  font="Helvetica 15")
cajaTextoEntradasB3.grid(row=9, column=1)

# ds
etiquetaD = tkinter.Label(
    ventana, text="d", font="Helvetica 15")
etiquetaD.grid(row=10, column=0)

cajaTextoEntradasD = tkinter.Entry(
    ventana, font="Helvetica 15")
cajaTextoEntradasD.grid(row=10, column=1)

##BOTONES

botonSubmit = tkinter.Button(ventana, text="Submit Params",
                             width=35, height=2, command=lambda:submitFunction(globalSim))
botonSubmit.grid(row=11, column=0, columnspan=2)
botonStart = tkinter.Button(ventana, text="Start Sim",
                            width=35, height=2, command=lambda:startFunction())
botonStart.grid(row=12, column=0, columnspan=2)
botonReset = tkinter.Button(ventana, text="Reset Graph",
                            width=35, height=2, command=lambda:resetFunction(plotInput, plotOutput, plotTime))
botonReset.grid(row=14, column=0, columnspan=2)
botonPause = tkinter.Button(ventana, text="Pause Sim",
                            width=35, height=2, command=lambda:pauseFunction())
botonPause.grid(row=13, column=0, columnspan=2)

# Cajas de declaracion de ecuacion de primer orden
etiqueta = tkinter.Label(ventana, text="Entradas Ec. Prim. Ord:",
                         font="Helvetica 15")
etiqueta.grid(row=1, column=2, columnspan=2)

etiquetaK = tkinter.Label(
    ventana, text="K", font="Helvetica 15")
etiquetaK.grid(row=2, column=2)
cajaTextoEntradaK = tkinter.Entry(
    ventana, font="Helvetica 15")
cajaTextoEntradaK.grid(row=2, column=3)
etiquetaTau = tkinter.Label(
    ventana, text="Tau", font="Helvetica 15")
etiquetaTau.grid(row=3, column=2)
cajaTextoEntradaTau = tkinter.Entry(
    ventana, font="Helvetica 15")
cajaTextoEntradaTau.grid(row=3, column=3)
etiquetaTetaPrima = tkinter.Label(
    ventana, text="TetaP", font="Helvetica 15")
etiquetaTetaPrima.grid(row=4, column=2)
cajaTextoEntradaTetaPrima = tkinter.Entry(
    ventana, font="Helvetica 15")
cajaTextoEntradaTetaPrima.grid(row=4, column=3)


# Plots grids columns 2 a 7
# etiquetaYK = tkinter.Label(ventana, text="y(k)", font="Helvetica 15").grid(
#     row=0, column=3, columnspan=5)
# # 'y' y 't' son los arreglos con los datos ahi cambiaria a las C's y M's
# y = []
# t = []
# for x in list(range(0, 101)):
#     t.append(x/15.87)
# for x in t:
#     y.append(x+1)
# figure = plt.figure(figsize=(5, 4), dpi=100)
# figure.add_subplot(111).plot(t, y)
# # ventana es el objeto que contiene todo lo que se quiere desplegar y figure es la figura de la tabla.
# chart = FigureCanvasTkAgg(figure, ventana)
# chart.get_tk_widget().grid(row=2, column=3, columnspan=5, rowspan=10)



##Intervalo de muestreo
etiquetaIntervaloMuestreo = tkinter.Label(
    ventana, text="Intervalo de muestreo", font="Helvetica 15").grid(row=0, column=9, columnspan=2)
etiquetaIntervalo = tkinter.Label(
    ventana, text="Int", font="Helvetica 15")
etiquetaIntervalo.grid(row=1, column=9)
cajaTextoIntervalo = tkinter.Entry(
    ventana, font="Helvetica 15")
cajaTextoIntervalo.grid(row=1, column=10)


# Perturbaciones
etiquetaPert = tkinter.Label(
    ventana, text="Perturbaciones", font="Helvetica 15").grid(row=2, column=9, columnspan=2)
etiquetaMagnitudPert = tkinter.Label(
    ventana, text="Magn", font="Helvetica 15")
etiquetaMagnitudPert.grid(row=3, column=9)
cajaTextoMagnitudPert = tkinter.Entry(
    ventana, font="Helvetica 15")
cajaTextoMagnitudPert.grid(row=3, column=10)


# u(k)
etiquetaUk = tkinter.Label(ventana, text="u(k)", font="Helvetica 15").grid(row=4, column=9, columnspan=2)
etiquetaEscalon = tkinter.Label(ventana, text="Esc", font="Helvetica 15")
etiquetaEscalon.grid(row=5, column=9)
cajaTextoEscalon = tkinter.Entry(ventana, font="Helvetica 15")
cajaTextoEscalon.grid(row=5, column=10)

#Controlador
etiquetaControlPID = tkinter.Label(ventana, text="Params Control PID", font="Helvetica 15").grid(row=6, column=9, columnspan=2)
etiquetaKc = tkinter.Label(ventana, text="Kc", font="Helvetica 15")
etiquetaKc.grid(row=7, column=9)
cajaTextoKc = tkinter.Entry(ventana, font="Helvetica 15")
cajaTextoKc.grid(row=7, column=10)
etiquetaTi = tkinter.Label(ventana, text="Ti", font="Helvetica 15")
etiquetaTi.grid(row=8, column=9)
cajaTextoTi = tkinter.Entry(ventana, font="Helvetica 15")
cajaTextoTi.grid(row=8, column=10)
etiquetaTd = tkinter.Label(ventana, text="Td", font="Helvetica 15")
etiquetaTd.grid(row=9, column=9)
cajaTextoTd = tkinter.Entry(ventana, font="Helvetica 15")
cajaTextoTd.grid(row=9, column=10)
#
botonSubmitCont = tkinter.Button(ventana, text="Submit Ctrl Params",
                             width=35, height=2, command=lambda:updateControllerParams(controlador))
botonSubmitCont.grid(row=10, column=9, columnspan=2)

#Referencia
etiquetaReferencia = tkinter.Label(ventana, text="Referencia", font="Helvetica 15").grid(row=11, column=9, columnspan=2)
etiquetaRef = tkinter.Label(ventana, text="ReF", font="Helvetica 15")
etiquetaRef.grid(row=12, column=9)
cajaTextoRef = tkinter.Entry(ventana, font="Helvetica 15")
cajaTextoRef.grid(row=12, column=10)

#Modo
etiquetaManOAuto = tkinter.Label(ventana, text="Manual o Auto", font="Helvetica 15").grid(row=13, column=9, columnspan=2)
choiceMode = tkinter.IntVar()
cajaOpcionManual = tkinter.Radiobutton(ventana, text="Manual", variable=choiceMode, value = 0)
cajaOpcionManual.grid(row=14, column=9)
cajaOpcionAuto = tkinter.Radiobutton(ventana, text="Auto", variable=choiceMode, value = 1)
cajaOpcionAuto.grid(row=14, column=10)




    

####################################################################################################
#####   FIN INTERFAZ
####################################################################################################


main()
