from customtkinter import CTk, CTkFrame, CTkEntry, CTkButton, CTkScrollableFrame, CTkLabel, DoubleVar, CTkFont
from customtkinter import StringVar, IntVar, CTkRadioButton
import customtkinter
from CTkMessagebox import CTkMessagebox

from modalAjouterCategorie import ModalAjouterCategorie
from modalAjouterProduit import ModalAjouterProduit
from modalModifierNumFacture import ModalModifierNumFacture
from modalRechercherModifierFacture import ModalRechercherModifierFacture
import data
import mysql_connexion_config
from CTkMenuBar import *
import modeleFacture
from num2words import num2words
from nouveau import Nouveau
from reinitialiser import Reinitialiser
from facture import Facture
from typeFacture.facture_proforma import FactureProforma
from typeFacture.facture_simple import FactureSimple

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


dropdown = CustomDropdownMenu(widget=menu_fichier)

dropdown.add_option(option="Nouveau", command=Nouveau(parent=root).relance_fantôme) 


# Rechercher un facture
def rechercher_facture():
    ModalRechercherModifierFacture(parent=root)

dropdown.add_option(option="Rechercher facture", command=rechercher_facture) 

dropdown1 = CustomDropdownMenu(widget=menu_theme)
dropdown1.add_option(option="sombre", command=lambda: customtkinter.set_appearance_mode("dark")) 
dropdown1.add_option(option="lumineux", command=lambda: customtkinter.set_appearance_mode("light")) 


dropdown2 = CustomDropdownMenu(widget=menu_other)
dropdown2.add_option(option="Réinitialiser", command=Reinitialiser().reinitialiser) 

# Modifier le numéro de la facture dans la base de donnée et à l'affichage
def modifier_num_facture():
    ModalModifierNumFacture(parent=root, frame1=frame1, paddings=paddings, my_font=my_font, facture_label=facture_label)

# Menu dropdown pour modifier le numéro de la facture
dropdown2.add_option(option="Modifier le numéro de la facture", command=modifier_num_facture) 

# Obtenir les catégories de produit dans la base de donnée et placer dans data.produit_par_categorie
mysql_connexion_config.cursor.execute("SELECT * FROM categories")
for row in mysql_connexion_config.cursor.fetchall():
    data.produit_par_categorie[row[1]] = {}

# Initialisation
paddings = 5
ctkbutton = 10


label_width = 75
my_font = CTkFont(family="Comfortaa", size=12, weight="bold", slant="italic")
categorie_selectionne = None

# ---------------------------------------------------------------

# Entête

frame1 = CTkFrame(master=mframe, border_color="gray", border_width=1)
frame1.pack(padx=paddings, pady=paddings, side="top", anchor="nw")


selected_option = StringVar(value="Option 1")  # valeur par défaut

def type_de_facture():
    option = selected_option.get()  # Récupère la valeur sélectionnée
    if option == "Option 2":
       factureProforma = FactureProforma(frame1, paddings, my_font)
       factureProforma.num_fact(facture_label)
       factureProforma.info_client()
        
    elif option == "Option 1":
        factureSimple = FactureSimple(frame1, paddings, my_font)
        factureSimple.num_fact(facture_label)
        factureSimple.info_client()
        
    else:
        print("Option sélectionnée inconnue :", option)



# Créer les boutons radio
radio1 = CTkRadioButton(
    frame1,
    text="Facture",
    variable=selected_option,
    value="Option 1",
    width=20,
    height=20,
    border_width_checked=5,
    border_width_unchecked=2,
    radiobutton_height=16,
    radiobutton_width=16,
    font=my_font,
    text_color="black",
    fg_color="skyblue",
    command=type_de_facture
)

radio2 = CTkRadioButton(
    frame1,
    text="Facture PROFORMA",
    variable=selected_option,
    value="Option 2",
    width=20,
    height=20,
    border_width_checked=5,
    border_width_unchecked=2,
    radiobutton_height=16,
    radiobutton_width=16,
    font=my_font,
    text_color="black",
    fg_color="skyblue",
    command=type_de_facture
)

