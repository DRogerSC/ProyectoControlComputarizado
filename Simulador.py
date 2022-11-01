
import numpy as np

class simulador:

    listcoefa = {1}
    listcoefb = {0, 1}
    listcoefc = {}
    coefd = 0
    coefPert = 0
    stepTime = 0
    maxSteps = 1000
    stepNum = 0

    inputMemory = {}
    outputMemory = {} 


    def printEquation():
        print("Ecuacion de diferencias:\n\n")
        print("")

    

    #Funcion que a partir de la lista de coeficientes a, calcula el valor maximo que se tiene que guardar del input para calcular el siguiente valor
    def calculateMaxInpDelay():

     #Funcion que a partir de la lista de coeficientes a, calcula el valor maximo que se tiene que guardar del input para calcular el siguiente valor
    def calculateMaxOutDelay():



    def returnStepResult():
    


    

def printMenu():
    print("1. Declarar coeficientes a\n")
    print("2. Declarar coeficientes b\n")
    print("3. Declarar coeficiente d\n")
    print("4. Declarar coeficiente perturbacion\n")
    print("5. Visualizar ecuacion de diferencias\n")
    print("6. Elegir tipo de señal de entrada\n")
    print("7. Iniciar simulador\n")
    inp = input("Elige tu opcion:\n")
    return inp









def main (argv, argc):

    #Hay que creer un archivo para no tener que crear los datos cada vez que se inicializa: 

        
    sim = simulador() 
    #Primer entrada:

    print("Bienvenido al simulador: ¿Que quieres hacer?\n")
    choice = printMenu()

    if choice == 1:
        print("Declara tus coeficientes con el siguiente formato:\n ")
        stringACoef = input("Ejemplo: 2.31 0.23 0 2 etc.\n")
        sim.listcoefa = list(map(float, stringACoef))
        sim.numa = sim.listcoefa.count()

    elif choice == 2:
        print("Declara tus coeficientes con el siguiente formato:\n ")
        stringBCoef = input("Ejemplo: 2.31 0.23 0 2 etc. \n")
        sim.listcoefb = list(map(float, stringBCoef))
       

    elif  choice == 3:
        print("Declara tus coeficiente d:\n ")
        stringBCoef = input("Ejemplo: 2.31 0.23 0 2 etc. \n")
        sim.listcoefb = list(map(float, stringBCoef))
    

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

