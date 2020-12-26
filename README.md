# Geekmarks

A simple run-through of how to use this repository.

## Documentation

| Documentation   |  Description                                                   |
| --------------- | -------------------------------------------------------------- |
| [spaCy]         | An open-source nlp platform                                    |
| [Prodigy]       | Annotator for creating data for machine learning models        |                     |

[spaCy]: https://spacy.io/usage
[Prodigy]: https://prodi.gy/docs/

## Dependencies

- Install spacy 
- Prodigy (paid)
```
$ pip install spacy
$ pip install *custom prodigy whl file goes here*
```

## Training and Evaluation

This repository comes with a semi-trained model, `geekmarks-ner-model`, which is accurate to about 40%, based on the overall precision, recall
and f-score when calling the `evaluate()` function on the `SUBJECT`, `NOUN`, `ADJECTIVE`, `VERB`, `PERSON`, `ORG` and `LOCATION` labels.
