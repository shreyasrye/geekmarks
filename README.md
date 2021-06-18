# Geekmarks

A simple run-through of how to use this repository.

## Documentation

| Documentation   |  Description                                                   |
| --------------- | -------------------------------------------------------------- |
| [spaCy]         | An open-source nlp platform                                    |
| [Prodigy]       | Annotator for creating data for machine learning models        |                     |

[spaCy]: https://spacy.io/usage
[Prodigy]: https://prodi.gy/docs/

## Virtual Environment
You can run this script to setup a virtual environment

`$ pip install virtualenv`

## Dependencies

- Install spacy: For more information on how to install, check the [spaCy Github page](https://github.com/explosion/spaCy)
```
$ pip install spacy
```
- Install Prodigy (paid): For more information on how to install, check the [Prodigy documentation](https://prodi.gy/docs/install)
```
$ pip install *custom prodigy .whl file goes here*
```
- Install Extruct

## Loading and Using Models
### Using the provided model
This repository comes with a semi-trained model, `geekmarks-ner-model`, which is accurate to about 40%, based on the overall precision, recall
and f-score when calling the `evaluate()` function on the `SUBJECT`, `NOUN`, `ADJECTIVE`, `VERB`, `PERSON`, `ORG` and `LOCATION` labels.

In order to use/ update this model, it needs to be loaded first: when running `ner.py`, call the `train()` function with a model in the argument: 
`train("./geekmarks-ner-model")` 

### Using a new/blank model
In order to create your own model, leave the *model* argument blank when calling the `train()` function: 

`train(None, "./output-directory")`

## Gathering and Preparing Data

This repository relies heavily on Prodigy for preparing data for training Spacy models.

### Annotating Data

Before annotating we need to format it for annotating with Prodigy. From the metadata that was extracted, This repository uses only the title and url or source for annotation. 

To filter this metadata from the rest of the metadata for each url, 

#### Pre-existing Model
When using an already trained model, you can annotate data very efficiently using prodigy's *Manual with suggestions from model* recipe: `ner.correct`. With this recipe,
you don't have to label each entity manually; With suggestions from the model and corrections here and there, the task becomes much easier. Here's an example:

```
$ prodigy ner.correct geekmarks_anno_dataset geekmarks-ner-model ./train_data.jsonl --label SUBJECT,NOUN,ADJECTIVE,VERB,PERSON,ORG,LOCATION
```

For an even faster approach, you can use the *Binary with active learning and a model in the loop* recipe, `ner.teach`. This leaves most of the annotation to the model, 
and you are only consulted to accept or reject labels that the model is unsure about tagging.

#### New/Blank Model
When using a brand new or **blank** model, annotating is slightly more tedious. 

Prodigy has two recipes that can be used for annotation with a new model:
- Fully manual --> Raw data is annotated by you by highlighting and clicking on text; the `ner.manual` command is used to do this.
- Manual with suggestions from patterns --> More efficient manual annotation with the help of patterns (specified by an additional parameter)

Once annotations are complete, they can be stored as a file with the `db-out` recipe:
```
$ prodigy db-out geekmarks_anno_dataset > ./annotations.jsonl
```
For more information on annotating data, see [Named Entity Recognition with Prodigy](https://prodi.gy/docs/named-entity-recognition).

### Formatting and Preparing the Data

Once the data is annotated and can be accessible as a file, it needs to be prepared it to be used in training. Since we are training with Spacy, we need to use data that conforms to this format:

```
TRAIN_DATA = [
    ("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
    ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]}),
]
```


## Training and Evaluation

### Training the Text Classification model

Unlike the NER model which was trained with spacy while using annotations from prodigy, the text classification model was trained only using prodigy.

Code snippet for reference:
```
$ prodigy train textcat tc_1_data blank:en --output ./geekmarks-tc-model --eval-split 0.15 --n-iter 100 --batch-size 10

✔ Loaded model 'blank:en'
Created and merged data for 154 total examples
Using 131 train / 23 eval (split 15%)
Component: textcat | Batch size: 10 | Dropout: 0.2 | Iterations: 100
ℹ Baseline accuracy: 0.587

=========================== ✨  Training the model ===========================

#    Loss       F-Score
--   --------   --------
1    1.17       0.595
2    2.16       0.596
3    0.93       0.569
4    1.23       0.602
5    2.33       0.614
6    2.33       0.535
7    1.14       0.549
8    0.45       0.569
9    3.07       0.600
10   2.81       0.614
11   0.35       0.624
12   2.10       0.632
13   0.19       0.641
14   1.17       0.600
15   0.12       0.582
16   0.23       0.581
17   0.16       0.569
18   0.60       0.585
19   0.60       0.572
20   0.83       0.583
21   0.20       0.570
22   1.01       0.554
23   0.20       0.551
24   0.07       0.576
25   1.05       0.584
26   0.09       0.578
27   0.08       0.580
28   2.49       0.604
29   0.16       0.597
30   0.64       0.597
31   1.39       0.616
32   0.26       0.614
33   0.29       0.623
34   0.82       0.633
35   0.92       0.639
36   0.42       0.641
37   0.08       0.656
38   0.66       0.655
39   0.31       0.659
40   0.05       0.664
41   0.99       0.665
42   0.45       0.677
43   0.65       0.676
44   0.03       0.671
45   0.03       0.679
46   0.04       0.684
47   0.04       0.690
48   0.70       0.696
49   0.22       0.690
50   0.39       0.701
51   0.02       0.711
52   0.03       0.704
53   1.32       0.713
54   0.02       0.717
55   0.02       0.713
56   0.04       0.700
57   0.02       0.702
58   0.03       0.683
59   0.03       0.685
60   0.03       0.687
61   0.02       0.686
62   0.71       0.696
63   0.10       0.708
64   0.15       0.716
65   0.07       0.717
66   1.02       0.729
67   0.02       0.734
68   0.02       0.744
69   0.02       0.751
70   0.16       0.752
71   0.02       0.757
72   0.01       0.768
73   0.02       0.772
74   0.02       0.742
75   0.01       0.762
76   0.02       0.768
77   0.03       0.767
78   1.01       0.768
79   0.01       0.764
80   0.01       0.763
81   0.02       0.779
82   0.01       0.778
83   1.14       0.779
84   1.01       0.787
85   0.02       0.787
86   0.01       0.787
87   0.02       0.785
88   0.02       0.784
89   0.55       0.782
90   0.01       0.782
91   1.01       0.790
92   0.09       0.792
93   0.12       0.801
94   0.01       0.808
95   0.01       0.811
96   0.01       0.812
97   0.01       0.818
98   0.01       0.814
99   0.03       0.819
100   0.01       0.822

============================= ✨  Results summary =============================

Label                   ROC AUC
---------------------   -------
RANKING                   1.000
NEWS                      0.775
PRODUCT/PLATFORM-INFO     0.803
COMPANY-INFO              0.737
COURSE                    1.000
CONCEPT-INFO              0.917
INTRO                     0.583
EVALUATION                0.682
TUTORIAL                  0.900


Best ROC AUC   0.822
Baseline       0.587
```
