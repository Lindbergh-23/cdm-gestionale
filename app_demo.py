import sqlite3
import streamlit as st

def calcola_carattere_controllo_cf(cf_15):
    """Calcola algebricamente la 16a lettera del Codice Fiscale (algoritmo ufficiale MEF)."""
    pari = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
        'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
        'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
    }
    dispari = {
        '0': 1, '1': 0, '2': 5, '3': 7, '4': 9, '5': 13, '6': 15, '7': 17, '8': 19, '9': 21,
        'A': 1, 'B': 0, 'C': 5, 'D': 7, 'E': 9, 'F': 13, 'G': 15, 'H': 17, 'I': 19, 'J': 21,
        'K': 2, 'L': 4, 'M': 18, 'N': 20, 'O': 11, 'P': 3, 'Q': 6, 'R': 8, 'S': 12,
        'T': 14, 'U': 16, 'V': 10, 'W': 22, 'X': 25, 'Y': 24, 'Z': 23
    }
    controllo = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    somma = 0
    for i, char in enumerate(cf_15):
        pos = i + 1  # Posizione 1-based
        if pos % 2 == 0:
            somma += pari.get(char, 0)
        else:
            somma += dispari.get(char, 0)
            
    return controllo[somma % 26]

def verifica_codice_fiscale(cf):
    cf = cf.strip().upper()
    if len(cf) != 16 or not cf.isalnum():
        return False, "Il Codice Fiscale deve contenere esattamente 16 caratteri alfanumerici."
    
    carattere_calcolato = calcola_carattere_controllo_cf(cf[:15])
    carattere_inserito = cf[15]
    
    if carattere_inserito != carattere_calcolato:
        return False, "Carattere di controllo (16ª lettera) non valido. Verificare la digitazione."
        
    return True, "OK"

def init_db():
    conn = sqlite3.connect("cdm_gestionale.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS registro_atleti 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nome TEXT, cognome TEXT, cf TEXT, 
                  telefono TEXT, scadenza TEXT, discipline TEXT)''')
    conn.commit()
    conn.close()

def inserisci_db(nome, cognome, cf, tel, scad, disc):
    conn = sqlite3.connect("cdm_gestionale.db")
    c = conn.cursor()
    c.execute("INSERT INTO registro_atleti (nome, cognome, cf, telefono, scadenza, discipline) VALUES (?, ?, ?, ?, ?, ?)",
              (nome, cognome, cf, tel, scad, disc))
    conn.commit()
    conn.close()

def ottieni_db():
    conn = sqlite3.connect("cdm_gestionale.db")
    c = conn.cursor()
    c.execute("SELECT * FROM registro_atleti")
    rows = c.fetchall()
    conn.close()
    return rows

def elimina_db(id_atleta):
    conn = sqlite3.connect("cdm_gestionale.db")
    c = conn.cursor()
    c.execute("DELETE FROM registro_atleti WHERE id = ?", (id_atleta,))
    conn.commit()
    conn.close()

init_db()

# INIZIALIZZAZIONE STATI (Sempre prima dell'interfaccia)
if "input_nome" not in st.session_state:
    st.session_state.input_nome = ""
if "input_cognome" not in st.session_state:
    st.session_state.input_cognome = ""
if "input_cf" not in st.session_state:
    st.session_state.input_cf = ""
if "input_tel" not in st.session_state:
    st.session_state.input_tel = ""
if "input_disc" not in st.session_state:
    st.session_state.input_disc = []
if "cf_errato" not in st.session_state:
    st.session_state.cf_errato = False

st.title("🥋 Centro Discipline Marziali - CDM")
st.caption("Piattaforma Gestionale Anagrafica & Certificati Medici")

tab1, tab2 = st.tabs(["📝 Inserimento Atleta", "🔍 Cerca & Gestione Atleti"])

with tab1:
    st.header("Nuova Iscrizione Atleta")
    
    with st.form(key="form_iscrizione", clear_on_submit=False):
        col_nome, col_cognome = st.columns(2)
        with col_nome:
            nome = st.text_input("Nome", value=st.session_state.input_nome)
        with col_cognome:
            cognome = st.text_input("Cognome", value=st.session_state.input_cognome)

        col_cf, col_tel = st.columns(2)
        with col_cf:
            label_cf = "❌ CODICE FISCALE (ERRATO - RICORREGGERE)" if st.session_state.cf_errato else "Codice Fiscale (16 car.)"
            codice_fiscale = st.text_input(label_cf, value=st.session_state.input_cf)
            
        with col_tel:
            telefono = st.text_input("Telefono", value=st.session_state.input_tel)

        col_cert, col_disc = st.columns(2)
        with col_cert:
            scadenza_cert = st.date_input("Scadenza Certificato Medico", format="DD/MM/YYYY")
        with col_disc:
            discipline = st.multiselect("Discipline", ["Judo", "Karate", "Ju-Jitsu", "Tai-Chi"], default=st.session_state.input_disc)

        btn_salva = st.form_submit_button("💾 Salva in Database")

    if btn_salva:
        st.session_state.input_nome = nome
        st.session_state.input_cognome = cognome
        st.session_state.input_cf = codice_fiscale
        st.session_state.input_tel = telefono
        st.session_state.input_disc = discipline

        if not nome or not cognome or not codice_fiscale or not telefono or not discipline:
            st.error("⚠️ Compilare tutti i campi prima di salvare!")
        else:
            cf_pulito = codice_fiscale.strip().upper()
            esito_cf, msg_cf = verifica_codice_fiscale(cf_pulito)
            
            if not esito_cf:
                st.session_state.cf_errato = True
                st.error(f"❌ Impossibile salvare: {msg_cf}")
                st.rerun()
            else:
                st.session_state.cf_errato = False
                disc_str = ", ".join(discipline)
                data_eur = scadenza_cert.strftime("%d/%m/%Y")
                inserisci_db(nome, cognome, cf_pulito, telefono, data_eur, disc_str)
                
                st.success(f"✅ Atleta {nome} {cognome} salvato con successo!")
                
                st.session_state.input_nome = ""
                st.session_state.input_cognome = ""
                st.session_state.input_cf = ""
                st.session_state.input_tel = ""
                st.session_state.input_disc = []
                st.rerun()

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
