import sqlite3
import streamlit as st

# Algoritmo Ufficiale Agenzia delle Entrate per la verifica del Carattere di Controllo del CF
def controlla_cf_algebrico(cf):
    cf = cf.strip().upper()
    if len(cf) != 16 or not cf.isalnum():
        return False, "Il Codice Fiscale deve contenere esattamente 16 caratteri alfanumerici."
    
    disp = {
        '0':1, '1':0, '2':5, '3':7, '4':9, '5':13, '6':15, '7':17, '8':19, '9':21,
        'A':1, 'B':0, 'C':5, 'D':7, 'E':9, 'F':13, 'G':15, 'H':17, 'I':19, 'J':21,
        'K':2, 'L':4, 'M':18, 'N':20, 'O':11, 'P':3, 'Q':6, 'R':8, 'S':12, 'T':14,
        'U':16, 'V':10, 'W':22, 'X':25, 'Y':24, 'Z':23
    }
    pari = {
        '0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
        'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6

### 1. Perché i campi si sono svuotati dopo il Salva?
Quella è la funzione `clear_on_submit=True` che avevamo impostato: quando clicchi su **Salva** (o premi *Enter* nel form), Streamlit invia i dati al database e **subito dopo pulisce tutte le caselle di testo** per lasciarti la maschera pronta per un nuovo inserimento. Quindi il fatto che ora vedi le caselle vuote è il segnale che il form si è resettato con successo dopo l'invio.

---

### 2. Perché ha salvato anche con il Codice Fiscale errato?
Nel blocco di codice precedente, se la chiamata alla classe `Atleta` del tuo modulo incontrava un'eccezione interna o non trovava la proprietà specifica, il controllo "scivolava" sul blocco `except` consentendo il salvataggio.

Per renderlo **rigido, severo e inattaccabile**, inseriamo l'algoritmo algebrico completo del Codice Fiscale italiano **direttamente nella funzione di verifica** di Streamlit. In questo modo:
1. Controlla che i caratteri siano esattamente 16.
2. Applica la formula matematica ufficiale sui primi 15 caratteri e calcola la 16ª lettera di controllo.
3. Se la lettera non coincide (es. "T" al posto di "U"), **blocca tassativamente il salvataggio** e mostra l'errore in rosso!

---

### Codice Corretto e Blindato per `app_demo.py`

```python
import sqlite3
import streamlit as st

# Algoritmo algebrico nativo per il controllo del Codice Fiscale
def valida_codice_fiscale_algebrico(cf):
    cf = cf.strip().upper()
    if len(cf) != 16 or not cf.isalnum():
        return False, "Il Codice Fiscale deve contenere esattamente 16 caratteri alfanumerici."
    
    # Mappe di conversione per il calcolo del carattere di controllo (16° carattere)
    disp = {
        '0': 1, '1': 0, '2': 5, '3': 7, '4': 9, '5': 13, '6': 15, '7': 17, '8': 19, '9': 21,
        'A': 1, 'B': 0, 'C': 5, 'D': 7, 'E': 9, 'F': 13, 'G': 15, 'H': 17, 'I': 19, 'J': 21,
        'K': 2, 'L': 4, 'M': 18, 'N': 20, 'O': 11, 'P': 3, 'Q': 6, 'R': 8, 'S': 12, 'T': 14,
        'U': 16, 'V': 10, 'W': 22, 'X': 25, 'Y': 24, 'Z': 23
    }
    
    pari = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I
