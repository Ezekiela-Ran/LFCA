from tkinter import Toplevel
from tkinter import Button
from tkinter import Label
from tkinter import Entry
import mysql_connexion_config
import data
from typeFacture.facture_proforma import FactureProforma
from typeFacture.facture_simple import FactureSimple

class ModalModifierNumFacture(Toplevel):
    def __init__(self, parent, frame1, paddings, my_font, facture_label):
        super().__init__(parent)
        self.title("Modifier numéro facture")
        self.frame1 = frame1
        self.paddings = paddings
        self.my_font = my_font
        self.facture_label = facture_label
    
        # Interface graphique
        Label(self, text="Numéro facture:").grid(row=0, column=0, padx=10, pady=10)
        
        def valider_entree(chiffre):
            return chiffre.isdigit() or chiffre == ""

        vcmd = (self.register(valider_entree), '%P')
        
        self.num_fact = Entry(self, validate="key", validatecommand=vcmd)
        self.num_fact.grid(row=0, column=1, padx=10, pady=10)

        Button(self, text="modifier", command=self.modifier).grid(row=1, columnspan=2, pady=10)

        def faire_grab_si_visible():
            if self.winfo_viewable():
                self.grab_set()
            else:
                self.after(10, faire_grab_si_visible)
        self.after(10, faire_grab_si_visible)
        
    def modifier(self):
        valeur = self.num_fact.get()
        if valeur.isdigit() and int(valeur) > 0 and not data.facture_proforma:
            # modifier l'id de la table info_client
            mysql_connexion_config.cursor.execute("ALTER TABLE info_client AUTO_INCREMENT = %s", (int(valeur),))
            
            # changer la valeur de data.id
            data.id = int(valeur)
            
            # actualiser la zone d'affichage
            factureSimple = FactureSimple(self.frame1, self.paddings, self.my_font)
            factureSimple.num_fact(self.facture_label)
            self.destroy()

        elif valeur.isdigit() and int(valeur) <= 0:
            Label(self, text="Valeur invalide!", fg="red").grid(row=2, columnspan=2, padx=10, pady=10)

        elif data.facture_proforma:
            Label(self, text="Le numéro de facture proforma ne peut pas être modifié", fg="red").grid(row=2, columnspan=2, padx=10, pady=10)

        else:
            Label(self, text="Entrée invalide!", fg="red").grid(row=2, columnspan=2, padx=10, pady=10)

        
        