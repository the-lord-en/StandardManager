# --- fichier : main_interface.py ---

# --- fichier : main_interface.py ---

import os
import sqlite3
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# from utilities import view_product, edit_product, init_db, DB_PATH, FOLDERS
from utilities import init_db, DB_PATH, FOLDERS  # temporaire
from create_product import create_product
from create_element import create_element
from utilities import view_product, edit_product, init_db, DB_PATH, FOLDERS

def main_interface():
    app = ttk.Window(themename="flatly")
    app.title("StandardManager – Interface principale")
    app.geometry("1000x600")

    topbar = ttk.Frame(app)
    topbar.pack(side=TOP, fill=X, padx=10, pady=10)
    search = ttk.Entry(topbar, width=50)
    search.pack(side=LEFT, padx=5)
    ttk.Button(topbar, text="Créer un produit", bootstyle="success", command=lambda: create_product(app)).pack(side=RIGHT, padx=5)
    ttk.Button(topbar, text="Créer un élément", bootstyle="info", command=lambda: create_element(app)).pack(side=RIGHT, padx=5)
    ttk.Button(topbar, text="Liste des éléments", bootstyle="secondary", command=lambda: messagebox.showinfo("Fonctionnalité à venir", "L'affichage de la liste complète des éléments sera intégré dans une future version.")).pack(side=RIGHT, padx=5)

    card_area = ttk.Frame(app)
    card_area.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    def load_product_cards():
        for widget in card_area.winfo_children():
            widget.destroy()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, nom FROM produits")
        for pid, nom in c.fetchall():
            f = ttk.Frame(card_area, borderwidth=1, relief="ridge", padding=10)
            f.pack(pady=5, fill=X)
            ttk.Label(f, text=nom, font=("Arial", 12)).pack(anchor=W)
            ttk.Button(f, text="Voir", bootstyle="info", command=lambda i=pid: view_product(i)).pack(side=RIGHT)
            ttk.Button(f, text="Modifier", bootstyle="warning", command=lambda i=pid: edit_product(i)).pack(side=RIGHT, padx=5)
        conn.close()

    load_product_cards()
    app.mainloop()

if __name__ == "__main__":
    init_db()
    main_interface()
