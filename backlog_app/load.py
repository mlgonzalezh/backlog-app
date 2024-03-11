import csv

def leer_integrantes(integrantes_file):
    integrantes = []
    with open(integrantes_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            integrantes.append(row[0])
    return integrantes

def leer_proyectos(proyectos_file):
    proyectos = []
    with open(proyectos_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            proyectos.append(row[0])
    return proyectos