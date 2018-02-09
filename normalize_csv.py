import sys

ADDRESS = 'Address'


class CSV:
    def __init__(self):
        self.headers = []
        self.rows = []
        self.load()

    def load(self):
        self.headers = process_headers(raw_input())

        for line in sys.stdin:
            self.rows.append(self.process_line(line.strip()))

    def address_index(self):
        return self.headers.index(ADDRESS)

    def process_line(self, line):
        ai = self.address_index()
        if ai == 0:
            end_quote = line.find('"', 2)
            second_split = line.split(',', end_quote + 1)
        elif ai == len(self.headers) - 1:

        first_split = line.split(self.address_index())
        # TODO put quoted string checks and balances in place.
        to_split = first_split[-1]

        return first_split[:-1] + second_split


def process_headers(header_line):
    return header_line.split(',')




class Row:
    def __init__(self):
        pass


class Column:
    def __init__(self, text):
        self.original_text = text
        self.normalized_text = ''


class TimestampColumn(Column):
    def __init__(self, *args):
        super(TimestampColumn, self).__init__(*args)


class ZipColumn(Column):
    def __init__(self, *args):
        super(ZipColumn, self).__init__(*args)


class AddressColumn(Column):
    def __init__(self, *args):
        super(AddressColumn, self).__init__(*args)


class FooBarDurationColumn(Column):
    def __init__(self, *args):
        super(FooBarDurationColumn, self).__init__(*args)


class TotalDurationColumn(Column):
    def __init__(self, *args):
        super(TotalDurationColumn, self).__init__(*args)


class NotesColumn(Column):
    def __init__(self, *args):
        super(NotesColumn, self).__init__(*args)


csv = CSV()
print csv.headers
for row in csv.rows:
    print row
