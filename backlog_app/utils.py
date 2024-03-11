import yaml
from yaml.loader import SafeLoader

def formatear_texto(texto, ancho_pixel):
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    
    # Definir el número de píxeles por carácter (puedes ajustar este valor según tus necesidades)
    pixeles_por_caracter = 8
    
    for palabra in palabras:
        if len(linea_actual) + len(palabra) <= ancho_pixel // pixeles_por_caracter:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "
    
    if linea_actual:
        lineas.append(linea_actual.strip())
    
    return "<br>".join(lineas)

# Open the file and load the file
def load_conf(yaml_file):
    with open(yaml_file, encoding='utf-8') as f:
        data = yaml.load(f, Loader=SafeLoader)
    return data