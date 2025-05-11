def view_product(pid):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT nom, dossier FROM produits WHERE id=?", (pid,))
    nom, dossier = cur.fetchone()

    cur.execute("""
        SELECT e.nom, e.dimensions, e.matiere, e.traitement, e.certificat, e.dxf_path,
               pe.quantite, pe.fournisseur
        FROM produit_elements pe
        JOIN elements e ON pe.element_id = e.id
        WHERE pe.produit_id = ?
    """, (pid,))

    lignes = cur.fetchall()
    conn.close()

    fournisseurs = {"decoupe laser": [], "matiere premiere": [], "usinage": []}
    fichiers_dxf = {"decoupe laser": [], "matiere premiere": [], "usinage": []}

    for l in lignes:
        (nom_e, dim, mat, trait, cert, dxf, qt, fourn) = l
        bloc = f"{nom_e}\ndimension : {dim}\nmatiere : {mat}\nquantite : {qt}"
        if trait:
            bloc += f"\ntraitement : {trait}"
        if cert:
            bloc += f"\ncertificat matiere : {cert}"
        bloc += "\n"
        fournisseurs[fourn].append(bloc)
        if dxf:
            fichiers_dxf[fourn].append(dxf)

    for cat, lignes in fournisseurs.items():
        if not lignes:
            continue
        txt = "Bonjour,\n\nPouvez-vous me faire un devis pour les éléments suivants :\n\n"
        txt += "\n".join(lignes)
        txt += "\nEn vous remerciant, d'avance.\n"
        datecode = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = os.path.join(FOLDERS["devis_archive"], f"{nom}_{cat}_{datecode}.txt")
        with open(archive_path, "w", encoding="utf-8") as f:
            f.write(txt)

        dxf_output = os.path.join(FOLDERS["devis_archive"], f"{nom}_{cat}_{datecode}_DXF")
        os.makedirs(dxf_output, exist_ok=True)
        for fpath in fichiers_dxf[cat]:
            if os.path.exists(fpath):
                shutil.copy(fpath, dxf_output)

    messagebox.showinfo("Mail généré", f"Devis généré pour {nom} dans le dossier 'devis_archive'.")