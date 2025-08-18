import data
from facture import Facture


class FactureSimple(Facture):
    def __init__(self, frame1, paddings, my_font):
        data.facture_proforma = False
        super().__init__(frame1, paddings, my_font)
    