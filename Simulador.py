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

class simulador:

    listcoefa = [1]
    listcoefb = [0, 1]
    coefd = 0
    coefPert = 0
    stepTime = 0
    maxSteps = 1000
    stepNum = 0
    maxOutDelay = 0
    maxInpDelay = 0

    inputMemory = []    #a
    outputMemory = []   #b
                        #perturbation


    def printEquation():
        print("Ecuacion de diferencias:\n\n")
        print("")

    

    #Funcion que a partir de la lista de coeficientes a, calcula el valor maximo que se tiene que guardar del input para calcular el siguiente valor
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
        


     #Funcion que a partir de la lista de coeficientes a, calcula el valor maximo que se tiene que guardar del input para calcular el siguiente valor
    def calculateMaxInpDelay(self):
        '''
        @name: 
        @brief: 
        @param: 
        @return: --
        '''
        self.maxInpDelay = len(self.listcoefb) + self.coefd
        for i in range(self.maxInpDelay):
            self.outputMemory.append(0)



    def returnStepResult(self):
        '''
        @name: 
        @brief: 
        @param:
        @return: --
        '''
        accum = 0
        for i in range(len(self.inputMemory)):
            accum += self.inputMemory[i]*self.listcoefa[i]

        for i in range(len(self.outputMemory)):
            accum += self.outputMemory[i+self.coefd]*self.listcoefb[i+self.coefd]

        self.outputMemory.pop()
        self.outputMemory.append()
        
        return accum
        
    

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
## CODIGO PRINCIPAL
###################

def main (argv, argc):



    #Se lee un archivo con los atributos de la clase; ya declarados y se vuelve a declarar la clase con estos atributos

    #MockCode
    #sim = simulador(listcoefa, listcoefb, coefd, coefPert, stepTime)
    

    sim = simulador() 
    
    #Primer entrada:
    print("Bienvenido al simulador: ¿Que quieres hacer?\n")
    choice = printMenu()

    if choice == 1:
        print("Declara tus coeficientes con el siguiente formato:\n ")
        stringACoef = input("Ejemplo: 2.31 0.23 0 2 etc.\n")
        sim.listcoefa = list(map(float, stringACoef))


    elif choice == 2:
        print("Declara tus coeficientes con el siguiente formato:\n ")
        stringBCoef = input("Ejemplo: 2.31 0.23 0 2 etc. \n")
        sim.listcoefb = list(map(float, stringBCoef))
       

    elif  choice == 3:
        print("Declara un delay entero (d):\n ")
        stringDCoef = input("Ejemplo: 2 \n")
        sim.coefd = list(map(int, stringDCoef))
    

    elif choice == 4:
        print("Declara una perturbacion constante (pert):\n ")
        stringDCoef = input("Ejemplo: 2 \n")
        sim.coefd = list(map(int, stringDCoef))


    elif choice == 5:
        print("Elige el tipo de señal de entrada:\n")
        choiceInp = printMenuEntrada()





    elif choice == 6:
        print("")


    elif choice == 7:

    
        #Numero de parametros, step time
    
    #Segunda entrada: 

        #Iteracion de parametros A & B

    #Tercera entrada

        #Tipo de senal: Escalon, senoidal, leer de .txt

    #Cuarta entrada

        #Numero de pasos a simular, opcion indefinida para simulacion a tiempo real

