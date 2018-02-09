from datetime import datetime
import sys

ADDRESS = 'Address'


class CSV:
    def __init__(self):
        self.headers = []
        self.rows = []
        self.load()

    def load(self):
        self.headers = process_headers(raw_input().strip())

        for line in sys.stdin:
            self.rows.append(self.process_line(line.strip()))

    def address_index(self):
        return self.headers.index(ADDRESS)

    def process_line(self, line):
        start_seek_index = 0
        cols = []

        for i in range(len(self.headers) - 1):
            header = self.headers[i]

            end_seek_index = line.index(',', start_seek_index)

            if header == ADDRESS:
                if line[start_seek_index] == '"':
                    end_seek_index = line.find('"', start_seek_index + 1) + 1

            col_class = col_lookups[header.lower()]
            col = col_class(line[start_seek_index:end_seek_index])
            col.normalize()
            cols.append(col)

            start_seek_index = end_seek_index + 1

        return cols


def process_headers(header_line):
    return header_line.split(',')


class Row:
    def __init__(self):
        pass


class Column:
    def __init__(self, text):
        self.original_text = text
        self.normalized_text = ''

    def normalize(self):
        pass


class TimestampColumn(Column):

    def normalize(self):
        timestamp = datetime.strptime(self.original_text, '%x %X %p')
        self.normalized_text = timestamp.isoformat()

    def process(self):
        pass



class ZipColumn(Column):

    def normalize(self):
        self.normalized_text = self.original_text.zfill(5)


class AddressColumn(Column):

    def normalize(self):
        self.normalized_text = self.original_text


class FooBarDurationColumn(Column):

    def normalize(self):
        end_index = self.original_text.index(':')
        hours = int(self.original_text[:end_index])

        start_index = end_index + 1
        end_index = self.original_text.index(':', start_index)
        minutes = int(self.original_text[start_index:end_index])

        start_index = end_index + 1
        seconds = float(self.original_text[start_index:])

        duration = hours * 60 * 60 + minutes * 60 + seconds

        self.normalized_text = duration


class TotalDurationColumn(Column):

    def normalize(self):
        pass


class NotesColumn(Column):

    def normalize(self):
        self.normalized_text = self.original_text


class NameColumn(Column):

    def normalize(self):
        self.normalized_text = self.original_text.upper()


col_lookups = {
    'timestamp': TimestampColumn,
    'zip': ZipColumn,
    'address': AddressColumn,
    'fooduration': FooBarDurationColumn,
    'barduration': FooBarDurationColumn,
    'totalduration': TotalDurationColumn,
    'fullname': NameColumn,
    'notes': NotesColumn,
}


csv = CSV()
print csv.headers
for row in csv.rows:
    print [k.normalized_text for k in row]