# Placer les boutons
radio1.grid(row=0, column=0, sticky="w", padx=10, pady=5)
radio2.grid(row=0, column=1, sticky="w", padx=10, pady=5)



# N°Facture
facture_label = CTkLabel(master=frame1, text="", font=my_font, fg_color="transparent", anchor="w")
facture_label.grid(column=0, row=5, padx=paddings, pady=paddings, sticky="w")

Facture(frame1=frame1, paddings=paddings, my_font=my_font).num_fact(facture_label)

type_de_facture()



# # CORPS 

# frame2 = CTkFrame(master=mframe, border_width=1, border_color="gray")
# frame2.pack(padx=paddings, pady=paddings, anchor="w", expand=True, fill="both")

# def pied_de_page():
    
#     def terminer():
#         if (
#             raison_social_input.get() != "" and
#             date_emission_input.get_date() != "" and
#             date_du_resultat_input.get_date() != "" and
#             responsable_input.get() != ""
#             ) and (
#             data.etat_validation_produits != {} and
#             data.valeur_ref_bull_analyse != {}
#             ):
                
#             mysql_connexion_config.cursor.execute("INSERT INTO info_client (raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#             (
#             raison_social_input.get(),
#             statistique_input.get() if statistique_input.get() != "" else None,
#             nif_input.get() if nif_input.get() != "" else None,
#             adresse_input.get()if adresse_input.get() != "" else None,
#             date_emission_input.get_date(),
#             date_du_resultat_input.get_date(),
#             reference_des_produits_input.get(),
#             responsable_input.get() ))
#             mysql_connexion_config.connexion.commit()
            
#             for produit in data.etat_validation_produits.keys():
                
#                 cursor = mysql_connexion_config.connexion.cursor(buffered=True)
#                 cursor.execute("SELECT id_produit FROM produits WHERE nom_produit = %s", (produit,))
#                 resultat = cursor.fetchone()
                
#                 if resultat:
#                     id_produit = resultat[0]
#                 else:
#                     print("Produit introuvable")
#                     cursor.close()
#                     return  # ou gérer l'erreur proprement
                
#                 # récupérer l'ID du client
#                 resultat_client = data.id 
                
#                 if resultat_client:
#                     id_client = resultat_client
#                 else:
#                     print("Client introuvable")
#                     return
                
#                 # récupérer les détails du produit
#                 cursor.execute("""SELECT physico, micro, toxico, sous_total FROM produit_details WHERE produit_id = %s """, (id_produit,))
#                 details = cursor.fetchone()
                    
#                 if not details:
#                     print("Détails du produit introuvables")
#                     cursor.close()
#                     return
                    
#                 physico, micro, toxico, sous_total = details
                
#                 data.total[produit] = sous_total
                
#                 # insérer les données dans produit_analyse
#                 cursor.execute("""INSERT INTO produit_analyse (client_id, produit_id, ref_bull_analyse, num_acte, physico, micro, toxico, sous_total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (id_client,id_produit, data.valeur_ref_bull_analyse[produit], data.valeur_num_acte.get(produit, ""), physico, micro, toxico, sous_total))
                
#                 mysql_connexion_config.connexion.commit()
#                 cursor.close()

#             total = 0
#             for sous_total in data.total.values():
#                 try:
#                     total += float(sous_total)
#                 except (ValueError, TypeError):
#                     print(f"Erreur: sous_total non numérique ({sous_total}) ignoré.")
            
#             cursor_for_total = mysql_connexion_config.connexion.cursor()
            
#             # récupérer l'ID du client
#             id_client = data.id
            
#             cursor_for_total.execute("INSERT INTO total(client_id, total) VALUES (%s, %s)", (id_client, total))
#             mysql_connexion_config.connexion.commit()
            
#             # Montant à payer en lettre
#             mysql_connexion_config.cursor.execute("SELECT total FROM total WHERE client_id = %s", (data.id,))
#             montant = mysql_connexion_config.cursor.fetchone()
#             montant_en_lettre = num2words(int(montant[0]), lang='fr')
#             montant_a_payer = CTkLabel(master=mframe, text=f"Montant à payer: {montant_en_lettre.upper()} Ariary ({montant[0]}Ar) ")
#             montant_a_payer.pack(side="bottom", anchor="center")
            
            
#             #  Saisie de la facture
#             mysql_connexion_config.cursor.execute("SELECT raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable FROM info_client WHERE id_client=%s",(data.id,))
            
