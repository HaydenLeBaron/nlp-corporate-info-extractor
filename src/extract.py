'''
Author: Hayden LeBaron
GitHub: HaydenTheBaron
Date: Nov 7, 2021
'''
# TODO: make robust enough so that it will never crash

import sys
import pandas as pd
from template import Template

OUTPUT_DIR_PATH = '../output/'

def extract(doc:str) -> Template:
    """Extracts corporate acquisition info from doc into a Template."""

    '''Read document into buffer'''
    doc_buf = ''
    with open(doc, 'r') as file:
        doc_buf = file.read()

    '''Generate candidates via semantic role labeling'''
    # TODO: From buffer, generate pandas dataframe that effectively maps template fields to candidates and metadata about those candidates (using SRL)
    '''>
    # TODO: draw structure of data frame
    acquired
    acqbus
    acqloc
    dlramt
    purchaser
    seller
    status
    ...>'''
    #TODO: implement step
    '''>Output SR labeled JSON to output files: one file per doc....>'''
    #TODO: implement

    '''Apply heuristics to find best candidate(s) (if any) for each field'''
    #TODO

    '''Construct and return template'''
    return Template(text=doc.split('/')[-1])



def main():
    """Main entry point for the information extraction program."""

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
    template_list = []
    for doc in doc_series:
        template_list.append(extract(doc))


    '''Write to output file'''
    output_file_path = OUTPUT_DIR_PATH + doclist_file_path.split('/')[-1] + '.templates' 
    with open(output_file_path, "w") as outf:
        for template in template_list:
            outf.write('%s\n' % template)

if __name__ == '__main__':
    main()
