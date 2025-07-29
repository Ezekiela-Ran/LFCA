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
    id_categorie INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie VARCHAR(100) NOT NULL UNIQUE
)""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits (
    id_produit INT AUTO_INCREMENT PRIMARY KEY,
    categorie_id INT NOT NULL,
    FOREIGN KEY (categorie_id) REFERENCES categories(id_categorie) ON DELETE CASCADE,
    nom_produit VARCHAR(100) NOT NULL UNIQUE
)""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produit_details (
    id_produit_detail INT AUTO_INCREMENT PRIMARY KEY,
    produit_id INT NOT NULL,
    physico INT,
    micro INT,
    toxico INT,
    sous_total INT,
    FOREIGN KEY (produit_id) REFERENCES produits(id_produit) ON DELETE CASCADE
)""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS info_client (
    id_client INT AUTO_INCREMENT PRIMARY KEY,
    raison_sociale VARCHAR(100) NOT NULL,
    statistique VARCHAR(100),
    nif VARCHAR(100),
    adresse VARCHAR(255),
    date_emission DATE NOT NULL,
    date_resultat DATE NOT NULL,
    reference_des_produits VARCHAR(255) NOT NULL,
    responsable VARCHAR(100) NOT NULL
)""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produit_analyse (
    id_produit_analyse INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    produit_id INT NOT NULL,
    ref_bull_analyse VARCHAR(50) NOT NULL,
    num_acte VARCHAR(50) NOT NULL,
    physico INT,
    micro INT,
    toxico INT,
    sous_total INT,
    FOREIGN KEY (client_id) REFERENCES info_client(id_client) ON DELETE CASCADE,
    FOREIGN KEY (produit_id) REFERENCES produits(id_produit) ON DELETE CASCADE
)""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS total (
    id_total INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    total INT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES info_client(id_client) ON DELETE CASCADE
)""")
