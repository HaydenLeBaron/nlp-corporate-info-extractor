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
from allennlp.predictors.sentence_tagger import SentenceTaggerPredictor
import spacy
import re

'''
TODO: change spacy.load("en_core_web_sm") to spacy.load("en_core_web_trf") for slower, but more accurate model
and run python -m spacy download en_core_web_trf to install the larger model. Create a flag for the program that chooses which models/options to use (fast/accurate flag)
'''
OUTPUT_DIR_PATH = '../output/'

def extract(doc_path:str,
            text_data:list[dict[str,str]],
            srl_predictor:SRLPredictor,
            spacy_model, #TODO: put type annotation by what is returned by spacy.load()
            is_verbose:bool=False) -> Template:
    """Extracts corporate acquisition info from a text into a Template.
    EXAMPLE text_data:
    [{'sentence': 'This is an example sentence'}, ...]
    """

    '''Run semantic role labler'''
    srl_json_str = json.dumps(srl_predictor.label_batch(text_data))

    #TODO: uncommentme
    #if is_verbose: print('=====SRL_JSON_STR for {}=====\n{}\n'.format(doc_path, srl_json_str))

    # Read to dataframe, flattening "verbs" list of dicts
    #srl_df = pd.json_normalize(json.loads(srl_json_str), record_path=['verbs'])
    #srl_df = pd.json_normalize(json.loads(srl_json_str), record_path=['verbs'], meta=[['words']],errors='ignore') # Gives us everything we want, except also includes "description" which is redundant data.
    #words_df = pd.json_normalize(json.loads(srl_json_str), record_path=['words']) # Gives us everything we want, except also includes "description" which is redundant data.

    #FIXME: restructure data #BKMRK
    #srl_df = pd.json_normalize(json.loads(srl_json_str),
    #                           record_path=['verbs'],
    #                           meta=['words'], errors='ignore').drop(columns=['description']) #'description' is
    #srl_df = pd.json_normalize(json.loads(srl_json_str), max_level=2)
    #srl_df = pd.json_normalize(json.loads(srl_json_str), record_path=['verbs'], meta=['verbs', 'description'], errors='ignore')

    #GOOD
    #srl_df = pd.json_normalize(json.loads(srl_json_str), record_path=['verbs'])['description']

    #srl_df = pd.json_normalize(json.loads(srl_json_str))
    #df2 = pd.read_json(json.dumps(srl_df['verbs']))
    #df2 = pd.json_normalize(json.loads(json.dumps(srl_df['verbs'].jloc[0])))
    #srl_tags_df = srl_verbs_df['tags']
    #srl_tags_df = pd.json_normalize(json.loads(srl_json_str), record_path=['verbs'])['tags']
    #words_df = pd.json_normalize(json.loads(srl_json_str))['words'] # Get words df



    #df2 = pd.read_json(srl_json_str).transpose().iloc[1]
    #words = df2
                                                    # redundant and can be derived with "words" and 'tags'


    srl_df = pd.json_normalize(json.loads(srl_json_str), record_path=['verbs'])['description'].tolist()

    if is_verbose:
        print('SEMANTIC ROLE DATAFRAME:\n{}'.format(srl_df))
        #print('DF 2:\n{}'.format(df2))
        #print('SEMANTIC ROLE VERBS_DATAFRAME:\n{}'.format(srl_verbs_df))
        #print('SEMANTIC ROLE TAGS DATAFRAME:\n{}'.format(srl_tags_df))
        #print('WORDS:\n{}'.format(words_df))



    """
EXAMPLE SEMANTIC ROLE DATAFRAME (srl_df):
          verb                                               tags                                              words
0         said  [B-ARG0, I-ARG0, I-ARG0, I-ARG0, I-ARG0, B-V, ...  [Santa, Fe, Southern, Pacific, Corp, said, it,...
1        filed  [O, O, O, O, O, O, B-ARG0, B-V, B-ARG1, I-ARG1...  [Santa, Fe, Southern, Pacific, Corp, said, it,...
2       asking  [O, O, O, O, O, O, O, O, B-ARG0, I-ARG0, B-V, ...  [Santa, Fe, Southern, Pacific, Corp, said, it,...
    """

    '''
    Extract Acqloc:
           1. Accumulate all "ARGM-LOC" spans of text into a list
           2. Map over ARGM-LOC entites, running a NER on each elt. Return a list of places.
           3. Rank options (sort list by rank) (TODO: implement this)
           4. If the list is empty, output '---'. Else choose the highest ranked option.
    '''

    '''1. Accumulate all "ARGM-LOC" entites into a list'''

    argmloc_spans = []
    for elt in srl_df:
        argmloc_spans.append(re.findall('\[ARGM-LOC.*?\]', elt))
    if is_verbose : print('===ARGMLOC_SPANS:===\n{}'.format(argmloc_spans))

    '''2. Map over ARGM-LOC spans, running a NER on each elt. Return a list of places.'''
    '''> spacy NER labels # TODO: encapsulate these programmatically in a class or something.
       > CARDINAL, DATE, EVENT, FAC, GPE, LANGUAGE, LAW, LOC, MONEY, NORP,
       > ORDINAL, ORG, PERCENT, PERSON, PRODUCT, QUANTITY, TIME, WORK_OF_ART
    '''
    #https://spacy.io/usage/linguistic-features#named-entities
    loc_ents = []
    for span in argmloc_spans: # TODO: use list comprehension
        labeled_span = spacy_model(' '.join(span))
        print('LABELED_SPAN:', labeled_span)
        print('LABELED_SPAN_ENTS:', labeled_span.ents)

        #filter labeled_span.ents such that ent.label_ == 'LOC'.
        loc_ents += list(map(lambda ent : ent.text,
                             list(filter(lambda ent: ent.label_ == 'LOC',
                                         labeled_span.ents))))

        print('LOC_ENTS:', loc_ents)
    '''4. Choose the highest ranked entity, or None if no candiates remaining candidates'''
    if loc_ents:
        acqloc = loc_ents[0] # Just choose the first location entity
    else:
        acqloc = None




    #TODO: extract Aqcloc
    # TODO: From buffer, generate pandas dataframe that effectively maps template fields to candidates and metadata about those candidates (using SRL)
    #TODO: implement step
    '''>Output SR labeled JSON to output files: one file per doc....>'''
    #TODO: implement

    '''Apply heuristics to find best candidate(s) (if any) for each field'''
    #TODO

    '''Construct and return template'''
    return Template(text=doc_path.split('/')[-1], acqloc=acqloc)



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
    if is_verbose : print('Loading models...')
    srl_predictor = SRLPredictor()
    spacy_model = spacy.load("en_core_web_sm")
    if is_verbose : print('Models loaded.')
    template_list = []
    for doc_path, text_data in zip(doc_series, batchdata_batch):
        template_list.append(extract(doc_path,
                                     text_data,
                                     srl_predictor=srl_predictor,
                                     spacy_model=spacy_model,
                                     is_verbose=is_verbose))

    '''Write to output file'''
    output_file_path = OUTPUT_DIR_PATH + doclist_file_path.split('/')[-1] + '.templates' 
    with open(output_file_path, "w") as outf:
        for template in template_list:
            if is_verbose : print('%s\n' % template)
            outf.write('%s\n' % template)

if __name__ == '__main__':
    main()
