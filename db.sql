DROP DATABASE Test;
CREATE DATABASE IF NOT EXISTS Test;
USE Test;



SELECT p.nom_produit, pa.ref_bull_analyse, pa.num_acte, pa.physico, pa.micro, pa.toxico, pa.sous_total FROM produit_analyse pa JOIN produits p ON pa.client_id = 1 AND p.id_produit = pa.produit_id;

SELECT total FROM total WHERE client_id = 1;