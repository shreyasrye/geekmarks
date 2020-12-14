import json 


def write_train_data(read_file, write_file):
    """ Filter the metadata so only the headlines & urls are used for train data. """
    for line in open(read_file, 'r'):
        dictionary = json.loads(line)
        # print('LINE:\n{}'.format(json.dumps(dictionary, indent=4)))
        text, publisher = "", ""
        for key, value in dictionary.items():
            if key == 'headline':
                text = value
            if key == 'publisher':
                try:
                    publisher = value['url']
                except KeyError:
                    publisher = value
        else:
            for key, value in dictionary.items():
                # print('KEY:{}\nVALUE:{}'.format(key, value))
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
        output = f'{{"text":{text},"meta":{publisher}}}'
        output_file = open(write_file, 'a', encoding='utf-8')
        output_file.write(output)
        output_file.write("\n")
        output_file.close()
        # print(output)


if __name__ == '__main__':
    write_train_data('metadata.txt', 'train_data.txt')
