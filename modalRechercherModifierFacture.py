from tkinter import Toplevel
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import IntVar, StringVar
import mysql_connexion_config
from tkcalendar import DateEntry

class ModalRechercherModifierFacture(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Recherche facture")
        
        self.paddings = 10
        
        
        # Interface graphique
        Label(self, text="Numéro facture:").grid(row=0, column=0, padx=10, pady=10)
        
        def valider_entree(chiffre):
            return chiffre.isdigit() or chiffre == ""

        vcmd = (self.register(valider_entree), '%P')
        
        
        self.numero_facture = Entry(self, width=5, validate='key', validatecommand=vcmd)
        self.numero_facture.grid(row=0, column=1, padx=10, pady=10)
        
        def faire_grab_si_visible():
            if self.winfo_viewable():
                self.grab_set()
            else:
                self.after(10, faire_grab_si_visible)
        self.after(10, faire_grab_si_visible)
        
        
        def on_numero_facture_return(event):
            
            mysql_connexion_config.cursor.execute("SELECT id_client FROM info_client")
            
            num_facture = []
            
            id_client = mysql_connexion_config.cursor.fetchall()
            for num in id_client:
                num_facture.append(num[0])
            
            num_fact = int(self.numero_facture.get())

            
            if num_fact in num_facture:
                
                self.num_fact = num_fact
                # Récupérer les valeurs de chaque champs dans la base de donnée
                
                mysql_connexion_config.cursor.execute("SELECT raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable FROM info_client WHERE id_client = %s", (num_fact,))
                
                info_client = mysql_connexion_config.cursor.fetchone()
                
                raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable = info_client
                
                Label(self, text="Raison social: ").grid(row=1, column=0, padx=self.paddings, pady=self.paddings)
                self.raison_social = Entry(self, textvariable=StringVar(value=raison_sociale))
                self.raison_social.grid(row=1, column=1, padx=self.paddings, pady=self.paddings)
                
                
                
                Label(self, text="statistique: ").grid(row=2, column=0, padx=self.paddings, pady=self.paddings)
                self.statistique = Entry(self, textvariable=StringVar(value=statistique))
                self.statistique.grid(row=2, column=1, padx=self.paddings, pady=self.paddings)
                
                Label(self, text="NIF: ").grid(row=3, column=0, padx=self.paddings, pady=self.paddings)
                self.NIF = Entry(self, textvariable=StringVar(value=nif))
                self.NIF.grid(row=3, column=1, padx=self.paddings, pady=self.paddings)
                
                Label(self, text="Adresse: ").grid(row=4, column=0, padx=self.paddings, pady=self.paddings)
                self.adresse = Entry(self, textvariable=StringVar(value=adresse))
                self.adresse.grid(row=4, column=1, padx=self.paddings, pady=self.paddings)
                
                
                Label(self, text="Date d'émission: ").grid(row=1, column=2, padx=self.paddings, pady=self.paddings)
                self.date_e = DateEntry(master=self, selectmode='day', date_pattern='yyyy-mm-dd', width=15)
                self.date_e.grid(row=1, column=3, padx=self.paddings, pady=self.paddings)
                self.date_e.set_date(date_emission)
                
                
                Label(self, text="Date du résultat: ").grid(row=2, column=2, padx=self.paddings, pady=self.paddings)
                self.date_du_resultat = DateEntry(master=self, selectmode='day', date_pattern='yyyy-mm-dd', width=15)
                self.date_du_resultat.grid(row=2, column=3, padx=self.paddings, pady=self.paddings)
                self.date_du_resultat.set_date(date_resultat)
                
                
                Label(self, text="Référence des produits: ").grid(row=3, column=2, padx=self.paddings, pady=self.paddings)
                self.reference_produits = Entry(self, textvariable=StringVar(value=reference_des_produits))
                self.reference_produits.grid(row=3, column=3, padx=self.paddings, pady=self.paddings)
                
                
                Label(self, text="Responsable: ").grid(row=4, column=2, padx=self.paddings, pady=self.paddings)
                self.Responsable = Entry(self, textvariable=StringVar(value=responsable))
                self.Responsable.grid(row=4, column=3, padx=self.paddings, pady=self.paddings)
                
                # Focus sur le champ raison social
                self.raison_social.focus_set()
                
                
                Button(self, text="Modifier et imprimer", command=self.modifier).grid(row=5, columnspan=4, pady=self.paddings)
            
            else:
                Label(self, text="Aucun facture correspondant!").grid(row=1, columnspan=4, padx=self.paddings, pady=self.paddings)
            
        self.numero_facture.bind("<Return>", on_numero_facture_return)
        
    def modifier(self):
        mysql_connexion_config.cursor.execute("UPDATE info_client SET raison_sociale = %s, statistique = %s, nif= %s, adresse= %s, date_emission= %s, date_resultat=%s, responsable= %s WHERE id_client = %s", (self.raison_social.get(), self.statistique.get(), self.NIF.get(),self.adresse.get(),self.date_e.get(), self.date_du_resultat.get(), self.Responsable.get(), self.num_fact))
        
        mysql_connexion_config.connexion.commit()
        
        self.destroy()