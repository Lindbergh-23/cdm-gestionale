"""==============================================================================

PROGETTO GESTIONALE CDM - DEMO WEB INTERATTIVA (Streamlit)
File: app_demo.py
Autori: Roberto (Generale) & Prof
==============================================================================
"""

from database import DatabaseCDM
from modulo_atleta import Atleta, verifica_codice_fiscale
import streamlit as st

# Configurazione della pagina web
st.set_page_config(
    page_title="Gestionale CDM", page_icon="🥋", layout="centered"
)

# Inizializzazione Database
db = DatabaseCDM()

st.title("🥋 Centro Difesa Marziale - CDM")
st.caption("Piattaforma Gestionale Anagrafica & Certificati Medici")

# TAB DELL'INTERFACCIA
tab1, tab2 = st.tabs(["📝 Inserimento Atleta", "🔍 Cerca & Verifica Scadenze"])

# ==========================================
# TAB 1: INSERIMENTO ATLETA
# ==========================================
with tab1:
  st.header("Nuova Iscrizione Atleta")

  with st.form("form_nuovo_atleta"):
    col1, col2 = st.columns(2)
    with col1:
      nome = st.text_input("Nome")
      cf = st.text_input("Codice Fiscale (16 car.)").upper()
      scadenza = st.date_input("Scadenza Certificato Medico")
    with col2:
      cognome = st.text_input("Cognome")
      telefono = st.text_input("Telefono")
      discipline = st.multiselect(
          "Discipline", ["Tai-Chi", "Qi Gong", "Kung Fu", "Judo"]
      )

    btn_salva = st.form_submit_button("💾 Salva in Database")

  if btn_salva:
    if not nome or not cognome or not cf:
      st.error("⚠️ Compilare tutti i campi obbligatori!")
    elif not verifica_codice_fiscale(cf):
      st.error(
          f"❌ Il Codice Fiscale '{cf}' non è valido secondo l'algoritmo"
          " ministeriale!"
      )
    else:
      nuovo = Atleta(
          nome=nome,
          cognome=cognome,
          codice_fiscale=cf,
          data_scadenza_certificato=scadenza.strftime("%Y-%m-%d"),
          telefono=telefono,
          discipline=discipline,
      )
      esito = db.inserisci_atleta(nuovo)
      if esito:
        st.success(f"✅ Atleta {nome} {cognome} registrato con successo nel DB!")
        st.balloons()  # Animazione grafica per il collaudo

# ==========================================
# TAB 2: CONSULTAZIONE DATABASE
# ==========================================
with tab2:
  st.header("Ricerca Schedario")
  st.info("Sistema relazionale collegato al database 'cdm_gestionale.db'")

  conn = db.connetti()
  cursor = conn.cursor()
  cursor.execute(
      "SELECT nome, cognome, codice_fiscale, data_scadenza_certificato,"
      " discipline FROM atleti"
  )
  righe = cursor.fetchall()
  conn.close()

  if righe:
    for r in righe:
      st.markdown(f"**👤 {r[0]} {r[1]}** — CF: `{r[2]}`")
      st.caption(f"Discipline: {r[4]} | 🗓️ Scadenza Certificato: **{r[3]}**")
      st.divider()
  else:
    st.warning("Nessun atleta presente nel Database.")