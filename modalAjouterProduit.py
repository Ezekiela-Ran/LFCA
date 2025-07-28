from tkinter import Toplevel
from tkinter import Button
from tkinter import Label
from tkinter import Entry
import mysql_connexion_config

class ModalAjouterProduit(Toplevel):
    def __init__(self, parent, categorie=None, callback=None):
        super().__init__(parent)
        self.title("Ajouter produit")
        self.categorie = categorie
        self.callback = callback
        
        # Interface graphique
        Label(self, text="Nom du produit:").grid(row=0, column=0, padx=10, pady=10)
        
        self.nom_du_produit = Entry(self)
        self.nom_du_produit.grid(row=0, column=1, padx=10, pady=10)

        Button(self, text="Ajouter", command=self.ajouter).grid(row=1, columnspan=2, pady=10)

        def faire_grab_si_visible():
            if self.winfo_viewable():
                self.grab_set()
            else:
                self.after(10, faire_grab_si_visible)
        self.after(10, faire_grab_si_visible)


    def ajouter(self):
        nouveau_produit = self.nom_du_produit.get()
        
        mysql_connexion_config.cursor.execute(
            "SELECT nom_produit FROM produits WHERE nom_produit = %s",
            (nouveau_produit,)
        )
        result = mysql_connexion_config.cursor.fetchone()
 
        if not result:
            
            mysql_connexion_config.cursor.execute(
                "INSERT INTO produits (categorie_id, nom_produit) VALUES ((SELECT id_categorie FROM categories WHERE nom_categorie = %s), %s)",
                (self.categorie, nouveau_produit)
            )
            
            mysql_connexion_config.cursor.execute(
                 "INSERT INTO produit_details (produit_id, num_acte, physico, micro, toxico, sous_total) VALUES ((SELECT id_produit FROM produits WHERE nom_produit = %s), '', 0, 0, 0, 0)", (nouveau_produit,)
            )
            mysql_connexion_config.connexion.commit()
            
            self.callback()
            self.destroy()
            
        else:
            Label(self, text=f"Le produit {nouveau_produit} existe déjà", fg="red").grid(row=2, column=0, padx=10, pady=10)