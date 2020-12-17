import json
import plac
import random
import warnings
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
from format_train_data import prodigy2spacy
from spacy.scorer import Scorer


def get_file(filename):
    with open(filename) as file:
        data = json.load(file)
        return data


# First time (new model)
TRAIN_DATA = []
TRAIN_DATA = prodigy2spacy("annotated_data.jsonl", TRAIN_DATA)



def train(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model != None:
        nlp = spacy.load(model)
    else:
        nlp = spacy.blank("en")
    print("Created blank 'en' model")
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe("ner")
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    with nlp.disable_pipes(*other_pipes), warnings.catch_warnings():
        warnings.filterwarnings("once", category=UserWarning, module='spacy')
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)


def test(model=None, n_iter=100):
    print("Loading from")
    nlp = spacy.load(model)

    test = "Artificial intelligence (AI) vs. natural language processing (NLP): What are the differences?"
    doc = nlp(test)

    for ent in doc.ents:
        print("Text: ", ent.text, " Label: ", ent.label_)
    # sc = Scorer()
    # sc.score(doc, gold)
    

if __name__ == '__main__':
    # First time (new model)
    # train(None, "./geekmars-ner")
    
    # Testing model
    test("geekmarks-ner")
