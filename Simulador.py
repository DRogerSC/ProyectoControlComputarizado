import matplotlib
import numpy as np
import pandas as pd

class simulador:
   
    numa = 0
    listcoefa = {}
    numb = 0
    listcoefb = {}
    numc = 0
    listcoefc = {}
    coefd = 0
    coefPert = 0
    stepTime = 0
    maxSteps = 1000
    

def printMenu():
    print("1. Declarar coeficientes a\n")
    print("2. Declarar coeficientes b\n")
    print("3. Declarar coeficientes d\n")
    print("4. Declarar coeficiente perturbacion\n")
    print("5. Visualizar ecuacion de diferencias\n")
    print("6. Elegir tipo de señal de entrada\n")
    print("7. Iniciar simulador\n")
    inp = input("Elige tu opcion:\n")
    return inp

def stringToList():
    return 




def main (argv, argc):
        
    sim = simulador() 
    #Primer entrada:

    print("Bienvenido al simulador: ¿Que quieres hacer?\n")
    choice = printMenu()

    if choice == 1:
        print("Declara tus coeficientes con el siguiente formato:\n ")
        stringACoef = input("Ejemplo: 2.31 0.23 0 2\n")
        sim.listcoefa = list(map(int, stringACoef))
        sim.numa = sim.listcoefa.count()

    elif choice == 2: 
        print("Declara tus coeficientes con el siguiente formato:\n ")
        stringBCoef = input("Ejemplo: 2.31 0.23 0 2\n")
        sim.listcoefb = list(map(int, stringBCoef))
        sim.numb = sim.listcoefb.count()

    elif  choice == 3:

    elif choice == 4:

    elif choice == 5:

    elif choice == 6:
    
        #Numero de parametros, step time
    
    #Segunda entrada: 

        #Iteracion de parametros A & B

    #Tercera entrada

        #Tipo de senal: Escalon, senoidal, leer de .txt

    #Cuarta entrada

        #Numero de pasos a simular, opcion indefinida para simulacion a tiempo real

