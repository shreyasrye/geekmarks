from numpy.lib.function_base import _parse_input_dimensions
import spacy
from spacy.util import minibatch, compounding
from ner import gold2spacy
from prettytable import PrettyTable
from collections import defaultdict


def nerOutput(model, TRAIN_DATA):
    nlp = spacy.load(model)

    table = PrettyTable(["Text", "Entities (Text, Label, Confidence)"])
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('--- Entities (detected with standard NER) ---')
        for ent in doc.ents:
            print('%d to %d: %s (%s)') % (ent.start, ent.end - 1, ent.label_, ent.text)
        print('')
        
        with nlp.disable_pipes('ner'):
            doc = nlp(text)

        (beams, somethingelse) = nlp.entity.beam_parse([ doc ], beam_width = 16, beam_density = 0.0001)

        entity_scores = defaultdict(float)
        for beam in beams:
            for score, ents in nlp.entity.moves.get_beam_parses(beam):
                for start, end, label in ents:
                    entity_scores[(start, end, label)] += score

        print('--- Entities and scores (detected with beam search) ---')
        for key in entity_scores:
            start, end, label = key
            print('%d to %d: %s (%f)') % (start, end - 1, label, entity_scores[key])
        # batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
        # for batch in batches:
        #     for text in batch:
        #         print(text)
        #     docs = [nlp.make_doc(text) for text[0] in batch]
        #     beams = ner.beam_parse(docs, beam_width=16)
        #     for beam in beams:
        #         entities = ner.moves.get_beam_annot(beam)
        #         print(entities)
        
        # beams = nlp.entity.beam_parse([doc], beam_width = 16, beam_density = 0.0001)
        # entity_scores = defaultdict(float)
        # for beam in beams:
        #     for score, ents in nlp.entity.moves.get_beam_parses(beam):
        #         for start, end, label in ents:
        #             entity_scores[(start,end, label)] += score
        # print(entity_scores)
        table.add_row([text, [(ent.text, ent.label_) for ent in doc.ents]])
    print(table)


if __name__ == "__main__":
    TRAIN_DATA = gold2spacy("evaluation/evaluation_data.jsonl", [])
    nerOutput("geekmarks-ner-model", TRAIN_DATA)


