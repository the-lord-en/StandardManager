# --- fichier : edit_product.py ---

import os
import shutil
import sqlite3
import webbrowser
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utilities import DB_PATH

def ouvrir_pdf(path):
    if path and os.path.exists(path):
        webbrowser.open(path)
    else:
        messagebox.showwarning("Fichier manquant", "Aucun fichier PDF valide trouvé.")

def ouvrir_pdf_produit(pid):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT pdf_path FROM produits WHERE id=?", (pid,))
    result = cur.fetchone()
    conn.close()
    if result:
        ouvrir_pdf(result[0])
    else:
        messagebox.showwarning("PDF introuvable", "Aucun PDF associé à ce produit.")

def edit_product(pid):
    win = ttk.Toplevel()
    win.title("Modifier un produit")
    win.geometry("600x700")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT nom, dossier, pdf_path FROM produits WHERE id=?", (pid,))
    nom, dossier, existing_pdf = cur.fetchone()

    nom_var = ttk.StringVar(value=nom)
    ttk.Label(win, text="Nom du produit").pack()
    ttk.Entry(win, textvariable=nom_var).pack(fill=X, padx=10)

    pdf_path = ttk.StringVar(value=existing_pdf or "")
    pdf_label = ttk.Label(win, text=os.path.basename(existing_pdf) if existing_pdf else "Aucun fichier PDF")
    pdf_label.pack()

    def select_pdf():
        path = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
        if path:
            pdf_path.set(path)
            pdf_label.config(text=os.path.basename(path))

    ttk.Button(win, text="Changer le fichier PDF", command=select_pdf).pack(pady=5)
    ttk.Button(win, text="Ouvrir le PDF", command=lambda: ouvrir_pdf(pdf_path.get()), bootstyle="info").pack(pady=2)

    list_frame = ttk.Frame(win)
    list_frame.pack(fill=BOTH, expand=YES, pady=10)

    ttk.Label(list_frame, text="Éléments du produit").pack()
    listbox = ttk.Treeview(list_frame, columns=("Nom", "Quantité", "Fournisseur"), show="headings")
    listbox.heading("Nom", text="Nom")
    listbox.heading("Quantité", text="Qté")
    listbox.heading("Fournisseur", text="Fournisseur")
    listbox.pack(fill=BOTH, expand=YES)

    cur.execute("""
        SELECT pe.id, e.nom, pe.quantite, pe.fournisseur
        FROM produit_elements pe
        JOIN elements e ON pe.element_id = e.id
        WHERE pe.produit_id=?
    """, (pid,))
    for row in cur.fetchall():
        listbox.insert("", "end", iid=row[0], values=row[1:])
    conn.close()

    def delete_selected():
        selected = listbox.selection()
        if selected:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            for item in selected:
                cur.execute("DELETE FROM produit_elements WHERE id=?", (int(item),))
                listbox.delete(item)
            conn.commit()
            conn.close()

    def save_changes():
        new_nom = nom_var.get()
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        pdf_dest = existing_pdf
        if pdf_path.get() and not pdf_path.get().startswith("Documents"):
            pdf_dest = os.path.join(dossier, os.path.basename(pdf_path.get()))
            shutil.copy(pdf_path.get(), pdf_dest)

        try:
            cur.execute("ALTER TABLE produits ADD COLUMN pdf_path TEXT")
        except sqlite3.OperationalError:
            pass  # déjà ajouté

        cur.execute("UPDATE produits SET nom=?, pdf_path=? WHERE id=?", (new_nom, pdf_dest, pid))
        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Produit mis à jour.")
        win.destroy()

    ttk.Button(win, text="Supprimer l’élément sélectionné", bootstyle="danger", command=delete_selected).pack(pady=5)
    ttk.Button(win, text="Enregistrer", bootstyle="success", command=save_changes).pack(pady=15)

