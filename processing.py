# En este archivo se procesará la infor de clientes .csv
import csv

# Devuelve la cantidad de clientes.
def contar():
    with open ('clientes.csv', encoding='utf-8') as archivo:
        archivo_csv  = csv.reader(archivo)
        contador = -1
        for row in archivo_csv:
            contador +=1
    return contador


# Devuelve lista de diccionarios
def tabular():
    with open ('clientes.csv', encoding='utf-8') as archivo:
        archivo_csv = csv.reader(archivo)
        lista =[]
        aux = 1
        for row in archivo_csv:
            if aux ==1:
                aux +=1
            else:
                diccionario ={
                'nombre': row[0],
                'edad': row[1],
                'direc': row[2],
                'país': row[3],
                'dni': row[4],
                'fechaAlta': row[5],
                'mail': row[6],
                'trabajo': row[7]
                }
                lista.append(diccionario)
    return lista


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
