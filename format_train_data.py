import json

def write_train_data(read_file, write_file):
    """ Filter the metadata so only the headlines & urls are used for train data. """
    for line in open(read_file, 'r'):
        dictionary = json.loads(line)
        text, publisher = "", ""
        for key, value in dictionary.items():
            if key == 'headline':
                text = value
            if key == 'publisher':
                try:
                    publisher = value['url']
                except (KeyError, TypeError):
                    publisher = value
        else:
            for key, value in dictionary.items():
                if key == '@graph':
                    for inner_dict in value:
                        for x, y in inner_dict.items():
                            if x == 'headline':
                                text = y
                            if x == 'publisher':
                                try:
                                    publisher = y['url']
                                except KeyError:
                                    publisher = y
        if text == "" and publisher == "":
            continue
        output = {
                "text": text,
                "meta": {
                    "source": publisher
                    }
            }
        output_file = open(write_file, 'a', encoding='utf-8')
        output_file.write(json.dumps(output))
        output_file.write("\n")
        output_file.close()


def prodigy2spacy(prodigy_file, empty_TRAIN_DATA: list):
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




if __name__ == "__main__":
    write_train_data("metadata/metadata_2.txt", "train_data/train_data_2.jsonl")
    
    # temp = []
    # TRAIN_DATA = prodigy2spacy("annotated_data.jsonl", temp)
    # for i in TRAIN_DATA:
    #     print(i)
