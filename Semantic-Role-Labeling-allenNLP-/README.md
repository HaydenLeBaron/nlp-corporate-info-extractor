## **Semantic Role Labeling using AllenNLP**

This script takes sample sentences which can be a single or list of sentences and uses AllenNLP's per-trained model on Semantic Role Labeling to make predictions.

## TO-DO

TODO: EXPERIMENT:: On the entire data set: Figure out correlations between each semantic role tag group \*-T 
- For each training document:
  - Tag each sentence for semantic role
  - Then group all data into a dictionary D1 mapping a tag group T to a set of tuples I:=(V, S) -- where T is the name of the tag (e.g. ARG0, ARGM-LOC, O [for O], V), V is the verb in the current frame, and S is the associated string (B's and I's of type T concatenated together). Ignore O's
  - Construct another dictionary D2 that is the same as D1, except T maps directly to a set of strings S (no V)
  - Find out what percent of the time a gold string GS in each field GF is approximately equal to some string S in T\[\]
  - Generate a table of the probability of GS being in T[] for all T and all fields F
  
```python
    ARG0  ARGM-LOC   V ...
GF1  P1    P2
GF2  P3    P4
GF3 ..........
GF4
GF5
GF6
GF7

# Therefore P1 would be: 
( (freq(GF1.value in set:ARG0) / (freq(GF1.value)) ) for each gold in golds
#NOTE: we only want to do this where GF1.value is not ---
# We are basically trying to determine the probability that the correct gold answer is in our
# set of candidates for each T
# so that we can determine which T's are most highly correlated with which field.
# At the end of this experiment, we should know things like "There is a 70% chance that the set ARG0 contains F5 (the PURCHASER)".
```

The next step would be to perform the same experiment, but only for frames where the verb V is a buy/sell verb. And to generate the tables depending on if the verb is a buy/sell verb. For example, I hypothesize that when the verb is a buy verb, the AGENT is probably the PURCHASER. Whereas with a sell verb, the AGENT is probably the SELLER.

The initial model (due Nov 10) will just pick some value from the most correlated set. The initial model will probably assign STATUS to the verb. STATUS will probably be the hardest thing to extract.

A subsequent model will pick the best value from the set based on multiple factors. 
- For example, (assuming that the AGENT is probably the purchaser), the PURCHASER field will have a bunch of AGENT (ARG0) candidates to choose from. Of those candidates, it will prefer to be filled out by a named entity. If it can't find a named entity, then it just won't be filled out at all.

- For fields without great correlation, I might have to implement custom logic for extracting it. For example, I think that the DLRAMT might be best extracted by just identifying a string with money related keywords next to it (like "dollars", "$", etc.).

## High level description of solution

### Brainstorm 1

1. Semantic Role tagging for the document.
2. Aggregate semantic tags into a two dictionaries for the entire document--A "buy-verb" dictionary, and a "sell-verb" dictionary that takes semantic tags and maps them to a set of strings. Keep 
3. Based on heuristics derived in experiments, assign each field to their most correlated semantic role dictionaies. The dictionaries contain candidates. Apply additional heuristic to select the best candidates. If we cannot get further evidence, simply fill out the field as blank.
  
## **Description**

**Semantic Role Labeling**

Semantic Role Labeling (SRL) recovers the latent predicate argument structure of a sentence, providing representations that answer basic questions about sentence meaning, including “who” did “what” to “whom,” etc. The AllenNLP SRL model is a reimplementation of a deep BiLSTM model (He et al, 2017).

The model used for this script is found at https://s3-us-west-2.amazonaws.com/allennlp/models/srl-model-2018.05.25.tar.gz

## **Install prerequisites**

Install AllenNLP

AllenNLP can be installed using pip3:

```pip3 install allennlp```

  
But there are other options: https://github.com/allenai/allennlp#installation

## **Usage**

To run script with SRL model:

on project directory or virtual enviroment

```$python3 allen_srl.py```

## **Interpreting the result**

AllenNLP uses PropBank Annotation. As a result,each verb sense has numbered arguments e.g., ARG-0, ARG-1,

etc.

ARG-0 is usually PROTO-AGENT

ARG-1 is usually PROTO-PATIENT

ARG-2 is usually benefactive, instrument, attribute

ARG-3 is usually start point, benefactive, instrument, attribute

ARG-4 is usually end point (e.g., for move or push style verbs)

## **License**

AllenNLP is licensed under Apache 2.0
