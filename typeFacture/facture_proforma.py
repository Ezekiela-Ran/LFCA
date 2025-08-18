import data
from facture import Facture

class FactureProforma(Facture):
    def __init__(self, frame1, paddings, my_font):
        data.facture_proforma = True
        super().__init__(frame1, paddings, my_font)
    
    