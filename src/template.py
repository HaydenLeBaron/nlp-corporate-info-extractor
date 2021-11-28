'''
Author: Hayden LeBaron
GitHub: HaydenTheBaron
Date: Nov 7, 2021
'''

class Template:
    """Represents an output IE template to be written to a file."""

    def __init__(self, *, text:str,
                 acquired:list[str]=None,
                 acqbus:list[str]=None,
                 acqloc:list[str]=None,
                 dlramt:list[str]=None,
                 purchaser:list[str]=None,
                 seller:list[str]=None,
                 status:list[str]=None):
        """
        (NAMED) ARGUMENTS:
        ===================
        REQUIRED:
        ----------
        text -- The unique filename identifier

        OPTIONAL:
        ----------
        acquired -- Entities that were acquired
        acqbus --  The business focus of the acquired entities
        acqloc --  The location of the acquired entities
        dlramt --  The amount paid for the acquired entities
        purchaser -- The entities that purchased the acquired entities
        seller -- Entities that sold the acquired entities
        status -- Status description of the acquisition event
        """
        self.text = text
        self.acquired = acquired
        self.acqbus = acqbus
        self.acqloc = acqloc
        self.dlramt = dlramt
        self.purchaser = purchaser
        self.seller = seller
        self.status = status

    def __str__(self):
        """Returns str of the template in the form expected by .templates output files."""

        # TEXT
        out = 'TEXT: %s\n' % self.text
        # AQCUIRED
        if self.acquired is None or len(self.acquired) == 0:
            out += 'ACQUIRED: ---\n'
        else:
            for elt in self.acquired:
                out += 'ACQUIRED: \"%s\"\n' % elt
        # ACQBUS
        if self.acqbus is None or len(self.acqbus) == 0:
            out += 'ACQBUS: ---\n'
        else:
            for elt in self.acqbus:
                out += 'ACQBUS: \"%s\"\n' % elt
        # ACQLOC
        if self.acqloc is None or len(self.acqloc) == 0:
            out += 'ACQLOC: ---\n'
        else:
            for elt in self.acqloc:
                out += 'ACQLOC: \"%s\"\n' % elt
        # DLRAMT
        if self.dlramt is None or len(self.dlramt) == 0:
            out += 'DLRAMT: ---\n'
        else:
            for elt in self.dlramt:
                out += 'DLRAMT: \"%s\"\n' % elt
        # PURCHASER
        if self.purchaser is None or len(self.purchaser) == 0:
            out += 'PURCHASER: ---\n'
        else:
            for elt in self.purchaser:
                out += 'PURCHASER: \"%s\"\n' % elt
        # SELLER
        if self.seller is None or len(self.seller) == 0:
            out += 'SELLER: ---\n'
        else:
            for elt in self.seller:
                out += 'SELLER: \"%s\"\n' % elt
        # STATUS
        if self.status is None or len(self.status) == 0:
            out += 'STATUS: ---\n'
        else:
            for elt in self.status:
                out += 'STATUS: \"%s\"\n' % elt

        return out
