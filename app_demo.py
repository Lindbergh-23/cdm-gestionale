import sqlite3
import streamlit as st
from modulo_atleta import Atleta

def init_db():
    conn = sqlite3.connect("cdm_gestionale.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS atleti 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nome TEXT, cognome TEXT, cf TEXT, 
                  telefono TEXT, scadenza TEXT, discipline TEXT)''')
    conn.commit()
    conn.close()

def inserisci_db(nome, cognome, cf, tel, scad, disc):
    conn = sqlite3.connect("cdm_gestionale.db")
    c = conn.cursor()
    c.execute("INSERT INTO atleti (nome, cognome, cf, telefono, scadenza, discipline) VALUES (?, ?, ?, ?, ?, ?)",
              (nome, cognome, cf, tel, scad, disc))
    conn.commit()
    conn.close()

def ottieni_db():
    conn = sqlite3.connect("cdm_gestionale.db")
    c = conn.cursor()
    c.execute("SELECT * FROM atleti")
    rows = c.fetchall()
    conn.close()
    return rows

def elimina_db(id_atleta):
    conn = sqlite3.connect("cdm_gestionale.db")
    c = conn.cursor()
    c.execute("DELETE FROM atleti WHERE id = ?", (id_atleta,))
    conn.commit()
    conn.close()

init_db()

st.title("🥋 Centro Difesa Marziale - CDM")
st.caption("Piattaforma Gestionale Anagrafica & Certificati Medici")

tab1, tab2 = st.tabs(["📝 Inserimento Atleta", "🔍 Cerca & Gestione Atleti"])

with tab1:
    st.header("Nuova Iscrizione Atleta")
    
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
            cf_pulito = codice_fiscale.strip().upper()
            
            # Formattiamo la data nel formato ISO YYYY-MM-DD richiesto da modulo_atleta.py
            data_iso = scadenza_cert.strftime("%Y-%m-%d")
            
            try:
                # Inizializzazione oggetto Atleta per la validazione algebrica
                atleta_obj = Atleta(nome, cognome, cf_pulito, telefono, data_iso, discipline)
                
                # Controllo validità CF
                if hasattr(atleta_obj, 'cf_valido') and not atleta_obj.cf_valido:
                    st.error(f"❌ Codice Fiscale '{cf_pulito}' NON valido algebricamente!")
                else:
                    disc_str = ", ".join(discipline) if discipline else ""
                    # Salviamo la data nel formato visivo europeo GG/MM/AAAA nel DB
                    data_eur = scadenza_cert.strftime("%d/%m/%Y")
                    inserisci_db(nome, cognome, cf_pulito, telefono, data_eur, disc_str)
                    st.success(f"✅ Atleta {nome} {cognome} salvato con successo!")
            except Exception as e:
                st.error(f"❌ Errore durante la validazione: {e}")

with tab2:
    st.header("Gestione & Elenco Atleti")
    
    atleti = ottieni_db()
    if atleti:
        for atl in atleti:
            id_atl, n, c, cf, tel, scad, disc = atl[0], atl[1], atl[2], atl[3], atl[4], atl[5], atl[6]
            
            col_dati, col_del = st.columns([4, 1])
            with col_dati:
                st.write(f"**{n} {c}** | CF: `{cf}` | Tel: {tel} | Scad. Certificato: **{scad}** | {disc}")
            with col_del:
                if st.button("🗑️ Elimina", key=f"del_{id_atl}"):
                    elimina_db(id_atl)
                    st.warning(f"Atleta {n} {c} eliminato.")
                    st.rerun()
            st.divider()
    else:
        st.info("Nessun atleta presente nel database.")
