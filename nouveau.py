from customtkinter import  CTkToplevel, CTkLabel

import sys
import subprocess

class Nouveau:
    def __init__(self, parent):
        
        self.root = parent
    
    def relance_fantôme(self):
        # Fenêtre fantôme
        fantôme = CTkToplevel()
        fantôme.geometry("400x200+500+300")
        fantôme.overrideredirect(True)  # Supprime la barre de titre
        fantôme.configure(fg_color=['gray86', 'gray17'])
        
        # Texte ou animation de transition
        label = CTkLabel(fantôme, text="Patientez...", font=("Arial", 20))
        label.pack(expand=True)

        self.root.withdraw()  # Masque l'appli actuelle
        fantôme.update()

        # Relance après un court délai
        fantôme.after(300, lambda: subprocess.Popen([sys.executable, *sys.argv]))
        fantôme.after(600, lambda: (fantôme.destroy(), self.root.quit()))
    