from datetime import datetime, timedelta
import pytz
import sys

# Outstanding:
# Unicode validation
# TotalDuration
# Unicode replacement character
# Add stderr warning
# Confirm existing implementations are correct


class CSV:
    """Represent a CSV by headers and rows of Cell objects."""

    def __init__(self):
        self.headers = []
        self.rows = []
        self.load()

    def load(self):
        """Load CSV data from stdin."""
        self.headers = process_headers(raw_input().strip())

        for line in sys.stdin:
            self.rows.append(self.process_line(line.strip()))

    def process_line(self, line):
        """Create Cell objects for each line column."""
        start_seek_index = 0
        cols = []

        for i in range(len(self.headers) - 1):
            header = self.headers[i]

            # Split lines by commas, ignoring commas within quotes.
            end_seek_index = line.index(',', start_seek_index)

            if header == AddressCell.name:
                if line[start_seek_index] == '"':
                    end_seek_index = line.find('"', start_seek_index + 1) + 1

            col_class = col_lookups[header.lower()]
            col = col_class(line[start_seek_index:end_seek_index])
            cols.append(col)

            start_seek_index = end_seek_index + 1

        return cols


def process_headers(header_line):
    """Extract line headers as delimited by a comma."""
    return header_line.split(',')


class Row:
    def __init__(self):
        pass


class Cell:
    """Generic class for representing a row/column cell."""

    def __init__(self, text):
        self.original_text = text
        self.normalized_text = ''

        self.validate_unicode()
        self.normalize()

    def validate_unicode(self):
        pass

    def normalize(self):
        pass


class TimestampCell(Cell):

    def normalize(self):
        eastern_tz = pytz.timezone('America/New_York')

        timestamp = datetime.strptime(self.original_text, '%x %X %p') + timedelta(hours=3)
        eastern_time = timestamp.replace(tzinfo=eastern_tz)

        self.normalized_text = eastern_time.isoformat()


class ZipCell(Cell):

    def normalize(self):
        self.normalized_text = self.original_text.zfill(5)


class AddressCell(Cell):
    name = 'Address'

    def normalize(self):
        self.normalized_text = self.original_text


class FooBarDurationCell(Cell):

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


class TotalDurationCell(Cell):

    def normalize(self):
        pass


class NotesCell(Cell):

    def normalize(self):
        self.normalized_text = self.original_text


class NameCell(Cell):

    def normalize(self):
        self.normalized_text = self.original_text.upper()


col_lookups = {
    'timestamp': TimestampCell,
    'zip': ZipCell,
    'address': AddressCell,
    'fooduration': FooBarDurationCell,
    'barduration': FooBarDurationCell,
    'totalduration': TotalDurationCell,
    'fullname': NameCell,
    'notes': NotesCell,
}


csv = CSV()
print ",".join(csv.headers)

for row in csv.rows:
    print ",".join(map(str, [k.normalized_text for k in row]))
