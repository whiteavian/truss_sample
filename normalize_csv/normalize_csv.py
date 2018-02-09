from datetime import datetime, timedelta
import pytz
import sys


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

        for i in range(len(self.headers)):
            header = self.headers[i]

            # Split lines by commas, ignoring commas within quotes.
            # The final column ends at the end of the line, rather than a comma.
            if i == len(self.headers) - 1:
                end_seek_index = len(line)
            else:
                end_seek_index = line.index(',', start_seek_index)

                if header.lower() == AddressCell.column_name:
                    if line[start_seek_index] == '"':
                        end_seek_index = line.find('"', start_seek_index + 1) + 1

            col_class = col_lookups[header.lower()]
            col = col_class(line[start_seek_index:end_seek_index])
            cols.append(col)

            start_seek_index = end_seek_index + 1

        self.calculate_total_duration()

        return cols

    def calculate_total_duration(self):
        """Set total duration based on foo and bar durations."""
        headers_lower = map(lambda h: h.lower(), self.headers)
        foo_duration_index = headers_lower.index(FooBarDurationCell.foo_column_name)
        bar_duration_index = headers_lower.index(FooBarDurationCell.bar_column_name)
        total_duration_index = headers_lower.index(TotalDurationCell.column_name)

        for row in self.rows:
            foo_value = row[foo_duration_index].normalized_text
            bar_value = row[bar_duration_index].normalized_text
            row[total_duration_index].add_foo_bar(foo_value, bar_value)


def process_headers(header_line):
    """Extract line headers as delimited by a comma."""
    return header_line.split(',')


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
    column_name = 'timestamp'

    def normalize(self):
        """Convert time from US/Pacific to US/Eastern in ISO-8601 format."""
        timestamp = datetime.strptime(self.original_text, '%x %X %p') + timedelta(hours=3)

        eastern_tz = pytz.timezone('US/Eastern')
        eastern_time = timestamp.replace(tzinfo=eastern_tz)

        self.normalized_text = eastern_time.isoformat()


class ZipCell(Cell):
    """Represent five digit US zip code column cells."""
    column_name = 'zip'

    def normalize(self):
        """Left pad zip code with zeros if less than length five."""
        self.normalized_text = self.original_text.zfill(5)


class AddressCell(Cell):
    """Represent user input address column cells."""
    column_name = 'address'

    def normalize(self):
        """Perform no normalization additional to unicode validation."""
        self.normalized_text = self.original_text


class FooBarDurationCell(Cell):
    """Represent either FooDuration or BarDuration column cells."""
    foo_column_name = 'fooduration'
    bar_column_name = 'barduration'

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
    column_name = 'totalduration'

    def normalize(self):
        self.normalized_text = self.original_text

    def add_foo_bar(self, foo_value, bar_value):
        """Set normalized text to the sum of foo and bar column values."""
        self.normalized_text = foo_value + bar_value


class NotesCell(Cell):
    """Represent user input notes column cells."""
    column_name = 'notes'

    def normalize(self):
        """Perform no normalization additional to unicode validation."""
        self.normalized_text = self.original_text


class NameCell(Cell):
    """Represent user name column cells."""
    column_name = 'fullname'

    def normalize(self):
        """Convert the name to uppercase."""
        self.normalized_text = self.original_text.upper()


# Lowercase column header name to child Cell classes.
col_lookups = {
    TimestampCell.column_name: TimestampCell,
    ZipCell.column_name: ZipCell,
    AddressCell.column_name: AddressCell,
    FooBarDurationCell.bar_column_name: FooBarDurationCell,
    FooBarDurationCell.foo_column_name: FooBarDurationCell,
    TotalDurationCell.column_name: TotalDurationCell,
    NameCell.column_name: NameCell,
    NotesCell.column_name: NotesCell,
}


def main():
    """Create a CSV object and print the normalizations to stout."""
    csv = CSV()
    print ",".join(csv.headers)

    for row in csv.rows:
        print ",".join(map(str, [k.normalized_text for k in row]))


if __name__ == '__main__':
    main()