#             info_client = mysql_connexion_config.cursor.fetchone()
#             raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable = info_client
            
            
#             mysql_connexion_config.cursor.execute("SELECT p.nom_produit, pa.ref_bull_analyse, pa.num_acte, pa.physico, pa.micro, pa.toxico, pa.sous_total FROM produit_analyse pa JOIN produits p ON pa.client_id = %s AND p.id_produit = pa.produit_id", (data.id,))
        
            
#             produit_analyser = [
#                 [designation, ref_analyse, num_acte, physico, micro, toxico, sous_total]
#                 for designation, ref_analyse, num_acte, physico, micro, toxico, sous_total in mysql_connexion_config.cursor.fetchall()
#             ]
            
#             mysql_connexion_config.cursor.execute("SELECT total FROM total WHERE client_id = %s", (data.id,))
            
#             net_a_payer = mysql_connexion_config.cursor.fetchone()

            
#             if len(data.etat_validation_produits) <= 23:
#                 modeleFacture.saisir_facture(data.id, raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable, produit_analyser, net_a_payer[0])
            
            
            
#             data.etat_validation_produits.clear()
#             data.valeur_ref_bull_analyse.clear()
#             data.valeur_num_acte.clear()
#             data.total.clear()
#             CTkMessagebox(message=f"Enregistrement effectué avec succès!\n Total: {total}",
#             icon="check", option_1="Fermer")
            
#             for widget in frame2.winfo_children():
#                 widget.destroy()
        
         
#         else:
#             CTkMessagebox(title="Error", message="Champs obligatoires non remplis ou aucun produit validé ou réf. bulletin d'analyse nulle", icon="cancel")
            
            
#     bouton_terminer = CTkButton(master=frame2, text="Terminer et imprimer", width=ctkbutton, command=terminer)
#     bouton_terminer.pack(side="right", anchor="se", padx=paddings, pady=paddings)
# pied_de_page()

# # SUB SECTION 2-1 (Première colonne)

# frame2_1 = CTkFrame(master=frame2)
# frame2_1.pack(padx=paddings, pady=paddings, fill="both", side="left")

# frame2_1_A = CTkFrame(master=frame2_1)
# frame2_1_A.pack(fill="x", padx=paddings, pady=paddings)

# product_type_label = CTkLabel(master=frame2_1_A, text="TYPE DE PRODUIT",fg_color="transparent")
# product_type_label.pack(side="left", padx=paddings, pady=paddings)

# # Ajouter un type de produit "MODAL WINDOW"


# def ajouter_un_categorie():
#     ModalAjouterCategorie(master=root, frame=frame2_1_B, callback=afficher_categories)

# bouton_ajouter_categorie = CTkButton(master=frame2_1_A, text="Ajouter", command=ajouter_un_categorie, width=ctkbutton)
# bouton_ajouter_categorie.pack(side="right", padx=paddings, pady=paddings)

# # Supprimer un Catégorie
# def supp_categorie():
    
#     for categorie in list(data.produit_par_categorie.keys()): 
#         if categorie == categorie_selectionne:
#             mysql_connexion_config.cursor.execute(
#                 "DELETE FROM categories WHERE nom_categorie = %s",
#                 (categorie_selectionne,)
#             )
#             mysql_connexion_config.connexion.commit()
#             del data.produit_par_categorie[categorie_selectionne]
            
#             for widget in frame2_1_B.winfo_children():
#                 widget.destroy()
#             for widget in frame2_2_C.winfo_children():
#                 widget.destroy()
#             afficher_categories()
#             break

# bouton_supprimer_categorie = CTkButton(master=frame2_1_A, text="Supprimer", command=supp_categorie, width=ctkbutton)
# bouton_supprimer_categorie.pack(side="right", padx=paddings, pady=paddings)

