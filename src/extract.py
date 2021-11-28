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
from collections import Counter
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

    """TODO: uncomment for SRL ARG0
    '''Run semantic role labler'''
    srl_json_str = json.dumps(srl_predictor.label_batch(text_data))
    srl_df = pd.json_normalize(json.loads(srl_json_str), record_path=['verbs'])['description'].tolist()

    if is_verbose : print('SEMANTIC ROLE DATAFRAME:\n{}'.format(srl_df))

    '''
    Extract AGENT:
           1. Accumulate all "ARG0" spans of text into a list
           2. Map over ARGM-LOC entites, running a NER on each elt. Return a list of places.
           3. Rank options (sort list by rank) (TODO: implement this)
           4. If the list is empty, output '---'. Else choose the highest ranked option.
    '''

    '''1. Accumulate all "ARG0" entites into a list'''

    '''2. Map over ARG0 spans, running a NER on each elt. Return a list of places.'''
    '''> spacy NER labels # TODO: encapsulate these programmatically in a class or something.
       > CARDINAL, DATE, EVENT, FAC, GPE, LANGUAGE, LAW, LOC, MONEY, NORP,
       > ORDINAL, ORG, PERCENT, PERSON, PRODUCT, QUANTITY, TIME, WORK_OF_ART
    '''
    #https://spacy.io/usage/linguistic-features#named-entities


    # Do something like this for some other fields SRL+NER
    arg0_spans = []
    for elt in srl_df:
        arg0_spans.append(re.findall('\[ARG0:.*?\]', elt)) 

    # Remove empty lists, unnest lists (extract 0th element), and extract 'DATA' from '[ARG0: DATA]'
    arg0_spans = list(map(lambda s : s[6:-1].strip(),
                          list(map(lambda ll : ll[0],
                                   list(filter(lambda l : len(l) != 0, arg0_spans))))))

    if is_verbose : print('===ARG0_SPANS:===\n{}'.format(arg0_spans))

    arg0_ents = []
    for span in argmloc_spans: # TODO: use list comprehension
        labeled_span = spacy_model(' '.join(span))
        print('LABELED_SPAN:', labeled_span)
        print('LABELED_SPAN_ENTS:', labeled_span.ents)

        #filter labeled_span.ents such that ent.label_ == 'LOC'.
        loc_ents += list(map(lambda ent : ent.text,
                             list(filter(lambda ent: ent.label_ == 'LOC',
                                         labeled_span.ents))))
    print('LOC_ENTS:', loc_ents)

    '''
    #4. Choose the highest ranked entity, or None if no candiates remaining candidates
    if loc_ents:
        acqloc = loc_ents[0] # Just choose the first location entity
    else:
        acqloc = None
    '''


    labeled_arg0spans = []
    for span in arg0_spans:
        labeled_arg0spans.append(spacy_model(span))
    loc_ents = []
    dlramt_ents = []
    org_ents = []
    for labeled_span in labeled_arg0spans:
        for ent in labeled_span.ents:
            print('(ent.text={},ent.label_={})'.format(ent.text, ent.label_))
            if ent.label_ == 'GPE': #Geo-Political Entity
                loc_ents.append(ent.text)
            elif ent.label_ == 'QUANTITY' or ent.label_ == 'MONEY':
                dlramt_ents.append(ent.text)
            elif ent.label_ == 'ORG':
                org_ents.append(ent.text)

    """


    labeled_sentences = []
    for s_dict in text_data:
        labeled_sentences.append(spacy_model(s_dict['sentence']))
    loc_ents = []
    dlramt_ents = []
    org_ents = []
    for labeled_span in labeled_sentences:
        for ent in labeled_span.ents:
            print('(ent.text={},ent.label_={})'.format(ent.text, ent.label_))
            if ent.label_ == 'GPE': #Geo-Political Entity
                loc_ents.append(ent.text)
            elif ent.label_ == 'QUANTITY' or ent.label_ == 'MONEY':
                dlramt_ents.append(ent.text)
            elif ent.label_ == 'ORG':
                org_ents.append(ent.text)

    # Remove duplicates. Then Extraction success!
    '''
PERFORMANCE FOR USING: property = list(set(property_ents))
                    RECALL             PRECISION          F-SCORE
ACQUIRED        0.59 (245/418)	   0.14 (245/1748)    0.23
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.40 (53/134)	   0.11 (53/478)      0.17
DLRAMT          0.07 (12/164)	   0.05 (12/263)      0.06
PURCHASER       0.63 (234/373)	   0.13 (234/1748)    0.22
SELLER          0.69 (108/156)	   0.06 (108/1748)    0.11
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.39 (652/1693)	   0.11 (652/5985)    0.17

PERFORMANCE FOR USING: x = n_most_common(1, x_ents)
                    RECALL             PRECISION          F-SCORE
ACQUIRED        0.10 (41/418)	   0.10 (41/396)      0.10
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.30 (40/134)	   0.17 (40/234)      0.22
DLRAMT          0.06 (10/164)	   0.07 (10/151)      0.06
PURCHASER       0.30 (111/373)	   0.28 (111/396)     0.29
SELLER          0.25 (39/156)	   0.10 (39/396)      0.14
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.14 (241/1693)	   0.15 (241/1573)    0.15

PERFORMANCE FOR USING: x = n_most_common(2, x_ents)
                    RECALL             PRECISION          F-SCORE
ACQUIRED        0.33 (140/418)	   0.18 (140/773)     0.24
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.37 (49/134)	   0.13 (49/367)      0.20
DLRAMT          0.07 (11/164)	   0.05 (11/207)      0.06
PURCHASER       0.47 (177/373)	   0.23 (177/773)     0.31
SELLER          0.44 (68/156)	   0.09 (68/773)      0.15
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.26 (445/1693)	   0.15 (445/2893)    0.19

PERFORMANCE FOR USING: x = n_most_common(3, x_ents)
                    RECALL             PRECISION          F-SCORE
ACQUIRED        0.50 (208/418)	   0.19 (208/1086)    0.28
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.37 (50/134)	   0.12 (50/429)      0.18
DLRAMT          0.07 (12/164)	   0.05 (12/232)      0.06
PURCHASER       0.58 (215/373)	   0.20 (215/1086)    0.29
SELLER          0.60 (93/156)	   0.09 (93/1086)     0.15
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.34 (578/1693)	   0.15 (578/3919)    0.21

PERFORMANCE FOR USING: x = n_most_common(4, x_ents)
                RECALL             PRECISION          F-SCORE
ACQUIRED        0.58 (243/418)	   0.19 (243/1309)    0.28
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.38 (51/134)	   0.11 (51/457)      0.17
DLRAMT          0.07 (12/164)	   0.05 (12/246)      0.06
PURCHASER       0.62 (232/373)	   0.18 (232/1309)    0.28
SELLER          0.67 (105/156)	   0.08 (105/1309)    0.14
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.38 (643/1693)	   0.14 (643/4630)    0.20

BEST WEIGHTS (n in n_most_common):
    - ACQUIRED=4
    - ACQLOC=2
    - DLRAMT=1
    - PURCHASER=2
    - SELLER=3

PERFORMANCE FOR USING: x = n_most_common(BEST_WEIGHT, x_ents)
                RECALL             PRECISION          F-SCORE
ACQUIRED        0.58 (243/418)	   0.19 (243/1309)    0.28
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.37 (49/134)	   0.13 (49/367)      0.20
DLRAMT          0.06 (10/164)	   0.07 (10/151)      0.06
PURCHASER       0.47 (177/373)	   0.23 (177/773)     0.31
SELLER          0.60 (93/156)	   0.09 (93/1086)     0.15
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.34 (572/1693)	   0.16 (572/3686)    0.21


PERFORMANCE FOR USING: x = n_most_common(BEST_WEIGHT, x_ents) BUT:
    - DLRAMT = []
    - SELLER = []
                RECALL             PRECISION          F-SCORE
ACQUIRED        0.58 (243/418)	   0.19 (243/1309)    0.28
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.37 (49/134)	   0.13 (49/367)      0.20
DLRAMT          0.00 (0/164)	   0.00 (0/0)         0.00
PURCHASER       0.47 (177/373)	   0.23 (177/773)     0.31
SELLER          0.00 (0/156)	   0.00 (0/0)         0.00
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.28 (469/1693)	   0.19 (469/2449)    0.23

PERFORMANCE FOR USING : x = list(set(arg0_spans)) for purchaser, seller, acquired
                RECALL             PRECISION          F-SCORE
ACQUIRED        0.13 (55/418)	   0.02 (55/2639)     0.04
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.37 (49/134)	   0.13 (49/367)      0.20
DLRAMT          0.00 (0/164)	   0.00 (0/0)         0.00
PURCHASER       0.47 (177/373)	   0.07 (177/2639)    0.12
SELLER          0.44 (68/156)	   0.03 (68/2639)     0.05
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.21 (349/1693)	   0.04 (349/8284)    0.07

PERFORMANCE FOR USING : x = list(set(arg1_spans)) for purchaser, seller, acquired
                    RECALL             PRECISION          F-SCORE
ACQUIRED        0.09 (39/418)	   0.01 (39/5235)     0.01
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.37 (49/134)	   0.13 (49/367)      0.20
DLRAMT          0.00 (0/164)	   0.00 (0/0)         0.00
PURCHASER       0.04 (15/373)	   0.00 (15/5235)     0.01
SELLER          0.01 (2/156)	   0.00 (2/5235)      0.00
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.06 (105/1693)	   0.01 (105/16072)   0.01

PERFORMANCE FOR USING: property = list(set(property_ents)) WHERE property_ents are chosen from ARG0 candidates (instead of all sentences)
                    RECALL             PRECISION          F-SCORE
ACQUIRED        0.16 (66/418)	   0.08 (66/808)      0.11
ACQBUS          0.00 (0/153)	   0.00 (0/0)         0.00
ACQLOC          0.07 (9/134)	   0.07 (9/131)       0.07
DLRAMT          0.00 (0/164)	   0.00 (0/0)         0.00
PURCHASER       0.47 (174/373)	   0.22 (174/808)     0.29
SELLER          0.44 (68/156)	   0.08 (68/808)      0.14
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.19 (317/1693)	   0.12 (317/2555)    0.15

PERFORMANCE FOR USING: property = n_most_common(BEST_WEIGHT, list(property_ents)) WHERE property_ents are chosen from ARG0 candidates (instead of all sentences)
                    RECALL             PRECISION          F-SCORE
ACQUIRED        0.16 (65/418)	   0.09 (65/752)      0.11 # WORSE than best
ACQBUS          0.00 (0/153)	   0.00 (0/564)       0.00 # WORSE than best
ACQLOC          0.07 (9/134)	   0.07 (9/131)       0.07 # WORSE than best
DLRAMT          0.00 (0/164)	   0.00 (0/0)         0.00
PURCHASER       0.40 (150/373)	   0.27 (150/564)     0.32 # BEST so far (0.1 better)
SELLER          0.43 (67/156)	   0.10 (67/686)      0.16 # BEST SO FAR (0.1 better)
STATUS          0.00 (0/295)	   0.00 (0/0)         0.00
--------        --------------     --------------     ----
TOTAL           0.17 (291/1693)	   0.11 (291/2697)    0.13
    '''
    n_most_common = lambda n, l : list(map(lambda tuple : tuple[0], Counter(l).most_common(n)))

    acqloc = n_most_common(2, loc_ents)
    #acqloc=list(set(loc_ents))

    #dlramt = n_most_common(1, dlramt_ents)
    dlramt = [] # Best strategy so far is to leave empty
    #dlramt = list(set(dlramt_ents)) #RECALL=0.07 (12/164); PRECISION=0.05 (12/263); F-SCORE=0.06

    purchaser = n_most_common(2, org_ents)
    #purchaser = list(set(org_ents))
    #purchaser = list(set(arg0_spans))


    #acqbus = n_most_common(2, org_ents)
    acqbus = [] # Best strategy so far is to leave empty (for f-score)


    seller = n_most_common(3, org_ents)
    #seller = [] # Best strategy so far is to leave empty (for f-score, but not recall)
    #seller = list(set(arg0_spans))
    #seller = list(set(org_ents)) #RECALL=0.69 (108/156); PRECISION=0.06 (108/1748); F-SCORE=0.11
    #TODO: use this high recall heuristic as a good starting point. Then use more heuristics (maybe SRL) to filter down

    acquired = n_most_common(4, org_ents)
    #acquired = list(set(arg0_spans))
    #acquired = list(set(org_ents))



    #TODO: extract Aqcloc
    #TODO: From buffer, generate pandas dataframe that effectively maps template fields to candidates and metadata about those candidates (using SRL)
    #TODO: implement step
    '''>Output SR labeled JSON to output files: one file per doc....>'''
    #TODO: implement

    '''Apply heuristics to find best candidate(s) (if any) for each field'''
    #TODO

    '''Construct and return template'''
    return Template(text=doc_path.split('/')[-1],
                    acquired=acquired,
                    acqloc=acqloc,
                    dlramt=dlramt,
                    purchaser=purchaser,
                    acqbus=acqbus,
                    seller=seller)



