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
        """Replace invalid unicode with the Unicode Replacement Character."""
        # TODO
        pass

    def normalize(self):
        """Empty parent class normalize implementation to force child implementation."""
        raise NotImplementedError


class TimestampCell(Cell):
    """Represent eastern time column cells."""

    def normalize(self):
        """Convert time from US/Pacific to US/Eastern in ISO-8601 format."""
        timestamp = datetime.strptime(self.original_text, '%x %X %p') + timedelta(hours=3)

        eastern_tz = pytz.timezone('US/Eastern')
        eastern_time = timestamp.replace(tzinfo=eastern_tz)

        self.normalized_text = eastern_time.isoformat()


class ZipCell(Cell):
    """Represent five digit US zip code column cells."""

    def normalize(self):
        """Left pad zip code with zeros if less than length five."""
        self.normalized_text = self.original_text.zfill(5)


class AddressCell(Cell):
    """Represent user input address column cells."""
    name = 'Address'

    def normalize(self):
        """Perform no normalization additional to unicode validation."""
        self.normalized_text = self.original_text


class FooBarDurationCell(Cell):
    """Represent either FooDuration or BarDuration column cells."""

    def normalize(self):
        """Convert duration to a floating point seconds format."""
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
    """Represent column cells as the sum of FooDuration and BarDuration."""

    def normalize(self):
        pass


class NotesCell(Cell):
    """Represent user input notes column cells."""

    def normalize(self):
        """Perform no normalization additional to unicode validation."""
        self.normalized_text = self.original_text


class NameCell(Cell):
    """Represent user name column cells."""

    def normalize(self):
        """Convert the name to uppercase."""
        self.normalized_text = self.original_text.upper()


# Lowercase column header name to child Cell classes.
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


def main():
    """Create a CSV object and print the normalizations to stout."""
    csv = CSV()
    print ",".join(csv.headers)

    for row in csv.rows:
        print ",".join(map(str, [k.normalized_text for k in row]))


if __name__ == '__main__':
    main()