# frame2_1_B = CTkScrollableFrame(master=frame2_1)
# frame2_1_B.pack(padx=paddings, pady=paddings, expand=True, fill="both", anchor="nw")

# # Sélection et affichage du type de produit
# def choisir_la_categorie_et_afficher_les_produit(categorie, frame_pour_affichage):
#     global categorie_selectionne
#     categorie_selectionne = categorie
#     for widget in frame_pour_affichage.winfo_children():
#         widget.destroy()
#     cursor = mysql_connexion_config.cursor
#     # Récupérer les produits de la catégorie depuis la base
#     cursor.execute("""
#     SELECT p.nom_produit, d.physico, d.micro, d.toxico, d.sous_total
#     FROM produits p
#     JOIN produit_details d ON p.id_produit = d.id_produit_detail
#     WHERE p.categorie_id = (
#         SELECT id_categorie FROM categories WHERE nom_categorie = %s
#     )
# """, (categorie_selectionne,))

#     produits = cursor.fetchall()
                
#     if produits:
#         for produit_row in produits:
#             nom_produit, physico, micro, toxico, sous_total = produit_row
#             # Synchroniser est_valide avec data.etat_validation_produits
#             est_valide = bool(data.etat_validation_produits.get(nom_produit, False))
            
#             rang = CTkFrame(
#                 master=frame_pour_affichage
#             )
#             rang.pack(fill="x", padx=5, pady=5)
            
#             etat_initial = {"border_width": rang.cget("border_width"), "fg_color": rang.cget("fg_color")}
            
#             CTkLabel(master=rang, text=nom_produit, width=label_width, wraplength=label_width, fg_color="transparent").pack(side="left", anchor="w", padx=5, pady=5)

#             valeur_ref = data.valeur_ref_bull_analyse.get(nom_produit, 0)
            
#             try:
#                 Ref_bull_var = IntVar(value=int(valeur_ref))
#             except (ValueError, TypeError):
#                 Ref_bull_var = IntVar(value=0)
#                 print("ref. bulletin analyse error!")

#             def valider_entree(chiffre):
#                 return chiffre.isdigit() or chiffre == ""

#             vcmd = (rang.register(valider_entree), '%P')   

#             Ref_bull_analyse = CTkEntry(master=rang, width=label_width, textvariable=Ref_bull_var, justify="right", state="disabled" if est_valide else "normal", validate="key", validatecommand=vcmd)
#             Ref_bull_analyse.pack(side="left", anchor="w", padx=5, pady=5)
            

#             valeur_numActe = data.valeur_num_acte.get(nom_produit, "")
#             try:
#                 Num_acte_var = StringVar(value=valeur_numActe)
#             except (ValueError, TypeError):
#                 Num_acte_var = StringVar(value="")
#                 print("ref. num acte error!")
                
            
#             Num_acte = CTkEntry(master=rang, width=label_width, textvariable=Num_acte_var, justify="right", state="disabled" if est_valide else "normal")
#             Num_acte.pack(side="left", anchor="w", padx=5, pady=5)
            
#             def keyrelease_reference_b_analyse(var_ref, nom):
#                 def handler(event):
#                     valeur1 = var_ref.get()
                    
#                     if valeur1 != 0:
#                         data.valeur_ref_bull_analyse[nom] = valeur1
                        
#                 return handler

#             Ref_bull_analyse.bind("<KeyRelease>", keyrelease_reference_b_analyse(Ref_bull_var, nom_produit))
            
#             def keyrelease_num_acte(var_acte, nom):
#                 def handler(event):
#                     valeur = var_acte.get()
                    
#                     if valeur != "":
#                         data.valeur_num_acte[nom] = valeur
                        
#                 return handler
            
#             Num_acte.bind("<KeyRelease>", keyrelease_num_acte(Num_acte_var, nom_produit))

#             Physico_var = DoubleVar(value=physico)
#             physico_avec_separateur = StringVar(value=f"{int(Physico_var.get()):,}".replace(",", " "))
#             Physico = CTkEntry(master=rang, state="disabled", width=label_width, justify="right", textvariable=physico_avec_separateur)
#             Physico.pack(side="left", anchor="w", padx=5, pady=5)