def main():
    """Main entry point for the information extraction program."""

    '''Handle optional args'''
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print("USAGE: `python3 extract.py <docList> [-v]`")
        return

    is_verbose = False
    if len(sys.argv) > 2:
        is_verbose = sys.argv[2] == '-v'
        if is_verbose : print('VERBOSE=TRUE')

    '''Perform information extraction into Template objects'''
    if is_verbose : print('Loading models...')
    srl_predictor = SRLPredictor()
    #srl_predictor = None
    nlp = spacy.load("en_core_web_sm")
    if is_verbose : print('Models loaded.')

    '''Extract docs into pandas series'''
    if is_verbose : print('Extracting docs into pandas series...')
    doclist_file_path = sys.argv[1]
    doc_series = pd.read_table(doclist_file_path, header=None).transpose().iloc[0]
    if is_verbose : print('Docs extracted into pandas series')

    '''Read docs into list'''
    if is_verbose : print('Reading docs into a list...')
    texts = []
    for doc in doc_series:
        with open(doc, 'r') as file:
            texts.append(file.read())
    if is_verbose : print('Docs read into a list.')

    '''Format list of texts'''
    if is_verbose : print('Formatting list of texts...')
    batchdata_batch = batchtexts_to_batchdata_batch(texts=texts,
                                                    rule_based=True) # The rulebased model gaveme 0.01 higher F-score
    #if is_verbose : print('BATCHDATA_BATCH = %s\n' % batchdata_batch)
    if is_verbose : print('List of texts formatted.')

    template_list = []
    docnum = 1
    for doc_path, text_data in zip(doc_series, batchdata_batch):
        if is_verbose : print('\n==============\nEXTRACTING FROM DOCUMENT #{}: {}\n==============\n'.format(docnum, doc_path))
        template_list.append(extract(doc_path,
                                     text_data,
                                     srl_predictor=srl_predictor,
                                     spacy_model=nlp,
                                     is_verbose=is_verbose))
        docnum += 1

    '''Write to output file'''
    output_file_path = OUTPUT_DIR_PATH + doclist_file_path.split('/')[-1] + '.templates'
    with open(output_file_path, "w") as outf:
        for template in template_list:
            if is_verbose : print('%s\n' % template)
            outf.write('%s\n' % template)

if __name__ == '__main__':
    main()
