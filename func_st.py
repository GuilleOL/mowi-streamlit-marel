from calendar import month
import datetime
from tkinter import Y
import streamlit as st
import sqlalchemy
from sql_engine import sql_engine
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import os 

engine_path = 'mssql+pymssql://Adminalaya:Alaya.2022@mowidbserver.database.windows.net/MowiDB'
engineAzure = sqlalchemy.create_engine(engine_path)

@st.cache
def read_df(dfname):
    return pd.read_feather(dfname)

def center_title(string):
    """
    Retorna texto de entrada centrad en formato HTML.
    Parameters
    ----------
    string : string
        Texto de entrada
    Returns
    -------
    ret: string
        Texto de entrada centrado en formato HTML
    """
    ret = "<h1 style='text-align: center;'> " + string + "</h1>"
    return ret


def head_st(path_base, options = ["Sin opciones"], pass_fname=None):
    """
    Genera encabezado del visualizador.
    Parameters
    ----------
    path_base : string
        Ubicación del repositorio
    Returns
    -------
    page : string
        Página seleccionada
    """
    # Head
    script_path = os.path.dirname(__file__)
    col_logo1, col_titulo, col_logo2 = st.columns([2, 6, 2])
    logo_alaya = Image.open( os.path.join (path_base , 'images','LogoAlaya.png' ))
    logo_mowi = Image.open( os.path.join (path_base , 'images','LogoMowi.png') )
    col_logo1.image(logo_alaya)
    col_logo2.image(logo_mowi)
    
    # SideBar
    stb = st.sidebar
    
    if pass_fname is None:
        st.session_state.show_page = True
        
    if 'show_page' not in st.session_state:
        yamldict = sql_engine.read_yaml(  os.path.join(path_base ,  pass_fname))
        #st.session_state["show_page"] = False 
        user = stb.text_input( "Usuario:" )
        paswd = stb.text_input( "Contraseña:",
                               type="password")
        page = ""
        if user in list(yamldict["users"].keys()):
            if paswd == yamldict["users"][user]:
                st.session_state["show_page"]= True  
        
    #if st.session_state["show_page"] == True:
    if 'show_page' not in st.session_state:
        page = ""
    else: 
        stb.markdown(center_title('Seleccione Vista:'),
                            unsafe_allow_html=True)
        page = stb.selectbox("", options )
        col_titulo.markdown(center_title(page), unsafe_allow_html=True)

    return page


