import json


def write_train_data(read_file, write_file):

    with open(read_file) as rf:
        for line in rf:
            line_json = json.loads(line)
            print(line_json)
    # for i in metadata:
    #     print(json.dumps(i['headline']) + json.dumps(i['url']))
        # cleaned_meta_ls.append("")
    # with open(write_file, 'w'):
    #     for i in cleaned_meta_ls:
    #         json.dumps(i['headline'])


if __name__ == '__main__':
    write_train_data('metadata.txt', 'train_data.txt')