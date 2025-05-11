# --- fichier : utilities.py ---

import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join("Documents", "StandardManager", "standardmanager.db")
FOLDERS = {
    "pdf": os.path.join("Documents", "StandardManager", "pdf"),
    "dxf": os.path.join("Documents", "StandardManager", "dxf"),
    "backup": os.path.join("Documents", "StandardManager", "backup"),
    "elements": os.path.join("Documents", "StandardManager", "elements"),
    "produits": os.path.join("Documents", "StandardManager", "produits"),
    "logs": os.path.join("Documents", "StandardManager", "logs")
}

def init_db():
    """
    Cette fonction doit être appelée au début de main_interface.py
    pour garantir que les dossiers et les colonnes nécessaires existent.
    """
    for folder in FOLDERS.values():
        os.makedirs(folder, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Création des tables si elles n'existent pas
    cur.execute('''CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        pdf_path TEXT,
        dossier TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS elements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        matiere TEXT,
        dimension TEXT,
        dimensions TEXT,
        traitement TEXT,
        certificat TEXT,
        dxf_path TEXT,
        pdf_path TEXT,
        dossier TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS produit_elements (
        produit_id INTEGER,
        element_id INTEGER,
        quantite INTEGER,
        fournisseur TEXT
    )''')

    # Ajout de colonnes manquantes dans les tables existantes
    colonnes_produits = ["pdf_path", "nom", "dossier"]
    colonnes_elements = ["nom", "matiere", "dimension", "dimensions", "traitement", "certificat", "dxf_path", "pdf_path", "dossier"]
    colonnes_pe = ["produit_id", "element_id", "quantite", "fournisseur"]

    for colonne in colonnes_produits:
        try:
            cur.execute(f"ALTER TABLE produits ADD COLUMN {colonne} TEXT")
        except sqlite3.OperationalError:
            pass

    for colonne in colonnes_elements:
        try:
            cur.execute(f"ALTER TABLE elements ADD COLUMN {colonne} TEXT")
        except sqlite3.OperationalError:
            pass

    for colonne in colonnes_pe:
        try:
            cur.execute(f"ALTER TABLE produit_elements ADD COLUMN {colonne} TEXT")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()


def view_product(pid):
    pass  # fonction temporaire pour éviter les erreurs

def edit_product(pid):
    pass  # fonction temporaire pour éviter les erreurs


def log_command(pid, bloc):
    print(f"[LOG] Commande pour produit {pid}:\n{bloc}")
