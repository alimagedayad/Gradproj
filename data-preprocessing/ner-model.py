import spacy
import random
import json
from spacy.training.example import Example


def train_spacy(data, iters):
    TRAIN_DATA = data
    nlp = spacy.blank('en')  # create blank Language class
    if 'ner' not in nlp.pipe_names:
        ner = nlp.add_pipe('ner')

    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iters):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)

                nlp.update(
                    [example],
                    drop=0.2,
                    sgd=optimizer,
                    losses=losses)
            print(losses)
    return nlp


TRAIN_DATA = json.loads(open("train.json", 'r').read())
prdnlp = train_spacy(TRAIN_DATA, 500)
modelfile = "spacy_ner_model"
prdnlp.to_disk(modelfile)