# --- fichier : create_product.py ---

import os
import sqlite3
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utilities import DB_PATH, FOLDERS

def create_product(parent):
    win = ttk.Toplevel(parent)
    win.title("Créer un produit")
    win.geometry("500x650")

    nom_var = ttk.StringVar()
    ttk.Label(win, text="Nom du produit").pack()
    ttk.Entry(win, textvariable=nom_var).pack(fill=X, padx=10)

    pdf_path = ttk.StringVar()

    def select_pdf():
        path = filedialog.askopenfilename(filetypes=[("Fichier PDF", "*.pdf")])
        if path:
            pdf_path.set(path)
            pdf_label.config(text=os.path.basename(path))

    ttk.Button(win, text="Sélectionner un fichier PDF", command=select_pdf).pack(pady=5)
    pdf_label = ttk.Label(win, text="Aucun fichier sélectionné")
    pdf_label.pack()

    list_frame = ttk.Frame(win)
    list_frame.pack(fill=BOTH, expand=YES, pady=10)

    ttk.Label(list_frame, text="Ajouter des éléments au produit").pack()
    listbox = ttk.Treeview(list_frame, columns=("Nom", "Quantité", "Fournisseur"), show="headings")
    listbox.heading("Nom", text="Nom")
    listbox.heading("Quantité", text="Qté")
    listbox.heading("Fournisseur", text="Fournisseur")
    listbox.pack(fill=BOTH, expand=YES)

    def add_element():
        elem_window = ttk.Toplevel(win)
        elem_window.title("Ajouter un élément existant")
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, nom FROM elements")
        elements = cur.fetchall()
        conn.close()

        selected = ttk.StringVar()
        combo = ttk.Combobox(elem_window, textvariable=selected, values=[f"{e[0]} - {e[1]}" for e in elements])
        combo.pack(pady=5)

        qt_var = ttk.IntVar(value=1)
        ttk.Label(elem_window, text="Quantité").pack()
        ttk.Entry(elem_window, textvariable=qt_var).pack()

        fourn = ttk.StringVar()
        fourn_combo = ttk.Combobox(elem_window, textvariable=fourn, values=["decoupe laser", "matiere premiere", "usinage"])
        fourn_combo.pack(pady=5)

        def confirm():
            if selected.get():
                eid = int(selected.get().split(" - ")[0])
                nom = selected.get().split(" - ")[1]
                listbox.insert("", "end", values=(nom, qt_var.get(), fourn.get()), tags=(eid,))
                elem_window.destroy()

        ttk.Button(elem_window, text="Ajouter", command=confirm).pack(pady=5)

    ttk.Button(win, text="Ajouter un élément", bootstyle="primary", command=add_element).pack(pady=5)

    def save_product():
        nom = nom_var.get()
        if not nom:
            messagebox.showerror("Erreur", "Nom requis")
            return

        dossier_path = os.path.join(FOLDERS["produits"], nom)
        os.makedirs(dossier_path, exist_ok=True)

        pdf_dest = ""
        if pdf_path.get():
            pdf_dest = os.path.join(dossier_path, os.path.basename(pdf_path.get()))
            shutil.copy(pdf_path.get(), pdf_dest)

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO produits (nom, dossier, pdf_path) VALUES (?, ?, ?)", (nom, dossier_path, pdf_dest))
        pid = cur.lastrowid

        for row in listbox.get_children():
            vals = listbox.item(row)["values"]
            tags = listbox.item(row)["tags"]
            eid = int(tags[0])
            qt = int(vals[1])
            fourn = vals[2]
            cur.execute("INSERT INTO produit_elements (produit_id, element_id, quantite, fournisseur) VALUES (?, ?, ?, ?)", (pid, eid, qt, fourn))

        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Produit enregistré.")
        win.destroy()

    ttk.Button(win, text="Enregistrer", bootstyle="success", command=save_product).pack(pady=10)
