import sys


class CSV:
    def __init__(self):
        self.headers = []
        self.rows = []
        self.load()

    def load(self):
        self.headers = process_headers(raw_input())

        for line in sys.stdin:
            self.rows.append(process_line(line.strip()))


def process_headers(header_line):
    return header_line.split(',')


def process_line(line):
    line_items = line.split('"')
    # also do this for single quotes
    num_items = len(line_items)

    # If our csv contains only a single column, which is quoted, return it.
    if num_items == 3 and line_items[0] == '' and line_items[2] == '':
        return [line_items[1]]

    split_line = []

    # Otherwise, split columns by comma, accounting for quoted fields.
    for i in range(num_items):
        if i != 0 and line_items[i - 1].endswith(','):
            prev_has_comma = True
        else:
            prev_has_comma = False

        if i != num_items - 1 and line_items[i + 1].startswith(','):
            next_has_comma = True
        else:
            next_has_comma = False

        quoted = prev_has_comma and next_has_comma
        quoted = quoted or (i == 0 and next_has_comma)
        quoted = quoted or (i == num_items - 1 and prev_has_comma)

        if not quoted:
            split_line.extend(line_items[i].split(','))
        else:
            split_line.append(line_items[i])

    return split_line


class Row:
    def __init__(self):
        pass


class Column:
    def __init__(self):
        pass


class TimestampColumn(Column):
    def __init__(self):
        pass


class ZipColumn(Column):
    def __init__(self):
        pass


class AddressColumn(Column):
    def __init__(self):
        pass


class FooBarDurationColumn(Column):
    def __init__(self):
        pass


class TotalDurationColumn(Column):
    def __init__(self):
        pass


class NotesColumn(Column):
    def __init__(self):
        pass


csv = CSV()
print csv.headers
for row in csv.rows:
    print row
