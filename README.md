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

- Install spacy: For more information on how to install, check the [spaCy Github page](https://github.com/explosion/spaCy)
```
$ pip install spacy
```
- Install Prodigy (paid): For more information on how to install, check the [Prodigy documentation](https://prodi.gy/docs/install)
```
$ pip install *custom prodigy .whl file goes here*
```
## Loading and Using Models
### Using the provided model
This repository comes with a semi-trained model, `geekmarks-ner-model`, which is accurate to about 40%, based on the overall precision, recall
and f-score when calling the `evaluate()` function on the `SUBJECT`, `NOUN`, `ADJECTIVE`, `VERB`, `PERSON`, `ORG` and `LOCATION` labels.

In order to use/ update this model, it needs to be loaded first: when running `ner.py`, call the `train()` function with a model in the argument: `train("./geekmarks-ner-model")` 

### Using a new/blank model
In order to create your own model, leave the *model* argument blank when calling the `train()` function: `train(None, "./output-directory")`

## Gathering and Preparing Data

This repository relies heavily on Prodigy for preparing data for training Spacy models.

### Annotating Data
When using an already trained model, you can annotate data very efficiently using prodigy's *Manual with suggestions from model* recipe: `ner.correct`. With this recipe,
you don't have to label each entity manually; With suggestions from the model and corrections here and there, the task becomes much easier. Here's an example:

```
$ prodigy ner.correct geekmarks_anno_dataset geekmarks-ner-model ./train_data.jsonl --label SUBJECT,NOUN,ADJECTIVE,VERB,PERSON,ORG,LOCATION
```

For an even faster approach, you can use the *Binary with active learning and a model in the loop* recipe, `ner.teach`. This leaves most of the annotation to the model, 
and you are only consulted to accept or reject labels that the model is unsure about tagging.

When using a brand new or **blank** model, annotating is slightly more tedious. 

Prodigy has two recipes that can be used for annotation with a new model:
- Fully manual --> Raw data is annotated by you by highlighting and clicking on text; the `ner.manual` command is used to do this.
- Manual with suggestions from patterns --> 

## Training and Evaluation


