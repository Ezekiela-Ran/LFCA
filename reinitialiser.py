import mysql_connexion_config
from CTkMessagebox import CTkMessagebox
import time
import mysql

class Reinitialiser:
    def __init__(self):
        pass
    
    def reinitialiser(self):
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
