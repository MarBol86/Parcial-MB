# En este archivo se procesará la infor de clientes .csv
import csv

# Devuelve la cantidad de clientes.
def contar(lista):
    return len(lista)


#Devuelve una lista de los encabezados del csv
def createHeaders():
    with open ('clientes.csv', encoding='utf-8') as archivo:
        archivo_csv = csv.reader(archivo)
        return next(archivo_csv)


# Devuelve lista de listas con las rows
def createRows():
    with open ('clientes.csv', encoding='utf-8') as archivo:
        archivo_csv = csv.reader(archivo)
        registro = next(archivo_csv)
        registro = next(archivo_csv)
        lista =[]
        while (registro):
            lista2 = []
            for element in registro:
                lista2.append(element)
            lista.append(lista2)
            registro = next(archivo_csv, None)
    return lista


# Devuelve una lista con lo encontrado.
def searchCountry(cadena):
    lista= createRows()
    newlist=[]
    cadena = cadena.lower()
    for element in lista:
        if cadena in element[3].lower():          
            if element[3] not in newlist:
                newlist.append(element[3])
    return newlist


# Devuelve una lista de listas con los clientes por país.
def rowsCountry(país):
    lista= createRows()
    newlist=[]
    for element in lista:
        if país ==element[3]:          
            newlist.append(element)
    return newlist


# Devuelve true si el usuario ya existe
def existir(userName):
    with open ('usuarios') as archivo:
        archivo_csv = csv.reader(archivo)
        try:
            for row in archivo_csv:
                if userName == row[0]:
                    return True
            return False   
        except IndexError:
            pass  
