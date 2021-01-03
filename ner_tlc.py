from numpy.lib.function_base import _parse_input_dimensions
import spacy
from ner import gold2spacy
from prettytable import PrettyTable


def nerOutput(model, TRAIN_DATA):
    nlp = spacy.load(model)

    table = PrettyTable(["Text", "Entities (Text, Label, Confidence)"])
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        beams = nlp.entity.beam_parse([ doc ], beam_width = 16, beam_density = 0.0001)
        table.add_row([text, [(ent.text, ent.label_) for ent in doc.ents]])
    print(table)

# entity_scores = defaultdict(float)
# for beam in beams:
#     for score, ents in nlp.entity.moves.get_beam_parses(beam):
#         for start, end, label in ents:
#             entity_scores[(start, label)] += score


if __name__ == "__main__":
    TRAIN_DATA = gold2spacy("evaluation/evaluation_data.jsonl", [])
    nerOutput("geekmarks-ner-model", TRAIN_DATA)


"""
Example Output:

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