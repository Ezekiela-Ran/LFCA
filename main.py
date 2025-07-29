from sqlite3 import Cursor
from customtkinter import CTk, CTkFrame, CTkEntry, CTkButton, CTkScrollableFrame, CTkLabel, DoubleVar, CTkFont
from customtkinter import StringVar, IntVar, CTkToplevel
import customtkinter
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
from modalAjouterCategorie import ModalAjouterCategorie
from modalAjouterProduit import ModalAjouterProduit
import data
import mysql_connexion_config
from CTkMenuBar import *
import sys
import subprocess
root = CTk()

# Paramètrage de la dimension de la fenêtre
screen_width = 1366
screen_height = root.winfo_screenheight()

# Appliquer ces dimensions comme taille minimale
root.geometry(f"{screen_width}x{int(screen_height * 0.8)}")
root.title("ACSSQDA")

# Fenêtre principale
mframe = CTkFrame(master=root)
mframe.pack(expand=True, fill="both")

# Thème
customtkinter.set_default_color_theme("blue") 
customtkinter.set_appearance_mode("system")  # "dark", "light", "system"

# Barre de menu
menu = CTkMenuBar(master=mframe)
menu_fichier = menu.add_cascade("fichier")
menu_theme = menu.add_cascade("thème")
menu_other = menu.add_cascade("plus")

# root.iconify()  # ou mframe.winfo_toplevel().iconify()

def relance_fantôme():
    # Fenêtre fantôme
    fantôme = CTkToplevel()
    fantôme.geometry("400x200+500+300")
    fantôme.overrideredirect(True)  # Supprime la barre de titre
    fantôme.configure(fg_color=['gray86', 'gray17'])
    
    # Texte ou animation de transition
    label = CTkLabel(fantôme, text="Patientez...", font=("Arial", 20))
    label.pack(expand=True)

    root.withdraw()  # Masque l'appli actuelle
    fantôme.update()

    # Relance après un court délai
    fantôme.after(300, lambda: subprocess.Popen([sys.executable, *sys.argv]))
    fantôme.after(600, lambda: (fantôme.destroy(), root.quit()))
    
dropdown = CustomDropdownMenu(widget=menu_fichier)

dropdown.add_option(option="Nouveau", command=relance_fantôme)
dropdown.add_option(option="Aperçu") 

dropdown1 = CustomDropdownMenu(widget=menu_theme)
dropdown1.add_option(option="sombre", command=lambda: customtkinter.set_appearance_mode("dark")) 
dropdown1.add_option(option="lumineux", command=lambda: customtkinter.set_appearance_mode("light")) 

dropdown2 = CustomDropdownMenu(widget=menu_other)
dropdown2.add_option(option="Réinitialiser") 

mysql_connexion_config.cursor.execute("SELECT * FROM categories")
for row in mysql_connexion_config.cursor.fetchall():
    data.produit_par_categorie[row[1]] = {}

# Initialisation
paddings = 5
ctkbutton = 10
leBoutonValiderEstCliquer = "non"

# Récupérer le dernier id inséré dans info_client
mysql_connexion_config.cursor.execute("SELECT MAX(id_client) FROM info_client")
result = mysql_connexion_config.cursor.fetchone()
id = result[0] + 1 if result and result[0] is not None else 1

label_width = 75
my_font = CTkFont(family="Comfortaa", size=12, weight="bold", slant="italic")
categorie_selectionne = None

# ---------------------------------------------------------------

# Entête

frame1 = CTkFrame(master=mframe, border_color="gray", border_width=1)
frame1.pack(padx=paddings, pady=paddings, side="top", anchor="nw")

# Raison social
raison_social_label = CTkLabel(master=frame1, text="* Raison social: ", font=my_font, fg_color="transparent", anchor="w")
raison_social_label.grid(column=0, row=0, padx=paddings, pady=paddings, sticky="w")

