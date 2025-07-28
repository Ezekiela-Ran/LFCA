import mysql.connector

connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Test"
)

# Création de la base de données et de la table
cursor = connexion.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Test")
cursor.execute("USE Test")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie VARCHAR(100) NOT NULL UNIQUE
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categorie_id INT NOT NULL,
    FOREIGN KEY (categorie_id) REFERENCES categories(id) ON DELETE CASCADE,
    nom_produit VARCHAR(100) NOT NULL UNIQUE
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produit_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produit_id INT NOT NULL,
    num_acte VARCHAR(100),
    physico INT,
    micro INT,
    toxico INT,
    sous_total INT,
    FOREIGN KEY (produit_id) REFERENCES produits(id) ON DELETE CASCADE
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS info_client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    raison_sociale VARCHAR(100) NOT NULL UNIQUE,
    statistique VARCHAR(100) UNIQUE,
    nif VARCHAR(100) UNIQUE,
    adresse VARCHAR(255) UNIQUE,
    date_emission DATE NOT NULL,
    date_resultat DATE NOT NULL,
    reference_des_produits VARCHAR(255) NOT NULL,
    responsable VARCHAR(100) NOT NULL)
""")

