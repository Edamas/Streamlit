import streamlit as st
import quandl
import pandas as pd
import datetime
import numpy as np

key = input('Digite sua apikey do Quandl. Deixe em branco para nenhuma. ')
if len(key) < 1:
    key = None
quandl.ApiConfig.api_key = key

st.set_page_config(page_title="BrasilComCenso.io", 
                   page_icon=":smiley:",
                   layout='centered',
                   initial_sidebar_state='auto')


def home():
    st.title("Python + Streamlit + Google Colab + Ngrok")
    st.subheader("Streamlit From Colab")
    
    st.sidebar.title("Seleção de Database:")
    database_filter = st.sidebar.selectbox('texto', ['Brazil', 'Organisation'], key=1)

def databases():
    db = quandl.Database.all()
    db_meta = pd.DataFrame()
    for n, database in enumerate(db.values):
        dic_meta = {}
        db_index = n
        for key, value in zip(database.data_fields(), database.to_list()):
            dic_meta[key] = value
        meta2 = database.datasets().meta
        for key in meta2:
            dic_meta[key] = meta2[key]
        dic_meta['Origin'] = 'Quandle/Nasdaq'
        
        if not dic_meta['premium'] and dic_meta['datasets_count'] >= 1 and dic_meta['downloads'] >= 1:
            db_meta = db_meta.append(pd.DataFrame.from_dict(dic_meta, orient='index').T, ignore_index=True)
    db_meta = db_meta.sort_values(by=['downloads'], ascending=False)
    db_meta.index = db_meta['database_code']
    del db_meta['database_code']
    return db_meta


def about():
    st.title("About")
    st.subheader("Inspired in:")
    st.write("'How to run streamlit apps from colab'")
    st.write("by *@jcharistech*")
    st.write("Medium:")
    st.write("https://medium.com/@jcharistech/how-to-run-streamlit-apps-from-colab-29b969a1bdfc)")
    st.subheader("Criado por:")
    st.write("**Elysio Neto**")
    st.write("***@edamas***")
    st.write("Github:")
    st.write("https://github.com/Edamas")

def graf(db_chart, subheader):
    st.subheader(subheader)
    st.area_chart(db_chart)

def main():
    
    menu = ["Home", "Databases", "About"]
    choice = st.sidebar.selectbox('Menu',menu)

    if choice == 'Home':
        home()
    
    elif choice == "Databases":
        st.title('Databases')
        st.subheader('Downloading databases list.')
        st.write('Please, be patient!')
        
        db_meta = databases()
        st.dataframe(db_meta)
        
        st.header('Análise de Databases')
        graf(db_meta['datasets_count'], 'Datasets por Database (log)')
        graf(db_meta['downloads'], 'Downloads por Database (log)')
        

    elif choice == 'About':
        about()


if __name__ == '__main__':
    main() 
