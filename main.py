from customtkinter import CTk, CTkFrame, CTkEntry, CTkButton, CTkScrollableFrame, CTkLabel, DoubleVar, CTkFont
from customtkinter import StringVar, IntVar
import customtkinter
from tkcalendar import DateEntry
from modalAjouterCategorie import ModalAjouterCategorie
from modalAjouterProduit import ModalAjouterProduit
import data
import mysql_connexion_config
from CTkMenuBar import *
from tkinter import messagebox

root = CTk()

# Paramètrage de la dimension de la fenêtre
screen_width = 1366
screen_height = root.winfo_screenheight()

# Appliquer ces dimensions comme taille minimale
root.geometry(f"{screen_width}x{int(screen_height * 0.8)}")
root.title("ACSQDA")

# Fenêtre principale
mframe = CTkFrame(master=root, fg_color="skyblue")
mframe.pack(expand=True, fill="both")

# Thème
customtkinter.set_default_color_theme("blue") 
customtkinter.set_appearance_mode("system")  # "dark", "light", "system"

# Barre de menu
menu = CTkMenuBar(master=mframe)
menu_fichier = menu.add_cascade("fichier")
menu_theme = menu.add_cascade("thème")
menu_other = menu.add_cascade("plus")

dropdown = CustomDropdownMenu(widget=menu_fichier)
dropdown.add_option(option="Nouveau") 
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


# Récupérer le dernier id inséré dans info_client
mysql_connexion_config.cursor.execute("SELECT MAX(id_client) FROM info_client")
result = mysql_connexion_config.cursor.fetchone()
id = result[0] + 1 if result and result[0] is not None else 1

label_width = 100
my_font = CTkFont(family="Comfortaa", size=12, weight="bold", slant="italic")
categorie_selectionne = None

# ---------------------------------------------------------------

# SECTION 1

frame1 = CTkFrame(master=mframe)
frame1.pack(padx=paddings, pady=paddings, side="top", anchor="nw")

# Raison social
raison_social_label = CTkLabel(master=frame1, text="* Raison social: ", font=my_font, fg_color="transparent", anchor="w")
raison_social_label.grid(column=0, row=0, padx=paddings, pady=paddings)

raison_social_input = CTkEntry(master=frame1, textvariable=StringVar())
raison_social_input.grid(column=1, row=0, padx=paddings, pady=paddings)

# Statistique
statistique_label = CTkLabel(master=frame1, text="Statistique: ", font=my_font, fg_color="transparent", anchor="w")
statistique_label.grid(column=0, row=1, padx=paddings, pady=paddings)

statistique_input = CTkEntry(master=frame1, textvariable=StringVar())
statistique_input.grid(column=1, row=1, padx=paddings, pady=paddings)

# NIF
nif_label = CTkLabel(master=frame1, text="NIF: ", font=my_font, fg_color="transparent", anchor="w")
nif_label.grid(column=0, row=2, padx=paddings, pady=paddings)

nif_input = CTkEntry(master=frame1, textvariable=StringVar())
nif_input.grid(column=1, row=2, padx=paddings, pady=paddings)

# Adresse
adresse_label = CTkLabel(master=frame1, text="Adresse: ", font=my_font, fg_color="transparent", anchor="w")
adresse_label.grid(column=0, row=3, padx=paddings, pady=paddings)

adresse_input = CTkEntry(master=frame1, textvariable=StringVar())
adresse_input.grid(column=1, row=3, padx=paddings, pady=paddings)

# N°Facture
facture_label = CTkLabel(master=frame1, text=f"Facture N°{id}", font=my_font, fg_color="transparent", anchor="w")
facture_label.grid(column=0, row=4, padx=paddings, pady=paddings)

# date d'émission

date_emission_label = CTkLabel(master=frame1, text="* Date d'émission: ", font=my_font, fg_color="transparent", anchor="w")
date_emission_label.grid(column=2, row=0, padx=paddings, pady=paddings)

date_emission_input = DateEntry(master=frame1, selectmode='day', date_pattern='yyyy-mm-dd', bd=adresse_input.cget("border_width"), width=15)
date_emission_input.grid(column=3, row=0, padx=paddings, pady=paddings)

# Date du résultat
date_du_resultat_label = CTkLabel(master=frame1, text="* Date du résultat: ", font=my_font, fg_color="transparent", anchor="w")
date_du_resultat_label.grid(column=2, row=1, padx=paddings, pady=paddings)

date_du_resultat_input = DateEntry(master=frame1, selectmode='day', date_pattern='yyyy-mm-dd', width=15)
date_du_resultat_input.grid(column=3, row=1, padx=paddings, pady=paddings)

# Référence des produits (en int)
reference_des_produits_label = CTkLabel(master=frame1, text="Référence des produits: ", font=my_font, fg_color="transparent", anchor="w")
reference_des_produits_label.grid(column=2, row=2, padx=paddings, pady=paddings)

reference_des_produits_input = CTkEntry(master=frame1, textvariable=StringVar())
reference_des_produits_input.grid(column=3, row=2, padx=paddings, pady=paddings)