raison_social_input = CTkEntry(master=frame1, textvariable=StringVar())
raison_social_input.grid(column=1, row=0, padx=paddings, pady=paddings)

# Statistique
statistique_label = CTkLabel(master=frame1, text="Statistique: ", font=my_font, fg_color="transparent", anchor="w")
statistique_label.grid(column=0, row=1, padx=paddings, pady=paddings, sticky="w")

statistique_input = CTkEntry(master=frame1, textvariable=StringVar())
statistique_input.grid(column=1, row=1, padx=paddings, pady=paddings)

# NIF
nif_label = CTkLabel(master=frame1, text="NIF: ", font=my_font, fg_color="transparent", anchor="w")
nif_label.grid(column=0, row=2, padx=paddings, pady=paddings, sticky="w")

nif_input = CTkEntry(master=frame1, textvariable=StringVar())
nif_input.grid(column=1, row=2, padx=paddings, pady=paddings)

# Adresse
adresse_label = CTkLabel(master=frame1, text="Adresse: ", font=my_font, fg_color="transparent", anchor="w")
adresse_label.grid(column=0, row=3, padx=paddings, pady=paddings, sticky="w")

adresse_input = CTkEntry(master=frame1, textvariable=StringVar())
adresse_input.grid(column=1, row=3, padx=paddings, pady=paddings)

# N°Facture
facture_label = CTkLabel(master=frame1, text=f"Facture N°{id}", font=my_font, fg_color="transparent", anchor="w")
facture_label.grid(column=0, row=4, padx=paddings, pady=paddings, sticky="w")

# date d'émission

date_emission_label = CTkLabel(master=frame1, text="* Date d'émission: ", font=my_font, fg_color="transparent", anchor="w")
date_emission_label.grid(column=2, row=0, padx=paddings, pady=paddings, sticky="w")

date_emission_input = DateEntry(master=frame1, selectmode='day', date_pattern='yyyy-mm-dd', bd=adresse_input.cget("border_width"), width=15)
date_emission_input.grid(column=3, row=0, padx=paddings, pady=paddings)

# Date du résultat
date_du_resultat_label = CTkLabel(master=frame1, text="* Date du résultat: ", font=my_font, fg_color="transparent", anchor="w")
date_du_resultat_label.grid(column=2, row=1, padx=paddings, pady=paddings, sticky="w")

date_du_resultat_input = DateEntry(master=frame1, selectmode='day', date_pattern='yyyy-mm-dd', width=15)
date_du_resultat_input.grid(column=3, row=1, padx=paddings, pady=paddings)

# Référence des produits (en int)
reference_des_produits_label = CTkLabel(master=frame1, text="Référence des produits: ", font=my_font, fg_color="transparent", anchor="w")
reference_des_produits_label.grid(column=2, row=2, padx=paddings, pady=paddings, sticky="w")

reference_des_produits_input = CTkEntry(master=frame1, textvariable=StringVar())
reference_des_produits_input.grid(column=3, row=2, padx=paddings, pady=paddings)

# Résponsable
responsable_label = CTkLabel(master=frame1, text="* Responsable: ", font=my_font, fg_color="transparent", anchor="w")
responsable_label.grid(column=2, row=3, padx=paddings, pady=paddings, sticky="w")

responsable_input = CTkEntry(master=frame1, textvariable=StringVar())
responsable_input.grid(column=3, row=3, padx=paddings, pady=paddings)

terminer = False