"""
Example Output:

defaultdict(<class 'float'>, {(0, 1, 'SUBJECT'): 1.0})
defaultdict(<class 'float'>, {(1, 3, 'SUBJECT'): 1.0, (4, 5, 'PERSON'): 1.0, (7, 8, 'ADJECTIVE'): 1.0})
defaultdict(<class 'float'>, {(0, 2, 'SUBJECT'): 1.0, (3, 4, 'NOUN'): 1.0, (6, 9, 'ADJECTIVE'): 1.0, (9, 10, 'NOUN'): 1.0})
defaultdict(<class 'float'>, {(0, 1, 'NOUN'): 1.0, (2, 3, 'NOUN'): 1.0, (4, 5, 'NOUN'): 1.0, (7, 9, 'PERSON'): 1.0, (10, 13, 'ORG'): 1.0})
defaultdict(<class 'float'>, {(1, 2, 'VERB'): 1.0, (3, 6, 'SUBJECT'): 1.0, (7, 8, 'NOUN'): 1.0})
defaultdict(<class 'float'>, {(0, 2, 'SUBJECT'): 1.0, (3, 4, 'NOUN'): 1.0})
defaultdict(<class 'float'>, {(1, 2, 'ADJECTIVE'): 1.0, (2, 3, 'NOUN'): 1.0, (4, 5, 'VERB'): 1.0, (6, 8, 'ADJECTIVE'): 1.0, (8, 9, 'NOUN'): 1.0})
defaultdict(<class 'float'>, {(0, 1, 'SUBJECT'): 1.0})
defaultdict(<class 'float'>, {(0, 2, 'SUBJECT'): 1.0})
defaultdict(<class 'float'>, {(1, 2, 'ORG'): 1.0, (3, 4, 'VERB'): 1.0, (4, 6, 'ADJECTIVE'): 1.0, (6, 7, 'ADJECTIVE'): 1.0, (7, 8, 'NOUN'): 1.0, (9, 10, 'NOUN'): 1.0})
defaultdict(<class 'float'>, {(0, 1, 'VERB'): 1.0, (1, 3, 'SUBJECT'): 1.0, (5, 6, 'NOUN'): 1.0, (7, 8, 'NOUN'): 1.0, (9, 12, 'ORG'): 1.0})
defaultdict(<class 'float'>, {(0, 1, 'ADJECTIVE'): 1.0, (1, 3, 'NOUN'): 1.0, (3, 4, 'NOUN'): 1.0, (5, 6, 'VERB'): 1.0, (8, 9, 'VERB'): 1.0})
defaultdict(<class 'float'>, {(0, 2, 'SUBJECT'): 1.0, (2, 3, 'VERB'): 1.0, (3, 6, 'VERB'): 1.0, (8, 10, 'VERB'): 1.0, (12, 15, 'NOUN'): 1.0})
defaultdict(<class 'float'>, {(0, 2, 'SUBJECT'): 1.0, (2, 3, 'NOUN'): 1.0, (6, 7, 'VERB'): 1.0, (8, 9, 'VERB'): 1.0, (9, 10, 'NOUN'): 1.0, (11, 12, 'NOUN'): 1.0})
defaultdict(<class 'float'>, {(1, 2, 'ADJECTIVE'): 1.0, (2, 3, 'ADJECTIVE'): 1.0, (3, 5, 'NOUN'): 1.0, (6, 9, 'SUBJECT'): 1.0})
defaultdict(<class 'float'>, {(1, 2, 'NOUN'): 1.0, (3, 4, 'VERB'): 1.0, (4, 6, 'NOUN'): 1.0, (7, 10, 'NOUN'): 1.0, (11, 12, 'NOUN'): 1.0, (13, 16, 'ORG'): 1.0})
defaultdict(<class 'float'>, {(1, 2, 'ADJECTIVE'): 1.0, (2, 3, 'NOUN'): 1.0, (4, 5, 'VERB'): 1.0, (5, 7, 'SUBJECT'): 1.0, (8, 11, 'ORG'): 1.0})
defaultdict(<class 'float'>, {(0, 2, 'VERB'): 1.0, (4, 6, 'NOUN'): 1.0})
defaultdict(<class 'float'>, {(1, 2, 'ADJECTIVE'): 1.0, (3, 4, 'ADJECTIVE'): 1.0, (4, 5, 'NOUN'): 1.0, (6, 8, 'NOUN'): 1.0})
defaultdict(<class 'float'>, {(0, 1, 'VERB'): 1.0, (2, 4, 'NOUN'): 1.0, (4, 6, 'NOUN'): 1.0})
+-------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                               Text                                              |                                                            Entities (Text, Label, Confidence Score)                                                           |
+-------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                              Next.                                              |                                                                     [('Next', 'SUBJECT')]                                                                     |
|                      4 Python Concepts That Beginners May Be Confused About                     |                                      [('Python Concepts', 'SUBJECT'), ('Beginners', 'PERSON'), ('Confused', 'ADJECTIVE')]                                     |
|                   Building Simulations in Python — A Step by Step Walkthrough                   |                       [('Building Simulations', 'SUBJECT'), ('Python', 'NOUN'), ('Step by Step', 'ADJECTIVE'), ('Walkthrough', 'NOUN')]                       |
|               Python, Pandas & XlsxWriter | by Dean McGrath | Towards Data Science              |                 [('Python', 'NOUN'), ('Pandas', 'NOUN'), ('XlsxWriter', 'NOUN'), ('Dean McGrath', 'PERSON'), ('Towards Data Science', 'ORG')]                 |
|                              I built a Next.js job board with Next.                             |                                            [('built', 'VERB'), ('Next.js job board', 'SUBJECT'), ('Next', 'NOUN')]                                            |
|                                   Bitwise Operators in Python                                   |                                                     [('Bitwise Operators', 'SUBJECT'), ('Python', 'NOUN')]                                                    |
|                          A Simple Tool to Create Your Web Scraping Bot                          |                        [('Simple', 'ADJECTIVE'), ('Tool', 'NOUN'), ('Create', 'VERB'), ('Web Scraping', 'ADJECTIVE'), ('Bot', 'NOUN')]                        |
|                                             Cheerio:                                            |                                                                    [('Cheerio', 'SUBJECT')]                                                                   |
|                                         Changing Lanes:                                         |                                                                [('Changing Lanes', 'SUBJECT')]                                                                |
|                   How Lyft is Migrating 100+ Frontend Microservices to Next.js                  |           [('Lyft', 'ORG'), ('Migrating', 'VERB'), ('100+', 'ADJECTIVE'), ('Frontend', 'ADJECTIVE'), ('Microservices', 'NOUN'), ('Next.js', 'NOUN')]          |
|               Display Rich Text In The Console Using Python - Towards Data Science              |                   [('Display', 'VERB'), ('Rich Text', 'SUBJECT'), ('Console', 'NOUN'), ('Python', 'NOUN'), ('Towards Data Science', 'ORG')]                   |
|                        6 coding hygiene tips that helped me get promoted.                       |                          [('6', 'ADJECTIVE'), ('coding hygiene', 'NOUN'), ('tips', 'NOUN'), ('helped', 'VERB'), ('promoted', 'VERB')]                         |
| JS 10 Brings Automatic Image Optimization,  Internationalized Routing, and Web Vitals Analytics | [('JS 10', 'SUBJECT'), ('Brings', 'VERB'), ('Automatic Image Optimization', 'VERB'), ('Internationalized Routing', 'VERB'), ('Web Vitals Analytics', 'NOUN')] |
|              JavaScript Promise Tutorial – How to Resolve or Reject Promises in JS              |            [('JavaScript Promise', 'SUBJECT'), ('Tutorial', 'NOUN'), ('Resolve', 'VERB'), ('Reject', 'VERB'), ('Promises', 'NOUN'), ('JS', 'NOUN')]           |
|                     An explainable topological search engine with Giotto-tda                    |                       [('explainable', 'ADJECTIVE'), ('topological', 'ADJECTIVE'), ('search engine', 'NOUN'), ('Giotto-tda', 'SUBJECT')]                      |
|            10 Examples to Master *args and **kwargs in Python - Towards Data Science            |            [('Examples', 'NOUN'), ('Master', 'VERB'), ('*args', 'NOUN'), ('**kwargs', 'NOUN'), ('Python', 'NOUN'), ('Towards Data Science', 'ORG')]           |
|                 3 Useful Projects to learn Python Classes - Towards Data Science                |               [('Useful', 'ADJECTIVE'), ('Projects', 'NOUN'), ('learn', 'VERB'), ('Python Classes', 'SUBJECT'), ('Towards Data Science', 'ORG')]              |
|                              Web Scraping with a Headless Browser:                              |                                                    [('Web Scraping', 'VERB'), ('Headless Browser', 'NOUN')]                                                   |
|                         A Minimalist and Fast Alternative to React Color                        |                             [('Minimalist', 'ADJECTIVE'), ('Fast', 'ADJECTIVE'), ('Alternative', 'NOUN'), ('React Color', 'NOUN')]                            |
|                                   Find your Next JS dream job!                                  |                                                 [('Find', 'VERB'), ('Next JS', 'NOUN'), ('dream job', 'NOUN')]                                                |
+-------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+

"""