def pieza_a_pieza(dfname):
    #df = read_df(dfname)
    
    # SideBar
    stb = st.sidebar
    
    stb.write("En este set de datos se puede hacer un análisis de los datos tomados por la marel.")
    
    stb.markdown(center_title('Seleccionar fecha por:'),
                 unsafe_allow_html=True)
    periodo = stb.selectbox("", ["","Anual","Mensual","Semanal","Diario","Un día"])
    
    if periodo == "":
        return 
    if periodo == "Un día":
        fecha_inicio = stb.date_input("Análisis día", datetime.date(2022, 1, 3))
        fecha_final = fecha_inicio + datetime.timedelta(days=1)
                
        #mask = (df['AlaImpPiezaWfeFechaHora'] >= pd.to_datetime(fecha_inicio) ) & (df['AlaImpPiezaWfeFechaHora'] < pd.to_datetime(fecha_final) )

    else:    
        stb.write("Informes de la Marel")
        col_izq, col_der = stb.columns([3, 3])
        if periodo=="Diario":
            fecha_inicio = col_izq.date_input("Fecha inicial", datetime.date(2022, 2, 5)) 
        elif periodo=="Semanal":
            fecha_inicio = col_izq.date_input("Fecha inicial", datetime.date(2021, 10, 5)) 
        elif periodo=="Mensual":
            fecha_inicio = col_izq.date_input("Fecha inicial", datetime.date(2021, 10, 5)) 
        else:
            fecha_inicio = col_izq.date_input("Fecha inicial", datetime.date(2019, 2, 5)) 
        fecha_final = col_der.date_input("Fecha final", datetime.date(2022, 2, 9)) 
        if fecha_inicio >= fecha_final: 
            stb.error('No puede elegir una fecha final que termine antes que la fecha inicial.') 
            return
        if periodo=="Diario":
            if  fecha_final - fecha_inicio > datetime.timedelta(days= 8): 
                stb.error('No se puede elegir con una diferencia de más de 8 días') 
                return
        if periodo=="Semanal":
            if  fecha_final - fecha_inicio > datetime.timedelta(weeks= 52): 
                stb.error('No se puede elegir con una diferencia de más de 52 semanas') 
                return
        if periodo=="Mensual":
            if  fecha_final - fecha_inicio > datetime.timedelta(weeks= 105): 
                stb.error('No se puede elegir con una diferencia de más de 24 meses') 
                return


    stb.markdown(center_title('Filtrar por:'),
                 unsafe_allow_html=True)
    

    if st.button("Graficar"):
        ### Aquí define el df
        query1 = """select * from [dbo].[vAlaya_recepcion] where AlaImpPiezaWfeFechaHora >= '{}' and AlaImpPiezaWfeFechaHora < '{}'""".format(fecha_inicio, fecha_final)
        ## EngineAzure
        df = pd.read_sql_query(query1, con=engineAzure, index_col=None)
        
        #
        ## Filtro de fechas
        if periodo == "Un día":  
            mask = (df['AlaImpPiezaWfeFechaHora'] >= pd.to_datetime(fecha_inicio) ) & (df['AlaImpPiezaWfeFechaHora'] < pd.to_datetime(fecha_final) )
        else:
            mask = (df['AlaImpPiezaWfeFechaHora'] >= pd.to_datetime(fecha_inicio) ) & (df['AlaImpPiezaWfeFechaHora'] < pd.to_datetime(fecha_final) )
        df = df[mask]
        
        centro = stb.selectbox("Centro:", [''] + list(df['AlaImpPiezaWfeCentro'].unique()) )
        jaula = stb.selectbox("Jaula:", [''] + list(df['AlaImpPiezaWfeJaula'].unique()) )
        lote = stb.selectbox("Lote:", [''] + list(df['AlaImpPiezaWfeLote'].unique()) )
        
        if centro!='':
            df = df[df['AlaImpPiezaWfeCentro'] == centro]
        if jaula!='':
            df = df[df['AlaImpPiezaWfeJaula'] == jaula]
        if lote!='':
            df = df[df['AlaImpPiezaWfeLote'] == lote]
        df['AlaImpPiezaWfeFechaHora'] = pd.to_datetime(df['AlaImpPiezaWfeFechaHora'])
        if len(df) == 0:
            st.warning('Sin registros en el día ' + str(fecha_inicio) ) 
            return
        st.write("Vista Previa:")  
        st.dataframe(df.head(10))
        ### Calculo de grafico y etc xD 
        
        if periodo == "Un día":  
            fig = px.histogram(df, x='AlaImpPiezaWfePesoNeto' )
            fig.update_layout(width = 600, height = 600, title = 'Peso salmón en marel  ' + str(fecha_inicio))
            col1, col2= st.columns(2)
            col1.plotly_chart(fig)
            
            fig2 = px.histogram(df, x='AlaImpPiezaWfePesoNeto',color = 'AlaImpPiezaWfeCentro' )
            fig2.update_layout(width = 600, height = 600, title = 'Peso salmón en marel  ' + str(fecha_inicio))
            col2.plotly_chart(fig2)
            
            df_mean = pd.DataFrame.from_dict( {"Peso Neto Promedio": [df['AlaImpPiezaWfePesoNeto'].mean()],
                                            "Peso Medio de salmones": [df['AlaImpPiezaWfePesoNeto'].median()],
                                            "Total Salmones": [df['AlaImpPiezaWfePesoNeto'].count()],
                                            "Peso Neto Total": [df['AlaImpPiezaWfePesoNeto'].sum()]
                                            }, columns = ["Total"], orient= "index")
                        
            for centro in list(df['AlaImpPiezaWfeCentro'].unique()):
                dfc = df[df['AlaImpPiezaWfeCentro'] == centro]
                st.write(centro)
                dfc_mean = pd.DataFrame.from_dict( {"Peso Neto Promedio": [dfc['AlaImpPiezaWfePesoNeto'].mean()],
                                                "Peso Medio de salmones": [dfc['AlaImpPiezaWfePesoNeto'].median()],
                                                "Total Salmones": [dfc['AlaImpPiezaWfePesoNeto'].count()],
                                                "Peso Neto Total": [dfc['AlaImpPiezaWfePesoNeto'].sum()]
                                                }, columns = [centro], orient= "index")
                df_mean = df_mean.join(dfc_mean)
            st.dataframe(df_mean)
            
        
        else:     
            if periodo=="Diario": freq = 'D'
            if periodo=="Semanal": freq = 'W'
            if periodo=="Mensual": freq = 'MS'
            if periodo=="Anual": freq = 'A'
            periodos = pd.date_range(start= fecha_inicio,end= fecha_final, freq= freq ).tolist()
            periodos.append(fecha_final)
            if periodos == []:
                periodos = [fecha_inicio, fecha_final]
                st.warning("El periodo elegido es menor al que se quiere analizar")
            for index, value in enumerate(periodos[:-1]):  
                mask_date = (df['AlaImpPiezaWfeFechaHora'] >= pd.to_datetime(periodos[index]) ) & (df['AlaImpPiezaWfeFechaHora'] <  pd.to_datetime(periodos[index+1]) )
                df2  = df[mask_date]
                if len(df2) == 0:
                    st.warning('Sin registros en el periodo Desde:' + str(periodos[index]).split(" ")[0]  + ' - Hasta:'  + str(periodos[index+1]).split(" ")[0]  )
                else:
                    fig = px.histogram(df2, x='AlaImpPiezaWfePesoNeto' )
                    fig.update_layout(width = 600, height = 600, title = 'Peso salmón en marel  Desde:' + str(periodos[index]).split(" ")[0]  + ' - Hasta:'  + str(periodos[index+1]).split(" ")[0]  )
                    fig2 = px.histogram(df, x='AlaImpPiezaWfePesoNeto',color = 'AlaImpPiezaWfeCentro' )
                    fig2.update_layout(width = 600, height = 600, title = 'Peso por Centro' )
                    fig2.update_layout(barmode='overlay')
                    col1, col2= st.columns(2)
                    col1.plotly_chart(fig)
                    col2.plotly_chart(fig2)
                    df_mean = pd.DataFrame.from_dict( {"Peso Neto Promedio": [df2['AlaImpPiezaWfePesoNeto'].mean()],
                                                    "Peso Medio de salmones": [df2['AlaImpPiezaWfePesoNeto'].median()],
                                                    "Total Salmones": [df2['AlaImpPiezaWfePesoNeto'].count()],
                                                    "Peso Neto Total": [df2['AlaImpPiezaWfePesoNeto'].sum()]
                                                    },columns = ["Total"],orient= "index")
                    
                    for centro in list(df2['AlaImpPiezaWfeCentro'].unique()):
                        dfc = df2[df2['AlaImpPiezaWfeCentro'] == centro]
                        dfc_mean = pd.DataFrame.from_dict( {"Peso Neto Promedio": [dfc['AlaImpPiezaWfePesoNeto'].mean()],
                                                        "Peso Medio de salmones": [dfc['AlaImpPiezaWfePesoNeto'].median()],
                                                        "Total Salmones": [dfc['AlaImpPiezaWfePesoNeto'].count()],
                                                        "Peso Neto Total": [dfc['AlaImpPiezaWfePesoNeto'].sum()]
                                                        }, columns = [centro], orient= "index")
                        df_mean = df_mean.join(dfc_mean)
                    st.dataframe(df_mean)
            pass

def readme( sdate ):
    #df = read_df(dfname)
    #st.dataframe(df.head(10))
    st.write(" Bienvenido a la plataforma de datos mowi, estos set de datos fueron actualizados el día {}".format(sdate))
    pass

def consumos(dfname):
    df = read_df(dfname)
    st.dataframe(df.head(10))
    pass
def produccion(dfname):
    df = read_df(dfname)
    st.dataframe(df.head(10))
    pass
def bateas(dfname):
    df = read_df(dfname)
    st.dataframe(df.head(10))
    pass