import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


# Funzione per connettersi al database SQLite
def connect_db():
    conn = sqlite3.connect('finanza.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS risultati (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valore REAL NOT NULL
        )
    ''')
    conn.commit()
    return conn


# Funzione per memorizzare i risultati nel database
def salva_risultato(tipo, valore):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO risultati (tipo, valore)
        VALUES (?, ?)
    ''', (tipo, valore))
    conn.commit()
    conn.close()


# Funzione per cancellare tutti i risultati dal database
def cancella_risultati():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM risultati')
    conn.commit()
    conn.close()
    messagebox.showinfo("Successo", "Tutti i risultati sono stati cancellati!")


# Funzione per calcolare l'interesse semplice
def calcola_interesse_semplice():
    try:
        P = float(entry_principale.get())
        r = float(entry_tasso.get()) / 100
        t = float(entry_tempo.get())
        interesse = P * r * t
        label_risultato.config(text=f"Interesse Semplice: € {interesse:.2f}")
        salva_risultato('Interesse Semplice', interesse)
    except ValueError:
        messagebox.showerror("Errore", "Inserisci valori numerici validi")


# Funzione per calcolare l'interesse composto
def calcola_interesse_composto():
    try:
        P = float(entry_principale.get())
        r = float(entry_tasso.get()) / 100
        t = float(entry_tempo.get())
        interesse = P * ((1 + r) ** t - 1)
        label_risultato.config(text=f"Interesse Composto: € {interesse:.2f}")
        salva_risultato('Interesse Composto', interesse)
    except ValueError:
        messagebox.showerror("Errore", "Inserisci valori numerici validi")


# Funzione per calcolare il montante semplice
def calcola_montante_semplice():
    try:
        P = float(entry_principale.get())
        r = float(entry_tasso.get()) / 100
        t = float(entry_tempo.get())
        montante = P * (1 + r * t)
        label_risultato.config(text=f"Montante Semplice: € {montante:.2f}")
        salva_risultato('Montante Semplice', montante)
    except ValueError:
        messagebox.showerror("Errore", "Inserisci valori numerici validi")


# Funzione per calcolare il montante composto
def calcola_montante_composto():
    try:
        P = float(entry_principale.get())
        r = float(entry_tasso.get()) / 100
        t = float(entry_tempo.get())
        montante = P * (1 + r) ** t
        label_risultato.config(text=f"Montante Composto: € {montante:.2f}")
        salva_risultato('Montante Composto', montante)
    except ValueError:
        messagebox.showerror("Errore", "Inserisci valori numerici validi")


# Funzione per calcolare il valore scontato semplice
def calcola_valore_scontato_semplice():
    try:
        M = float(entry_montante.get())
        r = float(entry_tasso.get()) / 100
        t = float(entry_tempo.get())
        valore_scontato = M / (1 + r * t)
        label_risultato.config(text=f"Valore Scontato Semplice: € {valore_scontato:.2f}")
        salva_risultato('Valore Scontato Semplice', valore_scontato)
    except ValueError:
        messagebox.showerror("Errore", "Inserisci valori numerici validi")


# Funzione per calcolare il valore scontato composto
def calcola_valore_scontato_composto():
    try:
        M = float(entry_montante.get())
        r = float(entry_tasso.get()) / 100
        t = float(entry_tempo.get())
        valore_scontato = M / (1 + r) ** t
        label_risultato.config(text=f"Valore Scontato Composto: € {valore_scontato:.2f}")
        salva_risultato('Valore Scontato Composto', valore_scontato)
    except ValueError:
        messagebox.showerror("Errore", "Inserisci valori numerici validi")


# Funzione per calcolare lo sconto semplice
def calcola_sconto_semplice():
    try:
        M = float(entry_montante.get())
        r = float(entry_tasso.get()) / 100
        t = float(entry_tempo.get())
        sconto = M * r * t / (1 + r * t)
        label_risultato.config(text=f"Sconto Semplice: € {sconto:.2f}")
        salva_risultato('Sconto Semplice', sconto)
    except ValueError:
        messagebox.showerror("Errore", "Inserisci valori numerici validi")


# Funzione per calcolare lo sconto composto
def calcola_sconto_composto():
    try:
        M = float(entry_montante.get())
        r = float(entry_tasso.get()) / 100
        t = float(entry_tempo.get())
        sconto = M * (1 - (1 / (1 + r) ** t))
        label_risultato.config(text=f"Sconto Composto: € {sconto:.2f}")
        salva_risultato('Sconto Composto', sconto)
    except ValueError:
        messagebox.showerror("Errore", "Inserisci valori numerici validi")


# Funzione per visualizzare i risultati memorizzati
def visualizza_risultati():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM risultati')
    rows = cursor.fetchall()
    conn.close()

    risultati_window = tk.Toplevel(root)
    risultati_window.title("Risultati Memorizzati")

    tree = ttk.Treeview(risultati_window, columns=("id", "tipo", "valore"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("tipo", text="Tipo")
    tree.heading("valore", text="Valore (€)")

    for row in rows:
        tree.insert("", "end", values=row)

    tree.pack(fill=tk.BOTH, expand=True)


# Creazione della finestra principale
root = tk.Tk()
root.title("Calcolatrice Finanziaria by Antonio Cufari ver. 1.0")

# Creazione dei widget per l'interfaccia
tk.Label(root, text="Principale (€):").grid(row=0, column=0, padx=10, pady=5)
entry_principale = tk.Entry(root)
entry_principale.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Tasso di interesse (%):").grid(row=1, column=0, padx=10, pady=5)
entry_tasso = tk.Entry(root)
entry_tasso.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Tempo (anni):").grid(row=2, column=0, padx=10, pady=5)
entry_tempo = tk.Entry(root)
entry_tempo.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Montante (€):").grid(row=3, column=0, padx=10, pady=5)
entry_montante = tk.Entry(root)
entry_montante.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Calcola Interesse Semplice", command=calcola_interesse_semplice).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="Calcola Interesse Composto", command=calcola_interesse_composto).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="Calcola Montante Semplice", command=calcola_montante_semplice).grid(row=6, column=0, columnspan=2, pady=10)
tk.Button(root, text="Calcola Montante Composto", command=calcola_montante_composto).grid(row=7, column=0, columnspan=2, pady=10)
tk.Button(root, text="Calcola Valore Scontato Semplice", command=calcola_valore_scontato_semplice).grid(row=8, column=0, columnspan=2, pady=10)
tk.Button(root, text="Calcola Valore Scontato Composto", command=calcola_valore_scontato_composto).grid(row=9, column=0, columnspan=2, pady=10)
tk.Button(root, text="Calcola Sconto Semplice", command=calcola_sconto_semplice).grid(row=10, column=0, columnspan=2, pady=10)
tk.Button(root, text="Calcola Sconto Composto", command=calcola_sconto_composto).grid(row=11, column=0, columnspan=2, pady=10)
tk.Button(root, text="Visualizza Risultati", command=visualizza_risultati).grid(row=12, column=0, columnspan=2, pady=10)
tk.Button(root, text="Cancella Tutti i Risultati", command=cancella_risultati).grid(row=13, column=0, columnspan=2, pady=10)

label_risultato = tk.Label(root, text="")
label_risultato.grid(row=14, column=0, columnspan=2, pady=10)

# Avvio del loop principale dell'interfaccia
root.mainloop()
