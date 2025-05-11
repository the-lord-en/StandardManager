# --- fichier : generate_request.py ---

import sqlite3
import os
from datetime import datetime
from tkinter import Toplevel, Text, Scrollbar, RIGHT, Y, END, BOTH, YES
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utilities import DB_PATH, log_command

def commander_produit(pid):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT e.nom, e.dimension, e.matiere, pe.quantite, e.traitement, e.certificat, pe.fournisseur
        FROM produit_elements pe
        JOIN elements e ON pe.element_id = e.id
        WHERE pe.produit_id = ?
    """, (pid,))
    lignes = cur.fetchall()
    conn.close()

    fournisseurs = {}
    for nom, dim, mat, qt, trait, cert, fourn in lignes:
        bloc = f"Nom du produit: {nom}\n"
        bloc += f"dimention: {dim}\n"
        bloc += f"matiere: {mat}\n"
        bloc += f"quantiter: {qt}\n"
        if trait:
            bloc += f"traitement: {trait}\n"
        if cert:
            bloc += f"certificat matiere: {cert}\n"
        bloc += "\n"
        fournisseurs.setdefault(fourn, []).append(bloc)

    win = Toplevel()
    win.title("Demande de devis générée")
    win.geometry("700x600")
    text = Text(win, wrap="word")
    text.pack(side="left", fill=BOTH, expand=YES)
    scrollbar = Scrollbar(win, command=text.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text.configure(yscrollcommand=scrollbar.set)

    copy_btn = ttk.Button(win, text="Copier le texte", bootstyle="primary", command=lambda: win.clipboard_append(text.get("1.0", END)))
    copy_btn.pack(pady=5)

    contenu_final = ""
    for fourn, blocs in fournisseurs.items():
        contenu_final += f"---- Fournisseur : {fourn} ----\n"
        contenu_final += "Bonjour,\n\n"
        contenu_final += "Pouvez-vous me faire un devis pour les éléments suivants :\n\n"
        for bloc in blocs:
            contenu_final += bloc
        contenu_final += "En vous remerciant d'avance.\n\n"
        contenu_final += "------------------------------\n\n"

    text.insert(END, contenu_final)
    log_command(pid, contenu_final)