#             Micro_var = DoubleVar(value=micro)
#             Micro_avec_separateur = StringVar(value=f"{int(Micro_var.get()):,}".replace(",", " "))
#             Micro = CTkEntry(master=rang, state="disabled", width=label_width, justify="right", textvariable=Micro_avec_separateur)
#             Micro.pack(side="left", anchor="w", padx=5, pady=5)

#             Toxico_var = DoubleVar(value=toxico)
#             Toxico_avec_separateur = StringVar(value=f"{int(Toxico_var.get()):,}".replace(",", " "))
#             Toxico = CTkEntry(master=rang, state="disabled", width=label_width, justify="right", textvariable=Toxico_avec_separateur)
#             Toxico.pack(side="left", anchor="w", padx=5, pady=5)


#             Sous_total_var = DoubleVar(value=sous_total)
#             Sous_total_avec_separateur = StringVar(value=f"{int(Sous_total_var.get()):,}".replace(",", " "))
#             Sous_total = CTkEntry(master=rang, state="disabled", width=label_width, justify="right", textvariable=Sous_total_avec_separateur)
#             Sous_total.pack(side="left", anchor="w", padx=5, pady=5)

#             def only_float(P):
#                 if P == "" or P.replace(".", "", 1).isdigit():
#                     return True
#                 return False

#             vcmd = (rang.register(only_float), "%P")
#             Physico.configure(validate="key", validatecommand=vcmd)
#             Micro.configure(validate="key", validatecommand=vcmd)
#             Toxico.configure(validate="key", validatecommand=vcmd)

#             def modifier(nom_produit, Physico, Micro, Toxico, Sous_total, Physico_var, Micro_var, Toxico_var, Sous_total_var):
                
#                 Physico.configure(state="normal", textvariable=Physico_var)
                
#                 Physico.focus_set()
                
#                 def on_physico_return(event):
                    
#                     physico_avec_separateur = StringVar(value=f"{int(Physico_var.get()):,}".replace(",", " "))
                    
#                     Physico.configure(state="disabled",textvariable=physico_avec_separateur)
                    
#                     Micro.configure(state="normal", textvariable=Micro_var)
                    
#                     cursor.execute("""
#                         UPDATE produit_details d
#                         JOIN produits p ON d.id_produit_detail = p.id_produit
#                         SET d.physico = %s
#                         WHERE p.nom_produit = %s
#                         AND p.categorie_id = (
#                         SELECT id_categorie FROM categories WHERE nom_categorie = %s
#                     )""",
#                     (Physico_var.get(), nom_produit, categorie_selectionne))

#                     mysql_connexion_config.connexion.commit()
#                     Micro.focus_set()
#                 Physico.bind("<Return>", on_physico_return)
                
#                 def on_micro_return(event):
                    
#                     Micro_avec_separateur = StringVar(value=f"{int(Micro_var.get()):,}".replace(",", " "))
                    
#                     Micro.configure(state="disabled", textvariable=Micro_avec_separateur)
                    
#                     Toxico.configure(state="normal", textvariable=Toxico_var)
                    
#                     cursor.execute("""
#                         UPDATE produit_details d
#                         JOIN produits p ON d.id_produit_detail = p.id_produit
#                         SET d.micro = %s
#                         WHERE p.nom_produit = %s
#                         AND p.categorie_id = (
#                         SELECT id_categorie FROM categories WHERE nom_categorie = %s
#                     )""",
#                     (Micro_var.get(), nom_produit, categorie_selectionne))
#                     mysql_connexion_config.connexion.commit()
#                     Toxico.focus_set()
#                 Micro.bind("<Return>", on_micro_return)
                
#                 def on_toxico_return(event):
#                     try:
#                         cursor.execute("""
#                             UPDATE produit_details d
#                             JOIN produits p ON d.id_produit_detail = p.id_produit
#                             SET d.toxico = %s
#                             WHERE p.nom_produit = %s
#                             AND p.categorie_id = (
#                             SELECT id_categorie FROM categories WHERE nom_categorie = %s
#                         )""",
#                         (Toxico_var.get(), nom_produit, categorie_selectionne))
                        
