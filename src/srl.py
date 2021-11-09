from allennlp.predictors import Predictor
from allennlp.models.archival import load_archive
import argparse
import json

#TODO: call this in main script
#TODO: delete tests at the bottom
class SRLPredictor:
    """
    Encapsulates a semantic role labeling model and methods for performing
    semantic role labeling on text.
    """

    def __init__(self):
        #Should work for pip3 install allennlp==2.1.0 allennlp-models==2.1.0
        self._model =  Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz")

    def text_to_batch_data(self, text:str) -> list[dict[str,str]]:
        #TODO: implement
        pass

    def label_batch(self, batch_data:list[dict[str,str]]) -> str:
        """Perform SRL prediction on batch_data formatted like so:
        EXAMPLE:
          [{'sentence': 'Which NFL team represented the AFC at Super Bowl 50?'},
          {'sentence': 'Where did Super Bowl 50 take place?'},
          {'sentence': 'Which NFL team won Super Bowl 50?'}]"""
        if len(batch_data) == 1:
            result = self._model.predict_json(batch_data[0])
            results = [result]
        else:
            results = self._model.predict_batch_json(batch_data)

        string_output = ''
        for model_input, output in zip(batch_data, results):
            string_output += self._model.dump_line(output)
        return string_output


    def label_sentence(self, sentence:str) -> str:
        return self._model.predict(sentence)

'''Test script'''
predictor = SRLPredictor()
batch_data = [{'sentence': 'Which NFL team represented the AFC at Super Bowl 50?'},
              {'sentence': 'Where did Super Bowl 50 take place?'},
              {'sentence': 'Which NFL team won Super Bowl 50?'}]
batch_output = predictor.label_batch(batch_data)
print('batch_output: ', batch_output)

sentence = 'I bought eggs from Sam'
sentence_output = predictor.label_sentence(sentence)
print ('sentence_output: ', sentence_output)
