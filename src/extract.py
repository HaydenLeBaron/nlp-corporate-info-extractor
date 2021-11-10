"""
Author: Hayden LeBaron
GitHub: HaydenTheBaron
Date: Nov 7, 2021
"""
# TODO: make robust enough so that it will never crash
# TODO: parse args with argparse module

import sys
import pandas as pd
from template import Template
from myutils import batchtexts_to_batchdata_batch
from srl import SRLPredictor

OUTPUT_DIR_PATH = '../output/'

def extract(doc_path:str, text_data:list[dict[str,str]], verbose:bool=False) -> Template:
    """Extracts corporate acquisition info from a text into a Template.
    EXAMPLE text_data:
    [{'sentence': 'This is an example sentence'}, ...]
    """

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
    if verbose:
        srl_predictor = SRLPredictor()
        srl_out = srl_predictor.label_batch(text_data)
        print('doc={} --> {}\n'.format(doc_path, srl_out))


    return Template(text=doc_path.split('/')[-1])



def main():
    """Main entry point for the information extraction program."""

    '''Handle optional args'''
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print("USAGE: `python3 extract.py <docList> [-v]`")
        return
    is_verbose = sys.argv[2] == '-v'
    if is_verbose : print('VERBOSE=TRUE')


    '''Extract docs into pandas series'''
    doclist_file_path = sys.argv[1]
    doc_series = pd.read_table(doclist_file_path, header=None).transpose().iloc[0]

    '''Read docs into list'''
    texts = []
    for doc in doc_series:
        with open(doc, 'r') as file:
            texts.append(file.read())

    '''Format list of texts'''
    batchdata_batch = batchtexts_to_batchdata_batch(texts=texts)
    if is_verbose : print('BATCHDATA_BATCH = %s\n' % batchdata_batch)

    '''Perform information extraction into Template objects'''
    template_list = []
    for doc_path, text_data in zip(doc_series, batchdata_batch):
        template_list.append(extract(doc_path, text_data, verbose=is_verbose))

    '''Write to output file'''
    output_file_path = OUTPUT_DIR_PATH + doclist_file_path.split('/')[-1] + '.templates' 
    with open(output_file_path, "w") as outf:
        for template in template_list:
            if is_verbose : print('%s\n' % template)
            outf.write('%s\n' % template)

if __name__ == '__main__':
    main()
