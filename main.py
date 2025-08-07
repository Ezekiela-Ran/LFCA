from customtkinter import CTk, CTkFrame, CTkEntry, CTkButton, CTkScrollableFrame, CTkLabel, DoubleVar, CTkFont
from customtkinter import StringVar, IntVar, CTkToplevel
import customtkinter
from CTkMessagebox import CTkMessagebox
import mysql
from tkcalendar import DateEntry
from modalAjouterCategorie import ModalAjouterCategorie
from modalAjouterProduit import ModalAjouterProduit
from modalModifierNumFacture import ModalModifierNumFacture
import data
import mysql_connexion_config
from CTkMenuBar import *
import sys
import subprocess
import time
import modeleFacture
from num2words import num2words

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


def reinitialiser():
    try:
        # Générer un suffixe unique (par exemple : timestamp)
        suffixe = time.strftime("%Y")

        # Liste des tables à sauvegarder
        tables = [
            "categories",
            "produits",
            "produit_details",
            "info_client",
            "produit_analyse",
            "total"
        ]

        for table in tables:
            nom_sauvegarde = f"{table}{suffixe}"
            requete = f"CREATE TABLE {nom_sauvegarde} AS SELECT * FROM {table}"
            mysql_connexion_config.cursor.execute(requete)

        # Suppression des anciennes tables
        for table in reversed(tables):
            mysql_connexion_config.cursor.execute(f"DROP TABLE IF EXISTS {table}")

        mysql_connexion_config.connexion.commit()
        
        CTkMessagebox(message="Réinitialisation terminée avec sauvegarde!", icon="check", option_1="Fermer")
    
    except mysql.connector.Error as err:
        mysql_connexion_config.connexion.rollback()
        print("Erreur:", err)

    
dropdown2 = CustomDropdownMenu(widget=menu_other)
dropdown2.add_option(option="Réinitialiser", command=reinitialiser) 

def modifier_num_facture():
    ModalModifierNumFacture(parent=root,zone_modif_num=num_fact)
#facture_label
dropdown2.add_option(option="Modifier le numéro de la facture", command=modifier_num_facture) 

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
data.id = id

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
def num_fact():    
    facture_label = CTkLabel(master=frame1, text=f"Facture N°{data.id}", font=my_font, fg_color="transparent", anchor="w")
    facture_label.grid(column=0, row=4, padx=paddings, pady=paddings, sticky="w")
num_fact()

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
_suivant = False

