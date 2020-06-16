import json
import os

def read_csv_file(filename, delimiter=','):
    # This function should read the given csv file, generate a list of dictionaries
    # Each row should be represented in the form of a dictionary, with column name as key and column data as value
    columns = []
    infile_data = []
    with open(filename)  as infile:
        for index, row in enumerate(infile):
            row = row.strip().split(delimiter)
            if index == 0:
                columns = row
            else:
                row_dict = {}
                for col_index, column in enumerate(row):
                    col_name = columns[col_index]
                    row_dict[col_name] = column
                infile_data.append(row_dict)
    print(columns)
    return infile_data


def calculate_total_injuries_and_death(rows):
    # Given the list of rows from the dataset, you will need to calculate the total
    # injuries and death on each accident. Find out the keys corresponding to each injury type
    # and death type. Add the values on those columns to get the total count.
    injured_keys = ['NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF CYCLIST INJURED', 'NUMBER OF MOTORIST INJURED']
    killed_keys = ['NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST KILLED']
    count = 0
    for row in rows:
        row_injured = sum([int(row[x]) for x in injured_keys])
        row_killed = sum([int(row[x]) for x in killed_keys])
        row['TOTAL INJURED'] = row_injured
        row['TOTAL KILLED'] = row_killed
        row['DATETIME'] = row['DATE'] + ' ' + row['TIME']
    return rows


def write_json_file(rows):

    if not os.path.exists('data'):
        os.makedirs('data')

    with open('data/data.json', 'w+')  as outfile:
        json.dump(rows, outfile)


rows = read_csv_file('accidents.csv', delimiter=';')
rows = calculate_total_injuries_and_death(rows)
write_json_file(rows)
