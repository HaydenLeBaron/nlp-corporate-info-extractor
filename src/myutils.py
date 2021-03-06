"""
Author: Hayden LeBaron
GitHub: HaydenTheBaron
Date: November 9, 2021

This file contains utilities for performing small, low level subtasks.
"""


from allennlp.data.tokenizers.sentence_splitter import SentenceSplitter
from allennlp.data.tokenizers.sentence_splitter import SpacySentenceSplitter

#TODO: potentially improve sentence splitting performance (and make warnings go away) by adding spacy POS tagging in the pipeline?
def batchtexts_to_batchdata_batch(texts:list[str], rule_based:bool=False) -> list[list[dict[str,str]]]:
    """Takes texts (each text represented by a string) and returns output of form
    [ # This list contains all texts
      [ #This list contains the sentences of a single text
        {'sentence': 'This is an example sentence'}
        ....
      ]
      ....
    ]
    rule_based -- slower, but more accurate sentence splitting
    """
    sentence_splitter = SpacySentenceSplitter(language='en_core_web_sm', rule_based=rule_based)
    texts = sentence_splitter.batch_split_sentences(texts=texts)

    # encase each sentence in a dictionary to get it ready to feed to the SRLPredictor
    return list(map(lambda text :
                    list(map(lambda sentence:
                             # And replace newlines with spaces
                             {'sentence' : sentence.replace('\n', ' ')}, text)),
                    texts))

'''
print(batchtexts_to_batchdata_batch(texts=['I like sushi. My favorite sushi restaurant is Itto.', 'You are stupid. I hate you.']))
'''
