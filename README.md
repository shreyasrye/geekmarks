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
$ prodigy train textcat tc_1_data blank:en --output ./geekmarks-tc-model --eval-split 0.15 --n-iter 100 --batch-size 100

✔ Loaded model 'blank:en'
Created and merged data for 154 total examples
Using 131 train / 23 eval (split 15%)
Component: textcat | Batch size: 100 | Dropout: 0.2 | Iterations: 100
ℹ Baseline accuracy: 0.466

=========================== ✨  Training the model ===========================

#    Loss       F-Score
--   --------   --------
1    0.00       0.465
2    0.00       0.509
3    0.00       0.555
4    0.00       0.560
5    0.00       0.571
6    0.00       0.568
7    0.00       0.555
8    0.00       0.545
9    0.00       0.535
10   0.00       0.538
11   0.00       0.503
12   0.00       0.487
13   0.00       0.496
14   0.00       0.509
15   0.00       0.524
16   0.00       0.536
17   0.00       0.536
18   0.00       0.533
19   0.00       0.529
20   0.00       0.529
21   0.00       0.529
22   0.00       0.538
23   0.00       0.532
24   0.00       0.528
25   0.00       0.528
26   0.00       0.522
27   0.00       0.527
28   0.00       0.532
29   0.00       0.537
30   0.00       0.552
31   0.00       0.562
32   0.00       0.561
33   0.00       0.576
34   0.00       0.571
35   0.00       0.580
36   0.00       0.584
37   0.00       0.581
38   0.00       0.584
39   0.00       0.581
40   0.00       0.570
41   0.00       0.562
42   0.00       0.559
43   0.00       0.562
44   0.00       0.567
45   0.00       0.571
46   0.00       0.574
47   0.00       0.572
48   0.00       0.573
49   0.00       0.576
50   0.00       0.585
51   0.00       0.580
52   0.00       0.582
53   0.00       0.586
54   0.00       0.592
55   0.00       0.595
56   0.00       0.604
57   0.00       0.605
58   0.00       0.601
59   0.00       0.606
60   0.00       0.610
61   0.00       0.614
62   0.00       0.621
63   0.00       0.622
64   0.00       0.625
65   0.00       0.623
66   0.00       0.625
67   0.00       0.623
68   0.00       0.622
69   0.00       0.622
70   0.00       0.621
71   0.00       0.626
72   0.00       0.621
73   0.00       0.627
74   0.00       0.634
75   0.00       0.632
76   0.00       0.630
77   0.00       0.634
78   0.00       0.636
79   0.00       0.636
80   0.00       0.636
81   0.00       0.639
82   0.00       0.643
83   0.00       0.654
84   0.00       0.658
85   0.00       0.660
86   0.00       0.659
87   0.00       0.659
88   0.00       0.660
89   0.00       0.659
90   0.00       0.655
91   0.00       0.662
92   0.00       0.670
93   0.00       0.667
94   0.00       0.666
95   0.00       0.664
96   0.00       0.658
97   0.00       0.649
98   0.00       0.641
99   0.00       0.636
100   0.00       0.633

============================= ✨  Results summary =============================

Label                   ROC AUC
---------------------   -------
INTRO                     0.867
COURSE                    0.136
COMPANY-INFO              0.882
TUTORIAL                  0.733
RANKING                   0.636
EVALUATION                0.318
NEWS                      0.931
PRODUCT/PLATFORM-INFO     0.682
CONCEPT-INFO              0.848


Best ROC AUC   0.670
Baseline       0.466
```