#                         physico_val = float(Physico_var.get())
#                         micro_val = float(Micro_var.get())
#                         toxico_val = float(Toxico_var.get())
#                         sous_total_val = physico_val + micro_val + toxico_val
#                         Sous_total_var.set(sous_total_val)
#                         cursor.execute("""
#                             UPDATE produit_details d
#                             JOIN produits p ON d.produit_id = p.id_produit
#                             SET d.sous_total = %s
#                             WHERE p.nom_produit = %s
#                             AND p.categorie_id = (
#                             SELECT id_categorie FROM categories WHERE nom_categorie = %s
#                         )""",
#                         (sous_total_val, nom_produit, categorie_selectionne))
#                         mysql_connexion_config.connexion.commit()
                        
#                         Sous_total_avec_separateur = StringVar(value=f"{int(Sous_total_var.get()):,}".replace(",", " "))
                        
#                         Sous_total.configure(state="disabled", textvariable=Sous_total_avec_separateur)
#                         Physico.configure(state="disabled")
#                         Micro.configure(state="disabled")
                        
#                         Toxico_avec_separateur = StringVar(value=f"{int(Toxico_var.get()):,}".replace(",", " "))
                        
#                         Toxico.configure(state="disabled", textvariable=Toxico_avec_separateur)
#                     except ValueError:
#                         print("Veuillez entrer un nombre valide.")
#                 Toxico.bind("<Return>", on_toxico_return)

#             # Synchronisation du bouton valider/annuler avec est_valide
#             def valider_produit(prod, rang, btn_m, btn_s, n_a, rba, valider_btn):
#                 est_valide = bool(data.etat_validation_produits.get(prod, False))
#                 if not est_valide:
#                     rang.configure(border_width=1, fg_color=['skyblue','gray17'] )
#                     btn_m.configure(state="disabled") 
#                     btn_s.configure(state="disabled")
#                     n_a.configure(state="disabled")
#                     rba.configure(state="disabled")
        
#                     data.etat_validation_produits[prod] = True
#                     valider_btn.configure(text="annuler")
                
#                 else:
#                     rang.configure(border_width=etat_initial["border_width"], fg_color=etat_initial["fg_color"])
#                     btn_m.configure(state="normal") 
#                     btn_s.configure(state="normal")
#                     n_a.configure(state="normal")
#                     rba.configure(state="normal")
#                     del data.etat_validation_produits[prod]
#                     valider_btn.configure(text="valider")
                    

#             bouton_modifier = CTkButton(
#                 master=rang,
#                 text="Modifier",
#                 width=ctkbutton,
                
#                 command=lambda prod=nom_produit, p=Physico, m=Micro, t=Toxico, s=Sous_total, pv=Physico_var, mv=Micro_var, tv=Toxico_var, sv=Sous_total_var: modifier(prod, p, m, t, s, pv, mv, tv, sv)
#             )
#             bouton_modifier.pack(side="left", anchor="w", padx=5, pady=5)

#             def supprimer_produit():
#                 cursor.execute(
#                     "DELETE FROM produits WHERE nom_produit = %s AND categorie_id = (SELECT id_categorie FROM categories WHERE nom_categorie = %s)",
#                     (nom_produit, categorie_selectionne)
#                 )
#                 mysql_connexion_config.connexion.commit()
                
#                 for widget in frame_pour_affichage.winfo_children():
#                     widget.destroy()
#                 choisir_la_categorie_et_afficher_les_produit(categorie_selectionne, frame_pour_affichage)

#             bouton_suppr = CTkButton(master=rang, text="suppr", width=ctkbutton, command=supprimer_produit)
#             bouton_suppr.pack(side="left", anchor="w", padx=5, pady=5)
            
