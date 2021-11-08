import sys
import pandas as pd

# TODO: needs to take an input file X and write to output file X.templates

OUTPUT_DIR_PATH = '../output/'


"""
Represents an output IE template to be written to a file.
"""
class Template:

    """
    (NAMED) ARGUMENTS:
    ===================

    REQUIRED:
    text -- (STRING) The unique filename identifier

    LIST(STRING) | NONE :
    acquired -- Entities that were acquired
    acqbus --  The business focus of the acquired entities
    acqloc --  The location of the acquired entities
    dlramt --  The amount paid for the acquired entities
    purchaser -- The entities that purchased the acquired entities
    seller -- Entities that sold the acquired entities
    status -- Status description of the acquisition event
    """
    def __init__(self, *, text, acquired=None, acqbus=None, acqloc=None, dlramt=None, purchaser=None, seller=None, status=None):
        self.text = text
        self.acquired = acquired
        self.acqbus = acqbus
        self.acqloc = acqloc
        self.dlramt = dlramt
        self.purchaser = purchaser
        self.seller = seller
        self.status = status

    """
    Prints a string representation of the template in the same form as expected of the .templates output files.
    """
    def __str__(self):
        # TEXT
        out = 'TEXT: %s\n' % self.text
        # AQCUIRED
        if self.acquired is None:
            out += 'ACQUIRED: ---\n'
        else:
            for elt in self.acquired:
                out += 'ACQUIRED: %s\n' % elt
        # ACQBUS
        if self.acqbus is None:
            out += 'ACQBUS: ---\n'
        else:
            for elt in self.acqbus:
                out += 'ACQBUS: %s\n' % elt
        # ACQLOC
        if self.acqloc is None:
            out += 'ACQLOC: ---\n'
        else:
            for elt in self.acqloc:
                out += 'ACQLOC: %s\n' % elt
        # DLRAMT
        if self.dlramt is None:
            out += 'DLRAMT: ---\n'
        else:
            for elt in self.dlramt:
                out += 'DLRAMT: %s\n' % elt
        # PURCHASER
        if self.purchaser is None:
            out += 'PURCHASER: ---\n'
        else:
            for elt in self.purchaser:
                out += 'PURCHASER: %s\n' % elt
        # SELLER
        if self.seller is None:
            out += 'SELLER: ---\n'
        else:
            for elt in self.seller:
                out += 'SELLER: %s\n' % elt
        # STATUS
        if self.status is None:
            out += 'STATUS: ---\n'
        else:
            for elt in self.status:
                out += 'STATUS: %s\n' % elt

        return out


def main():
    '''Print help message'''
    if sys.argv[1] == '-h' \
       or sys.argv[1] == '--help' \
       or len(sys.argv) > 2:
        print("Run: `python3 extract.py <docList>`")
        return

    '''Extract docs into pandas series'''
    doclist_file_path = sys.argv[1]
    doc_series = pd.read_table(doclist_file_path, header=None).transpose().iloc[0]




    '''Write to output file'''
    output_file_path = OUTPUT_DIR_PATH + doclist_file_path.split('/')[-1] + '.templates'
    dummy_template_1 = Template(text='ShouldbeAllEmpty')
    dummy_template_2 = Template(text='123',
                                acquired=['Acquired 1', 'Acquired 2'],
                                acqbus=['Acqbus1', 'Acqbus2'],
                                acqloc=['Acqloc'],
                                dlramt=['$1'],
                                purchaser=['Purchaser'],
                                seller=['Seller'],
                                status=['Current Status'])
    with open(output_file_path, "w") as outf:
        outf.write('%s' % dummy_template_1)
        outf.write('\n')
        outf.write('%s' % dummy_template_2)
        outf.write('\n')

if __name__ == '__main__':
    main()
