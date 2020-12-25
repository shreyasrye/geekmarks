import json
import plac
import random
import warnings
from pathlib import Path
from spacy.util import minibatch, compounding
from format_train_data import prodigy2spacy
import spacy
from spacy.gold import GoldParse
from spacy.scorer import Scorer

# example run

examples = [
    ('Who is Shaka Khan?',
     [(7, 17, 'PERSON')]),
    ('I like London and Berlin.',
     [(7, 13, 'LOC'), (18, 24, 'LOC')])
]


def get_file(filename):
    with open(filename) as file:
        data = json.load(file)
        return data


TRAIN_DATA = []
TRAIN_DATA = prodigy2spacy("train_data/annotated_data_2.jsonl", TRAIN_DATA)


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


TEST_DATA = []
TEST_DATA = prodigy2spacy("evaluation/evaluation_data.jsonl", TEST_DATA)


def evaluate(ner_model):
    scorer = Scorer()
    for input_, annot in TEST_DATA:
        
        # Gold standard
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annot)
        
        pred_value = ner_model(input_)
        scorer.score(pred_value, gold)
    return scorer.scores


if __name__ == '__main__':
    # First time (new model)
    # train(None, "./geekmars-ner-model")

    # Reloading model
    # train("./geekmarks-ner-model")
    
    # Testing model
    # nlp = spacy.load("./geekmarks-ner-model")
    # print(evaluate(nlp))

    print(examples)
    print("__________________________")
    print(TEST_DATA)