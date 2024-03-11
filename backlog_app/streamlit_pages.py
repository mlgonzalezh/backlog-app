import streamlit as st
from backlog_app.entities import Tarea, Backlog
from backlog_app.load import leer_integrantes, leer_proyectos
from backlog_app.utils import load_conf

conf = load_conf('conf.yaml')

INTEGRANTES_PATH = conf['INTEGRANTES_PATH']
PROYECTOS_PATH = conf['PROYECTOS_PATH']
TAREAS_PATH = conf['TAREAS_PATH']

BACKLOG_WIDE = conf['BACKLOG_WIDE']
BACKLOG_HIGH = conf['BACKLOG_HIGH']
PIXELS_QUOTIENT = conf['PIXELS_QUOTIENT']

integrantes = leer_integrantes(INTEGRANTES_PATH)
backlog = Backlog(integrantes, TAREAS_PATH)

# Página principal
def pagina_principal():
    st.title('Backlog')
    tareas_en_progreso = backlog.obtener_tareas(en_progreso=True)

    # Verificar si se ha hecho clic en el enlace "Finalizar" de alguna tarea
    id_tarea = st.query_params.get('id_tarea')
    action = st.query_params.get('action')
    if id_tarea and action == 'finalizar':
        tarea = next((tarea for tarea in tareas_en_progreso if tarea.id == id_tarea), None)
        if tarea:
            tarea.finalizar()
            backlog.actualizar(tarea)
            st.query_params.clear()

    # Crear tabla
    fig = backlog.crear_tabla(BACKLOG_WIDE, BACKLOG_HIGH, PIXELS_QUOTIENT)

    # Mostrar la tabla en Streamlit
    st.plotly_chart(fig)

# Página de creación de tareas
def pagina_crear_tarea():
    st.title('Crear Tarea')
    integrantes = leer_integrantes(INTEGRANTES_PATH)
    proyectos = leer_proyectos(PROYECTOS_PATH)

    persona = st.selectbox('Asignar a', integrantes)
    titulo = st.text_input('Nombre de la tarea')
    descripcion = st.text_area('Descripción de la tarea')
    proyecto = st.selectbox('Proyecto', proyectos)

    if st.button('Crear'):
        if persona and titulo and descripcion and proyecto:
            tarea = Tarea()
            tarea.asignar_codigo()
            tarea.asignar_titulo(titulo)
            tarea.asignar_descripcion(descripcion)
            tarea.asignar_proyecto(proyecto)
            tarea.asignar_persona(persona)
            tarea.iniciar()
            backlog.actualizar(tarea)
            st.success('Tarea creada exitosamente')
        else:
            st.error('Por favor, completa todos los campos')

# Página de modificar los campos de una tarea
def pagina_modificar_tarea():
    st.title('Modificar Tarea')
    tareas = backlog.obtener_tareas(en_progreso=True)
    tareas_dict = {f"{tarea.titulo} - {tarea.persona_asignada}": tarea for tarea in tareas}
    tarea = st.selectbox('Selecciona la tarea a modificar', list(tareas_dict.keys()))

    if tarea:
        tarea = tareas_dict[tarea]
        nueva_persona = st.selectbox('Asignar a', integrantes, index=integrantes.index(tarea.persona_asignada))
        nuevo_titulo = st.text_input('Nombre de la tarea', tarea.titulo)
        nueva_descripcion = st.text_area('Descripción de la tarea', tarea.descripcion)
        nuevo_proyecto = st.selectbox('Proyecto', leer_proyectos(PROYECTOS_PATH), index=leer_proyectos(PROYECTOS_PATH).index(tarea.proyecto))

        if st.button('Modificar'):
            tarea.asignar_titulo(nuevo_titulo)
            tarea.asignar_descripcion(nueva_descripcion)
            tarea.asignar_proyecto(nuevo_proyecto)
            tarea.asignar_persona(nueva_persona)
            backlog.modificar(tarea)
            st.success('Tarea modificada exitosamente')

# Página de histórico de tareas
def pagina_historico():
    st.title('Histórico Tareas')
    tareas_finalizadas = backlog.obtener_tareas(en_progreso=False)

    for tarea in tareas_finalizadas:
        st.write(f"**{tarea.titulo}**")
        st.write(f"Asignada a: {tarea.persona_asignada}")
        st.write(f"Descripción: {tarea.descripcion}")
        st.write(f"Proyecto: {tarea.proyecto}")
        st.write(f"Fecha de creación: {tarea.fecha_creacion}")
        st.write(f"Fecha de finalización: {tarea.fecha_finalizacion}")

        if st.button('Recuperar'):
            tarea.reiniciar()
            backlog.reiniciar(tarea)
            st.rerun()
            st.success('Tarea recuperada exitosamente')

        st.write('---')
    
    st.write('---')