import json
import spacy
from spacy.training.example import Example

nlp = spacy.load("spacy_ner_model")
examples = []
data = json.loads(open("../bank_statements/ready/hema.json", 'r').read())

for text, annots in data:
    doc = nlp.make_doc(text)
    examples.append(Example.from_dict(doc, annots))

print(nlp.evaluate(examples)) # This will provide overall and per entity metrics
