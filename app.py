import streamlit as st
from backlog_app.streamlit_pages import pagina_principal, pagina_crear_tarea, pagina_modificar_tarea, pagina_historico

def main():
    # Configurar el diseño de la página
    st.set_page_config(page_title='Backlog', page_icon='📎', layout="wide")

    # Menú de navegación
    menu = ['Backlog', 'Crear Tarea', 'Modificar Tarea', 'Histórico Tareas']
    choice = st.sidebar.selectbox('Selecciona una página', menu)

    if choice == 'Backlog':
        pagina_principal()
    elif choice == 'Crear Tarea':
        pagina_crear_tarea()
    elif choice == 'Modificar Tarea':
        pagina_modificar_tarea()
    else:
        pagina_historico()

if __name__ == '__main__':
    main()