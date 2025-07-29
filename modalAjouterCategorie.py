from tkinter import Toplevel
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import StringVar
import data
import mysql_connexion_config




class ModalAjouterCategorie(Toplevel):
   
    def __init__(self, master=None, frame=None, callback=None):
        super().__init__(master)
        self.title("Ajouter une catégorie")
        self.frame = frame
        self.callback = callback

         # Interface graphique
        Label(self, text="Catégorie du produit:").grid(row=0, column=0, padx=10, pady=10)
        
        self.nom_du_produit = Entry(self)
        self.nom_du_produit.grid(row=0, column=1, padx=10, pady=10)
        
        Button(master=self, text="Ajouter", command=self.ajouter_categorie).grid(row=1, columnspan=2, pady=10)

        def faire_grab_si_visible():
            if self.winfo_viewable():
                self.grab_set()
            else:
                self.after(10, faire_grab_si_visible)
        self.after(10, faire_grab_si_visible)



    def ajouter_categorie(self):
        nouvelle_categorie = self.nom_du_produit.get()
        if nouvelle_categorie and nouvelle_categorie not in data.produit_par_categorie.keys():
            data.produit_par_categorie[nouvelle_categorie] = {}
            
            mysql_connexion_config.cursor.execute("INSERT INTO categories (nom_categorie) VALUES (%s)", (nouvelle_categorie,))
            mysql_connexion_config.connexion.commit()
            
            for widget in self.frame.winfo_children():
                widget.destroy()
                
            # réafficher les boutons pour les catégories
            self.callback()
            self.destroy()
            
        else:
            Label(self, text=f"La catégorie {nouvelle_categorie} existe déjà", fg="red").grid(row=2, columnspan=2, padx=10, pady=10)
            
