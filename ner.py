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
                                publisher = y
        output = f"{{'text':{text},'meta':{publisher}}}"
        print(output)


# # Recursive function to get the nested key value pairs in the jsons.
# def get_nested_pair(key: str, dictionary: dict):
#     print(type(dictionary))
#     for k, value in dictionary.items():
#         if k == key:
#             return value
#         if type(value == list):
#             for d in value:
#                 return get_nested_pair(key, json.loads(d))


if __name__ == '__main__':
    write_train_data('metadata.txt', 'train_data.txt')