#             valider_bouton = CTkButton(
#                 master=rang,
#                 text="annuler" if est_valide else "valider",
#                 width=ctkbutton,
#                 command=lambda prod=nom_produit, r=rang, btn_m=bouton_modifier, btn_s=bouton_suppr, rba=Ref_bull_analyse, n_a=Num_acte: valider_produit(prod, r, btn_m, btn_s, n_a, rba)
#             )
#             # On doit passer le bouton lui-même à la fonction pour pouvoir changer son texte
#             valider_bouton.configure(command=lambda prod=nom_produit, r=rang, btn_m=bouton_modifier, btn_s=bouton_suppr, rba=Ref_bull_analyse, n_a=Num_acte, valider_btn=valider_bouton: valider_produit(prod, r, btn_m, btn_s, n_a, rba, valider_btn))
#             valider_bouton.pack(side="left", anchor="w", padx=5, pady=5)
#     else:
#         CTkLabel(master=frame_pour_affichage, text=f"Type de produit: {categorie_selectionne}", fg_color="transparent").pack(side="left", fill="both", expand=True)

# def afficher_categories():
#     if data.produit_par_categorie:
#         for categorie in list(data.produit_par_categorie.keys()):
#             CTkButton(master=frame2_1_B, text=categorie, width=ctkbutton, command=lambda categorie=categorie: choisir_la_categorie_et_afficher_les_produit(categorie, frame2_2_C)).pack(fill="x", padx=paddings, pady=paddings)
#     else:
#         CTkLabel(master=frame2_1_B, text="Aucun type de produit", fg_color="transparent").pack(fill="x", padx=paddings, pady=paddings)

# afficher_categories()

# # SUB SECTION 2-2 (Deuxième colonne)

# frame2_2 = CTkFrame(master=frame2)
# frame2_2.pack(padx=paddings, pady=paddings, expand=True, fill="both", side="right")

# frame2_2_A = CTkFrame(master=frame2_2)
# frame2_2_A.pack(padx=paddings, pady=paddings, fill="both")

# def ajouter_produit():
#     if categorie_selectionne:
#         ModalAjouterProduit(root, categorie_selectionne, callback=lambda: choisir_la_categorie_et_afficher_les_produit(categorie_selectionne, frame2_2_C))
#     return

# ajouter_produit_button = CTkButton(master=frame2_2_A, text="Ajouter produit", width=ctkbutton, command=ajouter_produit)
# ajouter_produit_button.pack(side="right", padx=paddings, pady=paddings)

# def etiquette():
#     frame2_2_B = CTkFrame(master=frame2_2)
#     frame2_2_B.pack(fill="x", padx=paddings, pady=paddings)

#     product_name_label = CTkLabel(master=frame2_2_B, text="Désignation", width=label_width, fg_color="transparent", wraplength=label_width)
#     product_name_label.grid(column=0, row=0, padx=paddings, pady=paddings)
    
#     ref_bulletin_analyse = CTkLabel(master=frame2_2_B, text="Ref. B. analyse", width=label_width, fg_color="transparent", wraplength=label_width)
#     ref_bulletin_analyse.grid(column=1, row=0, padx=paddings, pady=paddings)

#     act_label = CTkLabel(master=frame2_2_B, text="N°Acte", width=label_width, fg_color="transparent", wraplength=label_width)
#     act_label.grid(column=2, row=0, padx=paddings, pady=paddings)

#     physico_chimique_label = CTkLabel(master=frame2_2_B, text="Physico", width=label_width, fg_color="transparent", wraplength=label_width)
#     physico_chimique_label.grid(column=3, row=0, padx=paddings, pady=paddings)

#     micro_biologic_label = CTkLabel(master=frame2_2_B, text="Micro", width=label_width, fg_color="transparent", wraplength=label_width)
#     micro_biologic_label.grid(column=4, row=0, padx=paddings, pady=paddings)

#     toxicologic_label = CTkLabel(master=frame2_2_B, text="Toxico", width=label_width, fg_color="transparent", wraplength=label_width)
#     toxicologic_label.grid(column=5, row=0, padx=paddings, pady=paddings)

#     sous_total_label = CTkLabel(master=frame2_2_B, text="Sous total", width=label_width, fg_color="transparent", wraplength=label_width)
#     sous_total_label.grid(column=6, row=0, padx=paddings, pady=paddings)

# etiquette()

# frame2_2_C = CTkScrollableFrame(master=frame2_2)
# frame2_2_C.pack(fill="both", expand=True, padx=paddings, pady=paddings)
                

root.mainloop()
