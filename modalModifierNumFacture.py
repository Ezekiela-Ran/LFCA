from tkinter import Toplevel
from tkinter import Button
from tkinter import Label
from tkinter import Entry
import mysql_connexion_config
import data


class ModalModifierNumFacture(Toplevel):
    def __init__(self, parent, zone_modif_num):
        super().__init__(parent)
        self.title("Modifier numéro facture")
        self.zone_modif_num = zone_modif_num
        
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
        if valeur.isdigit() and int(valeur) > 0:
            data.id = int(valeur)
            mysql_connexion_config.cursor.execute("ALTER TABLE info_client AUTO_INCREMENT = %s", (int(valeur),))
            data.id = int(valeur)
            self.zone_modif_num()
        else:
            Label(self, text="Valeur invalide!", fg="red").grid(row=2, columnspan=2, padx=10, pady=10)
        
        self.destroy()