import json
import plac
import random
import warnings
from pathlib import Path
from spacy.util import minibatch, compounding
import spacy
from spacy.gold import GoldParse
from spacy.scorer import Scorer


def gold2spacy(prodigy_file, empty_TRAIN_DATA: list):
    for line in open(prodigy_file, 'r'):
        dictionary = json.loads(line)
        text, start_char, end_char, ent = "", None, None, ""
        ent_list = []
        for key, value in dictionary.items():
            if key == "text":
                text = value
            elif key == "spans":
                for dc in value:
                    for k, v in dc.items():
                        if k == "start":
                            start_char = v
                        elif k == "end":
                            end_char = v
                        elif k == "label":
                            ent = v
                    ent_list.append((start_char, end_char, ent))
            elif key == "answer" and value != "accept":
                continue
        spacy_formatted_line = (text, {"entities": ent_list})
        empty_TRAIN_DATA.append(spacy_formatted_line)
    return empty_TRAIN_DATA


TRAIN_DATA = gold2spacy("ner/annotations/annotated_2.jsonl", [])
TEST_DATA = gold2spacy("evaluation/evaluations_2.jsonl", [])


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
                docs = [nlp.make_doc(text) for text in batch]
                beams = ner.beam_parse(docs, beam_width=16)
                for beam in beams:
                    entities = ner.moves.get_beam_annot(beam)
                    print(entities)
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


def evaluate(ner_model, test_data):
    scorer = Scorer()
    for text, ent_dc in test_data:
        doc_gold_text = ner_model.make_doc(text)
        gold = GoldParse(doc_gold_text, entities=ent_dc['entities'])
        pred_value = ner_model(text)
        scorer.score(pred_value, gold)
    return scorer.scores


def pretty_print_eval(scores: dict):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EVALUATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for key, val in scores.items():
        if key == 'ents_per_type':
            print(f"{key} (Scores per entity label):")
            for k, v in val.items():
                print(f"\n    {k}")
                for x,y in v.items():
                    print(f"{x:>8} --> {y}")
            print()
        else:
            print(f"{key:16} --> {val}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

if __name__ == '__main__':
    # First time (new model)
    # train(None, "./geekmars-ner-model")

    # Reloading model
    # train("./geekmarks-ner-model", "./geekmarks-ner-model")
    
    # Testing model
    nlp = spacy.load("./geekmarks-ner-model")
    scores = evaluate(nlp, TEST_DATA)
    pretty_print_eval(scores)