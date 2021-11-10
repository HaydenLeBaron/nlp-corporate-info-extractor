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
import json

OUTPUT_DIR_PATH = '../output/'

def extract(doc_path:str, text_data:list[dict[str,str]], is_verbose:bool=False) -> Template:
    """Extracts corporate acquisition info from a text into a Template.
    EXAMPLE text_data:
    [{'sentence': 'This is an example sentence'}, ...]
    """


    '''Run semantic role labler'''
    srl_predictor = SRLPredictor()
    srl_json_str = json.dumps(srl_predictor.label_batch(text_data))
    if is_verbose: print('=====SRL_JSON_STR for {}=====\n{}\n'.format(doc_path, srl_json_str))

    # Read to dataframe, flattening "verbs" list of dicts
    #srl_df = pd.json_normalize(json.loads(srl_json_str), record_path=['verbs'])
    #srl_df = pd.json_normalize(json.loads(srl_json_str), record_path=['verbs'], meta=['words']) # Gives us everything we want, except also includes "description" which is redundant data.

    srl_df = pd.json_normalize(json.loads(srl_json_str),
                               record_path=['verbs'],
                               meta=['words']).drop(columns=['description']) #'description' is
                                                    # redundant and can be derived with "words" and 'tags'
    if is_verbose : print('SEMANTIC ROLE DATAFRAME:\n{}'.format(srl_df))

    """
EXAMPLE SEMANTIC ROLE DATAFRAME (srl_df):
          verb                                               tags                                              words
0         said  [B-ARG0, I-ARG0, I-ARG0, I-ARG0, I-ARG0, B-V, ...  [Santa, Fe, Southern, Pacific, Corp, said, it,...
1        filed  [O, O, O, O, O, O, B-ARG0, B-V, B-ARG1, I-ARG1...  [Santa, Fe, Southern, Pacific, Corp, said, it,...
2       asking  [O, O, O, O, O, O, O, O, B-ARG0, I-ARG0, B-V, ...  [Santa, Fe, Southern, Pacific, Corp, said, it,...
    """

    '''
    Extract Acqloc:
           1. Accumulate all "ARGM-LOC" entities into a list
           2. Map over ARGM-LOC entites, running a NER on each elt. Return a list of places.
           3. Rank options (sort list by rank) (TODO: implement this)
           4. If the list is empty, output '---'. Else choose the highest ranked option.
    '''

    '''Accumulate all "ARGM-LOC" entites into a list'''
    argmloc_entities = []
    print('for loop begin')
    for index, row in srl_df.iterrows():
        print('index: ', index)
        tags = row['tags']
        words = row['words']
        print('tags: ', tags)
        print('words: ', words)

        i = 0
        curr_begin = None
        curr_in = None
        while i < len(tags):
            # Extract entry
            if tags[i] == 'B-ARGM-LOC':
                curr_begin = i
                i+=1
                while i < len(tags) and tags[i] == 'I-ARGM-LOC':
                    curr_in = i
                    i+=1
                    # Leave loop => Found entity start/end indices (inclusive)
                if curr_in is None: # Single word entity
                    argmloc_entities.append(words[curr_begin])
                else:
                    argmloc_entities.append(words[curr_begin:(curr_in+1)])
                # Reset slice vars
                curr_begin = None
                curr_in = None
            i+=1
        print('===ARGMLOC_ENTITIES:===\n{}'.format(argmloc_entities))

        #TODO: extract argloc entities # BKMRK

    #TODO: extract Aqcloc
    # TODO: From buffer, generate pandas dataframe that effectively maps template fields to candidates and metadata about those candidates (using SRL)
    #TODO: implement step
    '''>Output SR labeled JSON to output files: one file per doc....>'''
    #TODO: implement

    '''Apply heuristics to find best candidate(s) (if any) for each field'''
    #TODO

    '''Construct and return template'''
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
        template_list.append(extract(doc_path, text_data, is_verbose=is_verbose))

    '''Write to output file'''
    output_file_path = OUTPUT_DIR_PATH + doclist_file_path.split('/')[-1] + '.templates' 
    with open(output_file_path, "w") as outf:
        for template in template_list:
            if is_verbose : print('%s\n' % template)
            outf.write('%s\n' % template)

if __name__ == '__main__':
    main()
