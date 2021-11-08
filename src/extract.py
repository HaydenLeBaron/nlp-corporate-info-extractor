'''
Author: Hayden LeBaron
GitHub: HaydenTheBaron
Date: Nov 7, 2021
'''

import sys
import pandas as pd
from template import Template

OUTPUT_DIR_PATH = '../output/'

"""
Main entry point for the information extraction program.
"""
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

    '''Perform information extraction into Template objects'''
    #TODO
    template_list = [Template(text='ShouldbeAllEmpty'),
                     Template(text='123',
                                acquired=['Acquired 1', 'Acquired 2'],
                                acqbus=['Acqbus1', 'Acqbus2'],
                                acqloc=['Acqloc'],
                                dlramt=['$1'],
                                purchaser=['Purchaser'],
                                seller=['Seller'],
                                status=['Current Status'])]

    '''Write to output file'''
    output_file_path = OUTPUT_DIR_PATH + doclist_file_path.split('/')[-1] + '.templates' 
    with open(output_file_path, "w") as outf:
        for template in template_list:
            outf.write('%s\n' % template)

if __name__ == '__main__':
    main()
