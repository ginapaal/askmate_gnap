def ID_generator(table):
    new_id = [0]
    for row in table:
        new_id.append(int(row[0]))
        new_id = max(new_id) + 1
    return str(new_id)



#def read_from_csv():
    #return table




#def write_to_csv():
    #pass
