import base64
import csv


def ID_generator(table):
    new_id = [0]
    for row in table:
        new_id.append(int(row[0]))
    new_id = max(new_id) + 1
    return str(new_id)


def read_from_csv(filename):
    table = []

    with open(filename, "r") as data:
        for line in data:
            lines = line.replace("\n", "")
            words = lines.split(',')
            table.append(words)

        for row in table:
            if filename == 'question.csv':
                try:
                    for word in row:
                        if word == row[2]:
                            byte_format = bytes(row[2], "utf-8")
                            row[2] = base64.b64decode(byte_format).decode("utf-8")
                        
                        elif word == row[3]:
                            byte_format = bytes(row[3], "utf-8")
                            row[3] = base64.b64decode(byte_format).decode("utf-8")
                except:
                    pass
            else:
                try:
                    for word in row:
                        if word == row[2]:
                            byte_format = bytes(row[2], "utf-8")
                            row[3] = base64.b64decode(byte_format).decode("utf-8")
                except:
                    pass

    return table


def write_to_csv(filename, new_data):
    with open(filename, "a") as table:
        if filename == 'question.csv':
            for word in new_data:
                if word == new_data[2] or word == new_data[3]:
                    utf8_encoded = word.encode('utf-8')
                    b64_encoded = base64.b64encode(utf8_encoded).decode("utf-8")
                    table.write(str(b64_encoded) + ",")
                else:
                    table.write(str(word) + ",")
        else:
            for word in new_data:
                if word == new_data[3]:
                    utf8_encoded = word.encode('utf-8')
                    b64_encoded = base64.b64encode(utf8_encoded).decode("utf-8")
                    table.write(str(b64_encoded) + ",")
                else:
                    table.write(str(word) + ",")
        table.write("\n")