# Résponsable
responsable_label = CTkLabel(master=frame1, text="* Responsable: ", font=my_font, fg_color="transparent", anchor="w")
responsable_label.grid(column=2, row=3, padx=paddings, pady=paddings)

responsable_input = CTkEntry(master=frame1, textvariable=StringVar())
responsable_input.grid(column=3, row=3, padx=paddings, pady=paddings)

# SECTION 2

frame2 = CTkFrame(master=mframe)
frame2.pack(padx=paddings, pady=paddings, anchor="w", expand=True, fill="both")

def pied_de_page():
    montant_a_payer = CTkLabel(master=frame2, text="Montant à payer: ")
    montant_a_payer.pack(side="bottom", anchor="center")

    def enregister():
        # Enregistrer les informations du client dans la base de données
        if raison_social_input.get() == "" or date_emission_input.get_date() == "" or date_du_resultat_input.get_date() == "" or responsable_input.get() == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires (*)!!")
            return
        else:
            mysql_connexion_config.cursor.execute(
                "INSERT INTO info_client (raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    raison_social_input.get(),
                    statistique_input.get() if statistique_input.get() != "" else None,
                    nif_input.get() if nif_input.get() != "" else None,
                    adresse_input.get()if adresse_input.get() != "" else None,
                    date_emission_input.get_date(),
                    date_du_resultat_input.get_date(),
                    reference_des_produits_input.get(),
                    responsable_input.get()
                )
            )
            mysql_connexion_config.connexion.commit()
            messagebox.showinfo("Succès", "Informations enregistrées avec succès!")
            
    
    bouton_enregistrer = CTkButton(master=frame2, command=enregister,text="Enregistrer", width=ctkbutton)
    bouton_enregistrer.pack(side="right", anchor="se", padx=paddings, pady=paddings)

    print_button = CTkButton(master=frame2, text="Imprimer", width=ctkbutton)
    print_button.pack(side="right", anchor="se", padx=paddings, pady=paddings)
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
    SELECT p.nom_produit, d.num_acte, d.physico, d.micro, d.toxico, d.sous_total
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
            nom_produit, num_acte, physico, micro, toxico, sous_total = produit_row
            row = CTkFrame(master=frame_pour_affichage)
            etat_initial = {"border_width": row.cget("border_width"), "fg_color": row.cget("fg_color")
}
            row.pack(fill="x", padx=5, pady=5)

            CTkLabel(master=row, text=nom_produit, width=label_width, wraplength=label_width, fg_color="transparent").pack(side="left", anchor="w", padx=5, pady=5)

            Num_acte_var = StringVar(value=num_acte)
            Num_acte = CTkEntry(master=row, width=label_width, textvariable=Num_acte_var)
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
                            JOIN produits p ON d.produit_id = p.id
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
            
            def valider_produit(prod, row, btn_m, btn_s, n_a):
                
                if etat["click"]:
                    row.configure(border_width=1, fg_color="skyblue")
                    btn_m.configure(state="disabled") 
                    btn_s.configure(state="disabled")
                    n_a.configure(state="disabled")
                    etat["click"] = False
                
                else:
                    row.configure(border_width=etat_initial["border_width"], fg_color=etat_initial["fg_color"])
                    btn_m.configure(state="normal") 
                    btn_s.configure(state="normal")
                    n_a.configure(state="normal")
                    etat["click"] = True
            
            valider_bouton = CTkButton(master=row, text="valider", width=ctkbutton, command=lambda prod=nom_produit, row=row, btn_m=bouton_modifier, btn_s=bouton_suppr, n_a=Num_acte: valider_produit(prod, row, btn_m, btn_s, n_a))
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

    product_name_label = CTkLabel(master=frame2_2_B, text="Désignation", width=label_width, fg_color="transparent")
    product_name_label.grid(column=0, row=0, padx=paddings, pady=paddings)

    act_label = CTkLabel(master=frame2_2_B, text="N°Acte", width=label_width, fg_color="transparent")
    act_label.grid(column=1, row=0, padx=paddings, pady=paddings)

    physico_chimique_label = CTkLabel(master=frame2_2_B, text="Physico", width=label_width, fg_color="transparent")
    physico_chimique_label.grid(column=2, row=0, padx=paddings, pady=paddings)

    micro_biologic_label = CTkLabel(master=frame2_2_B, text="Micro", width=label_width, fg_color="transparent")
    micro_biologic_label.grid(column=3, row=0, padx=paddings, pady=paddings)

    toxicologic_label = CTkLabel(master=frame2_2_B, text="Toxico", width=label_width, fg_color="transparent")
    toxicologic_label.grid(column=4, row=0, padx=paddings, pady=paddings)

    sous_total_label = CTkLabel(master=frame2_2_B, text="Sous total", width=label_width, fg_color="transparent")
    sous_total_label.grid(column=5, row=0, padx=paddings, pady=paddings)

etiquette()

frame2_2_C = CTkScrollableFrame(master=frame2_2)
frame2_2_C.pack(fill="both", expand=True, padx=paddings, pady=paddings)

root.mainloop()
