from tkinter import Toplevel
from tkinter import IntVar, StringVar
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel
import mysql_connexion_config
from tkcalendar import DateEntry
from CTkMessagebox import CTkMessagebox

class ModalRechercherModifierFacture(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Recherche facture")
        
        self.paddings = 10
        self.configure(bg="gray17")
        
        # Interface graphique
        first_frame = CTkFrame(self)
        first_frame.pack(fill="x", padx=self.paddings, pady=self.paddings)
        CTkLabel(first_frame, text="Numéro facture:").grid(row=0, column=0, padx=10, pady=10)
        
        def valider_entree(chiffre):
            return chiffre.isdigit() or chiffre == ""

        vcmd = (self.register(valider_entree), '%P')
        
        
        self.numero_facture = CTkEntry(first_frame, width=50, validate='key', validatecommand=vcmd)
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

            # for widget in second_frame.winfo_children():
            #     widget.destroy()

            second_frame = CTkFrame(self)
            second_frame.pack(fill="x", padx=self.paddings, pady=self.paddings)

            
            
            
            if num_fact in num_facture:
                
                self.num_fact = num_fact
                # Récupérer les valeurs de chaque champs dans la base de donnée
                # Récuperation des info_client:
                mysql_connexion_config.cursor.execute("SELECT raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable FROM info_client WHERE id_client = %s", (num_fact,))
                
                info_client = mysql_connexion_config.cursor.fetchone()
                
                raison_sociale, statistique, nif, adresse, date_emission, date_resultat, reference_des_produits, responsable = info_client
                
                
                
                CTkLabel(second_frame, text="Raison social: ").grid(row=1, column=0, padx=self.paddings, pady=self.paddings)
                self.raison_social = CTkEntry(second_frame, textvariable=StringVar(value=raison_sociale))
                self.raison_social.grid(row=1, column=1, padx=self.paddings, pady=self.paddings)
                
                
                
                CTkLabel(second_frame, text="statistique: ").grid(row=2, column=0, padx=self.paddings, pady=self.paddings)
                self.statistique = CTkEntry(second_frame, textvariable=StringVar(value=statistique))
                self.statistique.grid(row=2, column=1, padx=self.paddings, pady=self.paddings)
                
                CTkLabel(second_frame, text="NIF: ").grid(row=3, column=0, padx=self.paddings, pady=self.paddings)
                self.NIF = CTkEntry(second_frame, textvariable=StringVar(value=nif))
                self.NIF.grid(row=3, column=1, padx=self.paddings, pady=self.paddings)
                
                CTkLabel(second_frame, text="Adresse: ").grid(row=4, column=0, padx=self.paddings, pady=self.paddings)
                self.adresse = CTkEntry(second_frame, textvariable=StringVar(value=adresse))
                self.adresse.grid(row=4, column=1, padx=self.paddings, pady=self.paddings)
                
                
                CTkLabel(second_frame, text="Date d'émission: ").grid(row=1, column=2, padx=self.paddings, pady=self.paddings)
                self.date_e = DateEntry(master=second_frame, selectmode='day', date_pattern='yyyy-mm-dd', width=15)
                self.date_e.grid(row=1, column=3, padx=self.paddings, pady=self.paddings)
                self.date_e.set_date(date_emission)
                
                
                CTkLabel(second_frame, text="Date du résultat: ").grid(row=2, column=2, padx=self.paddings, pady=self.paddings)
                self.date_du_resultat = DateEntry(master=second_frame, selectmode='day', date_pattern='yyyy-mm-dd', width=15)
                self.date_du_resultat.grid(row=2, column=3, padx=self.paddings, pady=self.paddings)
                self.date_du_resultat.set_date(date_resultat)
                
                
                CTkLabel(second_frame, text="Référence des produits: ").grid(row=3, column=2, padx=self.paddings, pady=self.paddings)
                self.reference_produits = CTkEntry(second_frame, textvariable=StringVar(value=reference_des_produits))
                self.reference_produits.grid(row=3, column=3, padx=self.paddings, pady=self.paddings)
                
                
                CTkLabel(second_frame, text="Responsable: ").grid(row=4, column=2, padx=self.paddings, pady=self.paddings)
                self.Responsable = CTkEntry(second_frame, textvariable=StringVar(value=responsable))
                self.Responsable.grid(row=4, column=3, padx=self.paddings, pady=self.paddings)
                
                nom_produit = StringVar()
                
                
                third_frame = CTkFrame(self)
                third_frame.pack(fill="x", padx=self.paddings, pady=self.paddings)
                
                
                CTkLabel(third_frame, text="Saisisser le nom produit: ").grid(row=5, column=0, padx=self.paddings, pady=self.paddings)
                self.nom_produit_saisie = CTkEntry(third_frame, textvariable=nom_produit)
                self.nom_produit_saisie.grid(row=5, column=1, padx=self.paddings, pady=self.paddings)
                
                def on_nom_produit_saisie_return(event):
                
                    def modifier():
                        # Récuperation d'un produit analysé
                        mysql_connexion_config.cursor.execute("SELECT p.nom_produit, pa.ref_bull_analyse, pa.num_acte, pa.physico, pa.micro, pa.toxico, pa.sous_total FROM produit_analyse pa JOIN produits p ON pa.client_id = %s AND p.id_produit = pa.produit_id AND p.nom_produit = %s", (num_fact, nom_produit.get()))
                        
                        
                        self.produit_analyse = mysql_connexion_config.cursor.fetchone()
                        
                        print(self.produit_analyse)
                        
                        if self.produit_analyse:
                            
                            produit, ref_bull_analyse, num_acte, physico, micro, toxico, sous_total = self.produit_analyse
                        
                            label_width = 100
                            
                            ref_analyse_label = CTkLabel(third_frame, text="Réf. Bulletin analyse")
                            ref_analyse_label.grid(row=7, column=0)
                            
                            num_acte_label = CTkLabel(third_frame, text="Numéro d'acte")
                            num_acte_label.grid(row=7, column=1)
                            
                            physico_label = CTkLabel(third_frame, text="Physico")
                            physico_label.grid(row=7, column=2)
                            
                            micro_label = CTkLabel(third_frame, text="Micro")
                            micro_label.grid(row=7, column=3)
                            
                            toxico_label = CTkLabel(third_frame, text="Toxico")
                            toxico_label.grid(row=7, column=4)
                            
                            sous_total_label = CTkLabel(third_frame, text="Sous total")
                            sous_total_label.grid(row=7, column=5)
                    
                            
                            self.ref_analyse = CTkEntry(third_frame, textvariable=StringVar(value=ref_bull_analyse), width=label_width)
                            self.ref_analyse.grid(row=8, column=0)
                            
                            self.num_acte = CTkEntry(third_frame, textvariable=StringVar(value=num_acte), width=label_width)
                            self.num_acte.grid(row=8, column=1)
                            
                            self.physico = CTkEntry(third_frame, textvariable=StringVar(value=physico), width=label_width)
                            self.physico.grid(row=8, column=2)
                            
                            self.micro = CTkEntry(third_frame, textvariable=StringVar(value=micro), width=label_width)
                            self.micro.grid(row=8, column=3)
                            
                            self.toxico = CTkEntry(third_frame, textvariable=StringVar(value=toxico), width=label_width)
                            self.toxico.grid(row=8, column=4)
                            
                            self.sous_total = CTkEntry(third_frame, textvariable=StringVar(value=sous_total), width=label_width)
                            self.sous_total.grid(row=8, column=5)
                            
                        else:
                            CTkLabel(third_frame, text="Produit n'appartient pas à ce client! ").grid(row=7, columnspan=6)
                            
                    bouton_modifier = CTkButton(third_frame, text="Modifier", command=modifier)
                    bouton_modifier.grid(row=6, column=0, padx=self.paddings, pady=self.paddings)
                    
                    def supprimer():
                        
                        # obtenir le sous total du produit à supprimer
                        mysql_connexion_config.cursor.execute("SELECT pa.sous_total FROM produit_analyse pa JOIN produits p WHERE p.nom_produit = %s AND pa.client_id = %s", (self.nom_produit_saisie.get(), num_fact))
                        sous_total = mysql_connexion_config.cursor.fetchone()
                        
                        # obtenir le total à soustraire
                        mysql_connexion_config.cursor.execute("SELECT t.total FROM total t JOIN info_client ic WHERE t.client_id = %s", (num_fact,))
                        total = mysql_connexion_config.cursor.fetchone()
                        
                        update_total = int(total[0]) - int(sous_total[0])
                        
                        # correspondre la somme total 
                        mysql_connexion_config.cursor.execute("UPDATE total SET total=%s WHERE client_id=%s", (update_total, num_fact))
                        
                        mysql_connexion_config.cursor.execute("DELETE pa FROM produit_analyse pa JOIN produits p ON pa.produit_id = p.id_produit WHERE pa.client_id = %s AND p.nom_produit = %s", (num_fact, self.nom_produit_saisie.get()))
                        
                        
                        
                        mysql_connexion_config.connexion.commit()
                        CTkMessagebox(message=f"{self.nom_produit_saisie.get()} supprimé!", icon="check", option_1="Fermer")
                    
                    bouton_supprimer = CTkButton(third_frame, text="Supprimer", command=supprimer)
                    bouton_supprimer.grid(row=6, column=1, padx=self.paddings, pady=self.paddings)
                    
                    def ajouter():
                        pass
                    
                    bouton_ajouter = CTkButton(third_frame, text="Ajouter", command=ajouter)
                    bouton_ajouter.grid(row=6, column=2, padx=self.paddings, pady=self.paddings)
                    
                        
                self.nom_produit_saisie.bind("<Return>", on_nom_produit_saisie_return)
                    
                
                # Focus sur le champ raison social
                self.raison_social.focus_set()
                
                
                CTkButton(self, text="Modifier et imprimer", command=self.modifier).pack()
            
            else:
                # CTkLabel(self, text="Aucun facture correspondant!").pack()
                CTkMessagebox(message="Aucun facture correspondant!",
            icon="check", option_1="Fermer")
            
        self.numero_facture.bind("<Return>", on_numero_facture_return)
        
    def modifier(self):
        mysql_connexion_config.cursor.execute("UPDATE info_client SET raison_sociale = %s, statistique = %s, nif= %s, adresse= %s, date_emission= %s, date_resultat=%s, responsable= %s WHERE id_client = %s", (self.raison_social.get(), self.statistique.get(), self.NIF.get(),self.adresse.get(),self.date_e.get(), self.date_du_resultat.get(), self.Responsable.get(), self.num_fact))
        
        mysql_connexion_config.connexion.commit()
        
        if self.produit_analyse != None:
            mysql_connexion_config.cursor.execute("UPDATE produit_analyse pa JOIN produits p ON pa.produit_id = p.id_produit SET pa.ref_bull_analyse = %s, pa.num_acte = %s, pa.physico = %s, pa.micro = %s, pa.toxico = %s, pa.sous_total = %s WHERE p.nom_produit = %s", (self.ref_analyse.get(), self.num_acte.get(), self.physico.get(), self.micro.get(), self.toxico.get(), self.sous_total.get(), self.nom_produit_saisie.get()))
            mysql_connexion_config.connexion.commit()
        
        self.destroy()