DROP DATABASE Test;
CREATE DATABASE IF NOT EXISTS Test;
USE Test;



SELECT p.nom_produit, pa.ref_bull_analyse, pa.num_acte, pa.physico, pa.micro, pa.toxico, pa.sous_total FROM produit_analyse pa JOIN produits p ON pa.client_id = 1 AND p.id_produit = pa.produit_id;

SELECT total FROM total WHERE client_id = 1;

SELECT id_client FROM info_client;

SELECT raison_sociale FROM info_client WHERE id_client = 1;

UPDATE info_client SET raison_sociale = "Socobis" WHERE id_client = 1;

SELECT p.nom_produit, pa.ref_bull_analyse, pa.num_acte, pa.physico, pa.micro, pa.toxico, pa.sous_total FROM produit_analyse pa JOIN produits p ON pa.client_id = 1 AND p.id_produit = pa.produit_id AND p.nom_produit = "Coca cola";

DELETE pa
FROM produit_analyse pa
JOIN produits p ON pa.produit_id = p.id_produit
WHERE pa.client_id = 1 AND p.nom_produit = "Coca cola";


UPDATE produit_analyse pa
JOIN produits p ON pa.produit_id = p.id_produit
SET 
  pa.ref_bull_analyse = '',
  pa.num_acte = '',
  pa.physico = '',
  pa.micro = '',
  pa.toxico = '',
  pa.sous_total = ''
WHERE p.nom_produit = '';


SELECT pa.sous_total FROM produit_analyse pa JOIN produits p WHERE p.nom_produit = "Fanta" AND pa.client_id = 1;

SELECT t.total FROM total t JOIN info_client ic WHERE t.client_id = 1;