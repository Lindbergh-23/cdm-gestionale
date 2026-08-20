import streamlit as st
import database as db
from modulo_atleta import Atleta

# Titolo e intestazione
st.title("🥋 Centro Difesa Marziale - CDM")
st.caption("Piattaforma Gestionale Anagrafica & Certificati Medici")

tab1, tab2 = st.tabs(["📝 Inserimento Atleta", "🔍 Cerca & Verifica Scadenze"])

with tab1:
    st.header("Nuova Iscrizione Atleta")
    
    # st.form con clear_on_submit=True azzera tutti i campi dopo il salvataggio
    with st.form(key="form_iscrizione", clear_on_submit=True):
        col_nome, col_cognome = st.columns(2)
        with col_nome:
            nome = st.text_input("Nome")
        with col_cognome:
            cognome = st.text_input("Cognome")

        col_cf, col_tel = st.columns(2)
        with col_cf:
            codice_fiscale = st.text_input("Codice Fiscale (16 car.)")
        with col_tel:
            telefono = st.text_input("Telefono")

        col_cert, col_disc = st.columns(2)
        with col_cert:
            scadenza_cert = st.date_input("Scadenza Certificato Medico", format="DD/MM/YYYY")
        with col_disc:
            discipline = st.multiselect("Discipline", ["Judo", "Karate", "Ju-Jitsu", "Tai-Chi"])

        btn_salva = st.form_submit_button("💾 Salva in Database")

    if btn_salva:
        if not nome or not cognome or not codice_fiscale:
            st.error("⚠️ Inserire Nome, Cognome e Codice Fiscale!")
        else:
            # Creazione istanza Atleta e validazione CF
            cf_pulito = codice_fiscale.strip().upper()
            atleta_test = Atleta(nome, cognome, cf_pulito, telefono, str(scadenza_cert), discipline)
            
            # Controllo validità tramite il modulo_atleta
            if hasattr(atleta_test, 'cf_valido') and not atleta_test.cf_valido:
                st.error(f"❌ Codice Fiscale '{cf_pulito}' NON valido algebricamente! Verificare l'ultima lettera.")
            else:
                discipline_str = ", ".join(discipline) if discipline else ""
                db.inserisci_atleta(nome, cognome, cf_pulito, telefono, str(scadenza_cert), discipline_str)
                st.success(f"✅ Atleta {nome} {cognome} salvato con successo!")

with tab2:
    st.header("Gestione & Ricerca Atleti")
    
    # Visualizzazione tabella atleti
    atleti = db.ottieni_atleti()
    if atleti:
        for atl in atleti:
            # Assumendo struttura tuple: (id, nome, cognome, cf, telefono, scadenza, discipline)
            id_atl, n, c, cf, tel, scad, disc = atl[0], atl[1], atl[2], atl[3], atl[4], atl[5], atl[6]
            
            col_dati, col_del = st.columns([4, 1])
            with col_dati:
                st.write(f"**{n} {c}** | CF: `{cf}` | Tel: {tel} | Scad. Certificato: **{scad}** | {disc}")
            with col_del:
                if st.button("🗑️ Elimina", key=f"del_{id_atl}"):
                    db.elimina_atleta(id_atl)
                    st.warning(f"Atleta {n} {c} eliminato.")
                    st.rerun()
            st.divider()
    else:
        st.info("Nessun atleta presente nel database.")
