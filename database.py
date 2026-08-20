"""==============================================================================

PROGETTO GESTIONALE CDM - MODULO DATABASE (Lezione 5)
File: database.py
Autori: Roberto (Generale) & Prof
==============================================================================
"""

import sqlite3
from modulo_atleta import Atleta


class DatabaseCDM:

  def __init__(self, db_file="cdm_gestionale.db"):
    """Inizializza la connessione al file di database e crea le tabelle."""
    self.db_file = db_file
    self.crea_tabelle()

  def connetti(self):
    """Crea e restituisce una connessione al database SQLite."""
    return sqlite3.connect(self.db_file)

  def crea_tabelle(self):
    """Crea la tabella 'atleti' se non esiste già nel file del database."""
    query = """
        CREATE TABLE IF NOT EXISTS atleti (
            id_atleta TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            cognome TEXT NOT NULL,
            codice_fiscale TEXT UNIQUE NOT NULL,
            sesso TEXT,
            data_nascita TEXT,
            luogo_nascita TEXT,
            provincia_nascita TEXT,
            indirizzo TEXT,
            comune TEXT,
            cap TEXT,
            provincia TEXT,
            telefono TEXT,
            email TEXT,
            contatto_emergenza_nome TEXT,
            contatto_emergenza_tel TEXT,
            data_iscrizione TEXT,
            discipline TEXT,
            tipo_certificato TEXT,
            data_scadenza_certificato TEXT NOT NULL,
            ente_promozione TEXT,
            consenso_privacy INTEGER,
            consenso_foto INTEGER,
            note_mediche TEXT
        );
        """
    with self.connetti() as conn:
      cursor = conn.cursor()
      cursor.execute(query)
      conn.commit()

  def inserisci_atleta(self, atleta: Atleta):
      """Salva un oggetto Atleta nel database SQLite."""
      query = """
        INSERT INTO atleti (
            id_atleta, nome, cognome, codice_fiscale, sesso, data_nascita,
            luogo_nascita, provincia_nascita, indirizzo, comune, cap, provincia,
            telefono, email, contatto_emergenza_nome, contatto_emergenza_tel,
            data_iscrizione, discipline, tipo_certificato, data_scadenza_certificato,
            ente_promozione, consenso_privacy, consenso_foto, note_mediche
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
      discipline_str = (
          ", ".join(atleta.discipline)
          if isinstance(atleta.discipline, list)
          else str(atleta.discipline)
      )

      valori = (
          getattr(atleta, "id_atleta", ""),
          getattr(atleta, "nome", ""),
          getattr(atleta, "cognome", ""),
          getattr(atleta, "codice_fiscale", ""),
          getattr(atleta, "sesso", ""),
          getattr(atleta, "data_nascita", ""),
          getattr(atleta, "luogo_nascita", ""),
          getattr(atleta, "provincia_nascita", ""),
          getattr(atleta, "indirizzo", ""),
          getattr(atleta, "comune", ""),
          getattr(atleta, "cap", ""),
          getattr(atleta, "provincia", ""),
          getattr(atleta, "telefono", ""),
          getattr(atleta, "email", ""),
          getattr(atleta, "contatto_emergenza_nome", ""),
          getattr(atleta, "contatto_emergenza_tel", ""),
          getattr(atleta, "data_iscrizione", ""),
          discipline_str,
          getattr(atleta, "tipo_certificato", ""),
          atleta.scadenza_cert.strftime("%Y-%m-%d"),
          getattr(
              atleta, "ente_promozione", ""
          ),  # <-- Gestione sicura se il campo manca
          1 if getattr(atleta, "consenso_privacy", False) else 0,
          1 if getattr(atleta, "consenso_foto", False) else 0,
          getattr(atleta, "note_mediche", ""),
      )

      try:
          with self.connetti() as conn:
              cursor = conn.cursor()
              cursor.execute(query, valori)
              conn.commit()
              print(
                  f"✅ Atleta {atleta.nome} {atleta.cognome} salvato con successo"
                  " nel Database!"
              )
              return True
      except sqlite3.IntegrityError:
          print(
              f"⚠️ Errore SQL: Il Codice Fiscale '{atleta.codice_fiscale}' è già"
              " presente nel Database!"
          )
          return False