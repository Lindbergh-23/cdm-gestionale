"""==============================================================================

PROGETTO GESTIONALE CDM - MODULO ATLETA (Scatola 1 - Versione Completa L3)
File: modulo_atleta.py
Autori: Roberto (Generale) & Prof
==============================================================================
"""

import time
import uuid
from datetime import datetime

def genera_uuid_v7():
  """Genera un ID compatto Time-Ordered unendo timestamp in millisecondi e casualità UUID4

  per evitare ogni rischio di duplicato nello stesso millisecondo.
  """
  timestamp_hex = f"{int(time.time() * 1000):08x}"[-4:]  # Ultimi 4 caratteri del timestamp
  random_hex = uuid.uuid4().hex[:4]  # Primi 4 caratteri casuali
  return (timestamp_hex + random_hex).upper()

# Mappature ufficiali per il calcolo del Carattere di Controllo (16° carattere)
TABELLA_DISPARI = {
    '0': 1,
    '1': 0,
    '2': 5,
    '3': 7,
    '4': 9,
    '5': 13,
    '6': 15,
    '7': 17,
    '8': 19,
    '9': 21,
    'A': 1,
    'B': 0,
    'C': 5,
    'D': 7,
    'E': 9,
    'F': 13,
    'G': 15,
    'H': 17,
    'I': 19,
    'J': 21,
    'K': 2,
    'L': 4,
    'M': 18,
    'N': 20,
    'O': 11,
    'P': 3,
    'Q': 6,
    'R': 8,
    'S': 12,
    'T': 14,
    'U': 16,
    'V': 10,
    'W': 22,
    'X': 25,
    'Y': 24,
    'Z': 23,
}

TABELLA_PARI = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9,
    'K': 10,
    'L': 11,
    'M': 12,
    'N': 13,
    'O': 14,
    'P': 15,
    'Q': 16,
    'R': 17,
    'S': 18,
    'T': 19,
    'U': 20,
    'V': 21,
    'W': 22,
    'X': 23,
    'Y': 24,
    'Z': 25,
}

TABELLA_RESTO = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z',
}

def verifica_codice_fiscale(cf):
  """Verifica la validità formale ed algebrica di un Codice Fiscale italiano."""
  cf = cf.strip().upper()

  # 1. Controllo di lunghezza e caratteri alfanumerici
  if len(cf) != 16 or not cf.isalnum():
    return False

  # 2. Calcolo del carattere di controllo sui primi 15 caratteri
  somma = 0
  for i, char in enumerate(cf[:15]):
    pos = i + 1  # posizione 1-based (1 = dispari, 2 = pari, ecc.)
    if pos % 2 != 0:
      somma += TABELLA_DISPARI[char]
    else:
      somma += TABELLA_PARI[char]

  resto = somma % 26
  carattere_atteso = TABELLA_RESTO[resto]

  # 3. Confronto con la 16-esima lettera inserita
  return cf[15] == carattere_atteso

class Atleta:

  def __init__(
      self,
      nome,
      cognome,
      codice_fiscale,
      data_scadenza_certificato,
      sesso="",
      data_nascita="",
      luogo_nascita="",
      provincia_nascita="",
      indirizzo="",
      comune="",
      cap="",
      provincia="",
      telefono="",
      email="",
      contatto_emergenza_nome="",
      contatto_emergenza_tel="",
      data_iscrizione=None,
      discipline=None,
      tipo_certificato="Non Agonistico",
      note_mediche="",
      id_atleta=None,
  ):
    """Costruttore anagrafico completo dell'Atleta CDM."""
    # Identificativo Univoco Cronologico
    self.id_atleta = id_atleta if id_atleta else genera_uuid_v7()

    # Dati Anagrafici
    self.nome = nome.strip().title()
    self.cognome = cognome.strip().title()
    self.codice_fiscale = codice_fiscale.strip().upper()
    self.sesso = sesso.strip().upper()
    self.data_nascita = data_nascita
    self.luogo_nascita = luogo_nascita.strip().title()
    self.provincia_nascita = provincia_nascita.strip().upper()

    # Residenza
    self.indirizzo = indirizzo.strip().title()
    self.comune = comune.strip().title()
    self.cap = cap.strip()
    self.provincia = provincia.strip().upper()

    # Contatti ed Emergenza
    self.telefono = telefono.strip()
    self.email = email.strip().lower()
    self.contatto_emergenza_nome = contatto_emergenza_nome.strip().title()
    self.contatto_emergenza_tel = contatto_emergenza_tel.strip()

    # Dati Associativi e Sanitari
    self.data_iscrizione = (
        data_iscrizione
        if data_iscrizione
        else datetime.now().strftime("%Y-%m-%d")
    )
    self.discipline = discipline if discipline is not None else []
    self.tipo_certificato = tipo_certificato
    self.note_mediche = note_mediche.strip()

    # Conversione Data Certificato per Calcolo Dinamico (ISO %Y-%m-%d)
    self.scadenza_cert = datetime.strptime(
        data_scadenza_certificato, "%Y-%m-%d"
    ).date()

  def stato_certificato(self):
    """Calcola lo stato del certificato medico rispetto alla data odierna."""
    oggi = datetime.now().date()
    giorni_rimanenti = (self.scadenza_cert - oggi).days

    if giorni_rimanenti <= 0:
      return "🔴 SCADUTO", giorni_rimanenti
    elif giorni_rimanenti <= 30:
      return "🟡 IN SCADENZA", giorni_rimanenti
    else:
      return "🟢 VALIDO", giorni_rimanenti

  def mostra_scheda_completa(self):
    """Stampa a schermo l'anagrafica completa dell'atleta."""
    stato, giorni = self.stato_certificato()
    discipline_str = (
        ", ".join(self.discipline) if self.discipline else "Nessuna"
    )

    print("=" * 70)
    print(
        f"ID: [{self.id_atleta}] - ATLETA: {self.nome.upper()}"
        f" {self.cognome.upper()} ({self.sesso})"
    )
    print(
        f"CF: {self.codice_fiscale} | Nato/a a: {self.luogo_nascita}"
        f" ({self.provincia_nascita}) il {self.data_nascita}"
    )
    print(
        f"Residenza: {self.indirizzo} - {self.cap} {self.comune}"
        f" ({self.provincia})"
    )
    print(f"Contatti: Tel. {self.telefono} | Email: {self.email}")
    print(
        f"Emergenza: {self.contatto_emergenza_nome} ({self.contatto_emergenza_tel})"
    )
    print(
        f"Iscritto il: {self.data_iscrizione} | Discipline:"
        f" {discipline_str}"
    )
    print(
        f"Certificato [{self.tipo_certificato}]:"
        f" {self.scadenza_cert.strftime('%d/%m/%Y')} -> {stato} ({giorni} gg)"
    )
    if self.note_mediche:
      print(f"Note Mediche: {self.note_mediche}")
    print("=" * 70)