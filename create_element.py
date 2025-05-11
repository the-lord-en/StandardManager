import os
import shutil
import sqlite3
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utilities import DB_PATH, FOLDERS

def create_element(parent):
    win = ttk.Toplevel(parent)
    win.title("Créer un élément")
    win.geometry("400x500")

    nom_var = ttk.StringVar()
    dim_var = ttk.StringVar()
    mat_var = ttk.StringVar()
    trait_var = ttk.StringVar()
    cert_var = ttk.StringVar()
    dxf_path = None
    pdf_path = None

    def browse_dxf():
        nonlocal dxf_path
        dxf_path = filedialog.askopenfilename(filetypes=[("Fichiers DXF", "*.dxf")])
        if dxf_path:
            lbl_dxf.config(text=os.path.basename(dxf_path))

    def browse_pdf():
        nonlocal pdf_path
        pdf_path = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
        if pdf_path:
            lbl_pdf.config(text=os.path.basename(pdf_path))

    ttk.Label(win, text="Nom de l'élément").pack()
    ttk.Entry(win, textvariable=nom_var).pack(fill=X, padx=10)

    ttk.Label(win, text="Dimension").pack()
    ttk.Entry(win, textvariable=dim_var).pack(fill=X, padx=10)

    ttk.Label(win, text="Matière").pack()
    ttk.Entry(win, textvariable=mat_var).pack(fill=X, padx=10)

    ttk.Label(win, text="Traitement").pack()
    ttk.Entry(win, textvariable=trait_var).pack(fill=X, padx=10)

    ttk.Label(win, text="Certificat matière").pack()
    ttk.Entry(win, textvariable=cert_var).pack(fill=X, padx=10)

    ttk.Button(win, text="Sélectionner un fichier DXF", command=browse_dxf).pack(pady=5)
    lbl_dxf = ttk.Label(win, text="Aucun fichier sélectionné")
    lbl_dxf.pack()

    ttk.Button(win, text="Sélectionner un fichier PDF", command=browse_pdf).pack(pady=5)
    lbl_pdf = ttk.Label(win, text="Aucun fichier sélectionné")
    lbl_pdf.pack()

    def save_element():
        nom = nom_var.get()
        if not nom:
            messagebox.showerror("Erreur", "Le nom est requis.")
            return

        dossier = os.path.join(FOLDERS["elements"], nom)
        os.makedirs(dossier, exist_ok=True)

        dxf_dest = os.path.join(dossier, os.path.basename(dxf_path)) if dxf_path else ""
        pdf_dest = os.path.join(dossier, os.path.basename(pdf_path)) if pdf_path else ""

        if dxf_path:
            shutil.copy(dxf_path, dxf_dest)
        if pdf_path:
            shutil.copy(pdf_path, pdf_dest)

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO elements (nom, dimensions, matiere, traitement, certificat, dxf_path, pdf_path, dossier)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (nom, dim_var.get(), mat_var.get(), trait_var.get(), cert_var.get(), dxf_dest, pdf_dest, dossier)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Élément enregistré.")
        win.destroy()

    ttk.Button(win, text="Enregistrer", bootstyle="success", command=save_element).pack(pady=20)