def suivant():
    global terminer 
    
    terminer = True
    
    # Enregistrer les informations du client dans la base de données
    if raison_social_input.get() == "" or date_emission_input.get_date() == "" or date_du_resultat_input.get_date() == "" or responsable_input.get() == "":
            CTkMessagebox(title="Error", message="Veuillez complétez tous les champs obligatoires", icon="cancel")
            return
    else:
        global _suivant
        _suivant = True
        btn_suivant()
        frame2 = CTkFrame(master=mframe, border_width=1, border_color="gray")
        frame2.pack(padx=paddings, pady=paddings, anchor="w", expand=True, fill="both")
        
        def pied_de_page():
            
            
            def terminer():
                if data.etat_validation_produits != {} and data.valeur_ref_bull_analyse != {}:
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
                    
                    for produit in data.etat_validation_produits.keys():
                        
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
                        resultat_client = data.id 
                        
                        if resultat_client:
                            id_client = resultat_client
                        else:
                            print("Client introuvable")
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
                        cursor.execute("""INSERT INTO produit_analyse (client_id, produit_id, ref_bull_analyse, num_acte, physico, micro, toxico, sous_total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (id_client,id_produit, data.valeur_ref_bull_analyse[produit], data.valeur_num_acte.get(produit, ""), physico, micro, toxico, sous_total))
                        
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
                    id_client = data.id
                    
                    cursor_for_total.execute("INSERT INTO total(client_id, total) VALUES (%s, %s)", (id_client, total))
                    mysql_connexion_config.connexion.commit()
                    
                    # Montant à payer en lettre
                    mysql_connexion_config.cursor.execute("SELECT total FROM total WHERE client_id = %s", (data.id,))
                    montant = mysql_connexion_config.cursor.fetchone()
                    montant_en_lettre = num2words(int(montant[0]), lang='fr', to='currency')
                    montant_a_payer = CTkLabel(master=mframe, text=f"Montant à payer: {montant_en_lettre.upper()} Ariary ({montant[0]}Ar) ")
                    montant_a_payer.pack(side="bottom", anchor="center")
                    
                    
                    #  Saisie de la facture
                    mysql_connexion_config.cursor.execute("SELECT raison_sociale FROM info_client WHERE id_client=%s",(data.id,))
                    raison_social = mysql_connexion_config.cursor.fetchone()
                    
                    mysql_connexion_config.cursor.execute("SELECT p.nom_produit, pa.ref_bull_analyse, pa.num_acte, pa.physico, pa.micro, pa.toxico, pa.sous_total FROM produit_analyse pa JOIN produits p ON pa.client_id = %s AND p.id_produit = pa.produit_id", (data.id,))
                
                    
                    produit_analyser = [
                        [designation, ref_analyse, num_acte, physico, micro, toxico, sous_total]
                        for designation, ref_analyse, num_acte, physico, micro, toxico, sous_total in mysql_connexion_config.cursor.fetchall()
                    ]

                    
                    if len(data.etat_validation_produits) <= 23:
                        modeleFacture.saisir_facture(raison_social[0], produit_analyser)
                    
                    
                    
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
                    CTkMessagebox(title="Error", message="Aucun produit validé ou réf. bulletin d'analyse est vide", icon="cancel")
                    
                    
            bouton_terminer = CTkButton(master=frame2, text="Terminer et imprimer", width=ctkbutton, command=terminer)
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
                       
            if produits:
                for produit_row in produits:
                    nom_produit, physico, micro, toxico, sous_total = produit_row
                    # Synchroniser est_valide avec data.etat_validation_produits
                    est_valide = bool(data.etat_validation_produits.get(nom_produit, False))
                    
                    rang = CTkFrame(
                        master=frame_pour_affichage
                    )
                    rang.pack(fill="x", padx=5, pady=5)
                    
                    etat_initial = {"border_width": rang.cget("border_width"), "fg_color": rang.cget("fg_color")}
                    
                    CTkLabel(master=rang, text=nom_produit, width=label_width, wraplength=label_width, fg_color="transparent").pack(side="left", anchor="w", padx=5, pady=5)

                    valeur_ref = data.valeur_ref_bull_analyse.get(nom_produit, 0)
                    
                    try:
                        Ref_bull_var = IntVar(value=int(valeur_ref))
                    except (ValueError, TypeError):
                        Ref_bull_var = IntVar(value=0)
                        print("ref. bulletin analyse error!")

                    def valider_entree(chiffre):
                        return chiffre.isdigit() or chiffre == ""

                    vcmd = (rang.register(valider_entree), '%P')   

                    Ref_bull_analyse = CTkEntry(master=rang, width=label_width, textvariable=Ref_bull_var, justify="right", state="disabled" if est_valide else "normal", validate="key", validatecommand=vcmd)
                    Ref_bull_analyse.pack(side="left", anchor="w", padx=5, pady=5)
                    

                    valeur_numActe = data.valeur_num_acte.get(nom_produit, "")
                    try:
                        Num_acte_var = StringVar(value=valeur_numActe)
                    except (ValueError, TypeError):
                        Num_acte_var = StringVar(value="")
                        print("ref. num acte error!")
                      
                    
                    Num_acte = CTkEntry(master=rang, width=label_width, textvariable=Num_acte_var, justify="right", state="disabled" if est_valide else "normal")
                    Num_acte.pack(side="left", anchor="w", padx=5, pady=5)
                    
                    def keyrelease_reference_b_analyse(var_ref, nom):
                        def handler(event):
                            valeur1 = var_ref.get()
                            
                            if valeur1 != 0:
                                data.valeur_ref_bull_analyse[nom] = valeur1
                                
                        return handler

                    Ref_bull_analyse.bind("<KeyRelease>", keyrelease_reference_b_analyse(Ref_bull_var, nom_produit))
                    
                    def keyrelease_num_acte(var_acte, nom):
                        def handler(event):
                            valeur = var_acte.get()
                          
                            if valeur != "":
                                data.valeur_num_acte[nom] = valeur
                                
                        return handler
                    
                    Num_acte.bind("<KeyRelease>", keyrelease_num_acte(Num_acte_var, nom_produit))

                    Physico_var = DoubleVar(value=physico)
                    Physico = CTkEntry(master=rang, state="disabled", width=label_width, justify="right", textvariable=Physico_var)
                    Physico.pack(side="left", anchor="w", padx=5, pady=5)

                    Micro_var = DoubleVar(value=micro)
                    Micro = CTkEntry(master=rang, state="disabled", width=label_width, justify="right", textvariable=Micro_var)
                    Micro.pack(side="left", anchor="w", padx=5, pady=5)

                    Toxico_var = DoubleVar(value=toxico)
                    Toxico = CTkEntry(master=rang, state="disabled", width=label_width, justify="right", textvariable=Toxico_var)
                    Toxico.pack(side="left", anchor="w", padx=5, pady=5)

                    Sous_total_var = DoubleVar(value=sous_total)
                    Sous_total = CTkEntry(master=rang, state="disabled", width=label_width, justify="right", textvariable=Sous_total_var)
                    Sous_total.pack(side="left", anchor="w", padx=5, pady=5)

                    def only_float(P):
                        if P == "" or P.replace(".", "", 1).isdigit():
                            return True
                        return False

                    vcmd = (rang.register(only_float), "%P")
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

                    # Synchronisation du bouton valider/annuler avec est_valide
                    def valider_produit(prod, rang, btn_m, btn_s, n_a, rba, valider_btn):
                        est_valide = bool(data.etat_validation_produits.get(prod, False))
                        if not est_valide:
                            rang.configure(border_width=1, fg_color=['skyblue','gray17'] )
                            btn_m.configure(state="disabled") 
                            btn_s.configure(state="disabled")
                            n_a.configure(state="disabled")
                            rba.configure(state="disabled")
                
                            data.etat_validation_produits[prod] = True
                            valider_btn.configure(text="annuler")
                        
                        else:
                            rang.configure(border_width=etat_initial["border_width"], fg_color=etat_initial["fg_color"])
                            btn_m.configure(state="normal") 
                            btn_s.configure(state="normal")
                            n_a.configure(state="normal")
                            rba.configure(state="normal")
                            del data.etat_validation_produits[prod]
                            valider_btn.configure(text="valider")
                            

                    bouton_modifier = CTkButton(
                        master=rang,
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

                    bouton_suppr = CTkButton(master=rang, text="suppr", width=ctkbutton, command=supprimer_produit)
                    bouton_suppr.pack(side="left", anchor="w", padx=5, pady=5)
                    
                    valider_bouton = CTkButton(
                        master=rang,
                        text="annuler" if est_valide else "valider",
                        width=ctkbutton,
                        command=lambda prod=nom_produit, r=rang, btn_m=bouton_modifier, btn_s=bouton_suppr, rba=Ref_bull_analyse, n_a=Num_acte: valider_produit(prod, r, btn_m, btn_s, n_a, rba)
                    )
                    # On doit passer le bouton lui-même à la fonction pour pouvoir changer son texte
                    valider_bouton.configure(command=lambda prod=nom_produit, r=rang, btn_m=bouton_modifier, btn_s=bouton_suppr, rba=Ref_bull_analyse, n_a=Num_acte, valider_btn=valider_bouton: valider_produit(prod, r, btn_m, btn_s, n_a, rba, valider_btn))
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
                    
def btn_suivant():
    bouton_suivant = CTkButton(master=frame1, command=suivant,text="Suivant", width=ctkbutton, state="disabled" if _suivant else "normal")
    bouton_suivant.grid(column=3, row=4, padx=paddings, pady=paddings)
    return bouton_suivant
btn_suivant()
bouton_suivant = btn_suivant()

# CORP (body)
if not terminer :
    frame2 = CTkFrame(master=mframe)
    frame2.pack_forget()


root.mainloop()
