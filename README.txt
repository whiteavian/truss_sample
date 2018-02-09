This project reads CSV input from stdin and prints a normalized CSV to stdout.
To setup, within a virtual environment, run

python setup.py develop

Then, from that environment, an example use of running the normalization on a
file called sample.csv and outputting to a file called sample_normalized.csv
from the top level directory would be:

cat sample.csv | python normalize_csv/normalize_csv.py > sample_normalized.csv

Unicode validation with a stderr warning and TotalDuration are not yet
implemented.