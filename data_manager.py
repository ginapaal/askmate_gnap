import base64


def ID_generator(table):
    new_id = [0]
    for row in table:
        try:
            new_id.append(int(row[0]))
        except:
            continue
    new_id = max(new_id) + 1
    return str(new_id)


def read_from_csv(filename):
    table = []
    with open(filename, "r") as data:
        for line in data:
            lines = line.replace("\n", "")
            words = lines.split(',')
            table.append(words)
    return table


def write_to_csv(filename, new_data):
    with open(filename, "a") as table:
        if filename == 'question.csv':
            for word in new_data:
                if word == new_data[2] or word == new_data[3]:
                    word_encoded = base64.b64encode(bytes(word, 'utf-8'))
                    table.write(str(word_encoded) + ",")
                else:
                    table.write(str(word) + ",")
        else:
            for word in new_data:
                if word == new_data[3]:
                    word_encoded = base64.b64encode(bytes(word, 'utf-8'))
                    table.write(str(word_encoded) + ",")
                else:
                    table.write(str(word) + ",")
        table.write('\n')