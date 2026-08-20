import streamlit as st

st.title("🥋 Centro Difesa Marziale - CDM")

# Layout con colonne ordinate
col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome")
    codice_fiscale = st.text_input("Codice Fiscale (16 car.)")

with col2:
    cognome = st.text_input("Cognome")
    telefono = st.text_input("Telefono")

col3, col4 = st.columns(2)

with col3:
    scadenza_cert = st.date_input("Scadenza Certificato Medico", format="DD/MM/YYYY")

with col4:
    discipline = st.multiselect("Discipline", ["Judo", "Karate", "Ju-Jitsu", "Tai-Chi"])
