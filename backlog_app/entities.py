import os
import csv
import uuid
from datetime import datetime
import plotly.graph_objects as go
from backlog_app.utils import formatear_texto

class Tarea:
    def __init__(self, 
                 id_code:str = None, 
                 titulo:str = None, 
                 descripcion:str = None, 
                 proyecto:str = None,
                 persona_asignada:str = None,
                 fecha_creacion:str = None,
                 en_progreso:str = None,
                 fecha_finalizacion:str = None):

        # Puede ser creada desde:
        # 1. Boton crear tarea
        # 2. Desde csv

        self.id = id_code
        self.titulo = titulo
        self.descripcion = descripcion
        self.proyecto = proyecto
        self.persona_asignada = persona_asignada
        self.fecha_creacion = fecha_creacion
        self.en_progreso = en_progreso
        self.fecha_finalizacion = fecha_finalizacion
        self.formatear_campos()

    def formatear_campos(self):
        if isinstance(self.titulo, str):
            self.titulo = self.titulo.replace('\n', ' ')

        if isinstance(self.descripcion, str):
            self.descripcion = self.descripcion.replace('\n', ' ')

        if isinstance(self.en_progreso, str):
            self.en_progreso = self.en_progreso.lower() == 'true'
    
    def asignar_codigo(self):
        self.id = uuid.uuid4().hex
    
    def asignar_titulo(self, titulo):
        self.titulo = titulo.replace('\n', ' ')
    
    def asignar_descripcion(self, descripcion):
        self.descripcion = descripcion.replace('\n', ' ')
    
    def asignar_proyecto(self, proyecto):
        self.proyecto = proyecto
    
    def asignar_persona(self, persona):
        self.persona_asignada = persona
    
    def iniciar(self):
        self.fecha_creacion = datetime.now().strftime('%Y-%m-%d')
        self.en_progreso = True
    
    def finalizar(self):
        self.fecha_finalizacion = datetime.now().strftime('%Y-%m-%d')
        self.en_progreso = False
    
    def reiniciar(self):
        self.fecha_finalizacion = None
        self.en_progreso = True
    
    def to_csv(self):
        row = [self.id, self.titulo, self.descripcion, self.proyecto, self.persona_asignada, self.fecha_creacion, self.en_progreso, self.fecha_finalizacion]
        return row


class Backlog:
    def __init__(self, integrantes, tareas_file:str = None):
        self.integrantes = integrantes
        self.tareas_file = tareas_file
        self.tareas_en_progreso = []
        self.tareas_finalizadas = []
        self.cargar_tareas()
    
    def cargar_tareas(self):
        self.tareas_en_progreso = []
        self.tareas_finalizadas = []

        if not self.tareas_file:
            return
        
        if not os.path.exists(self.tareas_file):
            with open(self.tareas_file, 'w', newline='', encoding='utf-8') as file:
                csv.writer(file)
        with open(self.tareas_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                tarea = Tarea(
                    id_code = row[0],
                    titulo = row[1],
                    descripcion = row[2],
                    proyecto = row[3],
                    persona_asignada = row[4],
                    fecha_creacion = row[5],
                    en_progreso = row[6],
                    fecha_finalizacion = row[7]
                )
                if tarea.en_progreso:
                    self.tareas_en_progreso.append(tarea)
                else:
                    self.tareas_finalizadas.append(tarea)
    
    def obtener_tareas(self, en_progreso=True):
        self.cargar_tareas()
        if en_progreso:
            return self.tareas_en_progreso
        else:
            return self.tareas_finalizadas
    
    def quitar_del_csv(self, tarea_id):
        with open(self.tareas_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            with open(self.tareas_file, 'w', encoding='utf-8') as file:
                for line in lines:
                    if tarea_id not in line:
                        file.write(line)
    
    def escribir_en_csv(self, tarea):
        with open(self.tareas_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(tarea.to_csv())
    
    def actualizar(self, tarea):
        if tarea.en_progreso:
            self.tareas_en_progreso.append(tarea)
            self.escribir_en_csv(tarea)
        
        if not tarea.en_progreso:
            self.tareas_en_progreso = [t for t in self.tareas_en_progreso if t.id != tarea.id]
            self.tareas_finalizadas.append(tarea)
            self.quitar_del_csv(tarea.id)
            self.escribir_en_csv(tarea)
    
    def modificar(self, tarea):
        self.tareas_en_progreso = [t for t in self.tareas_en_progreso if t.id != tarea.id]
        self.tareas_en_progreso.append(tarea)
        self.quitar_del_csv(tarea.id)
        self.escribir_en_csv(tarea)
    
    def reiniciar(self, tarea):
        self.tareas_finalizadas = [t for t in self.tareas_finalizadas if t.id != tarea.id]
        self.tareas_en_progreso.append(tarea)
        self.quitar_del_csv(tarea.id)
        self.escribir_en_csv(tarea)
        
    
    def crear_tabla(self, backlog_wide, backlog_high, quotient):
        data = []
        integrantes = [f"<b>{integrante}</b>" for integrante in self.integrantes]
        row_wide = int(backlog_wide / quotient)
        for integrante in self.integrantes:
            tareas_integrante = [tarea for tarea in self.tareas_en_progreso if tarea.persona_asignada == integrante]
            tareas_data = [
                f"<b>{formatear_texto(tarea.titulo, row_wide)}</b><br>" \
                f"{formatear_texto(tarea.descripcion, row_wide)}<br>" \
                f"<b>Proyecto:</b> {tarea.proyecto}<br>" \
                f"<a href='?id_tarea={tarea.id}&action=finalizar' target='_self' style='background-color: #ff0000; border: none; color: red; padding: 5px 10px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 4px 2px; cursor: pointer;'><b>Finalizar</b></a>"
                for tarea in tareas_integrante
            ]
            data.append(tareas_data)
        
        # Crear la tabla utilizando Plotly
        fig = go.Figure(data=[go.Table(
            header=dict(values=integrantes, fill_color='paleturquoise', align='left'),
            cells=dict(values=data, fill_color='lavender', align='left')
        )])

        # Configurar el diseño de la tabla
        fig.update_layout(
            autosize=False,
            width=backlog_wide,
            height=backlog_high,
            margin=dict(l=0, r=0, b=0, t=0),
            template='plotly_white'
        )

        return fig



    
