import streamlit as st
import pandas as pd
import os 
from func_st import  head_st, readme , pieza_a_pieza , consumos , produccion , bateas 

st.set_page_config(page_title="Despcritive - Mowi",
                   page_icon="🐟" ,
                   layout="wide"
                   )


## Preload configuration
#option = head_st("./", options=["","Bateas","Pieza a pieza", "Consumos","Produccion"] ,pass_fname="./conf.yml")

script_path = os.path.dirname(__file__)
option = head_st( script_path , options=["","Pieza a pieza", "Consumos", "Produccion", "Bateas"] ,pass_fname="./conf.yml")


## Selección de menu
if option == "Pieza a pieza":
    pieza_a_pieza( os.path.join( script_path, "data","piezas.feather") )
elif option == "Consumos":
    consumos(os.path.join( script_path, "data", "consumos.feather") )
elif option == "Produccion":
    produccion(os.path.join( script_path, "data", "produccion.feather") ) 
elif option == "Bateas":
    bateas(os.path.join( script_path, "data", "bateas.feather") )
else:
    readme("08/02/21")


    