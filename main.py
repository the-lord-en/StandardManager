# StandardManager - Version modernisée avec ttkbootstrap + liste produits
# Auteur : Benoit Barbey

import os
import sqlite3
import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

APP_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "StandardManager")
DB_PATH = os.path.join(APP_FOLDER, "produits.db")
DXF_FOLDER = os.path.join(APP_FOLDER, "dxf")
PDF_FOLDER = os.path.join(APP_FOLDER, "pdf")
BACKUP_FOLDER = os.path.join(APP_FOLDER, "backup")

for folder in [APP_FOLDER, DXF_FOLDER, PDF_FOLDER, BACKUP_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            dimensions TEXT,
            matiere TEXT,
            quantite INTEGER,
            traitement TEXT,
            certificat TEXT,
            fournisseur TEXT,
            categorie TEXT,
            dxf_path TEXT,
            remarques TEXT,
            nb_decoupes INTEGER,
            m_soudure REAL,
            nb_pointages INTEGER,
            nb_pieces INTEGER,
            transport_heure INTEGER,
            peinture_heure INTEGER,
            date_ajout TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT nom, dimensions, matiere, quantite, fournisseur FROM produits ORDER BY date_ajout DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def start_gui():
    app = ttk.Window(themename="flatly")
    app.title("StandardManager - Benoit Barbey")
    app.geometry("1000x600")

    nav = ttk.Frame(app, padding=10)
    nav.pack(side=LEFT, fill=Y)

    content = ttk.Frame(app, padding=20)
    content.pack(side=RIGHT, expand=YES, fill=BOTH)

    title = ttk.Label(content, text="Produits enregistrés", font=("Helvetica", 16))
    title.pack(pady=10)

    tree = ttk.Treeview(content, columns=("Nom", "Dimensions", "Matière", "Quantité", "Fournisseur"), show='headings')
    for col in ("Nom", "Dimensions", "Matière", "Quantité", "Fournisseur"):
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill=BOTH, expand=True)

    def refresh_list():
        for i in tree.get_children():
            tree.delete(i)
        for row in get_all_products():
            tree.insert("", END, values=row)

    def add_product():
        top = ttk.Toplevel(app)
        top.title("Ajouter un produit")
        top.geometry("400x700")
        entries = {}
        champs = ["nom", "dimensions", "matiere", "quantite", "traitement",
                  "certificat", "fournisseur", "categorie", "remarques",
                  "nb_decoupes", "m_soudure", "nb_pointages", "nb_pieces",
                  "transport_heure", "peinture_heure"]
        for c in champs:
            ttk.Label(top, text=c.capitalize().replace("_", " ")).pack(anchor=W)
            e = ttk.Entry(top)
            e.pack(fill=X, pady=2)
            entries[c] = e

        def enregistrer():
            data = {k: v.get() for k, v in entries.items()}
            dxf_path = filedialog.askopenfilename(title="Choisir un fichier DXF")
            if dxf_path:
                new_path = os.path.join(DXF_FOLDER, f"{data['nom']}.dxf")
                try:
                    with open(dxf_path, 'rb') as src, open(new_path, 'wb') as dst:
                        dst.write(src.read())
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de copier le fichier : {e}")
                    return
            else:
                new_path = ""

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO produits (
                    nom, dimensions, matiere, quantite, traitement, certificat, fournisseur, categorie,
                    dxf_path, remarques, nb_decoupes, m_soudure, nb_pointages, nb_pieces,
                    transport_heure, peinture_heure, date_ajout
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data["nom"], data["dimensions"], data["matiere"], int(data["quantite"]),
                data["traitement"], data["certificat"], data["fournisseur"], data["categorie"],
                new_path, data["remarques"], int(data["nb_decoupes"]), float(data["m_soudure"]),
                int(data["nb_pointages"]), int(data["nb_pieces"]), int(data["transport_heure"]),
                int(data["peinture_heure"]), datetime.date.today().isoformat()
            ))
            conn.commit()
            conn.close()
            top.destroy()
            refresh_list()
            messagebox.showinfo("Succès", "Produit enregistré avec succès.")

        ttk.Button(top, text="Enregistrer", bootstyle="success", command=enregistrer).pack(pady=10)

    ttk.Button(nav, text="Ajouter un produit", width=20, bootstyle="primary", command=add_product).pack(pady=5)
    ttk.Button(nav, text="Rafraîchir la liste", width=20, bootstyle="info", command=refresh_list).pack(pady=5)
    ttk.Button(nav, text="Quitter", width=20, bootstyle="danger", command=app.quit).pack(pady=5)

    refresh_list()
    app.mainloop()

if __name__ == "__main__":
    init_db()
    start_gui()
