import base64


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
    return table


def write_to_csv(filename, new_data):
    table = read_from_csv(filename)
    new_id = ID_generator(table)
    new_data.insert(0, new_data)
    with open(filename, "a") as table:
        for data in table:
            f.write(data + ",")
        f.write('\n')
    updated_table = read_from_csv(filename)
    return updated_table