def enregister():
    global terminer 
    terminer = True
    # Enregistrer les informations du client dans la base de données
    if raison_social_input.get() == "" or date_emission_input.get_date() == "" or date_du_resultat_input.get_date() == "" or responsable_input.get() == "":
            CTkMessagebox(title="Error", message="Veuillez complétez tous les champs obligatoires", icon="cancel")
            return
    else:

        frame2 = CTkFrame(master=mframe, border_width=1, border_color="gray")
        frame2.pack(padx=paddings, pady=paddings, anchor="w", expand=True, fill="both")
        
        def pied_de_page():
            # mysql_connexion_config.cursor.execute("SELECT total FROM total WHERE client_id = ")
            montant_a_payer = CTkLabel(master=frame2, text="Montant à payer: ")
            montant_a_payer.pack(side="bottom", anchor="center")

            bouton_imprimer = CTkButton(master=frame2, text="Imprimer", width=ctkbutton)
            bouton_imprimer.pack(side="right", anchor="se", padx=paddings, pady=paddings)
            
            
            def terminer():
                if data.etat_validation_produits and data.valeur_ref_bull_analyse != {} :
                    mysql_connexion_config.cursor.execute("INSERT INTO info_client (raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                    raison_social_input.get(),
                    statistique_input.get() if statistique_input.get() != "" else None,
                    nif_input.get() if nif_input.get() != "" else None,
                    adresse_input.get()if adresse_input.get() != "" else None,
                    date_emission_input.get_date(),
                    date_du_resultat_input.get_date(),
                    reference_des_produits_input.get(),
                    responsable_input.get() ))
                    mysql_connexion_config.connexion.commit()
                    
                    for produit in data.etat_validation_produits:
                        cursor = mysql_connexion_config.connexion.cursor(buffered=True)
                        cursor.execute("SELECT id_produit FROM produits WHERE nom_produit = %s", (produit,))
                        resultat = cursor.fetchone()
                        
                        if resultat:
                            id_produit = resultat[0]
                        else:
                            print("Produit introuvable")
                            cursor.close()
                            return  # ou gérer l'erreur proprement
                        
                        # récupérer l'ID du client
                        cursor.execute("SELECT id_client FROM info_client WHERE raison_sociale = %s", (raison_social_input.get(),))
                        resultat_client = cursor.fetchone()   
                        
                        if resultat_client:
                            id_client = resultat_client[0]
                        else:
                            print("Client introuvable")
                            cursor.close()
                            return
                        
                        # récupérer les détails du produit
                        cursor.execute("""SELECT physico, micro, toxico, sous_total FROM produit_details WHERE produit_id = %s """, (id_produit,))
                        details = cursor.fetchone()
                            
                        if not details:
                            print("Détails du produit introuvables")
                            cursor.close()
                            return
                            
                        physico, micro, toxico, sous_total = details
                        
                        data.total[produit] = sous_total
                        
                        # insérer les données dans produit_analyse
                        cursor.execute("""INSERT INTO produit_analyse (client_id, produit_id, ref_bull_analyse, num_acte, physico, micro, toxico, sous_total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (id_client,id_produit, data.valeur_ref_bull_analyse[produit], data.valeur_num_acte[produit], physico, micro, toxico, sous_total))
                        
                        mysql_connexion_config.connexion.commit()
                        cursor.close()
        
                    total = 0
                    for sous_total in data.total.values():
                        try:
                            total += float(sous_total)
                        except (ValueError, TypeError):
                            print(f"Erreur: sous_total non numérique ({sous_total}) ignoré.")
                    
                    cursor_for_total = mysql_connexion_config.connexion.cursor()
                    
                    # récupérer l'ID du client
                    cursor_for_total.execute("SELECT id_client FROM info_client WHERE raison_sociale = %s", (raison_social_input.get(),))
                    resultat_client = cursor_for_total.fetchone()
                    # Assure que tous les resultats sont lues avant la prochaine requête
                    while cursor_for_total.nextset():
                        pass
                        
                    if resultat_client:
                        id_client = resultat_client[0]
                    else:
                        print("Client introuvable")
                        cursor_for_total.close()
                        return
                    
                    cursor_for_total.execute("INSERT INTO total(client_id, total) VALUES (%s, %s)", (id_client, total))
                    mysql_connexion_config.connexion.commit()
                    
                    
                    
                    data.etat_validation_produits.clear()
                    data.valeur_ref_bull_analyse.clear()
                    data.valeur_num_acte.clear()
                    data.total.clear()
                    CTkMessagebox(message=f"Enregistrement effectué avec succès!\n Total: {total}",
                  icon="check", option_1="Fermer")
                    
                    for widget in frame2.winfo_children():
                        widget.destroy()
                    
                    bouton_suivant.configure(state="disabled")
                    
                else:
                    CTkMessagebox(title="Error", message="Veuillez validez au moin un produit!", icon="cancel")
            
            bouton_terminer = CTkButton(master=frame2, text="Terminer", width=ctkbutton, command=terminer)
            bouton_terminer.pack(side="right", anchor="se", padx=paddings, pady=paddings)
        pied_de_page()

        # SUB SECTION 2-1 (Première colonne)

        frame2_1 = CTkFrame(master=frame2)
        frame2_1.pack(padx=paddings, pady=paddings, fill="both", side="left")

        frame2_1_A = CTkFrame(master=frame2_1)
        frame2_1_A.pack(fill="x", padx=paddings, pady=paddings)

        product_type_label = CTkLabel(master=frame2_1_A, text="TYPE DE PRODUIT",fg_color="transparent")
        product_type_label.pack(side="left", padx=paddings, pady=paddings)

        # Ajouter un type de produit "MODAL WINDOW"

        
        def ajouter_un_categorie():
            ModalAjouterCategorie(master=root, frame=frame2_1_B, callback=afficher_categories)

        bouton_ajouter_categorie = CTkButton(master=frame2_1_A, text="Ajouter", command=ajouter_un_categorie, width=ctkbutton)
        bouton_ajouter_categorie.pack(side="right", padx=paddings, pady=paddings)

        # Supprimer un Catégorie
        def supp_categorie():
            
            for categorie in list(data.produit_par_categorie.keys()): 
                if categorie == categorie_selectionne:
                    mysql_connexion_config.cursor.execute(
                        "DELETE FROM categories WHERE nom_categorie = %s",
                        (categorie_selectionne,)
                    )
                    mysql_connexion_config.connexion.commit()
                    del data.produit_par_categorie[categorie_selectionne]
                    
                    for widget in frame2_1_B.winfo_children():
                        widget.destroy()
                    for widget in frame2_2_C.winfo_children():
                        widget.destroy()
                    afficher_categories()
                    break

        bouton_supprimer_categorie = CTkButton(master=frame2_1_A, text="Supprimer", command=supp_categorie, width=ctkbutton)
        bouton_supprimer_categorie.pack(side="right", padx=paddings, pady=paddings)

        frame2_1_B = CTkScrollableFrame(master=frame2_1)
        frame2_1_B.pack(padx=paddings, pady=paddings, expand=True, fill="both", anchor="nw")

        # Sélection et affichage du type de produit
        def choisir_la_categorie_et_afficher_les_produit(categorie, frame_pour_affichage):
            global categorie_selectionne
            categorie_selectionne = categorie
            for widget in frame_pour_affichage.winfo_children():
                widget.destroy()
            cursor = mysql_connexion_config.cursor
            # Récupérer les produits de la catégorie depuis la base
            cursor.execute("""
            SELECT p.nom_produit, d.physico, d.micro, d.toxico, d.sous_total
            FROM produits p
            JOIN produit_details d ON p.id_produit = d.id_produit_detail
            WHERE p.categorie_id = (
                SELECT id_categorie FROM categories WHERE nom_categorie = %s
            )
        """, (categorie_selectionne,))

            produits = cursor.fetchall()
            
            etat = {"click": True} 
            if produits:
                for produit_row in produits:
                    nom_produit, physico, micro, toxico, sous_total = produit_row
                    row = CTkFrame(master=frame_pour_affichage, fg_color= "skyblue" if data.etat_validation_produits.get(nom_produit, False) else ['gray86', 'gray17'])
                    etat_initial = {"border_width": row.cget("border_width"), "fg_color": row.cget("fg_color")}
                    
                    row.pack(fill="x", padx=5, pady=5)
                    
                    # Liste des produits disponibles
                    CTkLabel(master=row, text=nom_produit, width=label_width, wraplength=label_width, fg_color="transparent").pack(side="left", anchor="w", padx=5, pady=5)

                    Ref_bull_var = IntVar()
                    Ref_bull_analyse = CTkEntry(master=row, width=label_width, textvariable=Ref_bull_var, justify="right")
                    Ref_bull_analyse.pack(side="left", anchor="w", padx=5, pady=5)

                    Num_acte_var = StringVar()
                    Num_acte = CTkEntry(master=row, width=label_width, textvariable=Num_acte_var, justify="right")
                    Num_acte.pack(side="left", anchor="w", padx=5, pady=5)

                    Physico_var = DoubleVar(value=physico)
                    Physico = CTkEntry(master=row, state="disabled", width=label_width, justify="right", textvariable=Physico_var)
                    Physico.pack(side="left", anchor="w", padx=5, pady=5)

                    Micro_var = DoubleVar(value=micro)
                    Micro = CTkEntry(master=row, state="disabled", width=label_width, justify="right", textvariable=Micro_var)
                    Micro.pack(side="left", anchor="w", padx=5, pady=5)

                    Toxico_var = DoubleVar(value=toxico)
                    Toxico = CTkEntry(master=row, state="disabled", width=label_width, justify="right", textvariable=Toxico_var)
                    Toxico.pack(side="left", anchor="w", padx=5, pady=5)

                    Sous_total_var = DoubleVar(value=sous_total)
                    Sous_total = CTkEntry(master=row, state="disabled", width=label_width, justify="right", textvariable=Sous_total_var)
                    Sous_total.pack(side="left", anchor="w", padx=5, pady=5)

                    def only_float(P):
                        if P == "" or P.replace(".", "", 1).isdigit():
                            return True
                        return False

                    vcmd = (row.register(only_float), "%P")
                    Physico.configure(validate="key", validatecommand=vcmd)
                    Micro.configure(validate="key", validatecommand=vcmd)
                    Toxico.configure(validate="key", validatecommand=vcmd)

                    def modifier(nom_produit, Physico, Micro, Toxico, Sous_total, Physico_var, Micro_var, Toxico_var, Sous_total_var):
                        Physico.configure(state="normal")
                        Physico.focus_set()
                        def on_physico_return(event):
                            Micro.configure(state="normal")
                            Physico.configure(state="disabled")
                            cursor.execute("""
                                UPDATE produit_details d
                                JOIN produits p ON d.id_produit_detail = p.id_produit
                                SET d.physico = %s
                                WHERE p.nom_produit = %s
                                AND p.categorie_id = (
                                SELECT id_categorie FROM categories WHERE nom_categorie = %s
                            )""",
                            (Physico_var.get(), nom_produit, categorie_selectionne))

                            mysql_connexion_config.connexion.commit()
                            Micro.focus_set()
                        Physico.bind("<Return>", on_physico_return)
                        def on_micro_return(event):
                            Toxico.configure(state="normal")
                            Micro.configure(state="disabled")
                            cursor.execute("""
                                UPDATE produit_details d
                                JOIN produits p ON d.id_produit_detail = p.id_produit
                                SET d.micro = %s
                                WHERE p.nom_produit = %s
                                AND p.categorie_id = (
                                SELECT id_categorie FROM categories WHERE nom_categorie = %s
                            )""",
                            (Micro_var.get(), nom_produit, categorie_selectionne))
                            mysql_connexion_config.connexion.commit()
                            Toxico.focus_set()
                        Micro.bind("<Return>", on_micro_return)
                        def on_toxico_return(event):
                            try:
                                cursor.execute("""
                                    UPDATE produit_details d
                                    JOIN produits p ON d.id_produit_detail = p.id_produit
                                    SET d.toxico = %s
                                    WHERE p.nom_produit = %s
                                    AND p.categorie_id = (
                                    SELECT id_categorie FROM categories WHERE nom_categorie = %s
                                )""",
                                (Toxico_var.get(), nom_produit, categorie_selectionne))
                                
                                physico_val = float(Physico_var.get())
                                micro_val = float(Micro_var.get())
                                toxico_val = float(Toxico_var.get())
                                sous_total_val = physico_val + micro_val + toxico_val
                                Sous_total_var.set(sous_total_val)
                                cursor.execute("""
                                    UPDATE produit_details d
                                    JOIN produits p ON d.produit_id = p.id_produit
                                    SET d.sous_total = %s
                                    WHERE p.nom_produit = %s
                                    AND p.categorie_id = (
                                    SELECT id_categorie FROM categories WHERE nom_categorie = %s
                                )""",
                                (sous_total_val, nom_produit, categorie_selectionne))
                                mysql_connexion_config.connexion.commit()
                                Sous_total.configure(state="disabled")
                                Physico.configure(state="disabled")
                                Micro.configure(state="disabled")
                                Toxico.configure(state="disabled")
                            except ValueError:
                                print("Veuillez entrer un nombre valide.")
                        Toxico.bind("<Return>", on_toxico_return)

                    bouton_modifier = CTkButton(
                        master=row,
                        text="Modifier",
                        width=ctkbutton,
                        command=lambda prod=nom_produit, p=Physico, m=Micro, t=Toxico, s=Sous_total, pv=Physico_var, mv=Micro_var, tv=Toxico_var, sv=Sous_total_var: modifier(prod, p, m, t, s, pv, mv, tv, sv)
                    )
                    bouton_modifier.pack(side="left", anchor="w", padx=5, pady=5)

                    def supprimer_produit():
                        cursor.execute(
                            "DELETE FROM produits WHERE nom_produit = %s AND categorie_id = (SELECT id_categorie FROM categories WHERE nom_categorie = %s)",
                            (nom_produit, categorie_selectionne)
                        )
                        mysql_connexion_config.connexion.commit()
                        
                        for widget in frame_pour_affichage.winfo_children():
                            widget.destroy()
                        choisir_la_categorie_et_afficher_les_produit(categorie_selectionne, frame_pour_affichage)

                    bouton_suppr = CTkButton(master=row, text="suppr", width=ctkbutton, command=supprimer_produit)
                    bouton_suppr.pack(side="left", anchor="w", padx=5, pady=5)
                    
                    def valider_produit(prod, row, btn_m, btn_s, n_a, r_s):
                        
                        
                        if etat["click"]:
                            row.configure(border_width=1, fg_color="skyblue")
                            btn_m.configure(state="disabled") 
                            btn_s.configure(state="disabled")
                            n_a.configure(state="disabled")
                            
                            data.etat_validation_produits[prod] = etat["click"]
                            
                            data.valeur_ref_bull_analyse[prod] = Ref_bull_var.get()
                            
                            data.valeur_num_acte[prod] = Num_acte_var.get()
                            
                            etat["click"] = False
                           
                        
                        else:
                            row.configure(border_width=etat_initial["border_width"], fg_color=etat_initial["fg_color"])
                            btn_m.configure(state="normal") 
                            btn_s.configure(state="normal")
                            n_a.configure(state="normal")
                            
                            data.etat_validation_produits[prod] = etat["click"]
                            
                            data.valeur_ref_bull_analyse[prod] = Ref_bull_var.set(0)
                            
                            data.valeur_num_acte[prod] = Num_acte_var.set("")
                            
                            etat["click"] = True

                            
                    
                    valider_bouton = CTkButton(master=row, text="valider", width=ctkbutton, command=lambda prod=nom_produit, row=row, btn_m=bouton_modifier, btn_s=bouton_suppr, n_a=Num_acte, r_s=raison_social_input.get(): valider_produit(prod, row, btn_m, btn_s, n_a,r_s))
                    valider_bouton.pack(side="left", anchor="w", padx=5, pady=5)
            else:
                CTkLabel(master=frame_pour_affichage, text=f"Type de produit: {categorie_selectionne}", fg_color="transparent").pack(side="left", fill="both", expand=True)

        def afficher_categories():
            if data.produit_par_categorie:
                for categorie in list(data.produit_par_categorie.keys()):
                    CTkButton(master=frame2_1_B, text=categorie, width=ctkbutton, command=lambda categorie=categorie: choisir_la_categorie_et_afficher_les_produit(categorie, frame2_2_C)).pack(fill="x", padx=paddings, pady=paddings)
            else:
                CTkLabel(master=frame2_1_B, text="Aucun type de produit", fg_color="transparent").pack(fill="x", padx=paddings, pady=paddings)

        afficher_categories()

        # SUB SECTION 2-2 (Deuxième colonne)

        frame2_2 = CTkFrame(master=frame2)
        frame2_2.pack(padx=paddings, pady=paddings, expand=True, fill="both", side="right")

        frame2_2_A = CTkFrame(master=frame2_2)
        frame2_2_A.pack(padx=paddings, pady=paddings, fill="both")

        def ajouter_produit():
            if categorie_selectionne:
                ModalAjouterProduit(root, categorie_selectionne, callback=lambda: choisir_la_categorie_et_afficher_les_produit(categorie_selectionne, frame2_2_C))
            return

        ajouter_produit_button = CTkButton(master=frame2_2_A, text="Ajouter produit", width=ctkbutton, command=ajouter_produit)
        ajouter_produit_button.pack(side="right", padx=paddings, pady=paddings)

        def etiquette():
            frame2_2_B = CTkFrame(master=frame2_2)
            frame2_2_B.pack(fill="x", padx=paddings, pady=paddings)

            product_name_label = CTkLabel(master=frame2_2_B, text="Désignation", width=label_width, fg_color="transparent", wraplength=label_width)
            product_name_label.grid(column=0, row=0, padx=paddings, pady=paddings)
            
            ref_bulletin_analyse = CTkLabel(master=frame2_2_B, text="Ref. B. analyse", width=label_width, fg_color="transparent", wraplength=label_width)
            ref_bulletin_analyse.grid(column=1, row=0, padx=paddings, pady=paddings)

            act_label = CTkLabel(master=frame2_2_B, text="N°Acte", width=label_width, fg_color="transparent", wraplength=label_width)
            act_label.grid(column=2, row=0, padx=paddings, pady=paddings)

            physico_chimique_label = CTkLabel(master=frame2_2_B, text="Physico", width=label_width, fg_color="transparent", wraplength=label_width)
            physico_chimique_label.grid(column=3, row=0, padx=paddings, pady=paddings)

            micro_biologic_label = CTkLabel(master=frame2_2_B, text="Micro", width=label_width, fg_color="transparent", wraplength=label_width)
            micro_biologic_label.grid(column=4, row=0, padx=paddings, pady=paddings)

            toxicologic_label = CTkLabel(master=frame2_2_B, text="Toxico", width=label_width, fg_color="transparent", wraplength=label_width)
            toxicologic_label.grid(column=5, row=0, padx=paddings, pady=paddings)

            sous_total_label = CTkLabel(master=frame2_2_B, text="Sous total", width=label_width, fg_color="transparent", wraplength=label_width)
            sous_total_label.grid(column=6, row=0, padx=paddings, pady=paddings)

        etiquette()

        frame2_2_C = CTkScrollableFrame(master=frame2_2)
        frame2_2_C.pack(fill="both", expand=True, padx=paddings, pady=paddings)
                    

bouton_suivant = CTkButton(master=frame1, command=enregister,text="Suivant", width=ctkbutton)
bouton_suivant.grid(column=3, row=4, padx=paddings, pady=paddings)

# CORP (body)
if not terminer :
    frame2 = CTkFrame(master=mframe)
    frame2.pack_forget()


root.mainloop()
