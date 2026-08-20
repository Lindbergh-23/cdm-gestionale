import streamlit as st

# Titolo dell'applicazione
st.title("🥋 Centro Difesa Marziale - CDM")
st.caption("Piattaforma Gestionale Anagrafica & Certificati Medici")

# Creazione delle schede/tab principali
tab1, tab2 = st.tabs(["📝 Inserimento Atleta", "🔍 Cerca & Verifica Scadenze"])

with tab1:
    st.header("Nuova Iscrizione Atleta")
    
    # Riga 1: Dati Anagrafici Base (Nome e Cognome sempre insieme)
    col_nome, col_cognome = st.columns(2)
    with col_nome:
        nome = st.text_input("Nome")
    with col_cognome:
        cognome = st.text_input("Cognome")

    # Riga 2: Dati Fiscali e Contatti
    col_cf, col_tel = st.columns(2)
    with col_cf:
        codice_fiscale = st.text_input("Codice Fiscale (16 car.)")
    with col_tel:
        telefono = st.text_input("Telefono")

    # Riga 3: Certificato e Discipline
    col_cert, col_disc = st.columns(2)
    with col_cert:
        scadenza_cert = st.date_input("Scadenza Certificato Medico", format="DD/MM/YYYY")
    with col_disc:
        discipline = st.multiselect("Discipline", ["Judo", "Karate", "Ju-Jitsu", "Tai-Chi"])

    # Pulsante di salvataggio
    if st.button("💾 Salva in Database"):
        st.success("Atleta salvato con successo!")

with tab2:
    st.header("Ricerca e Controllo Scadenze")
    st.info("Funzionalità di ricerca attiva nel Database.")
