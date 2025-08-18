import data
import mysql_connexion_config
from customtkinter import CTkLabel, CTkEntry, StringVar
from tkcalendar import DateEntry

class Facture:
    def __init__(self, frame1, paddings, my_font):
        self.frame1 = frame1
        self.paddings = paddings
        self.my_font = my_font
        
        
        # Déterminer les paramètres selon le type de facture
        if data.facture_proforma:
            self.table = "facture_proforma"
            self.column = "id_proforma"
            self.label_prefix = "Facture PROFORMA N°"
            self.id = 1
        else:
            self.table = "info_client"
            self.column = "id_client"
            self.label_prefix = "Facture N°"
            self.id = data.id
    
    def num_fact(self, facture_label):
        
        # Récupérer le dernier ID inséré
        query = f"SELECT MAX({self.column}) FROM {self.table}"
        mysql_connexion_config.cursor.execute(query)
        self.result = mysql_connexion_config.cursor.fetchone()
        self.id = self.result[0] + 1 if self.result and self.result[0] is not None else self.id

        # Mettre à jour le label
        facture_label.configure(text=f"{self.label_prefix}{self.id}")

    def info_client(self):
        # Raison social
        raison_social_label = CTkLabel(master=self.frame1, text="* Raison social: ", font=self.my_font, fg_color="transparent", anchor="w")
        raison_social_label.grid(column=0, row=1, padx=self.paddings, pady=self.paddings, sticky="w")

        raison_social_input = CTkEntry(master=self.frame1, textvariable=StringVar())
        raison_social_input.grid(column=1, row=1, padx=self.paddings, pady=self.paddings)

        # Statistique
        statistique_label = CTkLabel(master=self.frame1, text="Statistique: ", font=self.my_font, fg_color="transparent", anchor="w")
        statistique_label.grid(column=0, row=2, padx=self.paddings, pady=self.paddings, sticky="w")

        statistique_input = CTkEntry(master=self.frame1, textvariable=StringVar())
        statistique_input.grid(column=1, row=2, padx=self.paddings, pady=self.paddings)

        # NIF
        nif_label = CTkLabel(master=self.frame1, text="NIF: ", font=self.my_font, fg_color="transparent", anchor="w")
        nif_label.grid(column=0, row=3, padx=self.paddings, pady=self.paddings, sticky="w")

        nif_input = CTkEntry(master=self.frame1, textvariable=StringVar())
        nif_input.grid(column=1, row=3, padx=self.paddings, pady=self.paddings)

        # Adresse
        adresse_label = CTkLabel(master=self.frame1, text="Adresse: ", font=self.my_font, fg_color="transparent", anchor="w")
        adresse_label.grid(column=0, row=4, padx=self.paddings, pady=self.paddings, sticky="w")

        adresse_input = CTkEntry(master=self.frame1, textvariable=StringVar())
        adresse_input.grid(column=1, row=4, padx=self.paddings, pady=self.paddings)
        
        # date d'émission
        date_emission_label = CTkLabel(master=self.frame1, text="* Date d'émission: ", font=self.my_font, fg_color="transparent", anchor="w")
        date_emission_label.grid(column=2, row=1, padx=self.paddings, pady=self.paddings, sticky="w")

        date_emission_input = DateEntry(master=self.frame1, selectmode='day', date_pattern='yyyy-mm-dd', bd=adresse_input.cget("border_width"), width=15)
        date_emission_input.grid(column=3, row=1, padx=self.paddings, pady=self.paddings)

        # Date du résultat
        date_du_resultat_label = CTkLabel(master=self.frame1, text="* Date du résultat: ", font=self.my_font, fg_color="transparent", anchor="w")
        date_du_resultat_label.grid(column=2, row=2, padx=self.paddings, pady=self.paddings, sticky="w")

        date_du_resultat_input = DateEntry(master=self.frame1, selectmode='day', date_pattern='yyyy-mm-dd', width=15)
        date_du_resultat_input.grid(column=3, row=2, padx=self.paddings, pady=self.paddings)

        # Référence des produits (en int)
        reference_des_produits_label = CTkLabel(master=self.frame1, text="Référence des produits: ", font=self.my_font, fg_color="transparent", anchor="w")
        reference_des_produits_label.grid(column=2, row=3, padx=self.paddings, pady=self.paddings, sticky="w")

        reference_des_produits_input = CTkEntry(master=self.frame1, textvariable=StringVar())
        reference_des_produits_input.grid(column=3, row=3, padx=self.paddings, pady=self.paddings)

        # Résponsable
        responsable_label = CTkLabel(master=self.frame1, text="* Responsable: ", font=self.my_font, fg_color="transparent", anchor="w")
        responsable_label.grid(column=2, row=4, padx=self.paddings, pady=self.paddings, sticky="w")

        responsable_input = CTkEntry(master=self.frame1, textvariable=StringVar())
        responsable_input.grid(column=3, row=4, padx=self.paddings, pady=self.paddings)
